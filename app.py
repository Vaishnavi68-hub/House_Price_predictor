import streamlit as st
import joblib
import numpy as np
import base64


def set_bg(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(f"""
    <style>

    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        filter: blur(8px);
        opacity: 0.65;
        z-index: -1;
    }}

    .stApp {{
        background: transparent !important;
    }}

    .title {{
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        color: white;
        margin-bottom: 5px;
    }}

    .subtitle {{
        text-align: center;
        color: white;
        font-weight: 700;
        margin-bottom: 25px;
    }}

    /* SIMPLE LABEL STYLE (NO BOX) */
    .label {{
        font-size: 15px;
        font-weight: 800;
        color: white;
        margin-top: 14px;
        margin-bottom: 6px;
    }}

    /* INPUT STYLE ONLY */
    div[data-baseweb="select"],
    div[data-baseweb="input"],
    div[data-baseweb="base-input"],
    div[data-testid="stNumberInputContainer"] {{
        background-color: #F5F0E1 !important;
        border-radius: 10px !important;
        border: 2px solid #5D4037 !important;
    }}

    input {{
        color: #3E2723 !important;
        font-weight: 600 !important;
    }}

    .stSelectbox span {{
        color: #3E2723 !important;
        font-weight: 600 !important;
    }}

    div[role="listbox"],
    ul[role="listbox"],
    li[role="option"] {{
        background-color: #F5F0E1 !important;
        color: #3E2723 !important;
        font-weight: 600 !important;
    }}

    div.stButton > button {{
        background-color: #5D4037;
        color: white;
        font-weight: 800;
        font-size: 18px;
        padding: 12px;
        border-radius: 10px;
        width: 100%;
        border: 2px solid #3E2723;
    }}

    div.stButton > button:hover {{
        background-color: #3E2723;
    }}

    .result {{
        margin-top: 25px;
        font-size: 26px;
        font-weight: 900;
        color: #ffffff;
        background-color: rgba(62, 39, 35, 0.95);
        padding: 18px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.25);
    }}

    </style>
    """, unsafe_allow_html=True)


set_bg("background.jpg")

model = joblib.load("house_model.pkl")

st.markdown("<div class='title'>🏠 House Price Predictor</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Simple AI Real Estate Estimator</div>", unsafe_allow_html=True)


mszoning_map = {
    "RL (Low density residential area)": 1,
    "RM (Medium density residential area)": 2,
    "FV (Floating village area)": 3,
    "RH (High density residential area)": 4,
    "C (Commercial area)": 5
}

lotconfig_map = {
    "Inside plot (normal)": 1,
    "Front road 2 sides": 2,
    "Corner plot": 3,
    "Cul-de-sac (dead end)": 4,
    "Front road 3 sides": 5
}

bldg_map = {
    "Single family house": 1,
    "Two family house": 2,
    "Duplex house": 3,
    "Townhouse end unit": 4,
    "Townhouse inside unit": 5
}

ms_subclass_map = {
    "Normal 1-floor house": 20,
    "Old 1-floor house": 30,
    "1-floor house with attic": 40,
    "Small house (1.5 floors)": 45,
    "Medium house (1.5 floors)": 50,
    "Modern 2-floor house": 60,
    "Old 2-floor house": 70,
    "Large multi-level house": 75,
    "Split-level house": 80,
    "Split entrance house": 85,
    "Two-family house (duplex)": 90,
    "Small apartment house": 120,
    "Medium apartment house": 150,
    "Large apartment house": 160,
    "Low-rise apartment building": 180,
    "Multi-family apartment building": 190
}

st.markdown("<div class='label'>House Type</div>", unsafe_allow_html=True)
selected_ms = st.selectbox("", list(ms_subclass_map.keys()))
MSSubClass = ms_subclass_map[selected_ms]

st.markdown("<div class='label'>MSZoning (Area / location type)</div>", unsafe_allow_html=True)
selected_mszoning = st.selectbox("", list(mszoning_map.keys()))
MSZoning = mszoning_map[selected_mszoning]

st.markdown("<div class='label'>Lot Area (Land size in sq ft)</div>", unsafe_allow_html=True)
LotArea = st.number_input("", min_value=0)

st.markdown("<div class='label'>Lot Configuration</div>", unsafe_allow_html=True)
selected_lotconfig = st.selectbox("", list(lotconfig_map.keys()))
LotConfig = lotconfig_map[selected_lotconfig]

st.markdown("<div class='label'>Building Type</div>", unsafe_allow_html=True)
selected_bldg = st.selectbox("", list(bldg_map.keys()))
BldgType = bldg_map[selected_bldg]

st.markdown("<div class='label'>Overall Condition (1–10)</div>", unsafe_allow_html=True)
OverallCond = st.slider("", 1, 10, 5)

st.markdown("<div class='label'>Year Built</div>", unsafe_allow_html=True)
YearBuilt = st.selectbox("", list(range(1900, 2026)))


if st.button("Predict Price 🚀"):

    input_data = np.array([[
        MSSubClass,
        MSZoning,
        LotArea,
        LotConfig,
        BldgType,
        OverallCond,
        YearBuilt
    ]])

    prediction = model.predict(input_data)

    st.markdown(
        f"<div class='result'>💰 Predicted Price: ₹ {prediction[0]:,.2f}</div>",
        unsafe_allow_html=True
    )