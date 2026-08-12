import streamlit as st
import math

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Physics Toolkit",
    page_icon="⚛️",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 10%, #172554 0%, transparent 30%),
        radial-gradient(circle at 90% 10%, #312e81 0%, transparent 30%),
        linear-gradient(135deg, #020617, #0f172a, #111827);
    color: white;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* HEADER */

.hero {
    padding: 40px;
    border-radius: 28px;
    margin-bottom: 30px;
    background: linear-gradient(
        135deg,
        rgba(14, 165, 233, 0.18),
        rgba(99, 102, 241, 0.20)
    );
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 20px 60px rgba(0,0,0,0.35);
}

.hero h1 {
    margin: 0;
    font-size: 48px;
    font-weight: 800;
    color: white;
}

.hero p {
    color: #cbd5e1;
    font-size: 17px;
}

/* CARD */

.card {
    padding: 28px;
    border-radius: 22px;
    margin-bottom: 22px;
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow: 0 12px 35px rgba(0,0,0,0.25);
}

/* INPUT */

div[data-baseweb="input"] {
    background: rgba(255,255,255,0.06) !important;
    border-radius: 13px !important;
}

/* SELECTBOX */

div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.06) !important;
    border-radius: 13px !important;
}

/* BUTTON */

.stButton > button {
    width: 100%;
    height: 52px;
    border: none !important;
    border-radius: 14px !important;
    color: white !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    background: linear-gradient(
        135deg,
        #06b6d4,
        #2563eb,
        #7c3aed
    ) !important;
    box-shadow: 0 10px 30px rgba(37,99,235,0.30);
}

.stButton > button:hover {
    transform: translateY(-2px);
}

/* RESULT */

.result {
    padding: 32px;
    margin-top: 25px;
    border-radius: 24px;
    text-align: center;
    background: linear-gradient(
        135deg,
        rgba(6,182,212,0.15),
        rgba(37,99,235,0.18),
        rgba(124,58,237,0.18)
    );
    border: 1px solid rgba(96,165,250,0.25);
    box-shadow: 0 15px 45px rgba(0,0,0,0.30);
}

