import streamlit as st
import math
import ast
import operator as op

# ============================================================
# PAGE
# ============================================================
st.set_page_config(
    page_title="Ar_PHYHBTU",
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
        radial-gradient(circle at 5% 5%, rgba(14,165,233,.12), transparent 25%),
        radial-gradient(circle at 95% 5%, rgba(124,58,237,.12), transparent 25%),
        linear-gradient(135deg,#020617,#0b1224 55%,#111827);
    color:#f8fafc;
}
.section-heading h2 {
    font-size: 24px !important;
}
.block-container {max-width:1150px;padding-top:1.6rem;padding-bottom:3rem;}
.hero,.field-card,.result-card,.constant-card {
    border:1px solid rgba(255,255,255,.10);
    background:linear-gradient(145deg,rgba(255,255,255,.065),rgba(255,255,255,.025));
    box-shadow:0 12px 35px rgba(0,0,0,.22);
    backdrop-filter:blur(16px);
}
.hero {padding:22px 26px;border-radius:18px;margin-bottom:16px;}
.hero h1 {margin:0;font-size:38px;font-weight:800;background:linear-gradient(90deg,#fff,#7dd3fc,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.hero p {color:#aebbd0;margin:.25rem 0;font-size:14px;}
.section-heading {margin:4px 0 18px;padding:0 2px;}
.field-card {padding:12px;border-radius:14px;margin-bottom:10px;}
.field-title {font-size:12px;font-weight:800;letter-spacing:.8px;color:#93c5fd;margin-bottom:8px;}
.result-card {padding:22px;border-radius:18px;text-align:center;margin-top:22px;background:linear-gradient(135deg,rgba(6,182,212,.13),rgba(37,99,235,.16),rgba(124,58,237,.16));}
.result-label {font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#93c5fd;font-weight:800;}
.result-number {font-size:38px;font-weight:850;margin:9px 0;color:#fff;}
.result-unit {font-size:16px;color:#cbd5e1;}
.constant-card {padding:12px 15px;border-radius:13px;margin-bottom:8px;}
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

.stTabs [data-baseweb="tab-list"] {gap:6px;}
.stTabs [data-baseweb="tab"] {padding:8px 14px;}
@media(max-width:700px){
    .hero h1{font-size:32px}.hero{padding:22px}.result-number{font-size:29px}
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# UNIT DATABASE
# Factor converts unit -> SI base unit.
# ============================================================
UNITS = {
    "Magnetic induction (B) ": {
        "tesla (T) [SI]": 1,
        "gauss (G) [CGS]": 1e-4
    },
    "Magnetic field (H)": {
        "ampere/meter (A m⁻¹)  [SI]": 1,
        "oersted (Oe) [CGS]": 1000/(4*math.pi)
    },
    "Magnetization (M)": {
        "ampere/meter (A m⁻¹)": 1,
        "emu cm⁻³": 1000
    },
    "Magnetic polarization (J)": {
        "tesla (T) [SI]": 1,
        "gauss (G) [CGS]": 1e-4
    },
    "Magnetic moment (m)": {
        "ampere·meter² (A m²)": 1,
        "emu (G cm³)": 1e-3
    },
    "Magnetic moment per unit mass (σ)": {
        "ampere·meter² kg⁻¹ (A m² kg⁻¹)": 1,
        "emu g⁻¹ [CGS]": 1
    },
    "Volume magnetic susceptibility (κ = M/H)": {
        "dimensionless [SI]": 1,
        "dimensionless [CGS]": 1/(4*math.pi)
    },
    "Mass magnetic susceptibility (χ = κ/ρ)": {
        "m³ kg⁻¹": 1,
        "emu Oe⁻¹ g⁻¹": 4*math.pi/1000
    },
    "Molar magnetic susceptibility (χₘ = χM*)": {
        "m³ mol⁻¹": 1,
        "emu Oe⁻¹ g⁻¹ mol⁻¹": 4*math.pi/1e6
    },
    "Magnetic permeability (μ = B/H)": {
        "henry/meter (H m⁻¹)": 1,
        "G Oe⁻¹": 1e7/(4*math.pi)
    },
    "Magnetic flux (λ)": {
        "weber (Wb)": 1,
        "maxwell (Mx)": 1e-8
    },
    "Magnetic scalar potential; Magnetomotive force (ϕ)": {
        "ampere (A) [SI]": 1,
        "gilbert [CGS]": 10/(4*math.pi)
    },
    "Magnetic vector potential": {
        "weber/meter (Wb m⁻¹)": 1,
        "emu (G cm)": 1e-6
    },
    "Magnetic pole strength (p)": {
        "ampere·meter (A m)": 1,
        "emu (G cm²)": 1e-1
    },
    "Demagnetizing factor": {
        "dimensionless (SI)": 1,
        "dimensionless (CGS)": 4*math.pi
    },
    "Magnetostriction constant (λ)": {
        "dimensionless (SI)": 1,
        "dimensionless (CGS)": 1
    },
    "Anisotropy constant (K, K₁, Kᵤ)": {
        "joule/m³ (J m⁻³)": 1,
        "erg/cm³": 1e-1
    },
    "Magnetostatic energy (Eₘ)": {
        "joule/m³ (J m⁻³)": 1,
        "erg/cm³": 1e-1
    },
    "Energy product (BH)ₘₐₓ": {
        "joule/m³ (J m⁻³)": 1,
        "erg/cm³": 1e-1
    },
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
    if x == 0: return "0"
    if abs(x) >= 1e6 or abs(x) < 1e-4:
        return f"{x:.6e}"
    return f"{x:.10g}"

# ============================================================
# SAFE SCIENTIFIC CALCULATOR
# ============================================================
BIN_OPS = {
    ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
    ast.Div: op.truediv, ast.Pow: op.pow, ast.Mod: op.mod,
}
UNARY_OPS = {ast.UAdd: op.pos, ast.USub: op.neg}
FUNCS = {
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "sqrt": math.sqrt, "log": math.log10, "ln": math.log,
    "exp": math.exp, "abs": abs, "asin": math.asin,
    "acos": math.acos, "atan": math.atan
}
NAMES = {"pi": math.pi, "e": math.e}

def safe_eval(expr):
    tree = ast.parse(expr, mode="eval")

    def walk(node):
        if isinstance(node, ast.Expression):
            return walk(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.Num):
            return node.n
        if isinstance(node, ast.BinOp) and type(node.op) in BIN_OPS:
            return BIN_OPS[type(node.op)](walk(node.left), walk(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in UNARY_OPS:
            return UNARY_OPS[type(node.op)](walk(node.operand))
        if isinstance(node, ast.Name) and node.id in NAMES:
            return NAMES[node.id]
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in FUNCS:
            if len(node.args) != 1:
                raise ValueError("Use one argument in a function.")
            return FUNCS[node.func.id](walk(node.args[0]))
        raise ValueError("Unsupported expression.")

    return walk(tree)

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="hero">
    <h1>🧑🏻‍🎓  Ar_PHYHBTU</h1>
    <p>Calculate • Convert • Explore</p>
    <p>Physics utility app for students — SI, CGS, magnetic quantities and scientific calculations.</p>
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
    <div class="section-heading">
        <h2>🔄 Universal Unit Converter</h2>
        <p>SI/MKS • CGS • Practical Units</p>
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
# CALCULATOR
# ============================================================
with calculator:
    st.markdown("""
    <div class="section-heading">
        <h2>🧮 Scientific Calculator</h3>
        <p>Arithmetic • Powers • Scientific Functions</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="field-card"><div class="field-title">🔢 EXPRESSION</div>', unsafe_allow_html=True)
    expression = st.text_input(
        "Expression",
        placeholder="Example: 2*(5+3), sqrt(25), sin(pi/2)",
        label_visibility="collapsed"
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.info("Functions: sin, cos, tan, asin, acos, atan, sqrt, log, ln, exp, abs • Constants: pi, e")

    if st.button("🧮  CALCULATE", key="calculate", use_container_width=True):
        try:
            if not expression.strip():
                raise ValueError("Enter an expression.")
            answer = safe_eval(expression)
            st.markdown(f"""
            <div class="result-card">
                <div class="result-label">✨ Answer</div>
                <div class="result-number">{fmt(answer)}</div>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Invalid expression: {e}")

# ============================================================
# CONSTANTS
# ============================================================
with constants:
    st.markdown("""
    <div class="section-heading">
        <h2>📐 Fundamental Constants</h2>
        <p>Frequently used Physics constants</p>
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
⚛️ <b>Ar_PHYHBTU</b><br>
Developed by Arun Kumar Yadav
H.B.T.U. Kanpur
</div>
""", unsafe_allow_html=True)
