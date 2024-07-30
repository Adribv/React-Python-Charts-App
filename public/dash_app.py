# dash_app.py

from dash import dcc, html, Dash
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import random

# Load CSV data
csv_path = r"./Nissan New Dataset.csv"  # Adjust the path according to your project structure
df = pd.read_csv(csv_path, encoding='latin1')

# Initialize the Dash app
app = Dash(__name__)

# Define dropdown button style
dropdown_button_style = {
    'width': '150px',
    'color': 'black',
    'backgroundColor': '#8b0000',
    'display': 'inline-block',
    'margin-right': '20px',
    'padding': '10px 20px',
    'border': 'none',
    'border-radius': '30px',
    'cursor': 'pointer',
    'textAlign': 'center'
}

# Define layout
app.layout = html.Div([
    # Heading
    html.H1(id='heading', style={'textAlign': 'center', 'fontSize': '45px'}),
    
    # Second division with dropdowns and graph
    html.Div([
        # Dropdowns in a single line
        html.Div([
            # Dropdown for brand
            dcc.Dropdown(
                id='brand-dropdown',
                placeholder='Select Brand',
                style=dropdown_button_style
            ),
            # Dropdown for model
            dcc.Dropdown(
                id='model-dropdown',
                placeholder='Select Model',
                style=dropdown_button_style
            ),
            # Dropdown for feature
            dcc.Dropdown(
                id='feature-dropdown',
                placeholder='Select Feature',
                style=dropdown_button_style
            ),
            # Dropdown for fact
            dcc.Dropdown(
                id='fact-dropdown',
                placeholder='Select Fact',
                style=dropdown_button_style
            ),
            # Dropdown for category
            dcc.Dropdown(
                id='category-dropdown',
                placeholder='Select Category',
                options=[
                    {'label': 'Segment', 'value': 'segment'},
                    {'label': 'Price', 'value': 'price'}
                ],
                style=dropdown_button_style
            ),
            # Dropdown for from date
            dcc.Input(
                id='from-date-input',
                type='text',
                placeholder='From Date (dd-mm-yyyy)',
                style=dropdown_button_style
            ),
            # Dropdown for to date
            dcc.Input(
                id='to-date-input',
                type='text',
                placeholder='To Date (dd-mm-yyyy)',
                style=dropdown_button_style
            ),
            
        ], style={'margin-bottom': '20px', 'display': 'flex', 'flex-wrap': 'wrap'}),
        
        # Graph
        html.Div([
            dcc.Graph(
                id='bar-chart',
                style={'height': '445px',}  # Set height of the graph
            )
        ], style={
            'width': '100%',  # Set width to 50%
            'float': 'justify',  # Float to the right
            'border': '1px solid black',  # Optional: Add a border for visualization
            #'padding': '1px'  # Add some padding for spacing
        })

    ]),
])

# Callbacks...

# Callback to update brand dropdown with all available brands
@app.callback(
    Output('brand-dropdown', 'options'),
    [Input('brand-dropdown', 'value')]  # This input won't be used, it's just to trigger the callback
)
def update_brand_dropdown(_):
    brands = df['brand'].unique()
    return [{'label': brand, 'value': brand} for brand in brands]

# Update model dropdown based on selected brand
@app.callback(
    Output('model-dropdown', 'options'),
    [Input('brand-dropdown', 'value')]
)
def update_model_dropdown(selected_brand):
    if selected_brand is None:
        # If no brand is selected, return all models
        models = df['model'].unique()
    else:
        # Otherwise, filter models based on the selected brand
        models = df[df['brand'] == selected_brand]['model'].unique()
        
    return [{'label': model, 'value': model} for model in models]

# Update feature dropdown based on selected model
@app.callback(
    Output('feature-dropdown', 'options'),
    [Input('model-dropdown', 'value')]
)
def update_feature_dropdown(selected_model):
    if selected_model is None:
        # If no model is selected, return an empty list for features
        return []
    else:
        # Filter the DataFrame based on selected model
        filtered_df = df[df['model'] == selected_model]
        # Get unique features from the filtered DataFrame
        features = filtered_df['Feature'].unique()
        # Create dropdown options
        return [{'label': feature, 'value': feature} for feature in features]

# Update fact dropdown based on selected model and feature
@app.callback(
    Output('fact-dropdown', 'options'),
    [Input('feature-dropdown', 'value')]
)
def update_fact_dropdown(selected_feature):
    if selected_feature is None:
        return []
    else:
        # Define the order of fact options
        fact_options = ['Very Positive', 'Positive', 'Neutral', 'Negative', 'Very Negative']
        return [{'label': fact, 'value': fact} for fact in fact_options]

# Update bar chart based on selected brand, model, feature, fact, and category
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('brand-dropdown', 'value'),
     Input('model-dropdown', 'value'),
     Input('feature-dropdown', 'value'),
     Input('fact-dropdown', 'value'),
     Input('category-dropdown', 'value'),
     Input('from-date-input', 'value'),
     Input('to-date-input', 'value')]
)
def update_bar_chart(selected_brand, selected_model, selected_feature, selected_fact, selected_category, from_date, to_date):
    if selected_model is None or selected_feature is None or selected_fact is None or selected_category is None or from_date is None or to_date is None or len(from_date.strip()) < 10 or len(to_date.strip()) < 10:
        # If any of the inputs is None, return an empty figure
        return go.Figure()
    else:
        # Convert date strings to datetime objects
        from_date = pd.to_datetime(from_date, format='%d-%m-%Y', errors='coerce')
        to_date = pd.to_datetime(to_date, format='%d-%m-%Y', errors='coerce')

        # Check if dates are valid
        if pd.isnull(from_date) or pd.isnull(to_date) or from_date > to_date:
            # If dates are not valid, return an empty figure
            return go.Figure()

    if selected_category == 'segment':
        return update_segment_chart(selected_model, selected_feature, selected_fact, from_date, to_date)
    elif selected_category == 'price':
        return update_price_chart(selected_model, selected_feature, selected_fact, from_date, to_date)

