st.markdown("""
<style>

/* ================================
   GLOBAL
================================ */

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(0, 210, 255, 0.12), transparent 30%),
        radial-gradient(circle at 90% 20%, rgba(120, 80, 255, 0.12), transparent 30%),
        linear-gradient(135deg, #050816 0%, #0b1020 45%, #111827 100%);
    color: #f8fafc;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* ================================
   SIDEBAR
================================ */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #070b18 0%,
            #0b1224 50%,
            #080c18 100%
        );

    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] > div {
    padding-top: 2rem;
}

section[data-testid="stSidebar"] h2 {
    color: #ffffff;
    font-weight: 700;
    letter-spacing: 0.5px;
}


/* ================================
   HERO HEADER
================================ */

.hero {
    position: relative;
    overflow: hidden;

    padding: 42px 45px;
    margin-bottom: 30px;

    border-radius: 28px;

    background:
        linear-gradient(
            135deg,
            rgba(14,165,233,0.22),
            rgba(99,102,241,0.20),
            rgba(168,85,247,0.18)
        );

    border: 1px solid rgba(255,255,255,0.12);

    box-shadow:
        0 20px 60px rgba(0,0,0,0.35),
        inset 0 1px 0 rgba(255,255,255,0.08);

    backdrop-filter: blur(20px);
}

.hero:before {
    content: "⚛";
    position: absolute;
    right: 45px;
    top: 5px;

    font-size: 150px;

    opacity: 0.08;

    transform: rotate(12deg);
}

.hero h1 {
    font-size: 48px;
    font-weight: 800;

    margin: 0;

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
    color: #b8c4d6;
    font-size: 17px;
    margin-top: 10px;
}


/* ================================
   MAIN CARD
================================ */

.card {
    padding: 28px;

    margin-bottom: 22px;

    border-radius: 24px;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.075),
            rgba(255,255,255,0.025)
        );

    border: 1px solid rgba(255,255,255,0.10);

    box-shadow:
        0 15px 40px rgba(0,0,0,0.25),
        inset 0 1px 0 rgba(255,255,255,0.05);

    backdrop-filter: blur(18px);
}

.card h2 {
    margin-top: 0;

    color: #ffffff;

    font-size: 25px;
    font-weight: 700;
}

.card p {
    color: #9caec4;
}


/* ================================
   INPUT BOX
================================ */

div[data-baseweb="input"] {
    background: rgba(255,255,255,0.06) !important;

    border: 1px solid rgba(255,255,255,0.10) !important;

    border-radius: 14px !important;

    transition: 0.25s ease;
}

div[data-baseweb="input"]:focus-within {
    border-color: #38bdf8 !important;

    box-shadow:
        0 0 0 2px rgba(56,189,248,0.15),
        0 0 20px rgba(56,189,248,0.10);
}

input {
    color: white !important;
}


/* ================================
   SELECTBOX
================================ */

div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.06) !important;

    border: 1px solid rgba(255,255,255,0.10) !important;

    border-radius: 14px !important;

    min-height: 48px;

    transition: 0.25s ease;
}

div[data-baseweb="select"] > div:hover {
    border-color: #38bdf8 !important;
}

div[data-baseweb="select"] span {
    color: #f8fafc !important;
}


/* ================================
   LABELS
================================ */

label {
    color: #cbd5e1 !important;

    font-weight: 600 !important;

    font-size: 14px !important;
}


/* ================================
   BUTTON
================================ */

.stButton > button {
    width: 100%;

    min-height: 52px;

    border: none !important;

    border-radius: 15px !important;

    background:
        linear-gradient(
            135deg,
            #06b6d4,
            #3b82f6,
            #7c3aed
        ) !important;

    color: white !important;

    font-size: 16px !important;

    font-weight: 700 !important;

    letter-spacing: 0.4px;

    box-shadow:
        0 8px 25px rgba(59,130,246,0.25);

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);

    box-shadow:
        0 12px 35px rgba(59,130,246,0.40);
}

.stButton > button:active {
    transform: scale(0.98);
}


/* ================================
   RESULT CARD
================================ */

.result {
    position: relative;

    overflow: hidden;

    padding: 35px;

    margin-top: 28px;

    border-radius: 25px;

    text-align: center;

    background:
        linear-gradient(
            135deg,
            rgba(6,182,212,0.18),
            rgba(37,99,235,0.18),
            rgba(124,58,237,0.20)
        );

    border: 1px solid rgba(96,165,250,0.25);

    box-shadow:
        0 15px 45px rgba(0,0,0,0.30);
}

.result:before {
    content: "✓";

    position: absolute;

    right: 25px;
    top: 15px;

    font-size: 55px;

    color: rgba(255,255,255,0.06);
}

.result p {
    color: #a5b4fc;

    font-size: 14px;

    text-transform: uppercase;

    letter-spacing: 2px;
}

.result h2 {
    color: white;

    font-size: 40px;

    font-weight: 800;

    margin: 10px 0;

    text-shadow:
        0 0 25px rgba(96,165,250,0.35);
}


/* ================================
   DIVIDER
================================ */

hr {
    border: none !important;

    height: 1px;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(255,255,255,0.15),
            transparent
        );
}


/* ================================
   METRIC / SMALL CARDS
================================ */

div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.045);

    padding: 18px;

    border-radius: 18px;

    border: 1px solid rgba(255,255,255,0.08);
}


/* ================================
   EXPANDER
================================ */

.streamlit-expanderHeader {
    background: rgba(255,255,255,0.04) !important;

    border-radius: 14px !important;

    color: white !important;
}


/* ================================
   ALERTS
================================ */

div[data-testid="stAlert"] {
    border-radius: 15px;
}


/* ================================
   FOOTER
================================ */

.footer {
    text-align: center;

    margin-top: 50px;

    padding: 20px;

    color: #64748b;

    font-size: 13px;
}


/* ================================
   MOBILE RESPONSIVE
================================ */

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

    .hero:before {
        font-size: 90px;
        right: 10px;
    }

    .card {
        padding: 20px;
    }

    .result h2 {
        font-size: 30px;
    }
}

</style>
""", unsafe_allow_html=True)
