import streamlit as st
import streamlit.components.v1 as components
import math
import ast
import operator as op
import pandas as pd

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
        radial-gradient(circle at 5% 5%, rgba(14,165,233,.12), transparent 28%),
        radial-gradient(circle at 95% 5%, rgba(124,58,237,.12), transparent 28%),
        linear-gradient(135deg,#020617,#0b1224 55%,#111827);
    color:#f8fafc;
}
.block-container {
    max-width:1150px;
    padding-top:1.6rem;
    padding-bottom:3rem;
}
.hero,.panel,.field-card,.result-card,.constant-card {
    border:1px solid rgba(255,255,255,.10);
    background:linear-gradient(145deg,rgba(255,255,255,.065),rgba(255,255,255,.025));
    box-shadow:0 12px 35px rgba(0,0,0,.22);
    backdrop-filter:blur(16px);
}
.hero {
    padding:34px;
    border-radius:26px;
    margin-bottom:22px;
}
.hero h1 {
    margin:0;
    font-size:46px;
    font-weight:800;
    background:linear-gradient(90deg,#fff,#7dd3fc,#a78bfa);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}
.hero p {
    color:#aebbd0;
    margin:.4rem 0;
    font-size:16px;
}
.panel {
    padding:25px;
    border-radius:22px;
    margin-bottom:18px;
}
.field-card {
    padding:16px;
    border-radius:18px;
    margin-bottom:14px;
}
.field-title {
    font-size:12px;
    font-weight:800;
    letter-spacing:.8px;
    color:#93c5fd;
    margin-bottom:8px;
}
.result-card {
    padding:30px;
    border-radius:24px;
    text-align:center;
    margin-top:22px;
    background:linear-gradient(
        135deg,
        rgba(6,182,212,.13),
        rgba(37,99,235,.16),
        rgba(124,58,237,.16)
    );
}
.result-label {
    font-size:12px;
    letter-spacing:2px;
    text-transform:uppercase;
    color:#93c5fd;
    font-weight:800;
}
.result-number {
    font-size:38px;
    font-weight:850;
    margin:9px 0;
    color:#fff;
}
.result-unit {
    font-size:16px;
    color:#cbd5e1;
}
.constant-card {
    padding:18px;
    border-radius:17px;
    margin-bottom:12px;
}
.constant-name {
    font-weight:750;
    color:#e2e8f0;
}
.constant-value {
    color:#7dd3fc;
    margin-top:6px;
}
.stButton > button {
    width:100%;
    height:50px;
    border:0!important;
    border-radius:14px!important;
    color:#fff!important;
    font-weight:800!important;
    background:linear-gradient(
        135deg,#06b6d4,#2563eb,#7c3aed
    )!important;
    box-shadow:0 9px 26px rgba(37,99,235,.28);
}
.stButton > button:hover {
    transform:translateY(-2px);
}
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
    background:rgba(255,255,255,.045)!important;
    border-radius:12px!important;
    border-color:rgba(255,255,255,.10)!important;
}
input {
    color:#fff!important;
}
button[data-baseweb="tab"] {
    font-weight:750!important;
}
@media(max-width:700px) {
    .hero {
        padding:18px;
        border-radius:20px;
        margin-bottom:12px;
    }
[data-testid="stHorizontalBlock"] {
    gap: 0.5rem !important;
}
}
    .hero h1 {
        font-size:28px;
        white-space:nowrap;
        letter-spacing:-1px;
    }

    .hero p {
        font-size:13px;
        line-height:1.45;
        margin:.25rem 0;
    }

    .panel {
        padding:14px;
        border-radius:18px;
        margin-bottom:12px;
    }

    .panel h2 {
        font-size:24px;
        line-height:1.1;
        white-space:nowrap;
        letter-spacing:-0.8px;
        margin:0 0 8px 0;
    }

    .panel p {
        font-size:13px;
        line-height:1.4;
        margin:0;
    }

    .result-number {
        font-size:29px;
    }
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# UNIT DATABASE
# Factor converts unit -> SI base unit.
# ============================================================
UNITS = {
    # ---------- MAGNETIC: assignment order ----------
    "Magnetic induction (B)": {
        "tesla (T) [SI]": 1,
        "gauss (G) [CGS]": 1e-4
    },
    "Magnetic field (H)": {
        "ampere/meter (A m⁻¹) [SI]": 1,
        "oersted (Oe) [CGS]": 1000/(4*math.pi)
    },
    "Magnetization (M)": {
        "ampere/meter (A m⁻¹)": 1,
        "emu cm⁻³ [CGS]": 1000
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
    "Magnetic flux (Φ)": {
        "weber (Wb)": 1,
        "maxwell (Mx)": 1e-8
    },
    "Magnetic scalar potential; Magnetomotive force (φ)": {
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
    "Demagnetizing factor (N)": {
        "dimensionless [SI]": 1,
        "dimensionless [CGS]": 4*math.pi
    },
    "Magnetostriction constant (λ)": {
        "dimensionless [SI]": 1,
        "dimensionless [CGS]": 1
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

    # ---------- GENERAL PHYSICAL QUANTITIES ----------
    "Length": {
        "meter (m)": 1,
        "kilometer (km)": 1e3,
        "centimeter (cm)": 1e-2,
        "millimeter (mm)": 1e-3,
        "micrometer (μm)": 1e-6,
        "nanometer (nm)": 1e-9,
        "angstrom (Å)": 1e-10,
        "picometer (pm)": 1e-12,
        "inch (in)": 0.0254,
        "foot (ft)": 0.3048,
        "mile (mi)": 1609.344
    },
    "Mass": {
        "kilogram (kg)": 1,
        "gram (g)": 1e-3,
        "milligram (mg)": 1e-6,
        "microgram (μg)": 1e-9,
        "tonne (t)": 1e3
    },
    "Time": {
        "second (s)": 1,
        "millisecond (ms)": 1e-3,
        "microsecond (μs)": 1e-6,
        "nanosecond (ns)": 1e-9,
        "minute (min)": 60,
        "hour (h)": 3600,
        "day (d)": 86400
    },
    "Area": {
        "square meter (m²)": 1,
        "square kilometer (km²)": 1e6,
        "square centimeter (cm²)": 1e-4,
        "square millimeter (mm²)": 1e-6,
        "square inch (in²)": 0.00064516,
        "square foot (ft²)": 0.09290304,
        "square nanometer (nm²)": 1e-18,
        "square angstrom (Å²)": 1e-20
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
        "kilometer/hour (km/h)": 1000/3600,
        "mile/hour (mph)": 1609.344/3600
    },
    "Acceleration": {
        "meter/second² (m/s²)": 1,
        "centimeter/second² (cm/s²)": 1e-2,
        "standard gravity (g)": 9.80665
    },
    "Force": {
        "newton (N)": 1,
        "dyne (dyn)": 1e-5,
        "kilonewton (kN)": 1e3
    },
    "Energy": {
        "joule (J)": 1,
        "erg": 1e-7,
        "kilojoule (kJ)": 1e3,
        "electronvolt (eV)": 1.602176634e-19,
        "calorie (cal)": 4.184
    },
    "Power": {
        "watt (W)": 1,
        "kilowatt (kW)": 1e3,
        "megawatt (MW)": 1e6,
        "erg/second (erg/s)": 1e-7,
        "horsepower (hp)": 745.699872
    },
    "Pressure": {
        "pascal (Pa)": 1,
        "kilopascal (kPa)": 1e3,
        "megapascal (MPa)": 1e6,
        "bar": 1e5,
        "atmosphere (atm)": 101325,
        "torr": 133.322368,
        "dyne/cm²": 0.1
    },
    "Frequency": {
        "hertz (Hz)": 1,
        "kilohertz (kHz)": 1e3,
        "megahertz (MHz)": 1e6,
        "gigahertz (GHz)": 1e9
    },
    "Electric Charge": {
        "coulomb (C)": 1,
        "millicoulomb (mC)": 1e-3,
        "microcoulomb (μC)": 1e-6,
        "nanocoulomb (nC)": 1e-9
    },
    "Electric Potential": {
        "volt (V)": 1,
        "millivolt (mV)": 1e-3,
        "kilovolt (kV)": 1e3
    },
    "Electric Current": {
        "ampere (A)": 1,
        "milliampere (mA)": 1e-3,
        "microampere (μA)": 1e-6
    },
    "Resistance": {
        "ohm (Ω)": 1,
        "milliohm (mΩ)": 1e-3,
        "kilohm (kΩ)": 1e3,
        "megohm (MΩ)": 1e6
    },
    "Capacitance": {
        "farad (F)": 1,
        "microfarad (μF)": 1e-6,
        "nanofarad (nF)": 1e-9,
        "picofarad (pF)": 1e-12
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
    }
}

# ============================================================
# MAGNETIC REFERENCE TABLE
# ============================================================
MAGNETIC_TABLE = [
    ("Magnetic induction", "B", "tesla (T)", "gauss (G)", "1 T = 10⁴ G"),
    ("Magnetic field", "H", "A m⁻¹", "oersted (Oe)", "1 A m⁻¹ = 4π × 10⁻³ Oe"),
    ("Magnetization", "M", "A m⁻¹", "emu cm⁻³", "1 A m⁻¹ = 10⁻³ emu cm⁻³"),
    ("Magnetic polarization", "J", "T", "G", "1 T = 10⁴/4π"),
    ("Magnetic moment", "m", "A m²", "emu = G cm³", "1 A m² = 10³ emu"),
    ("Magnetic moment per unit mass", "σ", "A m² kg⁻¹", "emu g⁻¹", "1 A m² kg⁻¹ = 1 emu g⁻¹"),
    ("Volume magnetic susceptibility", "κ", "dimensionless", "dimensionless", "SI = 1/4π CGS"),
    ("Mass magnetic susceptibility", "χ", "m³ kg⁻¹", "emu Oe⁻¹ g⁻¹", "1 m³ kg⁻¹ = 10³/4π"),
    ("Molar magnetic susceptibility", "χₘ", "m³ mol⁻¹", "emu Oe⁻¹ g⁻¹ mol⁻¹", "1 m³ mol⁻¹ = 10⁶/4π"),
    ("Magnetic permeability", "μ", "H m⁻¹", "G Oe⁻¹", "1 H m⁻¹ = 10⁷/4π"),
    ("Magnetic flux", "Φ", "weber (Wb)", "maxwell (Mx)", "1 Wb = 10⁸ Mx"),
    ("Magnetic scalar potential; Magnetomotive force", "φ", "A", "gilbert", "1 A = 4π/10 gilbert"),
    ("Magnetic vector potential", "A", "Wb m⁻¹", "emu = G cm", "1 Wb m⁻¹ = 10⁶ emu"),
    ("Magnetic pole strength", "p", "A m", "emu = G cm²", "1 A m = 10 emu"),
    ("Demagnetizing factor", "N", "dimensionless", "dimensionless", "SI = 4π CGS"),
    ("Magnetostriction constant", "λ", "dimensionless", "dimensionless", "SI = CGS"),
    ("Anisotropy constant", "K, K₁, Kᵤ", "J m⁻³", "erg cm⁻³", "1 J m⁻³ = 10 erg cm⁻³"),
    ("Magnetostatic energy", "Eₘ", "J m⁻³", "erg cm⁻³", "1 J m⁻³ = 10 erg cm⁻³"),
    ("Energy product", "(BH)ₘₐₓ", "J m⁻³", "erg cm⁻³", "1 J m⁻³ = 10 erg cm⁻³"),
]

# ============================================================
# CONVERSIONS
# ============================================================
def temp_to_k(x, unit):
    if unit == "Kelvin (K)":
        return x
    if unit == "Celsius (°C)":
        return x + 273.15
    return (x - 32) * 5/9 + 273.15


def k_to_temp(x, unit):
    if unit == "Kelvin (K)":
        return x
    if unit == "Celsius (°C)":
        return x - 273.15
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
                "0123456789-",
                "⁰¹²³⁴⁵⁶⁷⁸⁹⁻"
            )
        )

        return f"{mantissa} × 10{superscript}"

    return f"{x:.3f}".rstrip("0").rstrip(".")


# ============================================================
# SAFE SCIENTIFIC CALCULATOR
# ============================================================
BIN_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
}

UNARY_OPS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

FUNCS = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "sqrt": math.sqrt,
    "log": math.log10,
    "ln": math.log,
    "exp": math.exp,
    "abs": abs,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
}

