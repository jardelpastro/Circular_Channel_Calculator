import os
import math
from scipy.optimize import fsolve
import streamlit as st
import sys

# Get the directory where the script is running
if getattr(sys, 'frozen', False):  # Executável
    BASE_DIR = sys._MEIPASS
else:  # Desenvolvimento local
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminho para a pasta assets
ASSETS_DIR = os.path.join(BASE_DIR, "assets")


# Function to calculate the central angle (theta)
def calculate_theta(yD):
    return 2 * math.acos(1 - 2 * yD)

# Function to calculate the hydraulic radius
def calculate_hydraulic_radius(area, wetted_perimeter):
    return area / wetted_perimeter if wetted_perimeter != 0 else None

# Function to calculate shear stress (tension trativa)
def calculate_shear_stress(hydraulic_radius, slope, specific_weight=9000):
    return specific_weight * hydraulic_radius * slope

# Function to calculate velocity (V)
def calculate_velocity(flow_rate, area):
    return flow_rate / area if area != 0 else None

# Function to calculate y/D
def calculate_yD(diameter, flow_rate, roughness, slope):
    def equation(yD):
        theta = calculate_theta(yD)
        area = (theta - math.sin(theta)) * (diameter ** 2) / 8
        wetted_perimeter = theta * diameter / 2
        hydraulic_radius = calculate_hydraulic_radius(area, wetted_perimeter)
        calculated_flow = (1 / roughness) * area * (hydraulic_radius ** (2 / 3)) * (slope ** 0.5)
        return calculated_flow - flow_rate
    return fsolve(equation, 0.5)[0]

# Function to calculate the diameter (D)
def calculate_diameter(yD, flow_rate, roughness, slope):
    def equation(diameter):
        theta = calculate_theta(yD)
        area = (theta - math.sin(theta)) * (diameter ** 2) / 8
        wetted_perimeter = theta * diameter / 2
        hydraulic_radius = calculate_hydraulic_radius(area, wetted_perimeter)
        calculated_flow = (1 / roughness) * area * (hydraulic_radius ** (2 / 3)) * (slope ** 0.5)
        return calculated_flow - flow_rate
    return fsolve(equation, 1.0)[0]

# Function to calculate flow rate (Q)
def calculate_flow_rate(diameter, yD, roughness, slope):
    theta = calculate_theta(yD)
    area = (theta - math.sin(theta)) * (diameter ** 2) / 8
    wetted_perimeter = theta * diameter / 2
    hydraulic_radius = calculate_hydraulic_radius(area, wetted_perimeter)
    return (1 / roughness) * area * (hydraulic_radius ** (2 / 3)) * (slope ** 0.5)

# Function to calculate roughness (n)
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

# Map variables to formula images
formula_images = {
    "Flow Rate (Q)": os.path.join(ASSETS_DIR, "flow_rate_formula.png"),
    "Diameter (D)": os.path.join(ASSETS_DIR, "diameter_formula.png"),
    "y/D": os.path.join(ASSETS_DIR, "yD_formula.png"),
    "Slope (S)": os.path.join(ASSETS_DIR, "slope_formula.png"),
    "Roughness (n)": os.path.join(ASSETS_DIR, "roughness_formula.png"),
    "Shear Stress (τ)": os.path.join(ASSETS_DIR, "shear_stress_formula.png"),
    "Velocity (V)": os.path.join(ASSETS_DIR, "velocity_formula.png"),
}

# Streamlit Interface
st.title("Calculation of Circular Channels - Manning Equation")
st.sidebar.header("Select the variable to calculate")

# Sidebar to select the variable to calculate
variable_to_calculate = st.sidebar.radio(
    "Calculate:",
    options=["Flow Rate (Q)", "Diameter (D)", "y/D", "Slope (S)", "Roughness (n)"]
)

# Layout with two columns
col1, col2 = st.columns([1, 2])

with col1:
    st.header("Input Data")
    # Input fields for user-provided data
    flow_rate = st.number_input("Flow Rate (Q) [m³/s]:", value=0.1, step=0.001, format="%.3f")
    diameter = st.number_input("Diameter (D) [m]:", value=1.0, step=0.001, format="%.3f")
    yD = st.number_input("y/D (Water Depth / Diameter):", value=0.5, step=0.01, format="%.2f")
    slope = st.number_input("Slope (S) [m/m]:", value=0.00450, step=0.00001, format="%.5f")
    roughness = st.number_input("Roughness (n):", value=0.013, step=0.001, format="%.3f")

