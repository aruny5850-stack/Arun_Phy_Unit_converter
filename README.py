import streamlit as st

st.title("⚛️ Physics Unit Converter")

# Unit categories
categories = {
    "Length": {
        "Meter (m)": 1,
        "Centimeter (cm)": 0.01,
        "Kilometer (km)": 1000,
        "Millimeter (mm)": 0.001,
        "Micrometer (μm)": 1e-6,
        "Nanometer (nm)": 1e-9,
        "Angstrom (Å)": 1e-10
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
    }
}

# Category selection
category = st.selectbox(
    "Select Category",
    categories.keys()
)

# Get units for selected category
units = categories[category]

# Input
value = st.number_input(
    "Enter Value",
    value=1.0
)

col1, col2 = st.columns(2)

with col1:
    from_unit = st.selectbox(
        "From",
        units.keys()
    )

with col2:
    to_unit = st.selectbox(
        "To",
        units.keys()
    )

# Conversion
if st.button("Convert"):
    value_in_base = value * units[from_unit]
    result = value_in_base / units[to_unit]

    st.success(
        f"{value} {from_unit} = {result} {to_unit}"
    )
