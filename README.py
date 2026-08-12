import streamlit as st
import math

st.set_page_config(
    page_title="Physics Toolkit",
    page_icon="⚛️"
)

st.title("⚛️ Physics Toolkit")

# =========================
# UNIT CONVERTER Yaha se start hua hai
# =========================

categories = {
    "Length": {
        "Meter (m)": 1,
        "Centimeter (cm)": 0.01,
        "Kilometer (km)": 1000,
        "Millimeter (mm)": 0.001,
        "Micrometer (μm)": 1e-6,
        "Nanometer (nm)": 1e-9,
        "Angstrom (Å)": 1e-10,
        "Pico (pm)": 1e-12
    },

    "Mass": {
        "Kilogram (kg)": 1,
        "Gram (g)": 0.001,
        "Milligram (mg)": 1e-6
    },

    "Time": {
        "Second (s)": 1,
        "Millisecond (ms)": 1e-3,
        "Microsecond (μs)": 1e-6,
        "Nanosecond (ns)": 1e-9,
        "Minute (min)": 60,
        "Hour (h)": 3600
    },

    "Energy": {
        "Joule (J)": 1,
        "Electron Volt (eV)": 1.602176634e-19,
        "kilo Electron Volt (keV)": 1.602176634e-16,
        "Mega Electron Volt (MeV)": 1.602176634e-13
    }
}


# =========================
# TABS
# =========================

tab1, tab2 = st.tabs([
    "⚛️ Unit Converter",
    "🧮 Calculator"
])


# =========================
# TAB 1: UNIT CONVERTER
# =========================

with tab1:

    st.header("Unit Converter")

    category = st.selectbox(
        "Select Category",
        list(categories.keys()) + ["Temperature"]
    )

    value = st.number_input(
        "Enter Value",
        value=1.0
    )

    # Temperature
    if category == "Temperature":

        temperature_units = [
            "Celsius (°C)",
            "Kelvin (K)",
            "Fahrenheit (°F)"
        ]

        col1, col2 = st.columns(2)

        with col1:
            from_unit = st.selectbox(
                "From",
                temperature_units
            )

        with col2:
            to_unit = st.selectbox(
                "To",
                temperature_units
            )

        if st.button("Convert Temperature"):

            # Convert to Celsius first
            if from_unit == "Celsius (°C)":
                celsius = value

            elif from_unit == "Kelvin (K)":
                celsius = value - 273.15

            else:
                celsius = (value - 32) * 5 / 9

            # Celsius to target
            if to_unit == "Celsius (°C)":
                result = celsius

            elif to_unit == "Kelvin (K)":
                result = celsius + 273.15

            else:
                result = (celsius * 9 / 5) + 32

            st.success(
                f"{value} {from_unit} = {result} {to_unit}"
            )

    # Other categories
    else:

        units = categories[category]

        col1, col2 = st.columns(2)

        with col1:
            from_unit = st.selectbox(
                "From",
                list(units.keys())
            )

        with col2:
            to_unit = st.selectbox(
                "To",
                list(units.keys())
            )

        if st.button("Convert"):

            value_in_base = value * units[from_unit]

            result = value_in_base / units[to_unit]

            st.success(
                f"{value} {from_unit} = {result} {to_unit}"
            )


# =========================
# TAB 2: CALCULATOR
# =========================

with tab2:

    st.header("🧮 Scientific Calculator")

    expression = st.text_input(
        "Enter calculation",
        placeholder="Example: (10 + 5) * 2"
    )

    st.write(
        "Available: +  -  *  /  **  %  √  sin  cos  tan  log  ln  π"
    )

    if st.button("Calculate"):

        try:

            # Replace common mathematical symbols
            expression = expression.replace("√", "sqrt")
            expression = expression.replace("π", "pi")

            # Allowed mathematical functions
            allowed = {
                "sqrt": math.sqrt,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "log": math.log10,
                "ln": math.log,
                "pi": math.pi,
                "e": math.e,
                "abs": abs
            }

            result = eval(
                expression,
                {"__builtins__": {}},
                allowed
            )

            st.success(f"Result = {result}")

        except Exception:
            st.error(
                "Invalid calculation. Please check your expression."
            )