with col2:
    # Display the selected formula image
    st.subheader("Formula:")
    # Check if the file exists before displaying
    image_path = formula_images[variable_to_calculate]
    if os.path.exists(image_path):
        try:
            st.image(image_path, use_column_width=True)
        except Exception as e:
            st.error(f"Error loading image: {e}")
    else:
        st.error(f"Image not found: {image_path}")

# Automatic Calculation
try:
    hydraulic_radius = None
    shear_stress = None
    velocity = None

    if variable_to_calculate == "Flow Rate (Q)":
        result = calculate_flow_rate(diameter, yD, roughness, slope)
        theta = calculate_theta(yD)
        area = (theta - math.sin(theta)) * (diameter ** 2) / 8
        wetted_perimeter = theta * diameter / 2
        hydraulic_radius = calculate_hydraulic_radius(area, wetted_perimeter)
        shear_stress = calculate_shear_stress(hydraulic_radius, slope)
        velocity = calculate_velocity(result, area)
        st.success(f"Flow Rate (Q): {result:.4f} m³/s")

    elif variable_to_calculate == "Diameter (D)":
        result = calculate_diameter(yD, flow_rate, roughness, slope)
        theta = calculate_theta(yD)
        area = (theta - math.sin(theta)) * (result ** 2) / 8
        wetted_perimeter = theta * result / 2
        hydraulic_radius = calculate_hydraulic_radius(area, wetted_perimeter)
        shear_stress = calculate_shear_stress(hydraulic_radius, slope)
        velocity = calculate_velocity(flow_rate, area)
        st.success(f"Diameter (D): {result:.4f} m")

    elif variable_to_calculate == "y/D":
        result = calculate_yD(diameter, flow_rate, roughness, slope)
        theta = calculate_theta(result)
        area = (theta - math.sin(theta)) * (diameter ** 2) / 8
        wetted_perimeter = theta * diameter / 2
        hydraulic_radius = calculate_hydraulic_radius(area, wetted_perimeter)
        shear_stress = calculate_shear_stress(hydraulic_radius, slope)
        velocity = calculate_velocity(flow_rate, area)
        st.success(f"y/D: {result:.4f}")

    elif variable_to_calculate == "Slope (S)":
        result = calculate_slope(diameter, yD, flow_rate, roughness)
        theta = calculate_theta(yD)
        area = (theta - math.sin(theta)) * (diameter ** 2) / 8
        wetted_perimeter = theta * diameter / 2
        hydraulic_radius = calculate_hydraulic_radius(area, wetted_perimeter)
        shear_stress = calculate_shear_stress(hydraulic_radius, result)
        velocity = calculate_velocity(flow_rate, area)
        st.success(f"Slope (S): {result:.5f} m/m")

    elif variable_to_calculate == "Roughness (n)":
        result = calculate_roughness(diameter, yD, flow_rate, slope)
        theta = calculate_theta(yD)
        area = (theta - math.sin(theta)) * (diameter ** 2) / 8
        wetted_perimeter = theta * diameter / 2
        hydraulic_radius = calculate_hydraulic_radius(area, wetted_perimeter)
        shear_stress = calculate_shear_stress(hydraulic_radius, slope)
        velocity = calculate_velocity(flow_rate, area)
        st.success(f"Roughness (n): {result:.4f}")

    # Display Shear Stress and Velocity in all cases
    if shear_stress is not None:
       st.success(f"Shear Stress (τ): {shear_stress:.2f} N/m²")

    if velocity is not None:
        st.success(f"Velocity (V): {velocity:.2f} m/s")

    # Display all results
    st.subheader("Results:")
    st.markdown(f"""
    - **Flow Rate (Q):** {flow_rate:.4f} m³/s {"(calculated)" if variable_to_calculate == "Flow Rate (Q)" else ""}
    - **Diameter (D):** {diameter:.4f} m {"(calculated)" if variable_to_calculate == "Diameter (D)" else ""}
    - **y/D:** {yD:.4f} {"(calculated)" if variable_to_calculate == "y/D" else ""}
    - **Slope (S):** {slope:.5f} m/m {"(calculated)" if variable_to_calculate == "Slope (S)" else ""}
    - **Roughness (n):** {roughness:.4f} {"(calculated)" if variable_to_calculate == "Roughness (n)" else ""}
    """)

except Exception as e:
    st.error(f"An error occurred: {e}")