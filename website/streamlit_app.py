import streamlit as st
import pickle
import numpy as np
import streamlit.components.v1 as components


# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Laptop Price Predictor",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    #MainMenu, footer, header { visibility: hidden; }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }

    /* ── Sidebar: always visible, locked open ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(160deg, #0f0f0f 0%, #1a1a2e 50%, #16213e 100%);
        border-right: 1px solid rgba(255,255,255,0.07);
        min-width: 320px !important;
        max-width: 320px !important;
        transform: translateX(0) !important;
        visibility: visible !important;
    }

    /* Keep sidebar visible even when aria-expanded is false */
    [data-testid="stSidebar"][aria-expanded="false"] {
        margin-left: 0 !important;
        transform: translateX(0) !important;
        min-width: 320px !important;
    }

    /* Hide the collapse arrow button */
    [data-testid="stSidebarCollapseButton"],
    button[kind="header"] {
        display: none !important;
    }

    [data-testid="stSidebar"] * {
        color: #e8e8f0 !important;
    }

    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stNumberInput label,
    [data-testid="stSidebar"] .stCheckbox label {
        font-size: 0.78rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        color: #9494b8 !important;
    }

    [data-testid="stSidebar"] .stSelectbox > div > div {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 8px !important;
        color: #e8e8f0 !important;
    }

    [data-testid="stSidebar"] .stSelectbox > div > div:hover {
        border-color: rgba(99, 179, 237, 0.5) !important;
    }

    [data-testid="stSidebar"] input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 8px !important;
        color: #e8e8f0 !important;
    }

    [data-testid="stSidebar"] .stCheckbox {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px;
        padding: 10px 14px !important;
        margin-bottom: 6px;
    }

    /* ── Main area ── */
    .main .block-container {
        padding-left: 2rem !important;
    }

    .main-hero {
        background: linear-gradient(135deg, #f0f4ff 0%, #fafbff 100%);
        border-radius: 20px;
        padding: 3rem 3.5rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(99, 102, 241, 0.1);
        box-shadow: 0 4px 40px rgba(99, 102, 241, 0.06);
    }

    .hero-label {
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #6366f1;
        margin-bottom: 0.5rem;
    }

    .hero-title {
        font-family: 'DM Serif Display', serif;
        font-size: 2.8rem;
        line-height: 1.15;
        color: #0f0f1a;
        margin-bottom: 0.8rem;
    }

    .hero-sub {
        font-size: 1rem;
        color: #6b7280;
        font-weight: 300;
        line-height: 1.6;
        max-width: 520px;
    }

    /* ── Summary cards ── */
    .summary-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 14px;
        margin-bottom: 2rem;
    }

    .summary-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        box-shadow: 0 1px 8px rgba(0,0,0,0.04);
    }

    .summary-card .card-label {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #9ca3af;
        margin-bottom: 0.3rem;
    }

    .summary-card .card-value {
        font-size: 1.05rem;
        font-weight: 600;
        color: #111827;
    }

    /* ── Predict button ── */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.85rem 2rem !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.03em !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.35) !important;
        margin-top: 1rem;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.45) !important;
    }

    .stButton > button:active {
        transform: translateY(0px) !important;
    }

    /* ── Result card ── */
    .result-card {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a3e 100%);
        border-radius: 20px;
        padding: 2.5rem 3rem;
        text-align: center;
        border: 1px solid rgba(99, 102, 241, 0.25);
        box-shadow: 0 8px 50px rgba(99, 102, 241, 0.15);
        margin-top: 1.5rem;
    }

    .result-label {
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #818cf8;
        margin-bottom: 0.5rem;
    }

    .result-price {
        font-family: 'DM Serif Display', serif;
        font-size: 3.2rem;
        color: #ffffff;
        line-height: 1.1;
        margin-bottom: 0.4rem;
    }

    .result-currency {
        font-size: 0.85rem;
        color: #6b7280;
        font-weight: 400;
    }

    /* ── Sidebar section headers ── */
    .sidebar-section {
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #6366f1 !important;
        padding: 1rem 0 0.4rem 0;
        border-top: 1px solid rgba(255,255,255,0.06);
        margin-top: 0.5rem;
    }

    /* ── Spec badge row ── */
    .badge-row {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 1.5rem;
    }

    .badge {
        background: #f0f4ff;
        border: 1px solid #c7d2fe;
        border-radius: 20px;
        padding: 5px 13px;
        font-size: 0.78rem;
        font-weight: 500;
        color: #4338ca;
    }

    /* ── Info tip box ── */
    .tip-box {
        background: #fffbeb;
        border-left: 3px solid #f59e0b;
        border-radius: 0 10px 10px 0;
        padding: 0.8rem 1rem;
        font-size: 0.82rem;
        color: #78350f;
        margin-top: 1.5rem;
        line-height: 1.5;
    }

    hr.styled {
        border: none;
        border-top: 1px solid #e5e7eb;
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ── JS: open sidebar ONCE on load only — no MutationObserver ─────────────────
# The MutationObserver approach was blocking dropdown interactions because
# it fired forceOpen() on every DOM change (including dropdown menu opens),
# which stole focus and prevented option selection.
# Solution: run a simple one-shot delayed check instead.
components.html("""
<script>
    function openSidebar() {
        const sidebar = window.parent.document
            .querySelector('[data-testid="stSidebar"]');
        if (!sidebar) return;

        /* Force inline styles to keep it visible */
        sidebar.style.transform  = 'translateX(0)';
        sidebar.style.minWidth   = '320px';
        sidebar.style.visibility = 'visible';

        /* If collapsed state, click open */
        if (sidebar.getAttribute('aria-expanded') === 'false') {
            const btn = window.parent.document
                .querySelector('[data-testid="stSidebarCollapseButton"]');
            if (btn) btn.click();
        }
    }

    /* Run at 300ms and 1000ms after load — enough to catch late renders
       without hooking into every DOM mutation */
    setTimeout(openSidebar, 300);
    setTimeout(openSidebar, 1000);
</script>
""", height=0)


# ── Load model ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    with open('model/predictor.pickle', 'rb') as f:
        return pickle.load(f)

try:
    model = load_model()
    model_loaded = True
except FileNotFoundError:
    model_loaded = False


# ══════════════════════════════════════════════════════════════
#  SIDEBAR  —  all user inputs live here
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="padding: 1.4rem 0 1rem 0;">
        <div style="font-size:0.65rem; font-weight:700; letter-spacing:0.14em;
                    text-transform:uppercase; color:#6366f1; margin-bottom:4px;">
            Configuration Panel
        </div>
        <div style="font-family:'DM Serif Display',serif; font-size:1.35rem;
                    color:#ffffff; line-height:1.2;">
            Laptop Specs
        </div>
        <div style="font-size:0.78rem; color:#6b7280; margin-top:6px; font-weight:300;">
            Fill in the details to get an instant price estimate.
        </div>
    </div>
    """, unsafe_allow_html=True)

    predict_btn = st.button("⚡  Predict Price", use_container_width=True)

    # ── Hardware ──────────────────────────────────────────────
    st.markdown('<div class="sidebar-section">⚙️ &nbsp; Hardware</div>',
                unsafe_allow_html=True)

    ram = st.selectbox(
        "RAM",
        options=[4, 8, 16, 32, 64],
        index=1,
        format_func=lambda x: f"{x} GB",
    )

    weight = st.number_input(
        "Weight (kg)",
        min_value=0.5, max_value=5.0,
        value=1.5, step=0.1,
        format="%.1f",
        help="Laptop weight in kilograms"
    )

    col_tc, col_ips = st.columns(2)
    with col_tc:
        touchscreen = st.checkbox("Touch Screen", value=False)
    with col_ips:
        ips = st.checkbox("IPS Display", value=False)

    # ── Brand & Type ──────────────────────────────────────────
    st.markdown('<div class="sidebar-section">🏷️ &nbsp; Brand & Type</div>',
                unsafe_allow_html=True)

    company_display = {
        "Acer": "acer", "Apple": "apple", "Asus": "asus",
        "Dell": "dell", "HP": "hp", "Lenovo": "lenovo",
        "MSI": "msi", "Toshiba": "toshiba", "Other": "other",
    }
    company_label = st.selectbox("Brand", list(company_display.keys()), index=5)
    company = company_display[company_label]

    typename_display = {
        "2-in-1 Convertible": "2in1convertible",
        "Gaming":             "gaming",
        "Netbook":            "netbook",
        "Notebook":           "notebook",
        "Ultrabook":          "ultrabook",
        "Workstation":        "workstation",
    }
    typename_label = st.selectbox("Type", list(typename_display.keys()), index=3)
    typename = typename_display[typename_label]

    # ── Software ──────────────────────────────────────────────
    st.markdown('<div class="sidebar-section">🖥️ &nbsp; Software</div>',
                unsafe_allow_html=True)

    opsys_display = {
        "Windows": "windows", "macOS": "mac",
        "Linux":   "linux",   "Other": "other",
    }
    opsys_label = st.selectbox("Operating System", list(opsys_display.keys()))
    opsys = opsys_display[opsys_label]

    # ── Processor & GPU ───────────────────────────────────────
    st.markdown('<div class="sidebar-section">🔬 &nbsp; Processor & Graphics</div>',
                unsafe_allow_html=True)

    cpu_display = {
        "Intel Core i3": "intelcorei3",
        "Intel Core i5": "intelcorei5",
        "Intel Core i7": "intelcorei7",
        "AMD":           "amd",
        "Other":         "other",
    }
    cpu_label = st.selectbox("CPU", list(cpu_display.keys()), index=1)
    cpu = cpu_display[cpu_label]

    gpu_display = {
        "Intel":  "intel",
        "AMD":    "amd",
        "Nvidia": "nvidia",
    }
    gpu_label = st.selectbox("GPU", list(gpu_display.keys()), index=2)
    gpu = gpu_display[gpu_label]


# ══════════════════════════════════════════════════════════════
#  MAIN AREA
# ══════════════════════════════════════════════════════════════

st.markdown(f"""
<div class="main-hero">
    <div class="hero-label">AI-Powered Estimator</div>
    <div class="hero-title">Laptop Price<br>Predictor</div>
    <div class="hero-sub">
        Configure your desired laptop specifications in the sidebar
        and get an instant machine-learning price estimate in Sri Lankan Rupees.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="summary-grid">
    <div class="summary-card">
        <div class="card-label">Brand</div>
        <div class="card-value">{company_label}</div>
    </div>
    <div class="summary-card">
        <div class="card-label">Type</div>
        <div class="card-value">{typename_label}</div>
    </div>
    <div class="summary-card">
        <div class="card-label">RAM</div>
        <div class="card-value">{ram} GB</div>
    </div>
    <div class="summary-card">
        <div class="card-label">Weight</div>
        <div class="card-value">{weight:.1f} kg</div>
    </div>
    <div class="summary-card">
        <div class="card-label">CPU</div>
        <div class="card-value">{cpu_label}</div>
    </div>
    <div class="summary-card">
        <div class="card-label">GPU</div>
        <div class="card-value">{gpu_label}</div>
    </div>
</div>
""", unsafe_allow_html=True)

features = []
if touchscreen: features.append("Touch Screen")
if ips:         features.append("IPS Display")
features.append(opsys_label)

badges_html = "".join(f'<span class="badge">{f}</span>' for f in features)
st.markdown(f'<div class="badge-row">{badges_html}</div>', unsafe_allow_html=True)

st.markdown('<hr class="styled">', unsafe_allow_html=True)


# ── Prediction logic ──────────────────────────────────────────────────────────
if predict_btn:
    if not model_loaded:
        st.error("⚠️ Model file not found at `model/predictor.pickle`. "
                 "Please check the path and try again.")
    else:
        def one_hot(options, value):
            return [1 if opt == value else 0 for opt in options]

        feature_list = (
            [int(ram), float(weight),
             1 if touchscreen else 0,
             1 if ips else 0]
            + one_hot(['acer','apple','asus','dell','hp','lenovo','msi','other','toshiba'], company)
            + one_hot(['2in1convertible','gaming','netbook','notebook','ultrabook','workstation'], typename)
            + one_hot(['linux','mac','other','windows'], opsys)
            + one_hot(['amd','intelcorei3','intelcorei5','intelcorei7','other'], cpu)
            + one_hot(['amd','intel','nvidia'], gpu)
        )

        pred  = model.predict([feature_list])
        price = np.round(pred[0], 2) * 221

        st.markdown(f"""
        <div id="result-section" class="result-card">
            <div class="result-label">Estimated Market Price</div>
            <div class="result-price">LKR {price:,.0f}</div>
            <div class="result-currency">Sri Lankan Rupees &nbsp;·&nbsp;
                {company_label} {typename_label} &nbsp;·&nbsp; {ram} GB RAM
            </div>
        </div>
        """, unsafe_allow_html=True)

        components.html("""
            <script>
                window.parent.document
                    .getElementById('result-section')
                    .scrollIntoView({ behavior: 'smooth', block: 'center' });
            </script>
        """, height=0)

else:
    st.markdown("""
    <div style="text-align:center; padding: 3rem 2rem; color:#9ca3af;">
        <div style="font-size:3rem; margin-bottom:1rem;">💻</div>
        <div style="font-size:1rem; font-weight:500; color:#374151; margin-bottom:0.4rem;">
            Ready to estimate
        </div>
        <div style="font-size:0.85rem; font-weight:300; line-height:1.6;">
            Set your laptop specs in the sidebar,<br>then hit <strong>Predict Price</strong>.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="tip-box">
    💡 <strong>Tip:</strong> Prices are estimated based on historical laptop data
    and converted to LKR. Actual retail prices may vary based on market conditions,
    taxes, and availability.
</div>
""", unsafe_allow_html=True)
