import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
from flask_cors import CORS

# Load CSV data
csv_path = r"Nissan New Dataset.csv"
df = pd.read_csv(csv_path, encoding='latin1')
df[' index'] = range(1, len(df) + 1)
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y').dt.strftime('%Y-%m-%d')  # Convert to ISO format for consistency
feature_colors = {
    'All-Wheel Drive': '#000000',
    'Steering': '#004aad',
    'Interior Quality': '#ff914d',
    'Engine': '#5ce1e6',
    'Brake': '#ff66c4',
    'Seats': '#98FB98',
    'Transmission': '#800080',
    'Electric Motor': '#006400'
}

# Initialize the Dash app
app = dash.Dash(__name__)
CORS(app.server, resources={r"/*": {"origins": "*"}})

# Define dropdown button style with added margin-bottom for spacing
dropdown_button_style = {
    'width': '150px',  # Adjusted to be consistent with previous code
    'min-width': '200px',
    'max-width': '200px',
    'color': 'black',
    'backgroundColor': '#fff',
    'margin-bottom': '10px',
    'padding': '8px 10px',
    'border': 'none',
    'border-radius': '20px',
    'cursor': 'pointer',
    'textAlign': 'center',
    'fontSize': '14px'
}

# Define color mapping for sentiment
color_mapping = {
    'Very Positive': '#234f1e',
    'Positive': '#299617',
    'Neutral': '#545454',
    'Negative': '#d21401',
    'Very Negative': '#8b0000'
}

# Define layout
app.layout = html.Div([
    # Flex container for dropdowns and feedback section
    html.Div([
        # Dropdowns container
        html.Div([
            dcc.Dropdown(
                id='brand-dropdown',
                options=[{'label': 'Select All Brands', 'value': 'select_all'}] + [{'label': brand, 'value': brand} for brand in df['brand'].unique()],
                placeholder='Select Brand',
                style=dropdown_button_style,
                multi=True
            ),
            dcc.Dropdown(
                id='model-dropdown',
                options=[],
                placeholder='Select Model',
                style=dropdown_button_style,
                multi=True
            ),
            dcc.Dropdown(
                id='fact-dropdown',
                options=[],
                placeholder='Select Fact',
                style=dropdown_button_style,
                multi=True
            ),
            dcc.Dropdown(
                id='country-dropdown',
                options=[],
                placeholder='Select City',
                style=dropdown_button_style,
                multi=True
            ),
            dcc.Dropdown(
                id='source-dropdown',
                options=[],
                placeholder='Select Source',
                style=dropdown_button_style,
                multi=True
            ),
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=df['date'].min(),
                end_date=df['date'].max(),
                display_format='DD-MM-YYYY',
                style=dropdown_button_style
            ),
        ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'flex-start', 'width': '300px', 'padding': '10px'}),  # Vertically align dropdowns and fixed width

        # Feedback table section
        html.Div([
            dash_table.DataTable(
                id='datatable-paging-page-count',
                columns=[
                    {"name": i, "id": i, "type": "text"} for i in ['brand', 'model', 'feedback']
                ],
                page_current=0,
                page_size=5,
                page_action='custom',
                style_table={'height': '400px', 'overflowY': 'auto', 'overflowX': 'auto', 'width': '100%'},
                style_header={'textAlign': 'center'},
                style_cell={'textAlign': 'center', 'whiteSpace': 'normal', 'overflow': 'auto', 'textOverflow': 'ellipsis', 'minWidth': '50px', 'maxWidth': '180px'},
                style_cell_conditional=[
                    {'if': {'column_id': 'brand'}, 'width': '10%'},
                    {'if': {'column_id': 'model'}, 'width': '10%'},
                ],
            ),
        ], style={'flex': '1', 'padding': '20px', 'overflow': 'hidden'})  # Align feedback section to the right and take remaining space
    ], style={'display': 'flex', 'flexDirection': 'row'})  # Horizontal layout for dropdowns and feedback section
])

# Callbacks...

