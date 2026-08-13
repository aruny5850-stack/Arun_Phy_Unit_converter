import streamlit as st
import math
import pandas as pd

st.set_page_config(page_title="Ar_PHYHBTU",page_icon="⚗️",layout="wide")
'\n<style>\n.stApp{background:radial-gradient(circle at 15% 5%,#10254b22,transparent 30%),linear-gradient(135deg,#050914,#090d1c,#070b18);color:#f4f7ff}\n.block-container{max-width:1100px;padding-top:2rem}\n.hero,.card,.result{background:linear-gradient(145deg,#11182ce8,#0a1020e8);border:1px solid #8190b52e;border-radius:22px;box-shadow:0 14px 40px #0003}\n.hero{padding:28px 32px;margin-bottom:18px}.card{padding:22px;margin:14px 0}\n.title{font-size:44px;font-weight:800}.title span{background:linear-gradient(90deg,#55c7ff,#795cff);-webkit-background-clip:text;-webkit-text-fill-color:transparent}\n.sub{color:#c7d0e6;margin-top:7px}.desc{color:#8e9bb8;margin-top:5px}\n.section{color:#66b8ff;font-size:18px;font-weight:800;letter-spacing:.7px;margin-bottom:12px}\n.stSelectbox div[data-baseweb=select]>div,.stNumberInput input,.stTextInput input{background:#1f2335!important;color:#fff!important;border-radius:12px!important;border:1px solid #788cb52e!important;min-height:48px}\n.stSelectbox div[data-baseweb=select] span{color:#fff!important}\n.stButton>button{width:100%;height:55px;border:0!important;border-radius:15px!important;color:white!important;font-weight:800!important;background:linear-gradient(90deg,#13b9e7,#345de8,#783be8)!important}\n.result{padding:25px;text-align:center;margin-top:16px}.rlabel{color:#62b4ff;font-size:18px;font-weight:800;text-align:left}.rval{font-size:48px;font-weight:800;margin-top:18px}.runit{color:#5f7dff;font-size:21px;font-weight:800}.line{margin-top:20px;padding-top:17px;border-top:1px solid #9aa0be26;color:#d1d8e8;font-size:16px}\n@media(max-width:700px){.block-container{padding:1rem .7rem}.hero{padding:20px}.card{padding:17px}.title{font-size:31px}}\n</style>\n'
st.markdown('\n<style>\n.stApp{background:radial-gradient(circle at 15% 5%,#10254b22,transparent 30%),linear-gradient(135deg,#050914,#090d1c,#070b18);color:#f4f7ff}\n.block-container{max-width:1100px;padding-top:2rem}\n.hero,.card,.result{background:linear-gradient(145deg,#11182ce8,#0a1020e8);border:1px solid #8190b52e;border-radius:22px;box-shadow:0 14px 40px #0003}\n.hero{padding:28px 32px;margin-bottom:18px}.card{padding:22px;margin:14px 0}\n.title{font-size:44px;font-weight:800}.title span{background:linear-gradient(90deg,#55c7ff,#795cff);-webkit-background-clip:text;-webkit-text-fill-color:transparent}\n.sub{color:#c7d0e6;margin-top:7px}.desc{color:#8e9bb8;margin-top:5px}\n.section{color:#66b8ff;font-size:18px;font-weight:800;letter-spacing:.7px;margin-bottom:12px}\n.stSelectbox div[data-baseweb=select]>div,.stNumberInput input,.stTextInput input{background:#1f2335!important;color:#fff!important;border-radius:12px!important;border:1px solid #788cb52e!important;min-height:48px}\n.stSelectbox div[data-baseweb=select] span{color:#fff!important}\n.stButton>button{width:100%;height:55px;border:0!important;border-radius:15px!important;color:white!important;font-weight:800!important;background:linear-gradient(90deg,#13b9e7,#345de8,#783be8)!important}\n.result{padding:25px;text-align:center;margin-top:16px}.rlabel{color:#62b4ff;font-size:18px;font-weight:800;text-align:left}.rval{font-size:48px;font-weight:800;margin-top:18px}.runit{color:#5f7dff;font-size:21px;font-weight:800}.line{margin-top:20px;padding-top:17px;border-top:1px solid #9aa0be26;color:#d1d8e8;font-size:16px}\n@media(max-width:700px){.block-container{padding:1rem .7rem}.hero{padding:20px}.card{padding:17px}.title{font-size:31px}}\n</style>\n',unsafe_allow_html=True)

