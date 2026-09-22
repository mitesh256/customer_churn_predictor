import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="ChurnSight — Customer Intelligence",
    page_icon="◎",
    layout="wide"
)

# ── Premium CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0C1220;
    color: #E8EDF5;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 2rem 2.5rem; max-width: 1200px; }

/* App header */
.app-header {
    display: flex;
    align-items: center;
    gap: 10px;
    padding-bottom: 20px;
    border-bottom: 1px solid #1E2D45;
    margin-bottom: 28px;
}
.logo-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    background: #4F8EF7;
    display: inline-block;
}
.app-title {
    font-family: 'DM Serif Display', Georgia, serif;
    font-size: 1.4rem;
    font-weight: 400;
    color: #E8EDF5;
    margin: 0;
}
.app-subtitle {
    font-size: 0.72rem;
    color: #5A6A82;
    font-weight: 500;
    letter-spacing: 0.05em;
    margin-left: 4px;
}

/* Section labels */
.section-label {
    font-size: 0.68rem;
    font-weight: 600;
    color: #5A6A82;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 12px;
    margin-top: 20px;
}

/* Override Streamlit selectbox and inputs */
div[data-baseweb="select"] > div {
    background-color: #131C2E !important;
    border: 1px solid #1E2D45 !important;
    border-radius: 10px !important;
    color: #E8EDF5 !important;
}
div[data-baseweb="select"] > div:focus-within {
    border-color: #4F8EF7 !important;
}
input[type="number"] {
    background-color: #131C2E !important;
    border: 1px solid #1E2D45 !important;
    border-radius: 10px !important;
    color: #E8EDF5 !important;
}
.stSlider > div > div > div {
    background: #4F8EF7 !important;
}

/* Labels */
label, .stSelectbox label, .stSlider label, .stNumberInput label {
    color: #5A6A82 !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
}

