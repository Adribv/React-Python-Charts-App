from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as go
from flask_cors import CORS
import random

# Load CSV data
csv_path = r"Nissan New Dataset.csv"
df = pd.read_csv(csv_path, encoding='latin1')

# Initialize the Dash app
app = Dash(__name__, suppress_callback_exceptions=True)

# Configure CORS
CORS(app.server, resources={r"/": {"origins": ""}})

# External CSS stylesheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Define dropdown button style
dropdown_button_style = {
    'width': '200px',
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

# Define layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])

# Define the main page layout
def get_main_layout():
    return html.Div([
        html.H1(id='heading', style={'textAlign': 'center', 'fontSize': '45px'}),
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='brand-dropdown',
                    placeholder='Select Brand',
                    multi=True,
                    style=dropdown_button_style
                ),
                dcc.Dropdown(
                    id='model-dropdown',
                    placeholder='Select Model',
                    multi=True,
                    style=dropdown_button_style
                ),
                dcc.Dropdown(
                    id='feature-dropdown',
                    placeholder='Select Feature',
                    multi=True,
                    style=dropdown_button_style
                ),
                dcc.Dropdown(
                    id='fact-dropdown',
                    placeholder='Select Fact',
                    multi=True,
                    style=dropdown_button_style
                ),
                dcc.Dropdown(
                    id='category-dropdown',
                    placeholder='Select Category',
                    options=[
                        {'label': 'Segment', 'value': 'segment'},
                        {'label': 'Price', 'value': 'price'}
                    ],
                    multi=True,  # Enable multiple selection
                    style=dropdown_button_style
                ),
                dcc.Dropdown(
                    id='source-dropdown',
                    placeholder='Select Source',
                    multi=True,
                    style=dropdown_button_style
                ),
                dcc.DatePickerSingle(
                    id='from-date-picker',
                    placeholder='From Date',
                    display_format='DD-MM-YYYY',
                    style=dropdown_button_style
                ),
                dcc.DatePickerSingle(
                    id='to-date-picker',
                    placeholder='To Date',
                    display_format='DD-MM-YYYY',
                    style=dropdown_button_style
                ),
            ], style={'width': '220px', 'margin-right': '20px', 'display': 'inline-block', 'verticalAlign': 'top'}),
            html.Div([
                dcc.Graph(
                    id='stacked-bar-chart',
                    style={'height': '445px'}
                ),
                html.Div(id='selected-model-name', style={'textAlign': 'left', 'marginTop': '20px', 'fontSize': '20px', 'fontWeight': 'bold'}),
                html.Div(id='selected-model-features-table')
            ], style={
                'display': 'inline-block',
                'width': 'calc(100% - 260px)',
                'verticalAlign': 'top'
            })
        ]),
    ], style={'fontFamily': 'Arial, sans-serif'})

# Update table with selected model's features, showing 3 positive and 3 negative features per model
# Update table with selected model's features, showing 3 positive and 3 negative features per model
@app.callback(
    [Output('selected-model-features-table', 'children'),
     Output('selected-model-name', 'children')],
    [Input('model-dropdown', 'value')]
)
def update_selected_model_features_table(selected_models):
    # If no model is selected or "All" is selected, use all unique models in the dataframe
    if not selected_models or 'All' in selected_models:
        selected_models = df['model'].unique()

    # Display the selected model(s)
    selected_model_text = f"Selected Model(s): {', '.join(selected_models)}"

    # Create a list to hold tables for each model
    model_tables = []

    # Iterate through each selected model
    for selected_model in selected_models:
        # Filter dataframe based on the selected model
        filtered_df = df[df['model'] == selected_model]

        # Extract positive and negative features
        positive_features = filtered_df[filtered_df['CriticalRanking'] == 5].head(3)
        negative_features = filtered_df[filtered_df['CriticalRanking'] == 1].head(3)

        # Create table rows for positive and negative features
        positive_rows = [html.Tr([html.Td(
                        dcc.Link("+", href=f'/feedback/{row["model"]}/{row["Feature"]}/Positive', style={'color': 'green', 'fontWeight': 'bold'})
                    ), html.Td(row['Feature'])]) for _, row in positive_features.iterrows()]
        negative_rows = [html.Tr([html.Td(
                        dcc.Link("-", href=f'/feedback/{row["model"]}/{row["Feature"]}/Negative', style={'color': 'red', 'fontWeight': 'bold'})
                    ), html.Td(row['Feature'])]) for _, row in negative_features.iterrows()]

        # Add the table for the current model
        model_tables.append(
            html.Div([
                html.H3(f"Model: {selected_model}"),
                html.Table([
                    html.Thead(html.Tr([html.Th("Positive Features"), html.Th("Negative Features")])),
                    html.Tbody([
                        html.Tr([
                            html.Td(
                                html.Table(positive_rows),
                                style={'width': '50%', 'border': '1px solid black', 'verticalAlign': 'top', 'padding': '10px'}
                            ),
                            html.Td(
                                html.Table(negative_rows),
                                style={'width': '50%', 'border': '1px solid black', 'verticalAlign': 'top', 'padding': '10px'}
                            )
                        ])
                    ])
                ], style={'width': '100%', 'borderCollapse': 'collapse', 'marginBottom': '30px'})
            ])
        )

    # Return the list of tables for all selected models
    return html.Div(model_tables), selected_model_text