def fmt(x):
    if x==0:return "0"
    if 1e-4<=abs(x)<1e5:return f"{x:.3f}".rstrip("0").rstrip(".")
    return f"{x:.3e}".replace("e+0","e+").replace("e-0","e-")

U={
"Length":{"meter (m)":1,"kilometer (km)":1e3,"centimeter (cm)":1e-2,"millimeter (mm)":1e-3,"micrometer (µm)":1e-6,"nanometer (nm)":1e-9,"angstrom (Å)":1e-10,"picometer (pm)":1e-12,"inch (in)":.0254,"foot (ft)":.3048,"yard (yd)":.9144,"mile (mi)":1609.344},
"Area":{"square meter (m²)":1,"square centimeter (cm²)":1e-4,"square millimeter (mm²)":1e-6,"square kilometer (km²)":1e6,"square nanometer (nm²)":1e-18,"square angstrom (Å²)":1e-20},
"Volume":{"cubic meter (m³)":1,"liter (L)":1e-3,"milliliter (mL)":1e-6,"cubic centimeter (cm³)":1e-6,"cubic millimeter (mm³)":1e-9},
"Mass":{"kilogram (kg)":1,"gram (g)":1e-3,"milligram (mg)":1e-6,"microgram (µg)":1e-9,"tonne (t)":1e3},
"Time":{"second (s)":1,"millisecond (ms)":1e-3,"microsecond (µs)":1e-6,"nanosecond (ns)":1e-9,"minute (min)":60,"hour (h)":3600,"day (d)":86400},
"Temperature":{"kelvin (K)":"K","celsius (°C)":"C","fahrenheit (°F)":"F"},
"Frequency":{"hertz (Hz)":1,"kilohertz (kHz)":1e3,"megahertz (MHz)":1e6,"gigahertz (GHz)":1e9},
"Force":{"newton (N)":1,"dyne (dyn)":1e-5,"kilonewton (kN)":1e3},
"Energy":{"joule (J)":1,"erg":1e-7,"kilojoule (kJ)":1e3,"electron volt (eV)":1.602176634e-19,"calorie (cal)":4.184},
"Power":{"watt (W)":1,"kilowatt (kW)":1e3,"megawatt (MW)":1e6,"erg/s":1e-7,"horsepower (hp)":745.699872},
"Pressure":{"pascal (Pa)":1,"kilopascal (kPa)":1e3,"megapascal (MPa)":1e6,"bar":1e5,"atmosphere (atm)":101325,"dyne/cm²":.1},
"Velocity":{"meter/second (m/s)":1,"kilometer/hour (km/h)":1000/3600,"centimeter/second (cm/s)":1e-2,"mile/hour (mph)":1609.344/3600},
"Acceleration":{"meter/second² (m/s²)":1,"centimeter/second² (cm/s²)":1e-2,"standard gravity (g)":9.80665},
"Charge":{"coulomb (C)":1,"millicoulomb (mC)":1e-3,"microcoulomb (µC)":1e-6,"electron charge (e)":1.602176634e-19,"statcoulomb (statC)":3.33564095198152e-10},
"Voltage":{"volt (V)":1,"millivolt (mV)":1e-3,"kilovolt (kV)":1e3},
"Resistance":{"ohm (Ω)":1,"milliohm (mΩ)":1e-3,"kilohm (kΩ)":1e3,"megohm (MΩ)":1e6},
"Capacitance":{"farad (F)":1,"microfarad (µF)":1e-6,"nanofarad (nF)":1e-9,"picofarad (pF)":1e-12},
"Magnetic induction":{"tesla (T) [SI]":1,"gauss (G) [CGS]":1e-4,"millitesla (mT)":1e-3,"nanotesla (nT)":1e-9},
"Magnetic flux":{"weber (Wb) [SI]":1,"maxwell (Mx) [CGS]":1e-8}
}

