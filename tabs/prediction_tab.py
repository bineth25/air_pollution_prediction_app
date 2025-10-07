import streamlit as st
import pandas as pd
import numpy as np
import os

feature_names = ["O3 AQI", "CO AQI", "SO2 AQI", "NO2 AQI"]

def categorize_aqi(aqi_value: float) -> str:
    if aqi_value <= 50:
        return "Good"
    elif aqi_value <= 100:
        return "Moderate"
    elif aqi_value <= 150:
        return "Unhealthy_Sensitive"
    elif aqi_value <= 200:
        return "Unhealthy"
    else:
        return "Very_Unhealthy"

def get_category_color(category: str) -> str:
    color_map = {
        "Good": "#00E400",
        "Moderate": "#FFFF00",
        "Unhealthy_Sensitive": "#FF7E00",
        "Unhealthy": "#FF0000",
        "Very_Unhealthy": "#8F3F97"
    }
    return color_map.get(category, "#FFFF00")

def show_prediction_tab():
    st.header("🔮 US Air Quality Prediction")
    st.markdown("### Machine Learning Model Results Based on EPA Standards")
    
    # --- Ensure a prediction was made ---
    if not st.session_state.get('prediction_made', False):
        st.warning("⚠️ Please go to the 'Input Features' tab and generate a prediction first.")
        return

    # ✅ Remove .pkl loading (use session data instead)
    if "input_values" not in st.session_state:
        st.error("❌ No prediction data found. Please train and predict first.")
        return

    # ✅ Use stored prediction data directly
    y_pred_reg = st.session_state.input_values

    # Determine category using if-else logic
    overall_aqi = float(np.max([
        y_pred_reg["O3 AQI"], 
        y_pred_reg["CO AQI"], 
        y_pred_reg["SO2 AQI"], 
        y_pred_reg["NO2 AQI"]
    ]))
    category = categorize_aqi(overall_aqi)

    # Save to session
    st.session_state.model_prediction = {
        "category": category,
        "overall_aqi": overall_aqi
    }

    location_info = st.session_state.get('location_info', {'region': 'United States', 'city': 'Not specified'})
    
    # --- Display Results ---
    category_color = get_category_color(category)
    st.markdown(f"""
    <div style='background: {category_color};
                padding: 20px; border-radius: 8px; text-align: center; color: black; margin: 20px 0;
                border: 2px solid #2c3e50;'>
        <h2 style='margin: 0; font-size: 28px; font-weight: bold;'>Air Quality: {category.replace("_", " ")}</h2>
        <p style='margin: 10px 0; font-size: 20px;'><strong>Overall AQI: {overall_aqi:.0f}</strong></p>
        <p style='margin: 0; font-size: 14px;'>📍 {location_info['region']} | 🏙️ {location_info['city']}</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Pollutant Table ---
    st.subheader("📋 Predicted Pollutant Details")
    pollutant_data = {
        "Pollutant": ["Ozone (O3)", "Carbon Monoxide (CO)", "Sulfur Dioxide (SO2)", "Nitrogen Dioxide (NO2)"],
        "AQI Value": [
            y_pred_reg["O3 AQI"], y_pred_reg["CO AQI"],
            y_pred_reg["SO2 AQI"], y_pred_reg["NO2 AQI"]
        ]
    }
    st.dataframe(pd.DataFrame(pollutant_data), use_container_width=True)
