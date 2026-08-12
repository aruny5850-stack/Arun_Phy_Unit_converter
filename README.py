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

/* ========================================================
   GLOBAL
======================================================== */

.stApp {
    background:
        radial-gradient(
            circle at 8% 8%,
            rgba(14, 165, 233, 0.13),
            transparent 30%
        ),
        radial-gradient(
            circle at 92% 12%,
            rgba(124, 58, 237, 0.13),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #020617 0%,
            #0b1224 50%,
            #111827 100%
        );

    color: #f8fafc;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* ========================================================
   HERO
======================================================== */

.hero {
    position: relative;
    overflow: hidden;

    padding: 42px;
    margin-bottom: 30px;

    border-radius: 28px;

    background:
        linear-gradient(
            135deg,
            rgba(14, 165, 233, 0.18),
            rgba(37, 99, 235, 0.16),
            rgba(124, 58, 237, 0.18)
        );

    border: 1px solid rgba(255,255,255,0.12);

    box-shadow:
        0 20px 60px rgba(0,0,0,0.35),
        inset 0 1px 0 rgba(255,255,255,0.05);

    backdrop-filter: blur(18px);
}

.hero h1 {
    margin: 0;

    font-size: 48px;
    font-weight: 800;

    background:
        linear-gradient(
            90deg,
            #ffffff,
            #7dd3fc,
            #a78bfa
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    margin-top: 10px;

    color: #b8c4d6;

    font-size: 17px;
}


/* ========================================================
   MAIN CARD
======================================================== */

.main-card {
    padding: 28px;

    margin-bottom: 22px;

    border-radius: 24px;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.065),
            rgba(255,255,255,0.025)
        );

    border: 1px solid rgba(255,255,255,0.10);

    box-shadow:
        0 15px 40px rgba(0,0,0,0.25);

    backdrop-filter: blur(18px);
}

.main-card h2 {
    margin-top: 0;

    color: #ffffff;

    font-size: 25px;
}

.main-card p {
    color: #9caec4;
}


/* ========================================================
   FIELD BOX
======================================================== */

.field-box {
    padding: 18px;

    margin-bottom: 18px;

    border-radius: 18px;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.065),
            rgba(255,255,255,0.025)
        );

    border: 1px solid rgba(255,255,255,0.09);

    box-shadow:
        0 8px 25px rgba(0,0,0,0.16);

    transition: all 0.25s ease;
}

.field-box:hover {
    border-color: rgba(56,189,248,0.35);

    box-shadow:
        0 10px 30px rgba(14,165,233,0.10);
}

.field-title {
    color: #cbd5e1;

    font-size: 13px;

    font-weight: 700;

    margin-bottom: 8px;

    letter-spacing: 0.4px;
}


/* ========================================================
   STREAMLIT INPUTS
======================================================== */

div[data-baseweb="input"] {
    background: rgba(255,255,255,0.055) !important;

    border: 1px solid rgba(255,255,255,0.10) !important;

    border-radius: 13px !important;

    min-height: 46px;

    transition: 0.25s ease;
}

div[data-baseweb="input"]:focus-within {
    border-color: #38bdf8 !important;

    box-shadow:
        0 0 0 2px rgba(56,189,248,0.10);
}

input {
    color: #ffffff !important;
}


/* ========================================================
   SELECT BOX
======================================================== */

div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.055) !important;

    border: 1px solid rgba(255,255,255,0.10) !important;

    border-radius: 13px !important;

    min-height: 46px;

    transition: 0.25s ease;
}

div[data-baseweb="select"] > div:hover {
    border-color: #38bdf8 !important;
}

div[data-baseweb="select"] span {
    color: #f8fafc !important;
}


/* ========================================================
   LABEL
======================================================== */

label {
    color: #cbd5e1 !important;

    font-weight: 600 !important;
}


/* ========================================================
   CONVERT BUTTON
======================================================== */

.stButton > button {
    width: 100%;

    min-height: 52px;

    border: none !important;

    border-radius: 15px !important;

    color: white !important;

    font-size: 16px !important;

    font-weight: 700 !important;

    letter-spacing: 0.5px;

    background:
        linear-gradient(
            135deg,
            #06b6d4,
            #2563eb,
            #7c3aed
        ) !important;

    box-shadow:
        0 10px 30px rgba(37,99,235,0.28);

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);

    box-shadow:
        0 15px 38px rgba(37,99,235,0.42);
}

.stButton > button:active {
    transform: scale(0.98);
}


/* ========================================================
   RESULT
======================================================== */