mag=[
("Magnetic induction","B","tesla (T)","gauss (G)","1 T = 10⁴ G"),
("Magnetic field","H","A m⁻¹","oersted (Oe)","1 A m⁻¹ = 4π × 10⁻³ Oe"),
("Magnetization","M","A m⁻¹","emu cm⁻³","1 A m⁻¹ = 10⁻³ emu cm⁻³"),
("Magnetic polarization","J","T","G","1 T = 10⁴/4π emu cm⁻³"),
("Magnetic moment","m","A m²","emu = G cm³","1 A m² = 10³ emu"),
("Magnetic moment per unit mass","σ","A m² kg⁻¹","emu g⁻¹","1 A m² kg⁻¹ = 1 emu g⁻¹"),
("Volume magnetic susceptibility (κ = M/H)","κ","dimensionless","dimensionless","1 (SI) = 1/4π (CGS)"),
("Mass magnetic susceptibility (χ = κ/ρ)","χ","m³ kg⁻¹","emu Oe⁻¹ g⁻¹","1 m³ kg⁻¹ = 10³/4π emu Oe⁻¹ g⁻¹"),
("Molar magnetic susceptibility (χₘ = χM*)","χₘ","m³ mol⁻¹","emu Oe⁻¹ g⁻¹ mol⁻¹","1 m³ mol⁻¹ = 10⁶/4π emu Oe⁻¹ g⁻¹ mol⁻¹"),
("Magnetic permeability (μ = B/H)","μ","H m⁻¹","G Oe⁻¹","1 H m⁻¹ = 10⁷/4π G Oe⁻¹"),
("Magnetic flux","Φ","weber (Wb)","maxwell (Mx)","1 Wb = 10⁸ Mx"),
("Magnetic scalar potential; Magnetomotive force","φ","A","gilbert","1 A = 4π/10 gilbert"),
("Magnetic vector potential","A","Wb m⁻¹","emu = G cm","1 Wb m⁻¹ = 10⁶ emu"),
("Magnetic pole strength","p","A m","emu = G cm²","1 A m = 10 emu"),
("Demagnetizing factor","N","dimensionless","dimensionless","1 (SI) = 4π (CGS)"),
("Magnetostriction constant","λ","dimensionless","dimensionless","1 (SI) = 1 (CGS)"),
("Anisotropy constant","K, K₁, Kᵤ","J m⁻³","erg cm⁻³","1 J m⁻³ = 10 erg cm⁻³"),
("Magnetostatic energy","Eₘ","J m⁻³","erg cm⁻³","1 J m⁻³ = 10 erg cm⁻³"),
("Energy product","(BH)ₘₐₓ","J m⁻³","erg cm⁻³","1 J m⁻³ = 10 erg cm⁻³")
]

st.markdown('<div class="hero"><div class="title">⚗️ <span>Ar_PHYHBTU</span></div><div class="sub">Calculate • Convert • Explore</div><div class="desc">Physics utility app for students — SI, CGS, magnetic quantities and scientific calculations.</div></div>',unsafe_allow_html=True)

t1,t2,t3=st.tabs(["🔄 Unit Converter","🧮 Calculator","Σ Constants"])