# Define the feedback page layout
def get_feedback_layout(selected_model, selected_feature, selected_fact):
    # Filter feedback based on the selected model
    feedback = df[df['model'] == selected_model].head(10)
    feedback_list = feedback.to_dict('records')

    heading_text = f'Feedback for Model: {selected_model}'
    if selected_feature and selected_fact:
        heading_text += f' | Feature: {selected_feature} | Fact: {selected_fact}'

    return html.Div([
        html.H1(heading_text, style={'textAlign': 'center'}),
        dash_table.DataTable(
            id='feedback-table',
            columns=[
                {'name': 'Brand', 'id': 'brand'},
                {'name': 'Model', 'id': 'model'},
                {'name': 'Date', 'id': 'date'},
                {'name': 'Category', 'id': 'segment'},
                {'name': 'Feedback', 'id': 'feedback'}
            ],
            data=feedback_list,
            style_table={'overflowX': 'auto'},
            style_cell={
                'textAlign': 'left',
                'padding': '5px',
                'whiteSpace': 'normal',
                'height': 'auto'
            },
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }
            ]
        )
    ])



# Callback to update brand dropdown with all available brands
@app.callback(
    Output('brand-dropdown', 'options'),
    [Input('brand-dropdown', 'value')]
)
def update_brand_dropdown(_):
    brands = df['brand'].unique()
    options = [{'label': brand, 'value': brand} for brand in brands]
    options.insert(0, {'label': 'All', 'value': 'All'})
    return options

# Update model dropdown based on selected brand
@app.callback(
    Output('model-dropdown', 'options'),
    [Input('brand-dropdown', 'value')]
)
def update_model_dropdown(selected_brands):
    if not selected_brands or 'All' in selected_brands:
        models = df['model'].unique()
    else:
        models = df[df['brand'].isin(selected_brands)]['model'].unique()
        
    options = [{'label': model, 'value': model} for model in models]
    options.insert(0, {'label': 'All', 'value': 'All'})
    return options

# Update feature dropdown based on selected model
@app.callback(
    Output('feature-dropdown', 'options'),
    [Input('model-dropdown', 'value')]
)
def update_feature_dropdown(selected_models):
    if not selected_models or 'All' in selected_models:
        features = df['Feature'].unique()
    else:
        filtered_df = df[df['model'].isin(selected_models)]
        features = filtered_df['Feature'].unique()
        
    options = [{'label': feature, 'value': feature} for feature in features]
    options.insert(0, {'label': 'All', 'value': 'All'})
    return options

# Update fact dropdown based on selected feature
@app.callback(
    Output('fact-dropdown', 'options'),
    [Input('feature-dropdown', 'value')]
)
def update_fact_dropdown(selected_features):
    fact_options = ['Very Positive', 'Positive', 'Neutral', 'Negative', 'Very Negative']
    options = [{'label': fact, 'value': fact} for fact in fact_options]
    options.insert(0, {'label': 'All', 'value': 'All'})
    return options

# Update source dropdown with all unique sources
@app.callback(
    Output('source-dropdown', 'options'),
    [Input('source-dropdown', 'value')]
)
def update_source_dropdown(_):
    sources = df['source'].unique()  # Assuming there is a 'source' column in the dataframe
    options = [{'label': source, 'value': source} for source in sources]
    options.insert(0, {'label': 'All', 'value': 'All'})
    return options

