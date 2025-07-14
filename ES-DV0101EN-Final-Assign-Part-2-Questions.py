import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load dataset
data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv'
)

# Initialize app
app = dash.Dash(__name__)

# List of years for dropdown
year_list = [i for i in range(1980, 2024)]

# Layout
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", style={
        'textAlign': 'center',
        'color': '#503D36',
        'font-size': 24
    }),

    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            placeholder='Select a report type',
            style={
                'width': '80%',
                'padding': '3px',
                'font-size': '20px',
                'text-align-last': 'center'
            }
        )
    ]),

    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            placeholder='Select year'
        )
    ]),

    html.Div(id='output-container', className='chart-grid', style={'display': 'flex', 'flexDirection': 'column'})
])

# TASK 2.4 - Enable/Disable Year Dropdown
@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    return True

# TASK 2.5 - Recession Graphs
@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'),
     Input('select-year', 'value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        # Plot 1 - Line chart
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec, x='Year', y='Automobile_Sales',
                title='Average Automobile Sales during Recession Years'
            )
        )

        # Plot 2 - Bar chart
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales, x='Vehicle_Type', y='Automobile_Sales',
                title='Average Vehicle Sales by Type during Recession'
            )
        )

        # Plot 3 - Pie chart
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec, values='Advertising_Expenditure', names='Vehicle_Type',
                title='Ad Expenditure Share by Vehicle Type (Recession)'
            )
        )

        # Plot 4 - Bar chart (Unemployment)
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data,
                x='unemployment_rate',
                y='Automobile_Sales',
                color='Vehicle_Type',
                labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
                title='Effect of Unemployment Rate on Vehicle Type and Sales'
            )
        )

        return [
            html.Div(className='chart-item', children=[R_chart1, R_chart2], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[R_chart3, R_chart4], style={'display': 'flex'})
        ]
    elif selected_statistics == 'Yearly Statistics' and input_year:
        # Filter data for the selected year
        yearly_data = data[data['Year'] == input_year]

        # Plot 1 - Line chart for average automobile sales over all years
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x='Year',
                y='Automobile_Sales',
                title='Average Automobile Sales Over All Years'
            )
        )

        # Plot 2 - Total monthly automobile sales in the selected year
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas,
                x='Month',
                y='Automobile_Sales',
                title='Total Monthly Automobile Sales in {}'.format(input_year)
            )
        )

        # Plot 3 - Average vehicles sold by vehicle type in the selected year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title='Average Vehicles Sold by Vehicle Type in {}'.format(input_year)
            )
        )

        # Plot 4 - Total Advertisement Expenditure for each vehicle type in selected year
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Advertisement Expenditure per Vehicle Type in {}'.format(input_year)
            )
        )

        return [
            html.Div(className='chart-item', children=[Y_chart1, Y_chart2], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[Y_chart3, Y_chart4], style={'display': 'flex'})
        ]
    return []

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
