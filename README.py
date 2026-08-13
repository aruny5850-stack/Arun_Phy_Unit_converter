import streamlit as st
import math
import ast
import operator as op

# ============================================================
# PAGE
# ============================================================
st.set_page_config(
    page_title="Arun Toolkit",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# STYLE
# ============================================================
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 5% 5%, rgba(14,165,233,.12), transparent 28%),
        radial-gradient(circle at 95% 5%, rgba(124,58,237,.12), transparent 28%),
        linear-gradient(135deg,#020617,#0b1224 55%,#111827);
    color:#f8fafc;
}
.block-container {max-width:1150px;padding-top:1.6rem;padding-bottom:3rem;}
.hero,.panel,.field-card,.result-card,.constant-card {
    border:1px solid rgba(255,255,255,.10);
    background:linear-gradient(145deg,rgba(255,255,255,.065),rgba(255,255,255,.025));
    box-shadow:0 12px 35px rgba(0,0,0,.22);
    backdrop-filter:blur(16px);
}
.hero {padding:34px;border-radius:26px;margin-bottom:22px;}
.hero h1 {margin:0;font-size:46px;font-weight:800;background:linear-gradient(90deg,#fff,#7dd3fc,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.hero p {color:#aebbd0;margin:.4rem 0;font-size:16px;}
.panel {padding:25px;border-radius:22px;margin-bottom:18px;}
.field-card {padding:16px;border-radius:18px;margin-bottom:14px;}
.field-title {font-size:12px;font-weight:800;letter-spacing:.8px;color:#93c5fd;margin-bottom:8px;}
.result-card {padding:30px;border-radius:24px;text-align:center;margin-top:22px;background:linear-gradient(135deg,rgba(6,182,212,.13),rgba(37,99,235,.16),rgba(124,58,237,.16));}
.result-label {font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#93c5fd;font-weight:800;}
.result-number {font-size:38px;font-weight:850;margin:9px 0;color:#fff;}
.result-unit {font-size:16px;color:#cbd5e1;}
.constant-card {padding:18px;border-radius:17px;margin-bottom:12px;}
.constant-name {font-weight:750;color:#e2e8f0;}
.constant-value {color:#7dd3fc;margin-top:6px;}
.stButton > button {
    width:100%;height:50px;border:0!important;border-radius:14px!important;
    color:#fff!important;font-weight:800!important;
    background:linear-gradient(135deg,#06b6d4,#2563eb,#7c3aed)!important;
    box-shadow:0 9px 26px rgba(37,99,235,.28);
}
.stButton > button:hover {transform:translateY(-2px);}
div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
    background:rgba(255,255,255,.045)!important;
    border-radius:12px!important;
    border-color:rgba(255,255,255,.10)!important;
}
input {color:#fff!important;}
button[data-baseweb="tab"] {font-weight:750!important;}
@media(max-width:700px){
    .hero h1{font-size:32px}.hero{padding:25px}.panel{padding:18px}.result-number{font-size:29px}
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# UNIT DATABASE
# Factor converts unit -> SI base unit.
# ============================================================
UNITS = {
    "Length": {
        "meter (m)": 1, "kilometer (km)": 1e3, "centimeter (cm)": 1e-2,
        "millimeter (mm)": 1e-3, "micrometer (μm)": 1e-6,
        "nanometer (nm)": 1e-9, "angstrom (Å)": 1e-10,
        "inch (in)": 0.0254, "foot (ft)": 0.3048, "mile (mi)": 1609.344
    },
    "Mass": {
        "kilogram (kg)": 1, "gram (g)": 1e-3, "milligram (mg)": 1e-6,
        "microgram (μg)": 1e-9, "tonne (t)": 1e3
    },
    "Time": {
        "second (s)": 1, "millisecond (ms)": 1e-3, "microsecond (μs)": 1e-6,
        "nanosecond (ns)": 1e-9, "minute (min)": 60, "hour (h)": 3600,
        "day": 86400
    },
    "Area": {
        "square meter (m²)": 1, "square kilometer (km²)": 1e6,
        "square centimeter (cm²)": 1e-4, "square millimeter (mm²)": 1e-6,
        "square inch (in²)": 0.00064516, "square foot (ft²)": 0.09290304
    },
    "Volume": {
        "cubic meter (m³)": 1, "liter (L)": 1e-3, "milliliter (mL)": 1e-6,
        "cubic centimeter (cm³)": 1e-6, "cubic millimeter (mm³)": 1e-9
    },
    "Velocity": {
        "meter/second (m/s)": 1, "centimeter/second (cm/s)": 1e-2,
        "kilometer/hour (km/h)": 1000/3600, "mile/hour (mph)": 1609.344/3600
    },
    "Acceleration": {
        "meter/second² (m/s²)": 1, "centimeter/second² (cm/s²)": 1e-2,
        "standard gravity (g)": 9.80665
    },
    "Force": {
        "newton (N)": 1, "dyne (dyn)": 1e-5, "kilonewton (kN)": 1e3
    },
    "Energy": {
        "joule (J)": 1, "erg": 1e-7, "kilojoule (kJ)": 1e3,
        "electronvolt (eV)": 1.602176634e-19
    },
    "Power": {
        "watt (W)": 1, "kilowatt (kW)": 1e3,
        "erg/second (erg/s)": 1e-7, "horsepower (hp)": 745.699872
    },
    "Pressure": {
        "pascal (Pa)": 1, "kilopascal (kPa)": 1e3, "bar": 1e5,
        "atmosphere (atm)": 101325, "torr": 133.322368, "dyne/cm²": 0.1
    },
    "Frequency": {
        "hertz (Hz)": 1, "kilohertz (kHz)": 1e3,
        "megahertz (MHz)": 1e6, "gigahertz (GHz)": 1e9
    },
    "Electric Charge": {
        "coulomb (C)": 1, "millicoulomb (mC)": 1e-3,
        "microcoulomb (μC)": 1e-6, "nanocoulomb (nC)": 1e-9
    },
    "Electric Potential": {
        "volt (V)": 1, "millivolt (mV)": 1e-3, "kilovolt (kV)": 1e3
    },
    "Electric Current": {
        "ampere (A)": 1, "milliampere (mA)": 1e-3, "microampere (μA)": 1e-6
    },
    "Resistance": {
        "ohm (Ω)": 1, "milliohm (mΩ)": 1e-3, "kilohm (kΩ)": 1e3,
        "megohm (MΩ)": 1e6
    },
    "Capacitance": {
        "farad (F)": 1, "microfarad (μF)": 1e-6,
        "nanofarad (nF)": 1e-9, "picofarad (pF)": 1e-12
    },
    "Magnetic Field": {
        "tesla (T)": 1, "gauss (G)": 1e-4
    },
    "Magnetic Flux": {
        "weber (Wb)": 1, "maxwell (Mx)": 1e-8
    },
    "Density": {
        "kilogram/m³ (kg/m³)": 1,
        "gram/cm³ (g/cm³)": 1000,
        "gram/mL (g/mL)": 1000
    },
    "Dynamic Viscosity": {
        "pascal-second (Pa·s)": 1,
        "poise (P)": 0.1,
        "centipoise (cP)": 0.001
    },
    "Molar Amount": {
        "mole (mol)": 1,
        "millimole (mmol)": 1e-3,
        "micromole (μmol)": 1e-6,
        "nanomole (nmol)": 1e-9
    },
}

# ============================================================
# CONVERSIONS
# ============================================================
def temp_to_k(x, unit):
    if unit == "Kelvin (K)": return x
    if unit == "Celsius (°C)": return x + 273.15
    return (x - 32) * 5/9 + 273.15

def k_to_temp(x, unit):
    if unit == "Kelvin (K)": return x
    if unit == "Celsius (°C)": return x - 273.15
    return (x - 273.15) * 9/5 + 32

def convert_value(x, category, u1, u2):
    if category == "Temperature":
        return k_to_temp(temp_to_k(x, u1), u2)
    return x * UNITS[category][u1] / UNITS[category][u2]

def fmt(x):
    if x == 0:
        return "0"

    if abs(x) >= 1e6 or abs(x) < 1e-4:
        s = f"{x:.3e}"
        mantissa, exponent = s.split("e")
        exponent = int(exponent)

        superscript = str(exponent).translate(
            str.maketrans(
                "0123456789-+",
                "⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺"
            )
        )

        return f"{mantissa} × 10{superscript}"

    return f"{x:.3f}"

import math
import ast
import operator

# ============================================================
# SAFE SCIENTIFIC CALCULATOR
# ============================================================

ALLOWED_FUNCTIONS = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "sqrt": math.sqrt,
    "log": math.log10,     # log(100) = 2
    "ln": math.log,        # ln(e) = 1
    "exp": math.exp,
    "abs": abs,
}

ALLOWED_CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
}

ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def safe_eval(expression):
    expression = expression.strip()

    # Allow × and ÷ symbols
    expression = expression.replace("×", "*")
    expression = expression.replace("÷", "/")
    expression = expression.replace("^", "**")

    tree = ast.parse(expression, mode="eval")

    def evaluate(node):

        # Numbers
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Invalid value")

        # Binary operations
        if isinstance(node, ast.BinOp):
            op = ALLOWED_OPERATORS.get(type(node.op))

            if op is None:
                raise ValueError("Operator not allowed")

            left = evaluate(node.left)
            right = evaluate(node.right)

            return op(left, right)

        # Unary + / -
        if isinstance(node, ast.UnaryOp):
            op = ALLOWED_OPERATORS.get(type(node.op))

            if op is None:
                raise ValueError("Operator not allowed")

            return op(evaluate(node.operand))

        # Variables / constants
        if isinstance(node, ast.Name):

            if node.id in ALLOWED_CONSTANTS:
                return ALLOWED_CONSTANTS[node.id]

            if node.id in ALLOWED_FUNCTIONS:
                return ALLOWED_FUNCTIONS[node.id]

            raise ValueError(f"Unknown function or constant: {node.id}")

        # Function calls
        if isinstance(node, ast.Call):

            if not isinstance(node.func, ast.Name):
                raise ValueError("Invalid function")

            function_name = node.func.id

            if function_name not in ALLOWED_FUNCTIONS:
                raise ValueError(
                    f"Function '{function_name}' is not allowed"
                )

            if len(node.args) != 1:
                raise ValueError(
                    f"{function_name}() requires one argument"
                )

            argument = evaluate(node.args[0])

            return ALLOWED_FUNCTIONS[function_name](argument)

        raise ValueError("Invalid expression")

    return evaluate(tree.body)

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="hero">
    <h1>⚛️ Physics Toolkit</h1>
    <p>Calculate • Convert • Explore</p>
    <p>Physics utility app for students — SI, CGS and scientific calculations.</p>
</div>
""", unsafe_allow_html=True)

converter, calculator, constants = st.tabs([
    "🔄 Unit Converter", "🧮 Calculator", "📐 Constants"
])

# ============================================================
# CONVERTER
# ============================================================
with converter:
    st.markdown("""
    <div class="panel">
        <h2>🔄 Universal Unit Converter</h2>
        <p>Convert common physical quantities between SI/MKS, CGS and practical units.</p>
    </div>
    """, unsafe_allow_html=True)

    categories = list(UNITS.keys()) + ["Temperature"]

    st.markdown('<div class="field-card"><div class="field-title">📚 PHYSICAL QUANTITY</div>', unsafe_allow_html=True)
    category = st.selectbox("Physical quantity", categories, label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

    units = ["Kelvin (K)", "Celsius (°C)", "Fahrenheit (°F)"] if category == "Temperature" else list(UNITS[category].keys())

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="field-card"><div class="field-title">🔢 VALUE</div>', unsafe_allow_html=True)
        value = st.number_input("Value", value=1.0, format="%.10g", label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="field-card"><div class="field-title">📤 FROM UNIT</div>', unsafe_allow_html=True)
        from_unit = st.selectbox("From", units, label_visibility="collapsed", key="from_unit")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="field-card"><div class="field-title">📥 TO UNIT</div>', unsafe_allow_html=True)
    to_unit = st.selectbox("To", units, label_visibility="collapsed", key="to_unit")
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("⚡  CONVERT", key="convert", use_container_width=True):
        try:
            result = convert_value(value, category, from_unit, to_unit)
            st.markdown(f"""
            <div class="result-card">
                <div class="result-label">✨ Conversion Result</div>
                <div class="result-number">{fmt(result)}</div>
                <div class="result-unit">{to_unit}</div>
            </div>
            """, unsafe_allow_html=True)
            st.caption(f"{fmt(value)} {from_unit}  →  {fmt(result)} {to_unit}")
        except Exception as e:
            st.error(f"Conversion error: {e}")


# ============================================================
# SCIENTIFIC CALCULATOR
# ============================================================

with calculator:

    st.markdown("""
    <div class="panel">
        <h2>🧮 Scientific Calculator</h2>
        <p>Use +, −, ×, ÷, powers and common scientific functions.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="field-card">'
        '<div class="field-title">🔢 EXPRESSION</div>',
        unsafe_allow_html=True
    )

    expression = st.text_input(
        "Expression",
        placeholder="Example: 2*(5+3), sqrt(25), sin(pi/2)",
        label_visibility="collapsed"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.info(
        "Functions: sin, cos, tan, asin, acos, atan, "
        "sqrt, log, ln, exp, abs • Constants: pi, e"
    )

    if st.button(
        "🧮  CALCULATE",
        key="calculate",
        use_container_width=True
    ):

        try:

            if not expression.strip():
                raise ValueError("Enter an expression.")

            answer = safe_eval(expression)

            st.markdown(
                f"""
                <div class="result-card">
                    <div class="result-label">✨ Answer</div>
                    <div class="result-number">{fmt(answer)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        except ZeroDivisionError:
            st.error("❌ Cannot divide by zero.")

        except ValueError as e:
            st.error(f"❌ Invalid expression: {e}")

        except Exception as e:
            st.error(f"❌ Calculation error: {e}")
# ============================================================
# CONSTANTS
# ============================================================
with constants:
    st.markdown("""
    <div class="panel">
        <h2>📐 Fundamental Physical Constants</h2>
        <p>Frequently used constants for Physics calculations.</p>
    </div>
    """, unsafe_allow_html=True)

    constant_data = [
        ("Speed of Light (c)", "2.99792458 × 10⁸ m/s"),
        ("Planck Constant (h)", "6.62607015 × 10⁻³⁴ J·s"),
        ("Reduced Planck Constant (ℏ)", "1.054571817 × 10⁻³⁴ J·s"),
        ("Elementary Charge (e)", "1.602176634 × 10⁻¹⁹ C"),
        ("Electron Mass", "9.1093837 × 10⁻³¹ kg"),
        ("Proton Mass", "1.6726219 × 10⁻²⁷ kg"),
        ("Gravitational Constant (G)", "6.67430 × 10⁻¹¹ m³ kg⁻¹ s⁻²"),
        ("Boltzmann Constant (kB)", "1.380649 × 10⁻²³ J/K"),
        ("Avogadro Constant (NA)", "6.02214076 × 10²³ mol⁻¹"),
        ("Vacuum Permittivity (ε₀)", "8.8541878128 × 10⁻¹² F/m"),
        ("Vacuum Permeability (μ₀)", "1.25663706212 × 10⁻⁶ H/m"),
    ]

    for name, value in constant_data:
        st.markdown(f"""
        <div class="constant-card">
            <div class="constant-name">{name}</div>
            <div class="constant-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;color:#64748b;margin-top:40px;padding:20px;font-size:13px">
⚛️ <b>Physics Toolkit</b><br>
Python + Streamlit
</div>
""", unsafe_allow_html=True)
