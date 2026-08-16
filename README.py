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
    "oersted (Oe) [CGS]": 1000 / (4 * math.pi)
},

"Magnetization (M)": {
    "ampere/meter (A m⁻¹)": 1,
    "emu cm⁻³ [CGS]": 1000
},

"Magnetic polarization (J)": {
    "tesla (T) [SI]": 1,
    "emu/cm³ [CGS]": 4 * math.pi * 1e-4
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
    "dimensionless [CGS]": 1 / (4 * math.pi)
},

"Mass magnetic susceptibility (χ = κ/ρ)": {
    "m³ kg⁻¹": 1,
    "emu Oe⁻¹ g⁻¹": 4 * math.pi / 1000
},

"Molar magnetic susceptibility (χₘ = χM*)": {
    "m³ mol⁻¹": 1,
    "emu Oe⁻¹ g⁻¹ mol⁻¹": 4 * math.pi / 1e6
},

"Magnetic permeability (μ = B/H)": {
    "henry/meter (H m⁻¹)": 1,
    "G Oe⁻¹": 1e7 / (4 * math.pi)
},

"Magnetic flux (Φ)": {
    "weber (Wb)": 1,
    "maxwell (Mx)": 1e-8
},

"Magnetic scalar potential; Magnetomotive force (φ)": {
    "ampere (A) [SI]": 1,
    "gilbert [CGS]": 10 / (4 * math.pi)
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
    "dimensionless [CGS]": 4 * math.pi
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
    ("Magnetic field strength", "H", "A m⁻¹", "oersted (Oe)", "1 A m⁻¹ = 4π × 10⁻³ Oe"),
    ("Magnetization", "M", "A m⁻¹", "emu cm⁻³", "1 A m⁻¹ = 10⁻³ emu cm⁻³"),
    ("Magnetic polarization", "J", "T", "emu cm⁻³", "1 T = 10⁴/(4π) emu cm⁻³"),
    ("Magnetic moment", "m", "A m²", "emu", "1 A m² = 10³ emu"),
    ("Magnetic moment per unit mass", "σ", "A m² kg⁻¹", "emu g⁻¹", "1 A m² kg⁻¹ = 1 emu g⁻¹"),
    ("Volume magnetic susceptibility", "κ", "dimensionless", "dimensionless", "χSI = χCGS/(4π)"),
    ("Mass magnetic susceptibility", "χ", "m³ kg⁻¹", "emu Oe⁻¹ g⁻¹", "1 m³ kg⁻¹ = 10³/(4π) emu Oe⁻¹ g⁻¹"),
    ("Molar magnetic susceptibility", "χₘ", "m³ mol⁻¹", "emu Oe⁻¹ g⁻¹ mol⁻¹", "1 m³ mol⁻¹ = 10⁶/(4π) emu Oe⁻¹ g⁻¹ mol⁻¹"),
    ("Magnetic permeability", "μ", "H m⁻¹", "G Oe⁻¹", "1 H m⁻¹ = 10⁷/(4π) G Oe⁻¹"),
    ("Magnetic flux", "Φ", "weber (Wb)", "maxwell (Mx)", "1 Wb = 10⁸ Mx"),
    ("Magnetic scalar potential / Magnetomotive force", "φ", "A", "gilbert (Gi)", "1 A = 4π/10 gilbert"),
    ("Magnetic vector potential", "A", "Wb m⁻¹", "G cm", "1 Wb m⁻¹ = 10⁶ G cm"),
    ("Magnetic pole strength", "p", "A m", "G cm²", "1 A m = 10 G cm²"),
    ("Demagnetizing factor", "N", "dimensionless", "dimensionless", "NSI = NCGS/(4π)"),
    ("Magnetostriction constant", "λ", "dimensionless", "dimensionless", "SI = CGS"),
    ("Anisotropy constant", "K, K₁, Kᵤ", "J m⁻³", "erg cm⁻³", "1 J m⁻³ = 10 erg cm⁻³"),
    ("Magnetostatic energy density", "Eₘ", "J m⁻³", "erg cm⁻³", "1 J m⁻³ = 10 erg cm⁻³"),
    ("Energy product", "(BH)ₘₐₓ", "J m⁻³", "erg cm⁻³", "1 J m⁻³ = 10 erg cm⁻³"),
]
MAGNETISM_FORMULA_TABLE = [

    ("Magnetic induction / Magnetic flux density",
     r"B",
     r"B = \mu_0(H + M)",
     "Unit: tesla (T)"),

    ("Magnetic field strength",
     r"H",
     r"H = \frac{B}{\mu_0} - M",
     "Unit: A m⁻¹"),

    ("Magnetization",
     r"M",
     r"M = \frac{m}{V}",
     "Unit: A m⁻¹"),

    ("Magnetic polarization",
     r"J",
     r"J = \mu_0 M",
     "Unit: tesla (T)"),

    ("Magnetic susceptibility",
     r"\chi",
     r"\chi = \frac{M}{H}",
     "Dimensionless"),

    ("Relative permeability",
     r"\mu_r",
     r"\mu_r = \frac{\mu}{\mu_0}",
     "Dimensionless"),

    ("Absolute permeability",
     r"\mu",
     r"\mu = \frac{B}{H}",
     "Unit: H m⁻¹"),

    ("Vacuum permeability",
     r"\mu_0",
     r"\mu_0 = 4\pi \times 10^{-7}\ {\rm H\,m^{-1}}",
     "Exact SI value"),

    ("Magnetic dipole moment",
     r"m",
     r"m = IA",
     "Unit: A m²"),

    ("Torque on magnetic dipole",
     r"\tau",
     r"\boldsymbol{\tau} = \mathbf{m}\times\mathbf{B}",
     r"|\tau| = mB\sin\theta"),

    ("Potential energy of magnetic dipole",
     r"U",
     r"U = -\mathbf{m}\cdot\mathbf{B}",
     r"U = -mB\cos\theta"),

    ("Force on magnetic dipole",
     r"F",
     r"\mathbf{F} = \nabla(\mathbf{m}\cdot\mathbf{B})",
     "Non-uniform magnetic field"),

    ("Biot–Savart law",
     r"dB",
     r"d\mathbf{B} = \frac{\mu_0}{4\pi}\frac{I(d\boldsymbol{\ell}\times\hat{\mathbf r})}{r^2}",
     "Magnetic field due to current element"),

    ("Biot–Savart magnitude",
     r"dB",
     r"dB = \frac{\mu_0}{4\pi}\frac{I\,d\ell\sin\theta}{r^2}",
     "Magnitude"),

    ("Long straight current-carrying wire",
     r"B",
     r"B = \frac{\mu_0 I}{2\pi r}",
     "Infinite straight wire"),

    ("Circular current loop at centre",
     r"B",
     r"B = \frac{\mu_0 I}{2R}",
     "Single circular loop"),

    ("N-turn circular coil at centre",
     r"B",
     r"B = \frac{\mu_0 NI}{2R}",
     "N turns"),

    ("Circular loop on axis",
     r"B",
     r"B = \frac{\mu_0 I R^2}{2(R^2+x^2)^{3/2}}",
     "Single loop"),

    ("N-turn circular loop on axis",
     r"B",
     r"B = \frac{\mu_0 NIR^2}{2(R^2+x^2)^{3/2}}",
     "N turns"),

    ("Ampere's circuital law",
     r"\oint \mathbf{B}\cdot d\boldsymbol{\ell}",
     r"\oint \mathbf{B}\cdot d\boldsymbol{\ell} = \mu_0 I_{\rm enc}",
     "Steady current"),

    ("Ampere's law in H form",
     r"\oint \mathbf{H}\cdot d\boldsymbol{\ell}",
     r"\oint \mathbf{H}\cdot d\boldsymbol{\ell} = I_{\rm enc}",
     "Magnetic field strength"),

    ("Long solenoid",
     r"B",
     r"B = \mu_0 nI",
     r"n = N/L"),

    ("Solenoid field strength",
     r"H",
     r"H = nI",
     r"n = N/L"),

    ("Toroid magnetic field",
     r"B",
     r"B = \frac{\mu_0 NI}{2\pi r}",
     "Ideal toroid"),

    ("Toroid field strength",
     r"H",
     r"H = \frac{NI}{2\pi r}",
     "Inside toroid"),

    ("Lorentz magnetic force",
     r"F",
     r"\mathbf{F} = q(\mathbf{v}\times\mathbf{B})",
     r"|F| = qvB\sin\theta"),

    ("Total Lorentz force",
     r"F",
     r"\mathbf{F} = q(\mathbf{E}+\mathbf{v}\times\mathbf{B})",
     "Electric + magnetic force"),

    ("Force on current-carrying conductor",
     r"F",
     r"\mathbf{F}=I(\mathbf{L}\times\mathbf{B})",
     r"|F| = ILB\sin\theta"),

    ("Force between parallel currents",
     r"\frac{F}{L}",
     r"\frac{F}{L} = \frac{\mu_0 I_1I_2}{2\pi r}",
     "Long parallel conductors"),

    ("Cyclotron angular frequency",
     r"\omega_c",
     r"\omega_c = \frac{qB}{m}",
     "Non-relativistic"),

    ("Cyclotron frequency",
     r"f_c",
     r"f_c = \frac{qB}{2\pi m}",
     "Non-relativistic"),

    ("Cyclotron radius",
     r"r",
     r"r = \frac{mv}{qB}",
     r"v \perp B"),

    ("Helical pitch",
     r"p",
     r"p = v_{\parallel}T",
     "Charged particle in magnetic field"),

    ("Magnetic flux",
     r"\Phi_B",
     r"\Phi_B = \int \mathbf{B}\cdot d\mathbf{A}",
     "Unit: weber (Wb)"),

    ("Uniform magnetic flux",
     r"\Phi_B",
     r"\Phi_B = BA\cos\theta",
     "Uniform magnetic field"),

    ("Flux linkage",
     r"N\Phi_B",
     r"N\Phi_B = NBA\cos\theta",
     "N-turn coil"),

    ("Faraday's law",
     r"\varepsilon",
     r"\varepsilon = -\frac{d\Phi_B}{dt}",
     "Induced emf"),

    ("N-turn Faraday law",
     r"\varepsilon",
     r"\varepsilon = -N\frac{d\Phi_B}{dt}",
     "N turns"),

    ("Motional emf",
     r"\varepsilon",
     r"\varepsilon = Blv",
     "Perpendicular motion"),

    ("General motional emf",
     r"\varepsilon",
     r"\varepsilon = \int(\mathbf{v}\times\mathbf{B})\cdot d\boldsymbol{\ell}",
     "General form"),

    ("Self inductance",
     r"L",
     r"L = \frac{N\Phi}{I}",
     "Linear system"),

    ("Induced emf in inductor",
     r"\varepsilon_L",
     r"\varepsilon_L = -L\frac{dI}{dt}",
     "Self induction"),

    ("Solenoid inductance",
     r"L",
     r"L = \frac{\mu_0N^2A}{l}",
     "Long air-core solenoid"),

    ("Solenoid inductance with material",
     r"L",
     r"L = \frac{\mu N^2A}{l}",
     r"\mu = \mu_0\mu_r"),

    ("Mutual inductance",
     r"M",
     r"M = \frac{N_2\Phi_{21}}{I_1}",
     "Linear system"),

    ("Mutual induced emf",
     r"\varepsilon_2",
     r"\varepsilon_2 = -M\frac{dI_1}{dt}",
     "Mutual induction"),

    ("Coefficient of coupling",
     r"k",
     r"k = \frac{M}{\sqrt{L_1L_2}}",
     r"0 \leq k \leq 1"),

    ("Energy stored in inductor",
     r"U",
     r"U = \frac{1}{2}LI^2",
     "Magnetic energy"),

    ("Magnetic energy density",
     r"u",
     r"u = \frac{B^2}{2\mu_0}",
     "Vacuum"),

    ("Magnetic energy density in material",
     r"u",
     r"u = \frac{B^2}{2\mu}",
     "Linear isotropic material"),

    ("Energy density",
     r"u",
     r"u = \frac{1}{2}BH",
     "Linear magnetic medium"),

    ("Gauss's law for magnetism",
     r"\nabla\cdot\mathbf{B}",
     r"\nabla\cdot\mathbf{B}=0",
     "No magnetic monopoles"),

    ("Integral Gauss law for magnetism",
     r"\oint\mathbf{B}\cdot d\mathbf{A}",
     r"\oint\mathbf{B}\cdot d\mathbf{A}=0",
     "Closed surface"),

    ("Faraday–Maxwell equation",
     r"\nabla\times\mathbf{E}",
     r"\nabla\times\mathbf{E}=-\frac{\partial\mathbf{B}}{\partial t}",
     "Differential form"),

    ("Ampere–Maxwell law",
     r"\nabla\times\mathbf{B}",
     r"\nabla\times\mathbf{B}=\mu_0\mathbf{J}+\mu_0\epsilon_0\frac{\partial\mathbf{E}}{\partial t}",
     "Vacuum"),

    ("Magnetization relation",
     r"M",
     r"M=\chi H",
     "Linear magnetic material"),

    ("Magnetic induction in material",
     r"B",
     r"B=\mu_0(H+M)",
     "SI"),

    ("Using susceptibility",
     r"B",
     r"B=\mu_0(1+\chi)H",
     "Linear isotropic material"),

    ("Relative permeability",
     r"\mu_r",
     r"\mu_r=1+\chi",
     "Linear isotropic material"),

    ("Permeability",
     r"\mu",
     r"\mu=\mu_0\mu_r",
     "Absolute permeability"),

    ("Diamagnetic susceptibility",
     r"\chi",
     r"\chi<0",
     "Small negative susceptibility"),

    ("Paramagnetic susceptibility",
     r"\chi",
     r"\chi>0",
     "Positive susceptibility"),

    ("Curie's law",
     r"\chi",
     r"\chi=\frac{C}{T}",
     "Paramagnetic material"),

    ("Curie–Weiss law",
     r"\chi",
     r"\chi=\frac{C}{T-\theta}",
     "Above ordering temperature"),

    ("Inverse susceptibility",
     r"\frac{1}{\chi}",
     r"\frac{1}{\chi}=\frac{T-\theta}{C}",
     "Curie–Weiss form"),

    ("Langevin function",
     r"L(x)",
     r"L(x)=\coth x-\frac{1}{x}",
     "Classical paramagnetism"),

    ("Langevin parameter",
     r"x",
     r"x=\frac{\mu B}{k_BT}",
     "Dimensionless"),

    ("Langevin magnetization",
     r"M",
     r"M=M_sL(x)",
     "Classical model"),

    ("Low-field Langevin approximation",
     r"L(x)",
     r"L(x)\approx\frac{x}{3}",
     r"|x|\ll1"),

    ("High-field Langevin approximation",
     r"L(x)",
     r"L(x)\approx1-\frac{1}{x}",
     r"x\gg1"),

    ("Effective magnetic moment",
     r"\mu_{\rm eff}",
     r"\mu_{\rm eff}=g\sqrt{J(J+1)}\,\mu_B",
     "General angular momentum"),

    ("Spin-only effective moment",
     r"\mu_{\rm eff}",
     r"\mu_{\rm eff}=\sqrt{n(n+2)}\,\mu_B",
     "n = unpaired electrons"),

    ("Bohr magneton",
     r"\mu_B",
     r"\mu_B=\frac{e\hbar}{2m_e}",
     r"\approx9.274\times10^{-24}\ {\rm A\,m^2}"),

    ("Spontaneous magnetization",
     r"M_s",
     r"M=M_s\quad(H=0,\ T<T_C)",
     "Ferromagnetic state"),

    ("Exchange interaction",
     r"E_{\rm ex}",
     r"E_{\rm ex}=-2J\,\mathbf{S}_i\cdot\mathbf{S}_j",
     "Heisenberg model"),

    ("Saturation magnetization",
     r"M_s",
     r"M_s=n\mu",
     "Simple magnetic moment model"),

    ("Remanence / Retentivity",
     r"B_r",
     r"B_r=B\quad(H=0)",
     "After magnetization"),

    ("Coercive field",
     r"H_c",
     r"H=H_c\quad(B=0)",
     "Hysteresis loop"),

    ("Hysteresis loss per unit volume",
     r"W_h",
     r"W_h=\oint H\,dB",
     "Area of B-H loop"),

    ("Domain wall energy",
     r"\gamma",
     r"\gamma\approx4\sqrt{AK}",
     "Simple 180° wall model"),

    ("Domain wall width",
     r"\delta",
     r"\delta\approx\pi\sqrt{\frac{A}{K}}",
     "Simple 180° Bloch wall"),

    ("Uniaxial anisotropy energy",
     r"E_a",
     r"E_a=K_u\sin^2\theta",
     "First-order uniaxial"),

    ("Anisotropy field",
     r"H_k",
     r"H_k=\frac{2K_u}{\mu_0M_s}",
     "Uniaxial approximation"),

    ("Demagnetizing field",
     r"H_d",
     r"H_d=-NM",
     "SI convention"),

    ("Internal magnetic field",
     r"H_{\rm int}",
     r"H_{\rm int}=H_{\rm appl}-NM",
     "Simple demagnetizing relation"),

    ("Magnetostriction",
     r"\lambda",
     r"\lambda=\frac{\Delta L}{L}",
     "Relative length change"),
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

    # Scientific notation for very small or very large values
    if abs(x) >= 1e6 or abs(x) <= 1e-4:
        s = f"{x:.6e}"
        mantissa, exponent = s.split("e")
        exponent = int(exponent)

        mantissa = mantissa.rstrip("0").rstrip(".")

        superscript = str(exponent).translate(
            str.maketrans(
                "0123456789-",
                "⁰¹²³⁴⁵⁶⁷⁸⁹⁻"
            )
        )

        return f"{mantissa} × 10{superscript}"

    return f"{x:.6f}".rstrip("0").rstrip(".")

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
    "Physics Toolkit"
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

    # ========================================================
    # CGS / SI QUICK CONVERSION
    # The separate To Unit selector is intentionally removed.
    # CGS/SI buttons directly choose the target system unit.
    # ========================================================
    def _find_system_unit(unit_list, system, category_name):
        """Find the canonical SI/CGS target unit for the selected quantity.

        Many general units in the database are intentionally not tagged
        [SI]/[CGS], so the quick buttons use an explicit category map first.
        This prevents cases such as Force -> dyne/N from incorrectly showing
        "unit not available".
        """
        system = system.upper()

        # Exact canonical SI/CGS pairs for quantities where both systems exist.
        canonical_pairs = {
            "Magnetic induction (B)": {"SI": ("tesla (T) [SI]",), "CGS": ("gauss (G) [CGS]",)},
            "Magnetic field (H)": {"SI": ("ampere/meter (A m⁻¹) [SI]",), "CGS": ("oersted (Oe) [CGS]",)},
            "Magnetization (M)": {"SI": ("ampere/meter (A m⁻¹)",), "CGS": ("emu cm⁻³ [CGS]",)},
            "Magnetic polarization (J)": {"SI": ("tesla (T) [SI]",), "CGS": ("emu/cm³ [CGS]",)},
            "Magnetic moment (m)": {"SI": ("ampere·meter² (A m²)",), "CGS": ("emu (G cm³)",)},
            "Magnetic moment per unit mass (σ)": {"SI": ("ampere·meter² kg⁻¹ (A m² kg⁻¹)",), "CGS": ("emu g⁻¹ [CGS]",)},
            "Volume magnetic susceptibility (κ = M/H)": {"SI": ("dimensionless [SI]",), "CGS": ("dimensionless [CGS]",)},
            "Mass magnetic susceptibility (χ = κ/ρ)": {"SI": ("m³ kg⁻¹",), "CGS": ("emu Oe⁻¹ g⁻¹",)},
            "Molar magnetic susceptibility (χₘ = χM*)": {"SI": ("m³ mol⁻¹",), "CGS": ("emu Oe⁻¹ g⁻¹ mol⁻¹",)},
            "Magnetic permeability (μ = B/H)": {"SI": ("henry/meter (H m⁻¹)",), "CGS": ("G Oe⁻¹",)},
            "Magnetic flux (Φ)": {"SI": ("weber (Wb)",), "CGS": ("maxwell (Mx)",)},
            "Magnetic scalar potential; Magnetomotive force (φ)": {"SI": ("ampere (A) [SI]",), "CGS": ("gilbert [CGS]",)},
            "Magnetic vector potential": {"SI": ("weber/meter (Wb m⁻¹)",), "CGS": ("emu (G cm)",)},
            "Magnetic pole strength (p)": {"SI": ("ampere·meter (A m)",), "CGS": ("emu (G cm²)",)},
            "Demagnetizing factor (N)": {"SI": ("dimensionless [SI]",), "CGS": ("dimensionless [CGS]",)},
            "Magnetostriction constant (λ)": {"SI": ("dimensionless [SI]",), "CGS": ("dimensionless [CGS]",)},
            "Anisotropy constant (K, K₁, Kᵤ)": {"SI": ("joule/m³ (J m⁻³)",), "CGS": ("erg/cm³",)},
            "Magnetostatic energy (Eₘ)": {"SI": ("joule/m³ (J m⁻³)",), "CGS": ("erg/cm³",)},
            "Energy product (BH)ₘₐₓ": {"SI": ("joule/m³ (J m⁻³)",), "CGS": ("erg/cm³",)},
            "Length": {"SI": ("meter (m)",), "CGS": ("centimeter (cm)",)},
            "Mass": {"SI": ("kilogram (kg)",), "CGS": ("gram (g)",)},
            "Time": {"SI": ("second (s)",), "CGS": ("second (s)",)},
            "Area": {"SI": ("square meter (m²)",), "CGS": ("square centimeter (cm²)",)},
            "Volume": {"SI": ("cubic meter (m³)",), "CGS": ("cubic centimeter (cm³)",)},
            "Velocity": {"SI": ("meter/second (m/s)",), "CGS": ("centimeter/second (cm/s)",)},
            "Acceleration": {"SI": ("meter/second² (m/s²)",), "CGS": ("centimeter/second² (cm/s²)",)},
            "Force": {"SI": ("newton (N)",), "CGS": ("dyne (dyn)",)},
            "Energy": {"SI": ("joule (J)",), "CGS": ("erg",)},
            "Power": {"SI": ("watt (W)",), "CGS": ("erg/second (erg/s)",)},
            "Pressure": {"SI": ("pascal (Pa)",), "CGS": ("dyne/cm²",)},
            "Density": {"SI": ("kilogram/m³ (kg/m³)",), "CGS": ("gram/cm³ (g/cm³)",)},
            "Dynamic Viscosity": {"SI": ("pascal-second (Pa·s)",), "CGS": ("poise (P)",)},
        }

        choices = canonical_pairs.get(category_name, {}).get(system, ())
        for choice in choices:
            if choice in unit_list:
                return choice

        # Fallback for explicitly tagged units in any future/additional category.
        tag = f"[{system}]"
        for u in unit_list:
            if tag in u.upper():
                return u

        return None

    def _show_conversion(target_system):
        target_unit = _find_system_unit(units, target_system, category)
        if target_unit is None:
            st.warning(f"{target_system} unit is not available for this quantity.")
            return
        try:
            result = convert_value(value, category, from_unit, target_unit)
            st.session_state["last_conversion"] = {
                "value": value,
                "from_unit": from_unit,
                "result": result,
                "to_unit": target_unit,
            }
        except Exception as e:
            st.error(f"Conversion error: {e}")

    cgs_col, si_col = st.columns(2, gap="small")
    with cgs_col:
        if st.button("CGS", key="convert_cgs", use_container_width=True):
            _show_conversion("CGS")
    with si_col:
        if st.button("SI", key="convert_si", use_container_width=True):
            _show_conversion("SI")

    last = st.session_state.get("last_conversion")
    if last:
        st.markdown(
            f"""<div class=\"result-card\">
                <div class=\"result-label\">✨ Conversion Result</div>
                <div class=\"result-number\">{fmt(last['result'])}</div>
                <div class=\"result-unit\">{last['to_unit']}</div>
            </div>""",
            unsafe_allow_html=True
        )
        st.caption(
            f"{fmt(last['value'])} {last['from_unit']} → "
            f"{fmt(last['result'])} {last['to_unit']}"
        )



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

    # Fundamental Constants
    st.markdown("""
    <div class="panel">
        <h2>📐 Fundamental Constants</h2>
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


    # ============================================================
    # 🧲 MAGNETIC QUANTITIES — SI / CGS
    # ============================================================

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
        width=800,
        hide_index=True,
        height=520
    )



    # ============================================================
    # 📖 CLICKABLE MAGNETISM FORMULA CHAPTERS
    # ============================================================
    # Every formula is a real Streamlit button. On mobile/desktop it
    # opens a modal chapter window (st.dialog) instead of navigating
    # away from the Formula Sheet.
    #
    # Core chapters are written at MSc Physics / Materials /
    # Nanotechnology / Spintronics level. Other entries use the same
    # structured chapter layout and can be expanded later without
    # changing the UI.
    # ============================================================

    CORE_FORMULA_DETAILS = {
        "Magnetic induction / Magnetic flux density": {
            "overview": (
                "Magnetic induction B is the magnetic flux density inside a "
                "medium. It is the field quantity that directly enters the "
                "Lorentz force and magnetic flux. In SI, B is measured in tesla."
            ),
            "meaning": (
                "For a material, B is not determined by the externally applied "
                "field alone because the material develops magnetization M. "
                "The SI constitutive relation is B = μ₀(H + M)."
            ),
            "derivation": (
                "Starting from magnetization M as magnetic dipole moment per "
                "unit volume, the total magnetic response is represented by "
                "H + M. Multiplication by μ₀ converts this field-like quantity "
                "to magnetic induction B."
            ),
            "msc": (
                "In magnetic materials, B-H curves, permeability, saturation "
                "and hysteresis are central characterization tools. In thin "
                "films and spintronic devices, B determines the Zeeman energy "
                "and the magnetic torque acting on a magnetic moment."
            ),
            "spin": (
                "B couples directly to a magnetic moment through U = −m·B and "
                "τ = m×B. This makes B fundamental for magnetization switching, "
                "FMR, spin dynamics and magnetic sensing."
            ),
        },
        "Magnetic field strength": {
            "overview": (
                "Magnetic field strength H describes the externally supplied "
                "magnetizing field, separated from the material magnetization. "
                "Its SI unit is A m⁻¹."
            ),
            "meaning": (
                "In matter, B and H are distinct: B = μ₀(H + M). Therefore "
                "H represents the applied/current-generated part while M "
                "describes the material response."
            ),
            "derivation": (
                "Rearranging B = μ₀(H + M) gives H = B/μ₀ − M. For a vacuum, "
                "M = 0, so B = μ₀H."
            ),
            "msc": (
                "H is used in hysteresis loops, permeability measurements, "
                "demagnetizing-field calculations and magnetic material "
                "characterization. In ferromagnets, internal H must be "
                "distinguished from the applied H because of demagnetization."
            ),
            "spin": (
                "H is the natural control variable in many magnetization "
                "switching and FMR experiments. It sets the effective field "
                "that enters the Landau–Lifshitz–Gilbert equation."
            ),
        },
        "Magnetization": {
            "overview": (
                "Magnetization M is magnetic dipole moment per unit volume. "
                "It describes how strongly a material is magnetized."
            ),
            "meaning": (
                "M is a vector quantity. Its direction gives the net magnetic "
                "moment direction and its magnitude gives magnetic moment "
                "density."
            ),
            "derivation": (
                "For a sample with total magnetic moment m and volume V, "
                "M = m/V. For a uniformly magnetized sample this relation "
                "directly gives the macroscopic magnetization."
            ),
            "msc": (
                "M is used to describe diamagnetism, paramagnetism and "
                "ferromagnetism, including saturation magnetization, remanence, "
                "coercivity and hysteresis."
            ),
            "spin": (
                "Spintronic devices use magnetization as an information-bearing "
                "state. Mₛ, magnetic anisotropy and damping strongly influence "
                "STT/SOT switching, MRAM, spin valves and magnetic tunnel junctions."
            ),
        },
        "Magnetic polarization": {
            "overview": (
                "Magnetic polarization J is related to the magnetization by "
                "J = μ₀M in SI. It has the same dimensions as magnetic induction."
            ),
            "meaning": (
                "J isolates the material contribution to B. Using "
                "B = μ₀H + J, the total induction can be viewed as the sum of "
                "the applied-field contribution and material polarization."
            ),
            "derivation": (
                "Starting from B = μ₀(H + M), distribute μ₀: "
                "B = μ₀H + μ₀M. Defining J = μ₀M gives B = μ₀H + J."
            ),
            "msc": (
                "J is useful when comparing material magnetic response with "
                "the applied field, especially in magnetic characterization."
            ),
            "spin": (
                "Although spintronic literature commonly uses M and B, the "
                "J representation is useful for separating material response "
                "from the applied-field contribution."
            ),
        },
        "Magnetic susceptibility": {
            "overview": (
                "Magnetic susceptibility χ measures the linear response of "
                "magnetization to an applied magnetic field."
            ),
            "meaning": (
                "For a linear isotropic material, M = χH. The sign and magnitude "
                "of χ help distinguish diamagnetic, paramagnetic and strongly "
                "magnetic responses."
            ),
            "derivation": (
                "For small fields in the linear regime, the ratio M/H is "
                "approximately constant. Hence χ = M/H. Outside the linear "
                "regime, χ can depend on field and history."
            ),
            "msc": (
                "χ is central to magnetic characterization, Curie and "
                "Curie–Weiss analysis, magnetic phase transitions and "
                "magnetometry."
            ),
            "spin": (
                "Magnetic susceptibility is important for understanding "
                "paramagnetic moments, exchange interactions, magnetic ordering "
                "and dynamic magnetic response in spintronic materials."
            ),
        },
        "Relative permeability": {
            "overview": (
                "Relative permeability μᵣ compares a material's permeability "
                "with vacuum permeability."
            ),
            "meaning": (
                "μᵣ = μ/μ₀. For a linear isotropic SI medium, μ = μ₀(1 + χ), "
                "so μᵣ = 1 + χ."
            ),
            "derivation": (
                "Using B = μ₀(H + M) and M = χH gives "
                "B = μ₀(1 + χ)H. Comparing this with B = μH gives "
                "μᵣ = μ/μ₀ = 1 + χ."
            ),
            "msc": (
                "Permeability describes how readily a material supports magnetic "
                "flux and is useful in magnetic cores, shielding and material "
                "characterization."
            ),
            "spin": (
                "In spin dynamics, the effective magnetic response influences "
                "resonance conditions and the field distribution around magnetic "
                "layers."
            ),
        },
        "Absolute permeability": {
            "overview": (
                "Absolute permeability μ connects magnetic induction B with "
                "magnetic field H in a linear medium."
            ),
            "meaning": (
                "For a linear isotropic medium, B = μH. The value depends on "
                "the material and, in nonlinear magnetic materials, can depend "
                "on field and magnetic history."
            ),
            "derivation": (
                "From B = μ₀(H + M), if M = χH then B = μ₀(1 + χ)H. "
                "Therefore μ = μ₀(1 + χ) = μ₀μᵣ."
            ),
            "msc": (
                "μ is used in magnetic material characterization, inductors, "
                "transformers and electromagnetic boundary problems."
            ),
            "spin": (
                "Magnetic permeability enters microwave magnetic response and "
                "can influence FMR and spin-wave propagation in magnetic media."
            ),
        },
        "Vacuum permeability": {
            "overview": (
                "μ₀ is the vacuum permeability and is the proportionality "
                "constant connecting B and H in vacuum."
            ),
            "meaning": (
                "In vacuum M = 0, so B = μ₀H. It also appears throughout "
                "magnetostatics, inductance, magnetic energy and spin dynamics."
            ),
            "derivation": (
                "For vacuum, the constitutive relation reduces to B = μ₀H. "
                "The numerical SI value is approximately 1.25663706 × 10⁻⁶ H m⁻¹."
            ),
            "msc": (
                "μ₀ is required in Biot–Savart law, Ampere's law, dipole energy, "
                "inductance, magnetic energy density and anisotropy-field formulas."
            ),
            "spin": (
                "Spintronic quantities such as Hₖ = 2Kᵤ/(μ₀Mₛ) explicitly "
                "contain μ₀, linking material anisotropy to switching fields."
            ),
        },
        "Magnetic dipole moment": {
            "overview": (
                "The magnetic dipole moment m characterizes the strength and "
                "direction of a magnetic dipole. For a current loop, m = IA."
            ),
            "meaning": (
                "m is a vector normal to the loop according to the right-hand "
                "rule. Its interaction with B produces torque and potential energy."
            ),
            "derivation": (
                "For a planar current loop of area A carrying current I, the "
                "magnetic dipole moment is defined as m = IA."
            ),
            "msc": (
                "Atomic and molecular magnetic moments arise from orbital and "
                "spin angular momentum. Macroscopic magnetization is the moment "
                "density M = m/V."
            ),
            "spin": (
                "Spin angular momentum produces magnetic moments that form the "
                "basis of ferromagnetism, spin polarization, spin transfer and "
                "magnetic memory."
            ),
        },
        "Torque on magnetic dipole": {
            "overview": (
                "A magnetic dipole in a magnetic field experiences a torque "
                "that tends to align its magnetic moment with the field."
            ),
            "meaning": (
                "The vector relation is τ = m × B, with magnitude "
                "|τ| = mB sinθ."
            ),
            "derivation": (
                "Opposite forces on the two sides of a small current loop form "
                "a couple. Their net force is zero in a uniform field, but their "
                "moments produce τ = m × B."
            ),
            "msc": (
                "This torque explains alignment, magnetic resonance and the "
                "precessional motion of magnetic moments."
            ),
            "spin": (
                "The field torque is one of the central terms in the "
                "Landau–Lifshitz–Gilbert equation. It drives precession of "
                "magnetization and underlies FMR and switching physics."
            ),
        },
        "Potential energy of magnetic dipole": {
            "overview": (
                "The potential energy of a magnetic dipole in a field is "
                "U = −m·B = −mB cosθ."
            ),
            "meaning": (
                "The lowest-energy orientation is parallel alignment of m and B."
            ),
            "derivation": (
                "Because torque tends to rotate the dipole toward the field, "
                "integrating the rotational work gives U = −mB cosθ, with the "
                "chosen zero of energy at perpendicular orientation."
            ),
            "msc": (
                "This relation is used to understand magnetic alignment and "
                "Zeeman-type energy scales."
            ),
            "spin": (
                "The Zeeman interaction is fundamental to spin manipulation, "
                "magnetic resonance and the energetics of spin-polarized states."
            ),
        },
        "Force on magnetic dipole": {
            "overview": (
                "A magnetic dipole experiences a net translational force when "
                "the magnetic field is spatially non-uniform."
            ),
            "meaning": (
                "For a localized dipole, F = ∇(m·B). In a uniform field the "
                "net force is zero, although torque can still be present."
            ),
            "derivation": (
                "The two poles/current elements experience slightly different "
                "forces when B varies in space. The imbalance gives the gradient "
                "of the dipole-field interaction energy."
            ),
            "msc": (
                "This principle is used in magnetic trapping, sorting, "
                "magnetic-force microscopy and gradient-field measurements."
            ),
            "spin": (
                "Magnetic-field gradients can influence domain walls, textures "
                "and nanoscale magnetic elements."
            ),
        },
        "Ampere's circuital law": {
            "overview": (
                "Ampere's circuital law relates the circulation of magnetic field "
                "around a closed path to the enclosed current."
            ),
            "meaning": (
                "For steady currents, ∮B·dl = μ₀I_enclosed."
            ),
            "derivation": (
                "For a long straight current, the cylindrical symmetry makes B "
                "constant on a circular Amperian path, giving B(2πr)=μ₀I."
            ),
            "msc": (
                "It is especially powerful for wires, solenoids and toroids where "
                "symmetry makes the field calculation simple."
            ),
            "spin": (
                "Current-generated magnetic fields are used to control magnetic "
                "layers and generate Oersted fields in spintronic structures."
            ),
        },
        "Lorentz magnetic force": {
            "overview": (
                "The magnetic part of the Lorentz force on a charge is "
                "F = q(v × B)."
            ),
            "meaning": (
                "The force is perpendicular to both velocity and magnetic field, "
                "so a uniform magnetic field changes the direction of motion "
                "without doing work on an isolated charge."
            ),
            "derivation": (
                "For v perpendicular to B, the magnitude is F=qvB and circular "
                "motion follows from qvB = mv²/r."
            ),
            "msc": (
                "The Lorentz force is fundamental to charged-particle motion, "
                "Hall effects, magnetotransport and electromagnetic devices."
            ),
            "spin": (
                "Spintronic transport is often discussed together with ordinary "
                "charge transport, Hall effects and spin-dependent forces."
            ),
        },
        "Faraday's law": {
            "overview": (
                "Faraday's law states that changing magnetic flux induces an "
                "electromotive force."
            ),
            "meaning": (
                "ε = −dΦ/dt. The negative sign expresses Lenz's law: the induced "
                "response opposes the change in flux."
            ),
            "derivation": (
                "For N turns, ε = −N dΦ/dt. The result follows from the "
                "electromagnetic induction law and is one of Maxwell's equations."
            ),
            "msc": (
                "It is essential for transformers, inductors, generators and "
                "electromagnetic coupling."
            ),
            "spin": (
                "Time-dependent magnetic fields can induce electric signals in "
                "magnetic/spintronic structures and are important in spin pumping "
                "and dynamic magnetic measurements."
            ),
        },
        "Self inductance": {
            "overview": (
                "Self-inductance L measures the magnetic flux linkage produced "
                "by a circuit's own current."
            ),
            "meaning": (
                "For a linear inductor, λ = LI and the induced emf is "
                "ε = −L dI/dt."
            ),
            "derivation": (
                "Flux linkage is proportional to current in the linear regime. "
                "The proportionality constant is L."
            ),
            "msc": (
                "Inductance stores magnetic energy and is important in circuits, "
                "filters and electromagnetic devices."
            ),
            "spin": (
                "Inductive coupling and dynamic magnetic fields are relevant to "
                "microwave magnetic measurements and spin-dynamics experiments."
            ),
        },
        "Magnetic energy density": {
            "overview": (
                "Magnetic energy density gives the energy stored per unit volume "
                "in a magnetic field."
            ),
            "meaning": (
                "For vacuum, u = B²/(2μ₀). In a linear material, the corresponding "
                "expression is u = B²/(2μ)."
            ),
            "derivation": (
                "The energy supplied to build the field is integrated from the "
                "field-current relation, producing the quadratic dependence on B "
                "for a linear medium."
            ),
            "msc": (
                "Energy density is essential for comparing magnetic states, "
                "actuator performance and field-storage capability."
            ),
            "spin": (
                "Spintronic switching competes between Zeeman, anisotropy, "
                "exchange and demagnetizing energies. Energy density therefore "
                "helps determine stable magnetic states."
            ),
        },
        "Gauss's law for magnetism": {
            "overview": (
                "Gauss's law for magnetism states ∇·B = 0."
            ),
            "meaning": (
                "Magnetic field lines form closed loops; in classical "
                "electromagnetism there are no isolated magnetic monopoles."
            ),
            "derivation": (
                "The differential form corresponds to the integral relation "
                "∮B·dA = 0 over any closed surface."
            ),
            "msc": (
                "It is one of Maxwell's equations and constrains magnetic-field "
                "boundary conditions."
            ),
            "spin": (
                "Magnetic textures such as domains and skyrmions must satisfy "
                "the divergence-free condition for B even though their M texture "
                "can be highly non-uniform."
            ),
        },
        "Magnetization relation": {
            "overview": (
                "In a linear magnetic material, magnetization is proportional "
                "to magnetic field: M = χH."
            ),
            "meaning": (
                "χ is the magnetic susceptibility. The relation is valid in the "
                "linear-response regime."
            ),
            "derivation": (
                "Substitute M = χH into B = μ₀(H+M) to obtain "
                "B = μ₀(1+χ)H."
            ),
            "msc": (
                "This is the starting point for susceptibility measurements and "
                "the classification of magnetic materials."
            ),
            "spin": (
                "Linear response provides the basic framework for magnetic "
                "resonance, dynamic susceptibility and spin-wave response."
            ),
        },
        "Using susceptibility": {
            "overview": (
                "For a linear isotropic material, susceptibility converts the "
                "magnetic field H into magnetization M."
            ),
            "meaning": (
                "With M=χH, the induction becomes B=μ₀(1+χ)H."
            ),
            "derivation": (
                "Insert the linear constitutive relation M=χH into the material "
                "relation B=μ₀(H+M)."
            ),
            "msc": (
                "This relation connects measurable susceptibility with "
                "permeability and magnetic induction."
            ),
            "spin": (
                "It provides the static limit from which more advanced dynamic "
                "magnetic-response models are developed."
            ),
        },
        "Curie's law": {
            "overview": (
                "Curie's law describes ideal paramagnetic susceptibility as "
                "χ = C/T."
            ),
            "meaning": (
                "As temperature rises, thermal agitation makes magnetic moments "
                "harder to align, reducing susceptibility."
            ),
            "derivation": (
                "In the weak-field limit of the classical paramagnetic model, "
                "the leading response is inversely proportional to temperature."
            ),
            "msc": (
                "Curie's law is used to analyze paramagnets and estimate magnetic "
                "moment information from susceptibility measurements."
            ),
            "spin": (
                "It provides a simple starting point for understanding local "
                "moments before exchange interactions and collective ordering "
                "are included."
            ),
        },
        "Curie–Weiss law": {
            "overview": (
                "The Curie–Weiss law is χ = C/(T−θ), extending Curie's law by "
                "including an effective molecular-field interaction."
            ),
            "meaning": (
                "The Weiss temperature θ provides information about the tendency "
                "toward ferromagnetic or antiferromagnetic correlations."
            ),
            "derivation": (
                "A molecular field proportional to M is added to the applied "
                "field. Solving the resulting linear-response relation gives "
                "the Curie–Weiss form."
            ),
            "msc": (
                "It is widely used to estimate ordering scales and effective "
                "magnetic moments from experimental susceptibility."
            ),
            "spin": (
                "Exchange-driven collective ordering is the microscopic basis "
                "for many ferromagnetic, antiferromagnetic and spintronic materials."
            ),
        },
        "Effective magnetic moment": {
            "overview": (
                "The effective magnetic moment summarizes the magnetic moment "
                "deduced from susceptibility data."
            ),
            "meaning": (
                "It is especially useful for paramagnetic ions where spin and "
                "orbital contributions determine the observed response."
            ),
            "derivation": (
                "The exact expression depends on the unit convention and the "
                "model used for Curie or Curie–Weiss susceptibility."
            ),
            "msc": (
                "Comparing measured and theoretical effective moments helps "
                "identify oxidation states, spin states and magnetic interactions."
            ),
            "spin": (
                "Effective moments provide a bridge between microscopic spin "
                "states and macroscopic magnetic susceptibility."
            ),
        },
        "Bohr magneton": {
            "overview": (
                "The Bohr magneton μB is the natural magnetic-moment scale "
                "associated with an electron."
            ),
            "meaning": (
                "It sets the scale for electron orbital and spin magnetic moments."
            ),
            "derivation": (
                "The scale follows from the electron charge, reduced Planck "
                "constant and electron mass."
            ),
            "msc": (
                "Magnetic moments are commonly reported in units of μB when "
                "discussing atoms, ions and magnetic materials."
            ),
            "spin": (
                "Spin-polarized electrons, local magnetic moments and exchange "
                "interactions in spintronic materials are naturally expressed "
                "using μB."
            ),
        },
        "Spontaneous magnetization": {
            "overview": (
                "Spontaneous magnetization is the non-zero magnetization that "
                "can exist below a magnetic ordering temperature even without "
                "an externally applied field."
            ),
            "meaning": (
                "It arises from collective interactions between microscopic "
                "magnetic moments."
            ),
            "derivation": (
                "Mean-field and microscopic exchange models can produce a stable "
                "ordered state below the Curie temperature."
            ),
            "msc": (
                "It is a defining feature of ferromagnetism and is observed "
                "through magnetization curves and hysteresis."
            ),
            "spin": (
                "Stable spontaneous magnetization provides the two-state or "
                "multi-state magnetic basis used in spin valves, MRAM and other "
                "spintronic elements."
            ),
        },
        "Exchange interaction": {
            "overview": (
                "Exchange interaction is a quantum-mechanical interaction between "
                "spins arising from the combination of Coulomb interaction and "
                "wavefunction antisymmetry."
            ),
            "meaning": (
                "A simplified Heisenberg form is H_ex = −J Σ S_i·S_j, with the "
                "sign of J determining the preferred relative spin orientation "
                "under the chosen convention."
            ),
            "derivation": (
                "Exchange is not simply a classical magnetic dipole interaction; "
                "it originates from quantum statistics and electronic overlap."
            ),
            "msc": (
                "Exchange determines ferromagnetism, antiferromagnetism, "
                "ferrimagnetism and many magnetic phase transitions."
            ),
            "spin": (
                "Exchange is one of the most important spintronic energy scales. "
                "It controls spin stiffness, domain walls, spin waves and magnetic "
                "ordering in ultrathin films and multilayers."
            ),
        },
        "Saturation magnetization": {
            "overview": (
                "Saturation magnetization Mₛ is the maximum magnetization reached "
                "when the magnetic moments are essentially aligned with the field."
            ),
            "meaning": (
                "It reflects the density and magnitude of magnetic moments in the "
                "material."
            ),
            "derivation": (
                "In a simple moment model, Mₛ = nμ, where n is the number density "
                "of magnetic moments and μ is the moment per magnetic unit."
            ),
            "msc": (
                "Mₛ is extracted from hysteresis loops and enters the definitions "
                "of anisotropy field, exchange length and magnetic energy scales."
            ),
            "spin": (
                "Mₛ directly affects spin-wave frequency, damping dynamics, "
                "switching current and the torque efficiency in spintronic devices."
            ),
        },
        "Remanence / Retentivity": {
            "overview": (
                "Remanence is the residual magnetization or induction remaining "
                "after the external magnetizing field is removed."
            ),
            "meaning": (
                "It measures how strongly a material retains a magnetic state."
            ),
            "derivation": (
                "On a hysteresis loop, the value at H=0 after prior magnetization "
                "defines the remanent state."
            ),
            "msc": (
                "High remanence is useful in permanent magnets, while controlled "
                "remanence is important in magnetic memory."
            ),
            "spin": (
                "Non-volatile spintronic memory requires stable magnetic states, "
                "so remanence is closely connected to retention."
            ),
        },
        "Coercive field": {
            "overview": (
                "The coercive field Hc is the reverse magnetic field required "
                "to bring the magnetization or induction to a specified zero "
                "condition on a hysteresis loop."
            ),
            "meaning": (
                "It is a measure of magnetic resistance to reversal."
            ),
            "derivation": (
                "Read H at the point where the hysteresis curve crosses the "
                "chosen zero-magnetization or zero-induction reference."
            ),
            "msc": (
                "Coercivity depends on anisotropy, defects, domain-wall pinning, "
                "grain size and microstructure."
            ),
            "spin": (
                "Device switching must overcome magnetic energy barriers related "
                "to anisotropy and coercivity while maintaining adequate retention."
            ),
        },
        "Hysteresis loss per unit volume": {
            "overview": (
                "The hysteresis-loss density is the energy dissipated per cycle "
                "of magnetization reversal."
            ),
            "meaning": (
                "For a B-H loop, the enclosed area represents energy loss per "
                "unit volume: W_h = ∮H dB."
            ),
            "derivation": (
                "Magnetic work per unit volume is H dB. Integrating around a "
                "complete cycle gives the net dissipated energy."
            ),
            "msc": (
                "Hysteresis loss is important in magnetic cores and also provides "
                "a quantitative measure of dissipation during magnetic cycling."
            ),
            "spin": (
                "In nanoscale magnetic devices, energy dissipation during "
                "switching is a key design constraint for low-power spintronics."
            ),
        },
        "Domain wall energy": {
            "overview": (
                "Domain-wall energy is the energy per unit area associated with "
                "the transition region between differently magnetized domains."
            ),
            "meaning": (
                "Exchange favors smooth magnetization while anisotropy favors "
                "alignment along easy axes; their competition creates a finite "
                "wall width and energy."
            ),
            "derivation": (
                "For a simple 180° wall, a common approximation is "
                "γ ≈ 4√(AK), where A is exchange stiffness and K is anisotropy."
            ),
            "msc": (
                "Domain-wall energy determines domain size, wall stability and "
                "pinning behavior."
            ),
            "spin": (
                "Domain walls are information carriers in racetrack memory and "
                "their energy controls current-driven wall motion."
            ),
        },
        "Domain wall width": {
            "overview": (
                "Domain-wall width is the characteristic distance over which "
                "magnetization rotates between domains."
            ),
            "meaning": (
                "A simple 180° Bloch-wall model gives δ ≈ π√(A/K)."
            ),
            "derivation": (
                "Exchange stiffness A penalizes rapid spatial rotation, while "
                "anisotropy K favors the easy axis. Minimizing the total energy "
                "gives the square-root scaling."
            ),
            "msc": (
                "Wall width depends on material parameters and is strongly "
                "affected by geometry, interfaces and competing anisotropies."
            ),
            "spin": (
                "Narrow domain walls are important for high-density magnetic "
                "textures, racetrack devices and current-driven switching."
            ),
        },
        "Uniaxial anisotropy energy": {
            "overview": (
                "Uniaxial anisotropy describes the energy preference for "
                "magnetization to align with a particular easy axis."
            ),
            "meaning": (
                "For first-order uniaxial anisotropy, E_a = K_u sin²θ."
            ),
            "derivation": (
                "The angular dependence follows from symmetry: the lowest-order "
                "term invariant under reversal of the easy axis is proportional "
                "to sin²θ."
            ),
            "msc": (
                "Anisotropy controls easy-axis direction, coercivity, domain "
                "structure and thermal stability."
            ),
            "spin": (
                "Magnetic anisotropy is central to STT/SOT switching, MRAM "
                "retention and perpendicular magnetic anisotropy in thin films."
            ),
        },
        "Anisotropy field": {
            "overview": (
                "The anisotropy field is the characteristic field scale needed "
                "to overcome uniaxial anisotropy."
            ),
            "meaning": (
                "For the simple uniaxial approximation, H_k = 2K_u/(μ₀Mₛ)."
            ),
            "derivation": (
                "Equate the field torque/energy scale associated with MₛH "
                "to the anisotropy energy scale K_u, yielding the characteristic "
                "factor 2 in the simple model."
            ),
            "msc": (
                "H_k is obtained from magnetic characterization and is closely "
                "related to the stability and switching field of a magnetic layer."
            ),
            "spin": (
                "H_k is one of the key parameters in LLG simulations and "
                "spin-torque switching calculations."
            ),
        },
        "Demagnetizing field": {
            "overview": (
                "The demagnetizing field is the internal field produced by "
                "magnetic poles associated with a finite magnetized body."
            ),
            "meaning": (
                "For a simple uniformly magnetized geometry, H_d = −NM in SI "
                "with a geometry-dependent demagnetizing factor N."
            ),
            "derivation": (
                "Surface magnetic charges create a field opposing the component "
                "of magnetization that produces them."
            ),
            "msc": (
                "Demagnetization strongly affects hysteresis, shape anisotropy, "
                "thin-film magnetism and magnetic-domain formation."
            ),
            "spin": (
                "Shape anisotropy and demagnetizing fields determine preferred "
                "magnetization directions in nanomagnets and spintronic layers."
            ),
        },
        "Internal magnetic field": {
            "overview": (
                "The internal magnetic field is the effective field experienced "
                "inside a finite magnetic body after accounting for demagnetization."
            ),
            "meaning": (
                "A simple relation is H_int = H_appl − NM."
            ),
            "derivation": (
                "The demagnetizing field opposes magnetization, so it is subtracted "
                "from the externally applied field."
            ),
            "msc": (
                "Using internal rather than applied field is essential for "
                "interpreting magnetic measurements of finite samples."
            ),
            "spin": (
                "The effective internal field enters magnetization dynamics and "
                "changes resonance and switching conditions in nanomagnets."
            ),
        },
        "Magnetostriction": {
            "overview": (
                "Magnetostriction is the relative change in a material's length "
                "caused by magnetization."
            ),
            "meaning": (
                "The simplest definition is λ = ΔL/L."
            ),
            "derivation": (
                "Magnetization changes the equilibrium lattice strain through "
                "magnetoelastic coupling."
            ),
            "msc": (
                "Magnetostriction links magnetic and mechanical degrees of "
                "freedom and is important in sensors and actuators."
            ),
            "spin": (
                "Magnetoelastic coupling can modify anisotropy, damping and "
                "spin-wave behavior in thin films and heterostructures."
            ),
        },
    }

    def _generic_formula_chapter(term, symbol, formula, description):
        """Structured chapter for formula entries without a custom note."""
        return {
            "overview": (
                f"{term} is an important relation in magnetism. The displayed "
                f"formula is {formula}. It gives a compact mathematical link "
                f"between the physical quantities represented by the symbols."
            ),
            "meaning": (
                f"The symbol used for this relation is {symbol}. "
                f"{description}. Always keep the vector/scalar nature and unit "
                f"convention of each quantity consistent."
            ),
            "derivation": (
                "Use the defining relation of the physical quantity and the "
                "appropriate Maxwell, constitutive, energy, force or material "
                "model relation. The exact derivation depends on the assumptions "
                "stated with the formula, such as uniform fields, linear response, "
                "steady current or a simple material model."
            ),
            "msc": (
                "At MSc Physics / Materials Science level, this relation should "
                "be connected to the assumptions behind it, its limiting cases, "
                "units, measurable quantities and experimental interpretation."
            ),
            "spin": (
                "For spintronics, the relation can be connected to magnetic "
                "moments, magnetization dynamics, transport, magnetic energy, "
                "anisotropy, spin waves or device operation depending on the "
                "physical system."
            ),
        }

    @st.dialog("📖 Formula Chapter", width="large")
    def _open_formula_chapter(term, symbol, formula, description):
        detail = CORE_FORMULA_DETAILS.get(
            term,
            _generic_formula_chapter(term, symbol, formula, description)
        )

        st.markdown(
            f'<div style="font-size:25px;font-weight:800;margin-bottom:4px;">'
            f'{term}</div>',
            unsafe_allow_html=True
        )
        st.caption(f"Symbol: {symbol}  •  {description}")

        st.latex(formula)

        sections = [
            ("1. Concept & overview", detail["overview"]),
            ("2. Physical meaning", detail["meaning"]),
            ("3. Derivation / reasoning", detail["derivation"]),
            ("4. MSc Physics / Materials Science", detail["msc"]),
            ("5. Spintronics connection", detail["spin"]),
        ]

        for heading, body in sections:
            st.markdown(f"### {heading}")
            st.write(body)

        st.markdown("---")
        st.markdown("### Quick study points")
        st.markdown(
            "- Identify every symbol and its SI unit.\n"
            "- Check the assumptions before applying the relation.\n"
            "- Distinguish applied, internal and material-response fields where relevant.\n"
            "- For magnetic materials, connect the formula with M, B, H, χ, μ, anisotropy and energy.\n"
            "- For spintronics, look for its role in magnetization dynamics, switching, transport or magnetic stability."
        )


    # ============================================================
    # 📖 BOOK-STYLE FORMULA DISPLAY
    # ============================================================

    st.markdown("""
    <div class="panel">
        <h3>📖 Magnetism Formula Sheet</h3>
        <p>Important magnetic formulas and relations.</p>
    </div>
    """, unsafe_allow_html=True)

    for idx, (term, symbol, formula, description) in enumerate(MAGNETISM_FORMULA_TABLE):

        # Click the chapter title/card to open the detailed formula window.
        if st.button(
            f"📖  {term}",
            key=f"formula_chapter_{idx}",
            use_container_width=True
        ):
            _open_formula_chapter(term, symbol, formula, description)

        st.markdown(
            f"""
            <div style="
                margin:-7px 0 16px 0;
                padding:10px 16px 14px 16px;
                border-bottom:1px solid rgba(128,128,128,0.20);
            ">
                <div style="
                    color:#93c5fd;
                    font-size:14px;
                    margin-bottom:6px;
                ">
                    Symbol: {symbol}
                </div>
                <div style="
                    color:#94a3b8;
                    font-size:13px;
                ">
                    {description}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.latex(formula)
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