def filter_data_by_date_range(data_frame, from_date, to_date):
    # Convert date strings to datetime objects
    from_date = pd.to_datetime(from_date, format='%d-%m-%Y', errors='coerce')
    to_date = pd.to_datetime(to_date, format='%d-%m-%Y', errors='coerce')

    # Filter the DataFrame based on date range
    filtered_df = data_frame[
        (pd.to_datetime(data_frame['date'], format='%d-%m-%Y', errors='coerce') >= from_date) &
        (pd.to_datetime(data_frame['date'], format='%d-%m-%Y', errors='coerce') <= to_date)
    ]

    return filtered_df

def update_segment_chart(selected_model, selected_feature, selected_fact, from_date, to_date):
    # Filter the DataFrame based on selected feature and fact
    filtered_df = df[(df['Feature'] == selected_feature) & (df['fact'] == selected_fact)]

    # Filter by selected model's segment
    if selected_model and 'segment' in df.columns:
        model_segment = df[df['model'] == selected_model]['segment'].iloc[0]
        filtered_df = filtered_df[filtered_df['segment'] == model_segment]

    # Filter data by date range
    filtered_df = filter_data_by_date_range(filtered_df, from_date, to_date)

    # Get all models in the segment
    models_in_segment = df[df['segment'] == model_segment]['model'].unique()

    # Reorder models as per dataset order
    filtered_df['model'] = pd.Categorical(filtered_df['model'], categories=models_in_segment, ordered=True)

    # Count the total number of occurrences of the selected fact for each model
    model_counts = filtered_df.groupby('model', observed=False).size()

    # Set count to 0 for models that don't have any occurrences
    for model in models_in_segment:
        if model not in model_counts.index:
            model_counts[model] = 0

    # Sort the counts by model
    model_counts = model_counts.sort_index()

    # Assign colors to models
    model_colors = {
        'Magnite': '#000000',
        'Sonet': '#004aad',
        'Venue': '#ff914d',
        'Nexon': '#5ce1e6',
        'Kiger': '#ff66c4'
    }
    colors = [model_colors.get(model, '#{:06x}'.format(random.randint(0, 256**3-1))) for model in model_counts.index]

    # Create a bar chart for models
    fig = go.Figure(go.Bar(x=model_counts.index, y=model_counts.values, marker_color=colors))
    fig.update_layout(
        xaxis=dict(title='Model'),
        yaxis=dict(title=f'Total Count of {selected_fact} for {selected_feature}'),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)'
    )

    return fig

def update_price_chart(selected_model, selected_feature, selected_fact, from_date, to_date):
    if selected_model:
        # Get the price of the selected model
        selected_model_price = df[df['model'] == selected_model]['price'].iloc[0]

        # If the price is a string with commas, remove them and convert to float
        if isinstance(selected_model_price, str):
            selected_model_price = float(selected_model_price.replace(',', ''))
        else:
            selected_model_price = float(selected_model_price)

        # Filter based on price difference within ±200,000
        filtered_df = df[
            (pd.to_numeric(df['price'], errors='coerce') >= (selected_model_price - 200000)) &
            (pd.to_numeric(df['price'], errors='coerce') <= (selected_model_price + 200000))
        ]

        # Filter the DataFrame based on selected feature and fact
        filtered_df = filtered_df[(filtered_df['Feature'] == selected_feature) & (filtered_df['fact'] == selected_fact)]

        # Filter data by date range
        filtered_df = filter_data_by_date_range(filtered_df, from_date, to_date)

        # Get all models within the price range of ±200,000 of the selected model
        models_in_range = df[
            (pd.to_numeric(df['price'], errors='coerce') >= (selected_model_price - 200000)) &
            (pd.to_numeric(df['price'], errors='coerce') <= (selected_model_price + 200000))
        ]['model'].unique()

        # Create a DataFrame to hold the counts for all models within the price range
        model_counts = pd.Series(0, index=models_in_range)

        # Count the total number of occurrences of the selected fact for each model
        count_series = filtered_df['model'].value_counts()

        # Fill in the count for models with occurrences
        model_counts.update(count_series)

        # Sort the counts by model
        model_counts = model_counts.sort_index()

        # Assign colors to models
        model_colors = {
            'Magnite': '#000000',
            'Sonet': '#004aad',
            'Venue': '#ff914d',
            'Nexon': '#5ce1e6',
            'Kiger': '#ff66c4'
        }
        colors = [model_colors.get(model, '#{:06x}'.format(random.randint(0, 256**3-1))) for model in model_counts.index]

        # Create a bar chart for models
        fig = go.Figure(go.Bar(x=model_counts.index, y=model_counts.values, marker_color=colors))
        fig.update_layout(
            xaxis=dict(title='Model', categoryorder='array', categoryarray=models_in_range),
            yaxis=dict(title=f'Total Count of {selected_fact} for {selected_feature}'),
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)'
        )

        return fig
    else:
        # If no model is selected, return an empty figure
        return go.Figure()

# Update heading based on selected feature and fact
@app.callback(
    Output('heading', 'children'),
    [Input('feature-dropdown', 'value'),
     Input('fact-dropdown', 'value')]
)
def update_heading(selected_feature, selected_fact):
    if selected_feature and selected_fact:
        return f"{selected_fact} Sentiment on {selected_feature}"
    else:
        return "Sentiment on Feature"


# Run the app
if __name__ == '__main__':
    app.run_server(port=8057, debug=False)
