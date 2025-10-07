import streamlit as st
from tabs.input_tab import show_input_tab
from tabs.prediction_tab import show_prediction_tab
from tabs.analytics_tab import show_analytics_tab
from tabs.advice_tab import show_advice_tab
from tabs.alerts_tab import show_alerts_tab


st.set_page_config(
    page_title="US Air Quality — Department of Meteorology", 
    page_icon="🇺🇸", 
    layout="wide",
    initial_sidebar_state="collapsed"
)


st.markdown("""
<style>
    /* Basic navigation */
    .nav-container {
        background: #1a5276;
        padding: 1.5rem;
        margin: -1rem -1rem 2rem -1rem;
        border-bottom: 4px solid #2980b9;
    }
    
    .nav-title {
        color: white;
        font-size: 2rem;
        font-weight: bold;
        margin: 0;
        text-align: center;
        font-family: Arial, sans-serif;
    }
    
    .nav-subtitle {
        color: #ecf0f1;
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
        text-align: center;
    }
    
    /* Basic tabs with clear gaps */
    .stTabs [data-baseweb="tab-list"] {
        display: flex;
        justify-content: space-evenly; /* equal spacing across full width */
        padding: 0.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        padding: 0 5rem;
        background: white;
        border-radius: 6px;
        font-weight: 600;
        border: 1px solid #bdc3c7;
        color: #2c3e50;
        margin: 0 2px;
    }
    
    .stTabs [aria-selected="true"] {
        background: #3498db;
        color: white;
        border-color: #2980b9;
    }
    
    /* Content containers */
    .content-container {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #dfe6e9;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Basic metric styling */
    [data-testid="metric-container"] {
        background: #34495e;
        color: white;
        border: none;
        padding: 1rem;
        border-radius: 6px;
    }
    
    /* Basic buttons */
    .stButton > button {
        background: #3498db;
        border: none;
        border-radius: 6px;
        color: white;
        font-weight: 600;
        padding: 0.8rem 1.5rem;
    }
    
    .stButton > button:hover {
        background: #2980b9;
    }
    
    /* Input styling */
    .stNumberInput > div > div > input {
        border: 1px solid #bdc3c7;
        border-radius: 4px;
        padding: 0.5rem;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #3498db;
        outline: none;
    }
            
            
</style>
""", unsafe_allow_html=True)


if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "📥 Input Features"
if 'prediction_made' not in st.session_state:
    st.session_state.prediction_made = False


st.markdown("""
<div class="nav-container">
    <h1 class="nav-title">🌤️ US Air Quality Prediction System</h1>
    <p class="nav-subtitle">Department of Meteorology — Protecting American Communities</p>
</div>
""", unsafe_allow_html=True)


tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📥 Input Features",
    "🔮 Prediction", 
    "📊 Analytics",
    "💡 Advice",
    "📲 Alerts"
])

with tab1:
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    show_input_tab()
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    show_prediction_tab()
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    show_analytics_tab()
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    show_advice_tab()
    st.markdown('</div>', unsafe_allow_html=True)

with tab5:
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    show_alerts_tab()
    st.markdown('</div>', unsafe_allow_html=True)


st.markdown("""
<div style="text-align: center; padding: 2rem 0; color: #7f8c8d; margin-top: 3rem; 
            background: #ecf0f1; border-radius: 6px; border: 1px solid #bdc3c7;">
    <h4 style="color: #2c3e50; margin-bottom: 1rem;">United States Department of Meteorology</h4>
    <p style="margin: 0.5rem 0;">Official US Government Air Quality Monitoring System</p>
    <p style="margin: 0.5rem 0; font-size: 0.9rem;">© 2025 | Protecting American Air Quality</p>
</div>
""", unsafe_allow_html=True)