NAMES = {
    "pi": math.pi,
    "e": math.e,
}


def safe_eval(expr):
    expr = expr.strip()
    expr = expr.replace("×", "*")
    expr = expr.replace("÷", "/")
    expr = expr.replace("^", "**")

    tree = ast.parse(expr, mode="eval")

    def walk(node):
        if isinstance(node, ast.Expression):
            return walk(node.body)

        if isinstance(node, ast.Constant) and isinstance(
            node.value, (int, float)
        ):
            return node.value

        if isinstance(node, ast.Num):
            return node.n

        if isinstance(node, ast.BinOp) and type(node.op) in BIN_OPS:
            return BIN_OPS[type(node.op)](
                walk(node.left),
                walk(node.right)
            )

        if isinstance(node, ast.UnaryOp) and type(node.op) in UNARY_OPS:
            return UNARY_OPS[type(node.op)](
                walk(node.operand)
            )

        if isinstance(node, ast.Name) and node.id in NAMES:
            return NAMES[node.id]

        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in FUNCS
        ):
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
    <h1>🧑🏻‍🎓 Ar_PHYHBTU</h1>
    <p>Calculate • Convert • Explore</p>
    <p>
    </p>
</div>
""", unsafe_allow_html=True)

converter, calculator, constants = st.tabs([
    "Converter",
    "Calculator",
    "Constants"
])


# ============================================================
# CONVERTER
# ============================================================
with converter:

    st.markdown("""
    <div class="panel">
        <h2>🔄 Universal Unit Converter</h2>
        <p>
        </p>
    </div>
    """, unsafe_allow_html=True)

    categories = list(UNITS.keys()) + ["Temperature"]

    # Physical quantity
    with st.container(border=True):
        st.markdown(
            '<div class="field-title">📚 PHYSICAL QUANTITY</div>',
            unsafe_allow_html=True
        )

        category = st.selectbox(
            "Physical quantity",
            categories,
            label_visibility="collapsed",
            key="category"
        )

    if category == "Temperature":
        units = [
            "Kelvin (K)",
            "Celsius (°C)",
            "Fahrenheit (°F)"
        ]
    else:
        units = list(UNITS[category].keys())

    # ========================================================
    # IMPORTANT:
    # VALUE + FROM UNIT ARE NOW INSIDE ONE REAL STREAMLIT BOX
    # ========================================================
    with st.container(border=True):

        st.markdown(
            '<div class="field-title"> '
            '📤 Enter Value & Select UNIT</div>',
            unsafe_allow_html=True
        )
        value_col, unit_col = st.columns(
            [1.35, 1],
            gap="small"
        )

        with value_col:
            value = st.number_input(
                "Enter value",
                value=1.0,
                format="%.12g",
                label_visibility="collapsed",
                key="converter_value"
            )
 
        with unit_col:
            from_unit = st.selectbox(
                "From unit",
                units,
                label_visibility="collapsed",
                key="from_unit"
            )

    # TO UNIT remains separate
    with st.container(border=True):

        st.markdown(
            '<div class="field-title">📥 TO UNIT</div>',
            unsafe_allow_html=True
        )

        to_unit = st.selectbox(
            "To unit",
            units,
            label_visibility="collapsed",
            key="to_unit"
        )

    if st.button(
        "⚡  CONVERT",
        key="convert",
        use_container_width=True
    ):
        try:
            result = convert_value(
                value,
                category,
                from_unit,
                to_unit
            )

            st.markdown(
                f"""<div class="result-card">
    <div class="result-label">
        ✨ Conversion Result
    </div>
    <div class="result-number">
        {fmt(result)}
    </div>
    <div class="result-unit">
        {to_unit}
    </div>