.result-box {
    position: relative;

    overflow: hidden;

    padding: 35px;

    margin-top: 28px;

    border-radius: 25px;

    text-align: center;

    background:
        linear-gradient(
            135deg,
            rgba(6,182,212,0.16),
            rgba(37,99,235,0.18),
            rgba(124,58,237,0.20)
        );

    border: 1px solid rgba(96,165,250,0.28);

    box-shadow:
        0 15px 45px rgba(0,0,0,0.30),
        inset 0 1px 0 rgba(255,255,255,0.06);
}

.result-label {
    color: #93c5fd;

    font-size: 13px;

    font-weight: 700;

    letter-spacing: 2px;

    text-transform: uppercase;
}

.result-number {
    color: #ffffff;

    font-size: 42px;

    font-weight: 800;

    margin: 10px 0;

    text-shadow:
        0 0 25px rgba(96,165,250,0.35);
}

.result-unit {
    color: #cbd5e1;

    font-size: 16px;
}


/* ========================================================
   INFO BOX
======================================================== */

.info-box {
    padding: 18px;

    margin-top: 18px;

    border-radius: 16px;

    background: rgba(59,130,246,0.07);

    border: 1px solid rgba(59,130,246,0.15);

    color: #a9b9cc;

    font-size: 14px;
}


/* ========================================================
   CONSTANT CARD
======================================================== */

.constant-card {
    padding: 20px;

    margin-bottom: 14px;

    border-radius: 18px;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.055),
            rgba(255,255,255,0.02)
        );

    border: 1px solid rgba(255,255,255,0.08);

    transition: 0.25s ease;
}

.constant-card:hover {
    transform: translateY(-2px);

    border-color: rgba(96,165,250,0.25);
}

.constant-name {
    color: #e2e8f0;

    font-weight: 700;

    font-size: 16px;
}

.constant-value {
    color: #93c5fd;

    margin-top: 8px;

    font-size: 15px;
}


/* ========================================================
   TABS
======================================================== */

button[data-baseweb="tab"] {
    color: #94a3b8 !important;

    font-size: 16px !important;

    font-weight: 700 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #38bdf8 !important;
}


/* ========================================================
   SIDEBAR
======================================================== */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #050816,
            #0b1224
        );

    border-right: 1px solid rgba(255,255,255,0.08);
}


/* ========================================================
   MOBILE
======================================================== */