with t1:
    st.markdown('<div class="card"><div style="font-size:30px;font-weight:800">🔄 Universal Unit Converter</div><div class="sub">Convert common physical quantities between SI/MKS, CGS and practical units.</div></div>',unsafe_allow_html=True)
    st.markdown('<div class="card"><div class="section">📚 PHYSICAL QUANTITY</div>',unsafe_allow_html=True)
    q=st.selectbox("Physical quantity",list(U),label_visibility="collapsed")
    st.markdown("</div>",unsafe_allow_html=True)
    units=list(U[q])

    # SAME BOX: value + from-unit dropdown
    st.markdown('<div class="card"><div class="section">🔢 ENTER VALUE &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 📤 FROM UNIT</div>',unsafe_allow_html=True)
    c1,c2=st.columns([1,1],gap="medium")
    with c1: value=st.number_input("Value",value=1.0,format="%.12g",label_visibility="collapsed")
    with c2: source=st.selectbox("From unit",units,label_visibility="collapsed")
    st.markdown("</div>",unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="section">📥 TO UNIT</div>',unsafe_allow_html=True)
    target=st.selectbox("To unit",units,label_visibility="collapsed")
    st.markdown("</div>",unsafe_allow_html=True)

    if st.button("⚡ CONVERT"):
        if q=="Temperature":
            if source=="celsius (°C)": k=value+273.15
            elif source=="fahrenheit (°F)": k=(value-32)*5/9+273.15
            else:k=value
            if target=="celsius (°C)": result=k-273.15
            elif target=="fahrenheit (°F)": result=(k-273.15)*9/5+32
            else:result=k
        else:
            result=value*U[q][source]/U[q][target]
        st.markdown(f'<div class="result"><div class="rlabel">✨ CONVERSION RESULT</div><div class="rval">{fmt(result)}</div><div class="runit">{target}</div><div class="line">{fmt(value)} {source} &nbsp; → &nbsp; {fmt(result)} {target}</div></div>',unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="section">🧲 MAGNETIC QUANTITIES — SI / CGS</div><div class="desc">Assignment reference table in the supplied serial order.</div></div>',unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(mag,columns=["Magnetic Term","Symbol","SI Unit","CGS Unit","Conversion Factor"]),use_container_width=True,hide_index=True)

with t2:
    st.markdown('<div class="card"><div style="font-size:30px;font-weight:800">🧮 Scientific Calculator</div><div class="sub">Basic arithmetic, powers and common scientific functions.</div></div>',unsafe_allow_html=True)
    exp=st.text_input("Expression",placeholder="Example: 2*(3+4), sin(pi/2), sqrt(25), 2**10")
    if st.button("🧮 CALCULATE"):
        try:
            safe={"sin":math.sin,"cos":math.cos,"tan":math.tan,"asin":math.asin,"acos":math.acos,"atan":math.atan,"sqrt":math.sqrt,"log":math.log,"log10":math.log10,"exp":math.exp,"pi":math.pi,"e":math.e,"abs":abs,"pow":pow}
            r=eval(exp,{"__builtins__":{}},safe)
            st.success("Result = "+fmt(float(r)))
        except: st.error("Invalid expression.")

with t3:
    st.markdown('<div class="card"><div style="font-size:30px;font-weight:800">Σ Physical Constants</div><div class="sub">Frequently used physics constants.</div></div>',unsafe_allow_html=True)
    constants={
    "Speed of light, c":"2.99792458 × 10⁸ m s⁻¹","Planck constant, h":"6.62607015 × 10⁻³⁴ J s",
    "Reduced Planck constant, ħ":"1.054571817 × 10⁻³⁴ J s","Elementary charge, e":"1.602176634 × 10⁻¹⁹ C",
    "Electron mass, mₑ":"9.1093837139 × 10⁻³¹ kg","Proton mass, mₚ":"1.67262192595 × 10⁻²⁷ kg",
    "Avogadro constant, Nₐ":"6.02214076 × 10²³ mol⁻¹","Boltzmann constant, k":"1.380649 × 10⁻²³ J K⁻¹",
    "Vacuum permittivity, ε₀":"8.8541878188 × 10⁻¹² F m⁻¹","Vacuum permeability, μ₀":"1.25663706212 × 10⁻⁶ H m⁻¹",
    "Standard gravity, g":"9.80665 m s⁻²","1 eV":"1.602176634 × 10⁻¹⁹ J"}
    st.dataframe(pd.DataFrame(list(constants.items()),columns=["Constant","Value"]),use_container_width=True,hide_index=True)

st.markdown('<div style="text-align:center;color:#66738f;font-size:12px;margin-top:30px">Ar_PHYHBTU • Physics Utility App</div>',unsafe_allow_html=True)