# Update model dropdown options based on selected brand(s)
@app.callback(
    Output('model-dropdown', 'options'),
    [Input('brand-dropdown', 'value')]
)
def update_model_dropdown(selected_brands):
    if not selected_brands:
        return []
    elif 'select_all' in selected_brands:
        models = df['model'].unique()
    else:
        models = df[df['brand'].isin(selected_brands)]['model'].unique()
    return [{'label': model, 'value': model} for model in models]

# Update fact dropdown options based on selected model(s)
@app.callback(
    Output('fact-dropdown', 'options'),
    [Input('model-dropdown', 'value')]
)
def update_fact_dropdown(selected_models):
    if not selected_models:
        return []
    elif 'select_all' in selected_models:
        facts = df['fact'].unique()
    else:
        facts = df[df['model'].isin(selected_models)]['fact'].unique()
    return [{'label': fact, 'value': fact} for fact in facts]

# Update country dropdown options based on selected model(s) and fact(s)
@app.callback(
    Output('country-dropdown', 'options'),
    [Input('model-dropdown', 'value'),
     Input('fact-dropdown', 'value')]
)
def update_country_dropdown(selected_models, selected_facts):
    if not selected_models or not selected_facts:
        return []
    elif 'select_all' in selected_models or 'select_all' in selected_facts:
        countries = df['country'].unique()
    else:
        countries = df[(df['model'].isin(selected_models)) & (df['fact'].isin(selected_facts))]['country'].unique()
    return [{'label': country, 'value': country} for country in countries]

# Update source dropdown options based on selected model(s), fact(s), and country(s)
@app.callback(
    Output('source-dropdown', 'options'),
    [Input('model-dropdown', 'value'),
     Input('fact-dropdown', 'value'),
     Input('country-dropdown', 'value')]
)
def update_source_dropdown(selected_models, selected_facts, selected_countries):
    if not selected_models or not selected_facts or not selected_countries:
        return []
    elif 'select_all' in selected_models or 'select_all' in selected_facts or 'select_all' in selected_countries:
        sources = df['source'].unique()
    else:
        sources = df[(df['model'].isin(selected_models)) & 
                     (df['fact'].isin(selected_facts)) & 
                     (df['country'].isin(selected_countries))]['source'].unique()
    return [{'label': source, 'value': source} for source in sources]

# Update table based on selected features and date range
@app.callback(
    Output('datatable-paging-page-count', 'data'),
    [Input('brand-dropdown', 'value'),
     Input('model-dropdown', 'value'),
     Input('fact-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('source-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('datatable-paging-page-count', 'page_current'),
     Input('datatable-paging-page-count', 'page_size')]
)
def update_table(selected_brands, selected_models, selected_facts, selected_countries, selected_sources, start_date, end_date, page_current, page_size):
    if None in [selected_brands, selected_models, selected_facts, selected_countries, selected_sources]:
        return []
    elif not start_date or not end_date:
        return []
    else:
        from_date = pd.to_datetime(start_date, format='%Y-%m-%d', errors='coerce')
        to_date = pd.to_datetime(end_date, format='%Y-%m-%d', errors='coerce')

        if pd.isnull(from_date) or pd.isnull(to_date) or from_date > to_date:
            return []
        
        if 'select_all' in selected_brands:
            filtered_df = df
        else:
            filtered_df = df[df['brand'].isin(selected_brands)]
        
        filtered_df = filtered_df[(filtered_df['model'].isin(selected_models)) &
                                  (filtered_df['fact'].isin(selected_facts)) &
                                  (filtered_df['country'].isin(selected_countries)) &
                                  (filtered_df['source'].isin(selected_sources)) &
                                  (pd.to_datetime(filtered_df['date'], format='%Y-%m-%d') >= from_date) &
                                  (pd.to_datetime(filtered_df['date'], format='%Y-%m-%d') <= to_date)]
        
        if filtered_df.empty:
            return []
        
        return filtered_df.iloc[
               page_current * page_size:(page_current + 1) * page_size
               ].to_dict('records')

# Run the app
if __name__ == '__main__':
    app.run_server(port=8063, debug=False)