/* Predict button */
.stButton > button {
    width: 100%;
    background: #4F8EF7 !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 14px !important;
    margin-top: 20px !important;
    transition: opacity 0.15s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* Result cards */
.verdict-churn {
    background: rgba(247, 79, 106, 0.08);
    border: 1px solid rgba(247, 79, 106, 0.25);
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 20px;
}
.verdict-stay {
    background: rgba(61, 214, 140, 0.08);
    border: 1px solid rgba(61, 214, 140, 0.25);
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 20px;
}
.verdict-tag-churn {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #F74F6A;
    margin-bottom: 8px;
}
.verdict-tag-stay {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #3DD68C;
    margin-bottom: 8px;
}
.verdict-headline-churn {
    font-family: 'DM Serif Display', Georgia, serif;
    font-size: 1.7rem;
    color: #F8A0AF;
    margin-bottom: 8px;
    line-height: 1.2;
}
.verdict-headline-stay {
    font-family: 'DM Serif Display', Georgia, serif;
    font-size: 1.7rem;
    color: #7AE8B8;
    margin-bottom: 8px;
    line-height: 1.2;
}
.verdict-sub {
    font-size: 0.82rem;
    color: #5A6A82;
    line-height: 1.6;
}
.metric-box {
    background: #131C2E;
    border: 1px solid #1E2D45;
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 10px;
}
.metric-box .m-label {
    font-size: 0.67rem;
    color: #5A6A82;
    font-weight: 500;
    margin-bottom: 4px;
    letter-spacing: 0.04em;
}
.metric-box .m-value {
    font-size: 1.1rem;
    font-weight: 600;
    color: #E8EDF5;
}
.m-value-high { color: #F74F6A !important; }
.m-value-medium { color: #F7A84F !important; }
.m-value-low { color: #3DD68C !important; }

/* Divider */
.custom-divider {
    border: none;
    border-top: 1px solid #1E2D45;
    margin: 20px 0;
}

/* Prob bar */
.prob-track {
    background: #1E2D45;
    border-radius: 99px;
    height: 6px;
    margin-top: 8px;
    overflow: hidden;
}
.prob-fill-churn {
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, #F74F6A, #F7A84F);
}
.prob-fill-stay {
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, #4F8EF7, #3DD68C);
}
</style>
""", unsafe_allow_html=True)

# ── Header ──
st.markdown("""
<div class="app-header">
    <span class="logo-dot"></span>
    <span class="app-title">ChurnSight</span>
    <span class="app-subtitle">Customer Intelligence</span>
</div>
""", unsafe_allow_html=True)

# ── Layout: Form (left) + Results (right) ──
form_col, result_col = st.columns([1.1, 1], gap="large")

with form_col:
    st.markdown('<div class="section-label">Customer Profile</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        gender    = st.selectbox("Gender", ["Female", "Male"])
        partner   = st.selectbox("Partner", ["No", "Yes"])
    with c2:
        senior    = st.selectbox("Senior Citizen", ["No", "Yes"])
        dependents = st.selectbox("Dependents", ["No", "Yes"])

    tenure = st.slider("Tenure (months)", 0, 72, 12)

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Services</div>', unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        phone_service    = st.selectbox("Phone Service", ["No", "Yes"])
        internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
        online_backup    = st.selectbox("Online Backup", ["No", "Yes", "No internet service"])
        tech_support     = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])
        streaming_movies = st.selectbox("Streaming Movies", ["No", "Yes", "No internet service"])
    with c4:
        multiple_lines   = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])
        online_security  = st.selectbox("Online Security", ["No", "Yes", "No internet service"])
        device_protection = st.selectbox("Device Protection", ["No", "Yes", "No internet service"])
        streaming_tv     = st.selectbox("Streaming TV", ["No", "Yes", "No internet service"])

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Billing</div>', unsafe_allow_html=True)

    c5, c6 = st.columns(2)
    with c5:
        contract         = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
        paperless        = st.selectbox("Paperless Billing", ["No", "Yes"])
    with c6:
        payment          = st.selectbox("Payment Method", [
            "Electronic check", "Mailed check",
            "Bank transfer (automatic)", "Credit card (automatic)"
        ])

    c7, c8 = st.columns(2)
    with c7:
        monthly  = st.number_input("Monthly Charges ($)", 0.0, 200.0, 65.0, 0.5)
    with c8:
        total    = st.number_input("Total Charges ($)", 0.0, 10000.0, 500.0, 10.0)

    predict_clicked = st.button("Analyze Customer", type="primary")

# ── Helper functions ──
def b(val): return 1 if val == "Yes" else 0

def payload():
    return {
        "gender":          b(gender),
        "SeniorCitizen":   b(senior),
        "Partner":         b(partner),
        "Dependents":      b(dependents),
        "tenure":          tenure,
        "PhoneService":    b(phone_service),
        "PaperlessBilling":b(paperless),
        "MonthlyCharges":  monthly,
        "TotalCharges":    total,

        "MultipleLines_No_phone_service": 1 if multiple_lines == "No phone service" else 0,
        "MultipleLines_Yes":              1 if multiple_lines == "Yes" else 0,

        "InternetService_Fiber_optic": 1 if internet_service == "Fiber optic" else 0,
        "InternetService_No":          1 if internet_service == "No" else 0,

        "OnlineSecurity_No_internet_service": 1 if online_security == "No internet service" else 0,
        "OnlineSecurity_Yes":                 1 if online_security == "Yes" else 0,

        "OnlineBackup_No_internet_service": 1 if online_backup == "No internet service" else 0,
        "OnlineBackup_Yes":                 1 if online_backup == "Yes" else 0,

        "DeviceProtection_No_internet_service": 1 if device_protection == "No internet service" else 0,
        "DeviceProtection_Yes":                 1 if device_protection == "Yes" else 0,

        "TechSupport_No_internet_service": 1 if tech_support == "No internet service" else 0,
        "TechSupport_Yes":                 1 if tech_support == "Yes" else 0,

        "StreamingTV_No_internet_service": 1 if streaming_tv == "No internet service" else 0,
        "StreamingTV_Yes":                 1 if streaming_tv == "Yes" else 0,

        "StreamingMovies_No_internet_service": 1 if streaming_movies == "No internet service" else 0,
        "StreamingMovies_Yes":                 1 if streaming_movies == "Yes" else 0,

        "Contract_One_year": 1 if contract == "One year" else 0,
        "Contract_Two_year": 1 if contract == "Two year" else 0,

        "PaymentMethod_Credit_card_automatic": 1 if payment == "Credit card (automatic)" else 0,
        "PaymentMethod_Electronic_check":      1 if payment == "Electronic check" else 0,
        "PaymentMethod_Mailed_check":          1 if payment == "Mailed check" else 0,
    }

# ── Results ──
with result_col:
    if not predict_clicked:
        st.markdown("""
        <div style="height:60px"></div>
        <div style="text-align:center; color:#5A6A82; padding: 60px 20px;">
            <div style="font-size:2.5rem; opacity:0.3; margin-bottom:16px;">◎</div>
            <p style="font-size:0.88rem; line-height:1.7; max-width:260px; margin:0 auto;">
                Fill in the customer details and click Analyze to see the churn prediction.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        try:
            with st.spinner("Analyzing..."):
                res = requests.post(f"{API_URL}/predict", json=payload())

            if res.status_code == 200:
                data = res.json()
                prob     = data['churn_probability']
                is_churn = data['churn_prediction'] == 1
                risk     = data['risk_level']
                pct      = int(prob * 100)

                # Confidence
                conf = "High" if prob > 0.8 or prob < 0.2 else \
                       "Moderate" if prob > 0.6 or prob < 0.4 else "Low"

                if is_churn:
                    st.markdown(f"""
                    <div class="verdict-churn">
                        <div class="verdict-tag-churn">Churn Risk Detected</div>
                        <div class="verdict-headline-churn">This customer is likely to leave.</div>
                        <div class="verdict-sub">Consider a targeted retention offer — discounts, contract upgrades, or support outreach may help.</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="verdict-stay">
                        <div class="verdict-tag-stay">Customer Retained</div>
                        <div class="verdict-headline-stay">This customer is likely to stay.</div>
                        <div class="verdict-sub">Retention looks stable. Continue monitoring engagement and service satisfaction.</div>
                    </div>
                    """, unsafe_allow_html=True)

                # Probability bar
                fill_class = "prob-fill-churn" if is_churn else "prob-fill-stay"
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                    <span style="font-size:0.75rem; color:#5A6A82; font-weight:500;">Churn Probability</span>
                    <span style="font-size:1rem; font-weight:600; color:#E8EDF5;">{pct}%</span>
                </div>
                <div class="prob-track">
                    <div class="{fill_class}" style="width:{pct}%"></div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

                # Metric boxes
                risk_class = f"m-value-{risk.lower()}"
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.markdown(f"""
                    <div class="metric-box">
                        <div class="m-label">Risk Level</div>
                        <div class="m-value {risk_class}">{risk}</div>
                    </div>""", unsafe_allow_html=True)
                with m2:
                    st.markdown(f"""
                    <div class="metric-box">
                        <div class="m-label">Prediction</div>
                        <div class="m-value">{"Churn" if is_churn else "Stay"}</div>
                    </div>""", unsafe_allow_html=True)
                with m3:
                    st.markdown(f"""
                    <div class="metric-box">
                        <div class="m-label">Confidence</div>
                        <div class="m-value">{conf}</div>
                    </div>""", unsafe_allow_html=True)

            else:
                st.error(f"API Error {res.status_code}: {res.text}")

        except requests.exceptions.ConnectionError:
            st.error("FastAPI server nahi chal raha. Pehle `uvicorn api:app --reload` chalao.")