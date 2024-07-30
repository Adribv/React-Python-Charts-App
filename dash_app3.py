import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
from dash_table import DataTable
from textwrap import shorten
from flask_cors import CORS
from flask import request  # Import Flask's request object

# Load CSV data
csv_path = r"Nissan New Dataset.csv"
df = pd.read_csv(csv_path, encoding='latin1')

# Initialize the Dash app
app = dash.Dash(__name__)
CORS(app.server, resources={r"/*": {"origins": "*"}})

# CSS styles
styles = {
    'container': {
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center',
        'height': '100vh',
        'fontFamily': 'Arial, sans-serif',
        'backgroundColor': '#f0f0f0',
        'padding': '20px'
    },
    'left_div': {
        'width': '50%',
        'float': 'left',
        'paddingRight': '20px',
        'boxSizing': 'border-box'
    },
    'right_div': {
        'width': '50%',
        'float': 'right',
        'paddingLeft': '20px',
        'boxSizing': 'border-box'
    },
    'dropdown': {
        'width': '100%',
        'marginBottom': '10px',
        'display': 'block'
    },
    'datatable': {
        'overflowX': 'scroll',
        'border': '1px solid black'
    },
    'graph': {
        'height': 'calc(100vh - 120px)',
        'border': '1px solid black'
    }
}

# Define a function to limit text to 10 words with ellipsis
def limit_text(text, limit=10):
    if isinstance(text, str):
        if len(text.split()) > limit:
            return shorten(text, width=100, placeholder="...")
    return text

# Handle NaN values gracefully
df['feedback'] = df['feedback'].apply(limit_text)

# Select only the first 10 columns for display in DataTable
display_columns = df.columns[:10]

# Define layout
app.layout = html.Div(style=styles['container'], children=[
    html.Div(style=styles['left_div'], children=[
        html.H3('Data Analysis Dashboard'),
        html.Label('Select Date'),
        dcc.Dropdown(
            id='date-dropdown',
            options=[{'label': date, 'value': date} for date in df['date'].unique()],
            value=df['date'].unique()[0],
            style=styles['dropdown']
        ),
        html.Label('Select Models'),
        dcc.Dropdown(
            id='model-dropdown',
            options=[{'label': model, 'value': model} for model in df['model'].unique()],
            value=[df['model'].unique()[0]],
            multi=True,
            style=styles['dropdown']
        ),
    ]),
    html.Div(style=styles['right_div'], children=[
        DataTable(
            id='datatable',
            columns=[{'name': col, 'id': col} for col in display_columns],
            data=df[display_columns].to_dict('records'),
            style_table=styles['datatable'],
            style_cell={'textAlign': 'left', 'minWidth': '50px', 'width': '50px', 'maxWidth': '50px', 'whiteSpace': 'normal'},
            page_size=20
        ),
        html.Div(style=styles['graph'], children=[
            dcc.Graph(id='stacked-bar-graph')
        ]),
        html.Div(id='feedback-table', style={'marginTop': '20px'})
    ])
])


@app.callback(
    Output('datatable', 'data'),
    [Input('model-dropdown', 'value'), Input('date-dropdown', 'value')]
)
def update_datatable(selected_models, selected_date):
    if not selected_models:
        return []
    filtered_df = df[(df['model'].isin(selected_models)) & (df['date'] == selected_date)]
    filtered_df['feedback'] = filtered_df['feedback'].apply(limit_text)
    return filtered_df[display_columns].to_dict('records')


@app.callback(
    Output('stacked-bar-graph', 'figure'),
    [Input('model-dropdown', 'value'), Input('date-dropdown', 'value')]
)
def update_stackedgraph(selected_models, selected_date):
    if not selected_models:
        return go.Figure()
    filtered_df = df[(df['model'].isin(selected_models)) & (df['date'] == selected_date)]
    sentiment_counts = filtered_df['fact'].value_counts()
    total_count = sentiment_counts.sum()
    percentages = sentiment_counts / total_count * 100
    percentages = percentages.round(2)
    traces = []
    colors = ['#8b0000', '#d21401', '#545454', '#299617', '#234f1e']
    categories = ['Very Negative', 'Negative', 'Neutral', 'Positive', 'Very Positive']
    for i, category in enumerate(categories):
        trace = go.Bar(
            x=[category for _ in selected_models],
            y=[percentages.get(category, 0) for _ in selected_models],
            name=category,
            marker_color=colors[i],
            hoverinfo='y+name',
            showlegend=i == 0
        )
        traces.append(trace)
    layout = go.Layout(
        barmode='stack',
        xaxis={'title': 'Sentiments'},
        yaxis={'title': 'Percentage'},
        legend={'tracegroupgap': 10},
        title={'text': '<b>Sentiment Analysis</b>', 'font': {'size': 20}}
    )
    return {'data': traces, 'layout': layout}


@app.callback(
    Output('feedback-table', 'children'),
    [Input('stacked-bar-graph', 'clickData'), Input('model-dropdown', 'value'), Input('date-dropdown', 'value')]
)
def update_feedback_table(clickData, selected_models, selected_date):
    if clickData is None:
        return html.Div("Click on a bar to see feedback.")
    category = clickData['points'][0]['x']
    filtered_df = df[(df['fact'] == category) & (df['model'].isin(selected_models)) & (df['date'] == selected_date)]
    feedback_data = filtered_df[['feedback']].head().to_dict('records')
    if not feedback_data:
        return html.Div(f"No feedback available for category: {category}")

    # Construct the URL with query parameters
    url = f"/detailed_feedback?category={category}&models={','.join(selected_models)}&date={selected_date}"

    # Update layout with anchor tag
    return html.Div([
        html.H4(f'Feedback for Category: {category}'),
        html.A(f"View Detailed Feedback", href=url, target="_blank")
    ])
@app.server.route('/detailed_feedback')
def detailed_feedback():
    category = request.args.get('category')
    models = request.args.get('models').split(',')
    date = request.args.get('date')

    # Debugging output
    print(f"Category: {category}, Models: {models}, Date: {date}")

    # Ensure we work with a copy to avoid SettingWithCopyWarning
    filtered_df = df[(df['fact'] == category) & (df['model'].isin(models)) & (df['date'] == date)].copy()

    # Debugging output
    num_entries = len(filtered_df)
    print(f"Filtered DataFrame contains {num_entries} entries")

    # Select only the first 10 feedbacks if available
    feedback_data = filtered_df.head()

    if feedback_data.empty:
        return f"<h1>No feedback available for {category}</h1>"

    # Create an HTML table
    table_html = '<table border="1"><tr><th>Brand</th><th>Model</th><th>Date</th><th>Segment</th><th>Feedback</th></tr>'
    for _, row in feedback_data.iterrows():
        table_html += f"<tr><td>{row['brand']}</td><td>{row['model']}</td><td>{row['date']}</td><td>{row['segment']}</td><td>{row['feedback']}</td></tr>"
    table_html += '</table>'

    return f"<h1>Detailed Feedback for {category}</h1>{table_html}"

# Ensure this block is at the end
if __name__ == '__main__':
    app.run_server(port=8061, debug=True)
