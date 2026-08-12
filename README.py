import streamlit as st

st.title("⚛️ Physics Unit Converter")
st.write("Convert common length units easily.")

# User input
value = st.number_input("Enter value", min_value=0.0, value=1.0)

# Units
units = {
    "Meter (m)": 1,
    "Centimeter (cm)": 0.01,
    "Kilometer (km)": 1000,
    "Millimeter (mm)": 0.001,
    "Micrometer (μm)": 1e-6,
    "Nanometer (nm)": 1e-9,
    "Angstrom (Å)": 1e-10
}

col1, col2 = st.columns(2)

with col1:
    from_unit = st.selectbox("From", units.keys())

with col2:
    to_unit = st.selectbox("To", units.keys())

if st.button("Convert"):
    # First convert to meter
    value_in_meter = value * units[from_unit]

    # Then convert meter to target unit
    result = value_in_meter / units[to_unit]

    st.success(f"{value} {from_unit} = {result} {to_unit}")
