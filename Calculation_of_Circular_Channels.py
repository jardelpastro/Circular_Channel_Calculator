from dash import Dash, dcc, html, Input, Output, State
import math
from scipy.optimize import fsolve

# Function to calculate the central angle (theta)
def calculate_theta(yD):
    return 2 * math.acos(1 - 2 * yD)

# Function to calculate the hydraulic radius
def calculate_hydraulic_radius(area, wetted_perimeter):
    return area / wetted_perimeter if wetted_perimeter != 0 else None

# Função to calculate y/D
def calculate_yD(diameter, flow_rate, roughness, slope):
    def equation(yD):
        theta = calculate_theta(yD)
        area = (theta - math.sin(theta)) * (diameter ** 2) / 8
        wetted_perimeter = theta * diameter / 2
        hydraulic_radius = calculate_hydraulic_radius(area, wetted_perimeter)
        calculated_flow = (1 / roughness) * area * (hydraulic_radius ** (2 / 3)) * (slope ** 0.5)
        return calculated_flow - flow_rate

    initial_guess = 0.5
    return fsolve(equation, initial_guess)[0]

# Function to calculate the diameter (D)
def calculate_diameter(yD, flow_rate, roughness, slope):
    def equation(diameter):
        theta = calculate_theta(yD)
        area = (theta - math.sin(theta)) * (diameter ** 2) / 8
        wetted_perimeter = theta * diameter / 2
        hydraulic_radius = calculate_hydraulic_radius(area, wetted_perimeter)
        calculated_flow = (1 / roughness) * area * (hydraulic_radius ** (2 / 3)) * (slope ** 0.5)
        return calculated_flow - flow_rate

    initial_guess = 1.0
    return fsolve(equation, initial_guess)[0]

# Function to calculate flow rate (Q)
def calculate_flow_rate(diameter, yD, roughness, slope):
    theta = calculate_theta(yD)
    area = (theta - math.sin(theta)) * (diameter ** 2) / 8
    wetted_perimeter = theta * diameter / 2
    hydraulic_radius = calculate_hydraulic_radius(area, wetted_perimeter)
    return (1 / roughness) * area * (hydraulic_radius ** (2 / 3)) * (slope ** 0.5)

# Funtion to calculate roughness (n)
def calculate_roughness(diameter, yD, flow_rate, slope):
    theta = calculate_theta(yD)
    area = (theta - math.sin(theta)) * (diameter ** 2) / 8
    wetted_perimeter = theta * diameter / 2
    hydraulic_radius = calculate_hydraulic_radius(area, wetted_perimeter)
    return (area * (hydraulic_radius ** (2 / 3)) * (slope ** 0.5)) / flow_rate

# Function to calculate slope (S)
def calculate_slope(diameter, yD, flow_rate, roughness):
    theta = calculate_theta(yD)
    area = (theta - math.sin(theta)) * (diameter ** 2) / 8
    wetted_perimeter = theta * diameter / 2
    hydraulic_radius = calculate_hydraulic_radius(area, wetted_perimeter)
    return ((flow_rate * roughness) / (area * (hydraulic_radius ** (2 / 3)))) ** 2

# Starting app Dash
app = Dash(__name__)

# App Layout
app.layout = html.Div([
    html.H1("Calculation of Circular Channels - Manning Equation", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Diameter (D) [m]:"),
        dcc.Input(id='input-diameter', type='number', value=1.0, step=0.001),
        dcc.Checklist(
            options=[{'label': 'Calculate', 'value': 'diameter'}],
            id='check-diameter',
            inline=True,
            value=[]
        )
    ], style={'margin-bottom': '20px'}),

    html.Div([
        html.Label("y/D (Water Depth / Diameter):"),
        dcc.Input(id='input-yD', type='number', value=0.5, step=0.01),
        dcc.Checklist(
            options=[{'label': 'Calculate', 'value': 'yD'}],
            id='check-yD',
            inline=True,
            value=[]
        )
    ], style={'margin-bottom': '20px'}),

    html.Div([
        html.Label("Slope (S):"),
        dcc.Input(id='input-slope', type='number', value=0.00450, step=0.00001),
        dcc.Checklist(
            options=[{'label': 'Calculate', 'value': 'slope'}],
            id='check-slope',
            inline=True,
            value=[]
        )
    ], style={'margin-bottom': '20px'}),

    html.Div([
        html.Label("Roughness (n):"),
        dcc.Input(id='input-roughness', type='number', value=0.013, step=0.001),
        dcc.Checklist(
            options=[{'label': 'Calculate', 'value': 'roughness'}],
            id='check-roughness',
            inline=True,
            value=[]
        )
    ], style={'margin-bottom': '20px'}),

    html.Div([
        html.Label("Flow Rate(Q):"),
        dcc.Input(id='input-flow-rate', type='number', value=0.1, step=0.001),
        dcc.Checklist(
            options=[{'label': 'Calculate', 'value': 'flow_rate'}],
            id='check-flow-rate',
            value=['flow_rate'], # Start with a check
            inline=True,
            )
    ], style={'margin-bottom': '20px'}),

    html.H2("Calculated Results", style={'margin-top': '40px'}),
    html.Div(id='result-output', style={'margin-top': '20px', 'font-size': '20px'})
])

# Callback to uptade the results
@app.callback(
    Output('result-output', 'children'),
    [
        Input('input-diameter', 'value'),
        Input('input-yD', 'value'),
        Input('input-slope', 'value'),
        Input('input-roughness', 'value'),
        Input('input-flow-rate', 'value'),
        Input('check-diameter', 'value'),
        Input('check-yD', 'value'),
        Input('check-slope', 'value'),
        Input('check-roughness', 'value'),
        Input('check-flow-rate', 'value')
    ]
)
def update_results(diameter, yD, slope, roughness, flow_rate, check_diameter, check_yD, check_slope, check_roughness, check_flow_rate):
    try:
        highlighted = None

        # Identify what item is checked
        if 'diameter' in check_diameter:
            diameter = calculate_diameter(yD, flow_rate, roughness, slope)
            highlighted = 'diameter'
        elif 'yD' in check_yD:
            yD = calculate_yD(diameter, flow_rate, roughness, slope)
            highlighted = 'yD'
        elif 'slope' in check_slope:
            slope = calculate_slope(diameter, yD, flow_rate, roughness)
            highlighted = 'slope'
        elif 'roughness' in check_roughness:
            roughness = calculate_roughness(diameter, yD, flow_rate, slope)
            highlighted = 'roughness'
        elif 'flow_rate' in check_flow_rate:
            flow_rate = calculate_flow_rate(diameter, yD, roughness, slope)
            highlighted = 'flow_rate'
        else:
            return "Select a variable to calculate!"

        # Show the results

        return html.Div([
            html.Div(f"Flow Rate (Q): {flow_rate:.4f} m³/s", style={'color': 'blue'} if highlighted == 'flow_rate' else {}),
            html.Div(f"Diameter (D): {diameter:.4f} m", style={'color': 'blue'} if highlighted == 'diameter' else {}),
            html.Div(f"y/D: {yD:.2f}", style={'color': 'blue'} if highlighted == 'yD' else {}),
            html.Div(f"Slope (S): {slope:.5f} m/m", style={'color': 'blue'} if highlighted == 'slope' else {}),
            html.Div(f"Roughness (n): {roughness:.4f}", style={'color': 'blue'} if highlighted == 'roughness' else {}),

        ])
    except Exception as e:
        return str(e)

# Start App
if __name__ == '__main__':
    app.run_server(debug=True)