@media (max-width: 768px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .hero {
        padding: 28px;
    }

    .hero h1 {
        font-size: 34px;
    }

    .main-card {
        padding: 20px;
    }

    .result-number {
        font-size: 30px;
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

    return value


def from_kelvin(value, unit):

    if unit == "Kelvin (K)":
        return value

    if unit == "Celsius (°C)":
        return value - 273.15

    if unit == "Fahrenheit (°F)":
        return (value - 273.15) * 9 / 5 + 32

    return value


# =========================================================
# CONVERSION FUNCTION
# =========================================================

def convert(value, category, from_unit, to_unit):

    if category == "Temperature":

        kelvin = to_kelvin(value, from_unit)

        return from_kelvin(kelvin, to_unit)

    value_in_si = value * UNITS[category][from_unit]

    return value_in_si / UNITS[category][to_unit]


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
# HERO
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
# UNIT CONVERTER
# =========================================================

with converter_tab:

    st.markdown("""
    <div class="main-card">

        <h2>🔄 Universal Unit Converter</h2>

        <p>
        Convert physical quantities between MKS, CGS
        and commonly used scientific units.
        </p>

    </div>
    """, unsafe_allow_html=True)


    # -----------------------------------------------------
    # PHYSICAL QUANTITY
    # -----------------------------------------------------

    st.markdown("""
    <div class="field-box">

        <div class="field-title">
        📚 PHYSICAL QUANTITY
        </div>

    </div>
    """, unsafe_allow_html=True)

    categories = list(UNITS.keys()) + ["Temperature"]

    category = st.selectbox(
        "Select Physical Quantity",
        categories,
        label_visibility="collapsed"
    )


    # -----------------------------------------------------
    # UNITS
    # -----------------------------------------------------

    if category == "Temperature":

        units = [
            "Kelvin (K)",
            "Celsius (°C)",
            "Fahrenheit (°F)"
        ]

    else:

        units = list(UNITS[category].keys())


    col1, col2 = st.columns(2)


    # -----------------------------------------------------
    # VALUE
    # -----------------------------------------------------

    with col1:

        st.markdown("""
        <div class="field-box">

            <div class="field-title">
            🔢 ENTER VALUE
            </div>

        </div>
        """, unsafe_allow_html=True)

        value = st.number_input(
            "Value",
            value=1.0,
            format="%.10g",
            label_visibility="collapsed"
        )


    # -----------------------------------------------------
    # FROM UNIT
    # -----------------------------------------------------

    with col2:

        st.markdown("""
        <div class="field-box">

            <div class="field-title">
            📤 FROM UNIT
            </div>

        </div>
        """, unsafe_allow_html=True)

        from_unit = st.selectbox(
            "From Unit",
            units,
            key="from_unit",
            label_visibility="collapsed"
        )


    # -----------------------------------------------------
    # TO UNIT
    # -----------------------------------------------------

    st.markdown("""
    <div class="field-box">

        <div class="field-title">
        📥 TO UNIT
        </div>

    </div>
    """, unsafe_allow_html=True)

    to_unit = st.selectbox(
        "To Unit",
        units,
        key="to_unit",
        label_visibility="collapsed"
    )


    # -----------------------------------------------------
    # CONVERT
    # -----------------------------------------------------

    st.write("")

    convert_button = st.button(
        "⚡  CONVERT",
        key="convert_button",
        use_container_width=True
    )


    # -----------------------------------------------------
    # RESULT
    # -----------------------------------------------------

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
                <div class="result-box">

                    <div class="result-label">
                    ✨ Conversion Result
                    </div>

                    <div class="result-number">
                    {format_number(result)}
                    </div>

                    <div class="result-unit">
                    {to_unit}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="info-box">

                <b>Conversion:</b>
                {format_number(value)} {from_unit}
                →
                {format_number(result)} {to_unit}

                </div>
                """,
                unsafe_allow_html=True
            )

        except Exception as error:

            st.error(
                f"Conversion error: {error}"
            )


# =========================================================
# SCIENTIFIC CALCULATOR
# =========================================================

with calculator_tab:

    st.markdown("""
    <div class="main-card">

        <h2>🧮 Scientific Calculator</h2>

        <p>
        Perform mathematical and scientific calculations.
        </p>

    </div>
    """, unsafe_allow_html=True)


    st.markdown("""
    <div class="field-box">

        <div class="field-title">
        🔢 MATHEMATICAL EXPRESSION
        </div>

    </div>
    """, unsafe_allow_html=True)


    expression = st.text_input(
        "Expression",
        placeholder="Example: 2*(5+3)",
        label_visibility="collapsed"
    )


    st.markdown("""
    <div class="info-box">

    <b>Available functions:</b>

    sin • cos • tan • sqrt • log • ln • exp • pi • e

    <br><br>

    Examples:

    <br>
    <b>sqrt(25)</b>

    <br>
    <b>sin(pi/2)</b>

    <br>
    <b>2*(5+3)</b>

    </div>
    """, unsafe_allow_html=True)


    st.write("")


    calculate_button = st.button(
        "🧮  CALCULATE",
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
                <div class="result-box">

                    <div class="result-label">
                    ✨ Answer
                    </div>

                    <div class="result-number">
                    {format_number(result)}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        except Exception:

            st.error(
                "Invalid expression. Please check your input."
            )


# =========================================================
# PHYSICAL CONSTANTS
# =========================================================

with constants_tab:

    st.markdown("""
    <div class="main-card">

        <h2>📐 Fundamental Physical Constants</h2>

        <p>
        Important constants frequently used in Physics.
        </p>

    </div>
    """, unsafe_allow_html=True)


    constants = {

        "Speed of Light (c)":
            "2.99792458 × 10⁸ m/s",

        "Planck Constant (h)":
            "6.62607015 × 10⁻³⁴ J·s",

        "Reduced Planck Constant (ℏ)":
            "1.054571817 × 10⁻³⁴ J·s",

        "Elementary Charge (e)":
            "1.602176634 × 10⁻¹⁹ C",

        "Electron Mass":
            "9.1093837 × 10⁻³¹ kg",

        "Proton Mass":
            "1.6726219 × 10⁻²⁷ kg",

        "Gravitational Constant (G)":
            "6.67430 × 10⁻¹¹ m³ kg⁻¹ s⁻²",

        "Boltzmann Constant (kB)":
            "1.380649 × 10⁻²³ J/K",

        "Avogadro Constant (NA)":
            "6.02214076 × 10²³ mol⁻¹",

        "Vacuum Permittivity (ε₀)":
            "8.8541878 × 10⁻¹² F/m",

        "Vacuum Permeability (μ₀)":
            "1.2566371 × 10⁻⁶ H/m"
    }


    for name, value in constants.items():

        st.markdown(
            f"""
            <div class="constant-card">

                <div class="constant-name">
                {name}
                </div>

                <div class="constant-value">
                {value}
                </div>

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
    margin-top:45px;
    padding:20px;
    font-size:13px;
">

⚛️ <b>Physics Toolkit</b>

<br>

Built with Python + Streamlit

</div>
""", unsafe_allow_html=True)