.result-title {
    color: #93c5fd;
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.result-value {
    color: white;
    font-size: 40px;
    font-weight: 800;
    margin: 12px;
}

/* TABS */

button[data-baseweb="tab"] {
    font-size: 16px;
    font-weight: 600;
}

/* MOBILE */

@media (max-width: 768px) {

    .hero {
        padding: 25px;
    }

    .hero h1 {
        font-size: 34px;
    }

    .result-value {
        font-size: 28px;
    }

}

</style>
""", unsafe_allow_html=True)


# =========================================================
# UNIT DATABASE
# =========================================================

UNITS = {

    "Length": {
        "meter (m)": 1,
        "kilometer (km)": 1000,
        "centimeter (cm)": 1e-2,
        "millimeter (mm)": 1e-3,
        "micrometer (μm)": 1e-6,
        "nanometer (nm)": 1e-9,
        "angstrom (Å)": 1e-10,
        "inch (in)": 0.0254,
        "foot (ft)": 0.3048,
        "mile (mi)": 1609.344
    },

    "Mass": {
        "kilogram (kg)": 1,
        "gram (g)": 1e-3,
        "milligram (mg)": 1e-6,
        "microgram (μg)": 1e-9,
        "tonne (t)": 1000
    },

    "Time": {
        "second (s)": 1,
        "millisecond (ms)": 1e-3,
        "microsecond (μs)": 1e-6,
        "nanosecond (ns)": 1e-9,
        "minute (min)": 60,
        "hour (h)": 3600,
        "day": 86400
    },

    "Area": {
        "square meter (m²)": 1,
        "square centimeter (cm²)": 1e-4,
        "square millimeter (mm²)": 1e-6,
        "square kilometer (km²)": 1e6,
        "square inch (in²)": 0.00064516,
        "square foot (ft²)": 0.09290304
    },

    "Volume": {
        "cubic meter (m³)": 1,
        "liter (L)": 1e-3,
        "milliliter (mL)": 1e-6,
        "cubic centimeter (cm³)": 1e-6,
        "cubic millimeter (mm³)": 1e-9
    },

    "Velocity": {
        "meter/second (m/s)": 1,
        "centimeter/second (cm/s)": 1e-2,
        "kilometer/hour (km/h)": 1000 / 3600,
        "mile/hour (mph)": 1609.344 / 3600
    },

    "Acceleration": {
        "meter/second² (m/s²)": 1,
        "centimeter/second² (cm/s²)": 1e-2,
        "standard gravity (g)": 9.80665
    },

    "Force": {
        "newton (N)": 1,
        "dyne (dyn)": 1e-5,
        "kilonewton (kN)": 1000
    },

    "Energy": {
        "joule (J)": 1,
        "erg": 1e-7,
        "kilojoule (kJ)": 1000,
        "electronvolt (eV)": 1.602176634e-19
    },

    "Power": {
        "watt (W)": 1,
        "kilowatt (kW)": 1000,
        "erg/second (erg/s)": 1e-7,
        "horsepower (hp)": 745.699872
    },

    "Pressure": {
        "pascal (Pa)": 1,
        "dyne/cm²": 0.1,
        "bar": 1e5,
        "atmosphere (atm)": 101325,
        "torr": 133.322368
    },

    "Frequency": {
        "hertz (Hz)": 1,
        "kilohertz (kHz)": 1e3,
        "megahertz (MHz)": 1e6,
        "gigahertz (GHz)": 1e9
    },

    "Electric Charge": {
        "coulomb (C)": 1,
        "abcoulomb (abC)": 10,
        "statcoulomb (statC)": 3.33564e-10
    },

    "Magnetic Flux": {
        "weber (Wb)": 1,
        "maxwell (Mx)": 1e-8
    },

    "Magnetic Field": {
        "tesla (T)": 1,
        "gauss (G)": 1e-4
    }
}


# =========================================================
# TEMPERATURE
# =========================================================

def to_kelvin(value, unit):

    if unit == "Kelvin (K)":
        return value

    if unit == "Celsius (°C)":
        return value + 273.15

    if unit == "Fahrenheit (°F)":
        return (value - 32) * 5 / 9 + 273.15


def from_kelvin(value, unit):

    if unit == "Kelvin (K)":
        return value

    if unit == "Celsius (°C)":
        return value - 273.15

    if unit == "Fahrenheit (°F)":
        return (value - 273.15) * 9 / 5 + 32


# =========================================================
# CONVERSION
# =========================================================

def convert(value, category, from_unit, to_unit):

    if category == "Temperature":

        kelvin = to_kelvin(value, from_unit)

        return from_kelvin(kelvin, to_unit)

    value_in_si = value * UNITS[category][from_unit]

    result = value_in_si / UNITS[category][to_unit]

    return result


# =========================================================
# NUMBER FORMAT
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
Calculate • Convert • Explore
</p>

<p>
A modern scientific toolkit for Physics students
</p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# TABS
# =========================================================

converter_tab, calculator_tab, constants_tab = st.tabs([
    "🔄 Unit Converter",
    "🧮 Calculator",
    "📐 Constants"
])


# =========================================================
# CONVERTER
# =========================================================

with converter_tab:

    st.markdown("""
    <div class="card">

    <h2>🔄 Universal Unit Converter</h2>

    <p>
    Convert physical quantities between MKS, CGS
    and commonly used scientific units.
    </p>

    </div>
    """, unsafe_allow_html=True)

    categories = list(UNITS.keys()) + ["Temperature"]

    category = st.selectbox(
        "📚 Physical Quantity",
        categories
    )

    if category == "Temperature":

        units = [
            "Kelvin (K)",
            "Celsius (°C)",
            "Fahrenheit (°F)"
        ]

    else:

        units = list(UNITS[category].keys())

    col1, col2 = st.columns(2)

    with col1:

        value = st.number_input(
            "Enter Value",
            value=1.0,
            format="%.10g"
        )

        from_unit = st.selectbox(
            "From Unit",
            units,
            key="from_unit"
        )

    with col2:

        to_unit = st.selectbox(
            "To Unit",
            units,
            key="to_unit"
        )

        st.write("")

        convert_button = st.button(
            "⚡ CONVERT",
            key="convert_button",
            use_container_width=True
        )

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

                <div class="result-title">
                Conversion Result
                </div>

                <div class="result-value">
                {format_number(result)}
                </div>

                <div>
                {to_unit}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        except Exception as error:

            st.error(f"Conversion error: {error}")


# =========================================================
# CALCULATOR
# =========================================================

with calculator_tab:

    st.markdown("""
    <div class="card">

    <h2>🧮 Scientific Calculator</h2>

    <p>
    Perform basic and scientific calculations.
    </p>

    </div>
    """, unsafe_allow_html=True)

    expression = st.text_input(
        "Enter Expression",
        placeholder="Example: 2*(5+3)"
    )

    st.caption(
        "Available: sin, cos, tan, sqrt, log, ln, exp, pi, e"
    )

    calculate_button = st.button(
        "🧮 CALCULATE",
        key="calculate_button",
        use_container_width=True
    )

    if calculate_button:

        try:

            allowed_functions = {
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "sqrt": math.sqrt,
                "log": math.log10,
                "ln": math.log,
                "exp": math.exp,
                "pi": math.pi,
                "e": math.e,
                "abs": abs
            }

            result = eval(
                expression,
                {"__builtins__": {}},
                allowed_functions
            )

            st.markdown(
                f"""
                <div class="result">

                <div class="result-title">
                Answer
                </div>

                <div class="result-value">
                {format_number(result)}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        except Exception:

            st.error(
                "Invalid expression. Example: 2*(5+3)"
            )


# =========================================================
# CONSTANTS
# =========================================================

with constants_tab:

    st.markdown("""
    <div class="card">

    <h2>📐 Fundamental Physical Constants</h2>

    <p>
    Important constants used in Physics.
    </p>

    </div>
    """, unsafe_allow_html=True)

    constants = {
        "Speed of Light (c)": "2.99792458 × 10⁸ m/s",
        "Planck Constant (h)": "6.62607015 × 10⁻³⁴ J·s",
        "Reduced Planck Constant (ℏ)": "1.054571817 × 10⁻³⁴ J·s",
        "Elementary Charge (e)": "1.602176634 × 10⁻¹⁹ C",
        "Electron Mass": "9.1093837 × 10⁻³¹ kg",
        "Proton Mass": "1.6726219 × 10⁻²⁷ kg",
        "Gravitational Constant (G)": "6.67430 × 10⁻¹¹ m³ kg⁻¹ s⁻²",
        "Boltzmann Constant (kB)": "1.380649 × 10⁻²³ J/K",
        "Avogadro Constant (NA)": "6.02214076 × 10²³ mol⁻¹",
        "Vacuum Permittivity (ε₀)": "8.8541878 × 10⁻¹² F/m",
        "Vacuum Permeability (μ₀)": "1.2566371 × 10⁻⁶ H/m"
    }

    for name, value in constants.items():

        st.markdown(
            f"""
            <div class="card">

            <b>{name}</b>

            <br><br>

            {value}

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div style="
text-align:center;
color:#64748b;
margin-top:40px;
padding:20px;
">

⚛️ Physics Toolkit
<br>
Built with Python + Streamlit

</div>
""", unsafe_allow_html=True)
