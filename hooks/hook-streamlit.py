import math
from scipy.optimize import fsolve
import streamlit as st

# Function to calculate the central angle (theta)
def calculate_theta(yD):
    return 2 * math.acos(1 - 2 * yD)

# Function to calculate the hydraulic radius
def calculate_hydraulic_radius(area, wetted_perimeter):
    return area / wetted_perimeter if wetted_perimeter != 0 else None

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

# Streamlit Interface
st.title("Calculation of Circular Channels - Manning Equation")
st.sidebar.header("Select the variable to calculate")

# Sidebar to select the variable to calculate
variable_to_calculate = st.sidebar.radio(
    "Calculate:",
    options=["Flow Rate (Q)", "Diameter (D)", "y/D", "Slope (S)", "Roughness (n)"]
)



# Map variables to formula images
formula_images = {
    "Flow Rate (Q)": "assets/flow_rate_formula.png",
    "Diameter (D)": "assets/diameter_formula.png",
    "y/D": "assets/yD_formula.png",
    "Slope (S)": "assets/slope_formula.png",
    "Roughness (n)": "assets/roughness_formula.png"
}

# Layout with two columns
col1, col2 = st.columns([1,2])

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
    st.image(formula_images[variable_to_calculate], use_container_width=True)

# Automatic Calculation
try:
    if variable_to_calculate == "Flow Rate (Q)":
        result = calculate_flow_rate(diameter, yD, roughness, slope)
        st.success(f"Flow Rate (Q): {result:.4f} m³/s")
    elif variable_to_calculate == "Diameter (D)":
        result = calculate_diameter(yD, flow_rate, roughness, slope)
        st.success(f"Diameter (D): {result:.4f} m")
    elif variable_to_calculate == "y/D":
        result = calculate_yD(diameter, flow_rate, roughness, slope)
        st.success(f"y/D: {result:.4f}")
    elif variable_to_calculate == "Slope (S)":
        result = calculate_slope(diameter, yD, flow_rate, roughness)
        st.success(f"Slope (S): {result:.5f} m/m")
    elif variable_to_calculate == "Roughness (n)":
        result = calculate_roughness(diameter, yD, flow_rate, slope)
        st.success(f"Roughness (n): {result:.4f}")

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

if __name__ == "__main__":
    import os
    import webbrowser

    print("Starting Streamlit app...")

    try:
        # Open the default web browser to Streamlit's URL
        webbrowser.open("http://localhost:8501")

        # Run the Streamlit app
        os.system("streamlit run Calculation_of_Circular_Channels_st.py")
    except KeyboardInterrupt:
        print("Streamlit app stopped.")
    except Exception as e:
        print(f"An error occurred: {e}")
