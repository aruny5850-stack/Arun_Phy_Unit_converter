import streamlit as st
import math

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Physics Toolkit",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background: linear-gradient(135deg, #07111f, #0d1b2a);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

.hero {
    padding: 28px;
    border-radius: 22px;
    background: linear-gradient(135deg, #102a43, #243b53);
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 10px 35px rgba(0,0,0,0.25);
    margin-bottom: 25px;
}

.hero h1 {
    color: white;
    font-size: 42px;
    margin-bottom: 5px;
}

.hero p {
    color: #c9d6e2;
    font-size: 17px;
}

.card {
    background: rgba(255,255,255,0.06);
    padding: 25px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 20px;
}

.result {
    background: linear-gradient(135deg, #0b3d3d, #126e82);
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    margin-top: 20px;
    border: 1px solid rgba(255,255,255,0.15);
}

.result h2 {
    color: white;
    font-size: 34px;
}

.result p {
    color: #d8f3f0;
    font-size: 16px;
}

.small {
    color: #aab7c4;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# UNIT DATABASE
# Base unit = SI / MKS
# conversion factor means:
# value_in_SI = value * factor
# =========================================================

UNITS = {

    "Length": {
        "meter (m)": 1,
        "kilometer (km)": 1000,
        "centimeter (cm)": 0.01,
        "millimeter (mm)": 0.001,
        "micrometer (μm)": 1e-6,
        "nanometer (nm)": 1e-9,
        "angstrom (Å)": 1e-10,
        "inch (in)": 0.0254,
        "foot (ft)": 0.3048,
        "mile (mi)": 1609.344,
    },

    "Mass": {
        "kilogram (kg)": 1,
        "gram (g)": 1e-3,
        "milligram (mg)": 1e-6,
        "microgram (μg)": 1e-9,
        "tonne (t)": 1000,
    },

    "Time": {
        "second (s)": 1,
        "millisecond (ms)": 1e-3,
        "microsecond (μs)": 1e-6,
        "nanosecond (ns)": 1e-9,
        "minute (min)": 60,
        "hour (h)": 3600,
        "day": 86400,
    },

    "Area": {
        "square meter (m²)": 1,
        "square centimeter (cm²)": 1e-4,
        "square millimeter (mm²)": 1e-6,
        "square kilometer (km²)": 1e6,
        "square inch (in²)": 0.00064516,
        "square foot (ft²)": 0.09290304,
    },

    "Volume": {
        "cubic meter (m³)": 1,
        "liter (L)": 1e-3,
        "milliliter (mL)": 1e-6,
        "cubic centimeter (cm³)": 1e-6,
        "cubic millimeter (mm³)": 1e-9,
    },

    "Velocity": {
        "meter/second (m/s)": 1,
        "centimeter/second (cm/s)": 0.01,
        "kilometer/hour (km/h)": 1000 / 3600,
        "mile/hour (mph)": 1609.344 / 3600,
    },

    "Acceleration": {
        "meter/second² (m/s²)": 1,
        "centimeter/second² (cm/s²)": 0.01,
        "standard gravity (g)": 9.80665,
    },

    "Force": {
        "newton (N)": 1,
        "dyne (dyn)": 1e-5,
        "kilonewton (kN)": 1000,
    },

    "Energy": {
        "joule (J)": 1,
        "erg": 1e-7,
        "kilojoule (kJ)": 1000,
        "electronvolt (eV)": 1.602176634e-19,
    },

    "Power": {
        "watt (W)": 1,
        "kilowatt (kW)": 1000,
        "erg/second (erg/s)": 1e-7,
        "horsepower (hp)": 745.699872,
    },

    "Pressure": {
        "pascal (Pa)": 1,
        "dyne/cm²": 0.1,
        "bar": 1e5,
        "atmosphere (atm)": 101325,
        "torr": 133.322368,
    },

    "Frequency": {
        "hertz (Hz)": 1,
        "kilohertz (kHz)": 1e3,
        "megahertz (MHz)": 1e6,
        "gigahertz (GHz)": 1e9,
    },

    "Electric Charge": {
        "coulomb (C)": 1,
        "abcoulomb (abC)": 10,
        "statcoulomb (statC)": 3.33564e-10,
    },

    "Electric Potential": {
        "volt (V)": 1,
        "statvolt": 299.792458,
    },

    "Resistance": {
        "ohm (Ω)": 1,
        "abohm": 1e-9,
        "statohm": 8.987551787e11,
    },

    "Capacitance": {
        "farad (F)": 1,
        "abfarad": 1e9,
        "statfarad": 1.11265e-12,
    },

    "Magnetic Flux": {
        "weber (Wb)": 1,
        "maxwell (Mx)": 1e-8,
    },

    "Magnetic Field": {
        "tesla (T)": 1,
        "gauss (G)": 1e-4,
    },

    "Temperature": {
        "kelvin (K)": "temperature",
        "celsius (°C)": "temperature",
        "fahrenheit (°F)": "temperature",
    },
}


# =========================================================
# TEMPERATURE CONVERSION
# =========================================================

def temperature_to_kelvin(value, unit):

    if unit == "kelvin (K)":
        return value

    if unit == "celsius (°C)":
        return value + 273.15

    if unit == "fahrenheit (°F)":
        return (value - 32) * 5 / 9 + 273.15


def kelvin_to_temperature(value, unit):

    if unit == "kelvin (K)":
        return value

    if unit == "celsius (°C)":
        return value - 273.15

    if unit == "fahrenheit (°F)":
        return (value - 273.15) * 9 / 5 + 32


# =========================================================
# NORMAL CONVERSION
# =========================================================

def convert(value, category, from_unit, to_unit):

    # Temperature
    if category == "Temperature":

        kelvin = temperature_to_kelvin(value, from_unit)

        return kelvin_to_temperature(
            kelvin,
            to_unit
        )

    # Other quantities
    from_factor = UNITS[category][from_unit]
    to_factor = UNITS[category][to_unit]

    value_si = value * from_factor

    result = value_si / to_factor

    return result


# =========================================================
# FORMAT NUMBER
# =========================================================

def format_number(value):

    if value == 0:
        return "0"

    if abs(value) >= 1e6 or abs(value) < 1e-4:
        return f"{value:.6e}"

    return f"{value:.10g}"


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="hero">

<h1>⚛️ Physics Toolkit</h1>

<p>
A powerful physics utility for unit conversion,
scientific calculations and physical quantities.
</p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## ⚛️ Physics Toolkit")

    st.markdown("---")

    tool = st.radio(
        "Select Tool",
        [
            "🔄 Unit Converter",
            "📐 Physical Constants"
        ]
    )

    st.markdown("---")

    st.markdown("""
    **Supported systems**

    • SI / MKS  
    • CGS  
    • Electromagnetic CGS units  
    • Scientific notation  

    **Designed for Physics students**
    """)


# =========================================================
# UNIT CONVERTER
# =========================================================

if tool == "🔄 Unit Converter":

    st.markdown("""
    <div class="card">

    <h2>🔄 Universal Unit Converter</h2>

    <p class="small">
    Convert physical quantities between SI/MKS, CGS
    and other commonly used units.
    </p>

    </div>
    """, unsafe_allow_html=True)

    categories = list(UNITS.keys())

    category = st.selectbox(
        "📚 Physical Quantity",
        categories
    )

    units = list(UNITS[category].keys())

    col1, col2 = st.columns([1, 1])

    with col1:

        value = st.number_input(
            "Enter Value",
            value=1.0,
            format="%.10g"
        )

        from_unit = st.selectbox(
            "From",
            units,
            key="from"
        )

    with col2:

        to_unit = st.selectbox(
            "To",
            units,
            key="to"
        )

        st.write("")

        convert_button = st.button(
            "⚡ CONVERT",
            use_container_width=True
        )


    # =====================================================
    # RESULT
    # =====================================================

    if convert_button:

        try:

            result = convert(
                value,
                category,
                from_unit,
                to_unit
            )

            st.markdown(
                f"""
                <div class="result">

                <p>RESULT</p>

                <h2>
                {format_number(result)}
                </h2>

                <p>
                {from_unit} → {to_unit}
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

        except Exception as e:

            st.error(
                f"Conversion error: {e}"
            )


# =========================================================
# PHYSICAL CONSTANTS
# =========================================================

elif tool == "📐 Physical Constants":

    st.markdown("""
    <div class="card">

    <h2>📐 Fundamental Physical Constants</h2>

    </div>
    """, unsafe_allow_html=True)

    constants = {

        "Speed of light (c)": "299792458 m/s",

        "Planck constant (h)": "6.62607015 × 10⁻³⁴ J·s",

        "Reduced Planck constant (ℏ)": "1.054571817 × 10⁻³⁴ J·s",

        "Elementary charge (e)": "1.602176634 × 10⁻¹⁹ C",

        "Electron mass": "9.1093837139 × 10⁻³¹ kg",

        "Proton mass": "1.67262192595 × 10⁻²⁷ kg",

        "Gravitational constant (G)": "6.67430 × 10⁻¹¹ m³ kg⁻¹ s⁻²",

        "Boltzmann constant (kB)": "1.380649 × 10⁻²³ J/K",

        "Avogadro constant (NA)": "6.02214076 × 10²³ mol⁻¹",

        "Vacuum permittivity (ε₀)": "8.8541878188 × 10⁻¹² F/m",

        "Vacuum permeability (μ₀)": "1.25663706127 × 10⁻⁶ H/m",

    }

    for name, value in constants.items():

        st.markdown(
            f"""
            <div class="card">

            <b>{name}</b>

            <br>

            <span class="small">
            {value}
            </span>

            </div>
            """,
            unsafe_allow_html=True
        )