</div>""",
                unsafe_allow_html=True
            )

            st.caption(
                f"{fmt(value)} {from_unit} → "
                f"{fmt(result)} {to_unit}"
            )

        except Exception as e:
            st.error(f"Conversion error: {e}")


# ============================================================
# CALCULATOR — COMPACT 5-COLUMN PHONE STYLE
# ============================================================
with calculator:

    # Use a self-contained HTML/JS keypad so Streamlit's mobile
    # responsive columns cannot stack the keys vertically.
    components.html(r"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <style>
        * { box-sizing: border-box; }

        html, body {
          margin: 0;
          padding: 0;
          width: 100%;
          background: transparent;
          font-family: Arial, Helvetica, sans-serif;
          overflow: hidden;
        }

        .calc {
          width: min(100%, 620px);
          margin: 0 auto;
          padding: 4px 0 8px;
        }

        .display {
          background: #050505;
          border: 1px solid rgba(255,255,255,.08);
          border-radius: 22px;
          height: 128px;
          padding: 13px 18px 12px;
          margin-bottom: 8px;
          display: flex;
          flex-direction: column;
          justify-content: flex-end;
          overflow: hidden;
        }

        .history {
          height: 23px;
          color: #666;
          font-size: 14px;
          text-align: right;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }

        .screen {
          color: #fff;
          font-size: clamp(38px, 7vw, 54px);
          line-height: 1.05;
          font-weight: 400;
          text-align: right;
          white-space: nowrap;
          overflow-x: auto;
          scrollbar-width: none;
        }
        .screen::-webkit-scrollbar { display:none; }

        .mode {
          height: 19px;
          text-align: center;
          color: #737b87;
          font-size: 11px;
          letter-spacing: .5px;
          margin-bottom: 6px;
        }

        .keys {
          display: grid;
          grid-template-columns: repeat(5, minmax(0, 1fr));
          gap: 8px;
        }

        button {
          appearance: none;
          border: 0;
          outline: none;
          height: 58px;
          width: 100%;
          border-radius: 17px;
          background: #252525;
          color: #f4f4f4;
          font-size: 20px;
          font-weight: 500;
          cursor: pointer;
          box-shadow: inset 0 0 0 1px rgba(255,255,255,.025);
          -webkit-tap-highlight-color: transparent;
          user-select: none;
        }

        button:active {
          transform: scale(.96);
          background: #363636;
        }

        button.op {
          color: #ff7a00;
          font-size: 23px;
        }

        button.equal {
          background: #ff7a00;
          color: #fff;
          font-size: 24px;
        }

        button.equal:active { background: #e86e00; }

        @media (max-width: 500px) {
          .calc { padding-left: 0; padding-right: 0; }
          .display {
            height: 116px;
            border-radius: 20px;
            padding: 11px 15px;
          }
          .keys { gap: 6px; }
          button {
            height: 54px;
            border-radius: 16px;
            font-size: 18px;
          }
          button.op, button.equal { font-size: 21px; }
        }
      </style>
    </head>

    <body>
      <div class="calc">
        <div class="display">
          <div id="history" class="history"></div>
          <div id="screen" class="screen">0</div>
        </div>

        <div id="mode" class="mode">DEG</div>

        <div class="keys">
          <button data-a="second">2nd</button>
          <button data-a="mode">deg</button>
          <button data-a="sin">sin</button>
          <button data-a="cos">cos</button>
          <button data-a="tan">tan</button>

          <button data-a="power">xʸ</button>
          <button data-a="log">lg</button>
          <button data-a="ln">ln</button>
          <button data-a="(">(</button>
          <button data-a=")">)</button>

          <button data-a="sqrt">√x</button>
          <button data-a="clear">AC</button>
          <button data-a="back">⌫</button>
          <button data-a="percent" class="op">%</button>
          <button data-a="divide" class="op">÷</button>

          <button data-a="factorial">x!</button>
          <button data-a="7">7</button>
          <button data-a="8">8</button>
          <button data-a="9">9</button>
          <button data-a="multiply" class="op">×</button>

          <button data-a="inverse">1/x</button>
          <button data-a="4">4</button>
          <button data-a="5">5</button>
          <button data-a="6">6</button>
          <button data-a="minus" class="op">−</button>

          <button data-a="pi">π</button>
          <button data-a="1">1</button>
          <button data-a="2">2</button>
          <button data-a="3">3</button>
          <button data-a="plus" class="op">+</button>

          <button data-a="sign">±</button>
          <button data-a="e">e</button>
          <button data-a="0">0</button>
          <button data-a="dot">.</button>
          <button data-a="equals" class="equal">=</button>
        </div>
      </div>

      <script>
        let expr = "";
        let second = false;
        let degree = true;
        let lastAnswer = "";

        const screen = document.getElementById("screen");
        const history = document.getElementById("history");
        const mode = document.getElementById("mode");

        function show(value) {
          screen.textContent = value || "0";
          screen.scrollLeft = screen.scrollWidth;
        }

        function cleanNumber(n) {
          if (!Number.isFinite(n)) throw new Error("Math error");
          if (Math.abs(n) < 1e-12) n = 0;
          return Number(n.toPrecision(12)).toString();
        }

        function factorial(n) {
          if (!Number.isFinite(n) || n < 0 || Math.floor(n) !== n || n > 170)
            throw new Error("Invalid factorial");
          let r = 1;
          for (let i = 2; i <= n; i++) r *= i;
          return r;
        }

        function evaluate(s) {
          // Convert the calculator symbols to JavaScript math syntax.
          let x = s
            .replaceAll("÷", "/")
            .replaceAll("×", "*")
            .replaceAll("−", "-")
            .replaceAll("^", "**")
            .replaceAll("π", "Math.PI")
            .replace(/\be\b/g, "Math.E")
            .replace(/\blg\(/g, "Math.log10(")
            .replace(/\bln\(/g, "Math.log(")
            .replace(/\bsqrt\(/g, "Math.sqrt(");

          // Use wrapper functions instead of regex-editing trig arguments.
          // This correctly handles nested expressions such as sin(30+15),
          // sin(sqrt(900)), and inverse trig in both DEG and RAD modes.
          const sinFn = degree
            ? (v) => Math.sin(v * Math.PI / 180)
            : (v) => Math.sin(v);
          const cosFn = degree
            ? (v) => Math.cos(v * Math.PI / 180)
            : (v) => Math.cos(v);
          const tanFn = degree
            ? (v) => Math.tan(v * Math.PI / 180)
            : (v) => Math.tan(v);
          const asinFn = degree
            ? (v) => Math.asin(v) * 180 / Math.PI
            : (v) => Math.asin(v);
          const acosFn = degree
            ? (v) => Math.acos(v) * 180 / Math.PI
            : (v) => Math.acos(v);
          const atanFn = degree
            ? (v) => Math.atan(v) * 180 / Math.PI
            : (v) => Math.atan(v);

          x = x.replace(/\bsin\(/g, "sinFn(")
               .replace(/\bcos\(/g, "cosFn(")
               .replace(/\btan\(/g, "tanFn(")
               .replace(/\basin\(/g, "asinFn(")
               .replace(/\bacos\(/g, "acosFn(")
               .replace(/\batan\(/g, "atanFn(");

          // Only allow syntax that can be produced by this calculator.
          if (!/^[0-9+\-*/%().,\sA-Za-z_]+$/.test(x))
            throw new Error("Invalid");

          const result = Function(
            "sinFn", "cosFn", "tanFn", "asinFn", "acosFn", "atanFn",
            '"use strict"; return (' + x + ')'
          )(sinFn, cosFn, tanFn, asinFn, acosFn, atanFn);

          if (!Number.isFinite(result)) throw new Error("Math error");
          return result;
        }

        function refresh() {
          show(expr || "0");
          mode.textContent = degree ? "DEG" : "RAD";
          document.querySelector('[data-a="second"]').textContent = "2nd";
          document.querySelector('[data-a="mode"]').textContent =
            degree ? "deg" : "rad";
        }

        function add(v) {
          expr += v;
          refresh();
        }

        function unary(kind) {
          try {
            if (!expr) return;

            let n = evaluate(expr);

            if (kind === "sqrt") n = Math.sqrt(n);
            if (kind === "square") n = n * n;
            if (kind === "inverse") n = 1 / n;
            if (kind === "percent") n = n / 100;
            if (kind === "factorial") n = factorial(n);

            expr = cleanNumber(n);
            refresh();
          } catch(e) {
            history.textContent = expr;
            show("Error");
          }
        }

        function equals() {
          if (!expr) return;

          try {
            const old = expr;
            const result = evaluate(expr);
            const ans = cleanNumber(result);

            history.textContent = old + " =";
            expr = ans;
            lastAnswer = ans;
            show(ans);
          } catch(e) {
            history.textContent = expr;
            show("Error");
          }
        }

        function press(a) {
          if (/^[0-9]$/.test(a)) return add(a);

          if (a === "dot") return add(".");
          if (a === "plus") return add("+");
          if (a === "minus") return add("−");
          if (a === "multiply") return add("×");
          if (a === "divide") return add("÷");
          if (a === "power") return add("^");
          if (a === "(" || a === ")") return add(a);
          if (a === "pi") return add("π");
          if (a === "e") return add("e");

          if (a === "clear") {
            expr = "";
            history.textContent = "";
            show("0");
            return;
          }

          if (a === "back") {
            expr = expr.slice(0, -1);
            refresh();
            return;
          }

          if (a === "mode") {
            degree = !degree;
            refresh();
            return;
          }

          if (a === "second") {
            second = !second;
            const b = document.querySelector('[data-a="second"]');
            b.style.color = second ? "#ff7a00" : "#f4f4f4";
            return;
          }

          if (a === "sin") return add((second ? "asin(" : "sin("));
          if (a === "cos") return add((second ? "acos(" : "cos("));
          if (a === "tan") return add((second ? "atan(" : "tan("));
          if (a === "log") return add("lg(");
          if (a === "ln") return add("ln(");
          if (a === "sqrt") return unary("sqrt");
          if (a === "factorial") return unary("factorial");
          if (a === "inverse") return unary("inverse");
          if (a === "percent") return unary("percent");

          if (a === "sign") {
            if (!expr) return;
            if (expr.startsWith("-(") && expr.endsWith(")"))
              expr = expr.slice(2, -1);
            else
              expr = "-(" + expr + ")";
            refresh();
            return;
          }

          if (a === "equals") return equals();
        }

        document.querySelectorAll("button").forEach(btn => {
          btn.addEventListener("click", () => press(btn.dataset.a));
        });

        refresh();
      </script>
    </body>
    </html>
    """, height=570, scrolling=False)


# ============================================================
# CONSTANTS
# ============================================================
with constants:

    st.markdown("""
    <div class="panel">
        <h2>📐 Fundamental Constants</h2>
        <p>Frequently used constants for Physics calculations.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    /* Keep the magnetic reference table compact and scrollable on mobile */
    [data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
    }
    </style>
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


    # ========================================================
    # MAGNETIC QUANTITIES — SI / CGS
    # ========================================================
    st.markdown("""
    <div class="panel">
        <h3>🧲 Magnetic Quantities — SI / CGS</h3>
        <p>Assignment reference table in serial order.</p>
    </div>
    """, unsafe_allow_html=True)

    magnetic_df = pd.DataFrame(
        MAGNETIC_TABLE,
        columns=[
            "Magnetic Term",
            "Symbol",
            "SI Unit",
            "CGS Unit",
            "Conversion"
        ]
    )

    st.dataframe(
        magnetic_df,
        use_container_width=True,
        hide_index=True,
        height=520
    )


# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div style="
    text-align:center;
    color:#64748b;
    margin-top:40px;
    padding:20px;
    font-size:13px;
">
⚛️ <b>Ar_PHYHBTU</b><br>
Developed by Arun Yadav
</div>
""", unsafe_allow_html=True)