# Update stacked bar chart based on selected brand, model, feature, fact, category, and source
@app.callback(
    Output('stacked-bar-chart', 'figure'),
    [Input('brand-dropdown', 'value'),
     Input('model-dropdown', 'value'),
     Input('feature-dropdown', 'value'),
     Input('fact-dropdown', 'value'),
     Input('category-dropdown', 'value'),
     Input('source-dropdown', 'value'),
     Input('from-date-picker', 'date'),
     Input('to-date-picker', 'date')]
)
def update_stacked_bar_chart(selected_brands, selected_models, selected_features, selected_facts, selected_categories, selected_sources, from_date, to_date):
    if not from_date or not to_date:
        # Return an empty figure if dates are not provided
        return go.Figure()

    filtered_df = df.copy()

    if selected_brands and 'All' not in selected_brands:
        filtered_df = filtered_df[filtered_df['brand'].isin(selected_brands)]
    
    if selected_models and 'All' not in selected_models:
        filtered_df = filtered_df[filtered_df['model'].isin(selected_models)]
    
    if selected_features and 'All' not in selected_features:
        filtered_df = filtered_df[filtered_df['Feature'].isin(selected_features)]
    
    if selected_facts and 'All' not in selected_facts:
        filtered_df = filtered_df[filtered_df['fact'].isin(selected_facts)]
    
    if selected_sources and 'All' not in selected_sources:
        filtered_df = filtered_df[filtered_df['source'].isin(selected_sources)]

    # Convert the 'date' column to datetime format
    filtered_df['date'] = pd.to_datetime(filtered_df['date'], errors='coerce')

    # Ensure from_date and to_date are in datetime format
    from_date = pd.to_datetime(from_date, format='%Y-%m-%d', errors='coerce')
    to_date = pd.to_datetime(to_date, format='%Y-%m-%d', errors='coerce')

    # Filter based on date range
    filtered_df = filtered_df[(filtered_df['date'] >= from_date) & (filtered_df['date'] <= to_date)]

    # Group data by model and fact, then count occurrences
    model_fact_counts = filtered_df.groupby(['model', 'fact']).size().unstack(fill_value=0)

    # Define the fact categories
    fact_categories = ['Very Positive', 'Positive', 'Neutral', 'Negative', 'Very Negative']

    # Define colors for the stacked bars
    fact_colors = {
        
    'Very Positive': '#234f1e',
    'Positive': '#299617',  
    'Neutral': '#545454',    
    'Negative': '#d21401',
    'Very Negative': '#8b0000'

    }

    # Create traces for each fact category
    traces = []
    for fact in fact_categories:
        if fact in model_fact_counts.columns:
            traces.append(go.Bar(
                x=model_fact_counts.index,
                y=model_fact_counts[fact],
                name=fact,
                marker_color=fact_colors[fact]
            ))

    # Create the stacked bar chart figure
    fig = go.Figure(data=traces)
    fig.update_layout(
        barmode='stack',
        xaxis=dict(title='Model'),
        yaxis=dict(title='Count'),
        title='Sentiment Analysis by Model',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    return fig

# Update heading based on selected feature and fact
@app.callback(
    Output('heading', 'children'),
    [Input('feature-dropdown', 'value'),
     Input('fact-dropdown', 'value')]
)
def update_heading(selected_features, selected_facts):
    # Extract the first selected value if it's a list or use a default value
    feature = selected_features[0] if selected_features and selected_features[0] != 'Features' else 'Features'
    fact = selected_facts[0] if selected_facts and selected_facts[0] != '' else ''

    return f"{fact} Sentiment on {feature}"

# Update table with random models and features
@app.callback(
    Output('random-models-table', 'children'),
    [Input('stacked-bar-chart', 'figure')]
)
def update_random_models_table(_):
    # Filter only rows with CriticalRanking 1 or 5
    filtered_df = df[df['CriticalRanking'].isin([1, 5])]

    # Randomly select 5 models
    random_models = filtered_df['model'].unique()
    if len(random_models) > 5:
        random_models = random.sample(list(random_models), 5)
    else:
        random_models = list(random_models)

    # Create a filtered dataframe for these models
    random_df = filtered_df[filtered_df['model'].isin(random_models)]

    # Create table rows
    table_rows = []
    for _, row in random_df.iterrows():
        critical_ranking = "Positive" if row['CriticalRanking'] == 5 else "Negative"
        feature_link = html.A(row['Feature'], href=f"/feedback/{row['model']}/{row['Feature']}/{critical_ranking}")
        table_rows.append(html.Tr([
            html.Td(row['model']),
            html.Td(feature_link),
            html.Td(critical_ranking)
        ]))

    # Return the table component
    return html.Table([
        html.Thead(html.Tr([
            html.Th("Model"),
            html.Th("Feature"),
            html.Th("Critical Ranking")
        ])),
        html.Tbody(table_rows)
    ])

# Handle bar chart click event
@app.callback(
    Output('url', 'pathname'),
    [Input('stacked-bar-chart', 'clickData')],
    [State('feature-dropdown', 'value'), State('fact-dropdown', 'value')]
)
def redirect_on_click(clickData, selected_features, selected_facts):
    if clickData:
        model = clickData['points'][0]['x']
        feature = selected_features[0] if selected_features else 'None'
        fact = selected_facts[0] if selected_facts else 'None'
        return f'/feedback/{model}/{feature}/{fact}'
    return '/'

# Define layout for feedback page
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname.startswith('/feedback'):
        parts = pathname.split('/')
        model = parts[2]
        feature = parts[3] if len(parts) > 3 else 'None'
        fact = parts[4] if len(parts) > 4 else 'None'
        return get_feedback_layout(model, feature, fact)
    return get_main_layout()


# Run the app
if __name__ == '__main__':
    app.run_server(port=8057, debug=False, dev_tools_ui=False, dev_tools_props_check=False)
