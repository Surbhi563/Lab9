import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
import wikipediaapi

# Connect to the Wikipedia API
wiki = wikipediaapi.Wikipedia('en')

# Define the layout of the dashboard
app = dash.Dash(__name__)
app.title = 'Wikipedia Dashboard'

# Define styles for the layout
styles = {
 
    'textAlign': 'center',
    'fontFamily': 'Arial, sans-serif',
    'color': 'white',
}

# Define the header and footer
header = html.Div([
    html.Img(src='https://newagora.ca/wp-content/uploads/2019/08/Wikipedia-Logo-on-Black.jpg', style={'height': '200px','width': '100%'}),
 html.Div([
        dcc.Input(id='input-box', type='text', placeholder='Enter a page title'),
        html.Button('Search', id='button', n_clicks=0)
    ], style={'position': 'absolute', 'top': '10%', 'left': '85%', 'transform': 'translate(-50%, -50%)'})
], style={'width': '100%'})

footer = html.Div([
    html.P('Created by: Surbhi Dua', style={'fontSize': '14px', 'marginBottom': '0','marginTop': '10px'}),
    html.P('Data from Wikipedia', style={'fontSize': '12px', 'marginTop': '10px','paddingBottom': '5px'})
], style={'backgroundColor': 'black','position': 'fixed', 'bottom': '0', 'width': '100%'})

app.layout = html.Div(style=styles, children=[
    header,
    
    dcc.Graph(id='graph', style={'marginTop': '20px'}),
    footer
])

# Define the callback function to retrieve and process data
@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def update_figure(n_clicks, value):
    if not value:
        return go.Figure()

    # Retrieve the Wikipedia page content
    page = wiki.page(value)
    if not page.exists():
        return go.Figure()
    
    # Process the data
    sections = page.sections
    labels = [section.title for section in sections]
    values = [len(section.text.split()) for section in sections]
    
    # Create the bar chart
    trace = go.Bar(
        x=labels,
        y=values,
        marker={
            'color': values,
            'colorscale': 'Viridis'
        },
        hovertext=values,
        hovertemplate='%{hovertext} words',
        textposition='outside'
    )
    layout = go.Layout(
        title='Word Count by Section',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font={'color': 'black'},
        xaxis={
            'tickangle': -45,
            'tickfont': {'size': 14}
        },
        yaxis={
            'title': {'text': 'Word Count', 'font': {'size': 14}},
            'tickfont': {'size': 14},
            'gridcolor': '#555'
        },
        margin={'b': 120},
        height=600
    )

    fig = go.Figure(data=[trace], layout=layout)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
