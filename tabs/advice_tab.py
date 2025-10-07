import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()

def get_detailed_advice(category: str) -> dict:
    advice_table = {
        "Good": {
            "health_effects": "🌿 Excellent air quality that meets all EPA national standards. Pollution poses little or no risk to the US population.",
            "general_population": "✅ Ideal conditions for all outdoor activities across the United States. Perfect for hiking, sports, and community events. No restrictions needed for any American citizens.",
            "sensitive_groups": "🛡️ Completely safe for sensitive US populations including children, elderly, pregnant women, and people with asthma, heart, or lung conditions. Normal activities can continue without concern.",
            "precautions": "🎯 No special precautions required under current EPA guidelines. Continue normal daily routines and outdoor exercise programs.",
            "government_actions": "📊 Continue routine federal monitoring through the EPA AirNow network. Maintain public awareness campaigns about maintaining good air quality.",
            "outdoor_activities": "🏞️ Perfect for all outdoor activities: hiking, biking, sports, gardening, and community events",
            "indoor_recommendations": "🏠 Normal ventilation recommended. Windows can remain open for fresh air circulation",
            "long_term_health": "⭐ No long-term health risks associated with current air quality levels"
        },
        "Moderate": {
            "health_effects": "💛 Air quality is acceptable for most Americans under EPA standards, but there may be moderate health concern for very sensitive individuals.",
            "general_population": "👍 Generally acceptable conditions for outdoor activities throughout US communities. Most Americans will not be affected.",
            "sensitive_groups": "⚠️ US residents with respiratory conditions (asthma, COPD), heart disease, children, and elderly should consider reducing prolonged or heavy outdoor exertion. Watch for symptoms like coughing or shortness of breath.",
            "precautions": "📝 Sensitive US populations should monitor for symptoms. Consider choosing less strenuous outdoor activities or scheduling them for times when air quality is better.",
            "government_actions": "📢 Issue EPA health notices for sensitive groups. Increase state monitoring frequency. Alert healthcare providers to be prepared for increased respiratory complaints.",
            "outdoor_activities": "🚶 Suitable for light to moderate activities. Consider reducing intense exercise duration",
            "indoor_recommendations": "💨 Good indoor ventilation recommended. Air purifiers not necessary for most homes",
            "long_term_health": "📈 Minimal long-term risk with continued exposure at these levels"
        },
        "Unhealthy_Sensitive": {
            "health_effects": "🟠 Air quality exceeds EPA recommended levels for sensitive groups. Increased likelihood of adverse effects for vulnerable US populations.",
            "general_population": "📉 Most US residents may experience no immediate effects, but sensitive groups are likely to be affected. General population should monitor for unusual symptoms.",
            "sensitive_groups": "🚨 US sensitive populations should significantly reduce outdoor activities. Americans with asthma should keep rescue medication handy. Elderly and children should limit time outdoors.",
            "precautions": "😷 Consider rescheduling strenuous outdoor activities. Sensitive individuals may benefit from wearing N95 masks if spending extended time outdoors. Keep windows closed during peak pollution hours.",
            "government_actions": "🔔 Activate state health advisory systems. Alert US hospitals and clinics to prepare for increased respiratory cases. Restrict outdoor activities in US schools for sensitive children.",
            "outdoor_activities": "⏱️ Limit outdoor exercise to 30-60 minutes. Choose indoor alternatives when possible",
            "indoor_recommendations": "🪟 Keep windows closed during afternoon hours. Consider using air purifiers",
            "long_term_health": "⚖️ Extended exposure may worsen existing respiratory conditions"
        },
        "Unhealthy": {
            "health_effects": "🔴 Air quality violates EPA standards. All US residents may begin to experience health effects. Sensitive groups experience more serious effects.",
            "general_population": "🚫 All Americans should reduce prolonged or heavy exertion outdoors. Even healthy individuals may experience coughing, throat irritation, or breathing discomfort.",
            "sensitive_groups": "🏥 US sensitive groups should avoid all prolonged outdoor exertion. Stay indoors as much as possible. Those with pre-existing conditions should monitor symptoms closely.",
            "precautions": "🆘 US residents should wear N95 masks outdoors. Use high-efficiency air purifiers indoors. Keep windows and doors closed. Reschedule non-essential outdoor activities.",
            "government_actions": "📡 Issue federal health warnings to all media outlets. Activate emergency response plans. Consider implementing traffic restrictions in major US metropolitan areas.",
            "outdoor_activities": "❌ Avoid strenuous outdoor activities. Limit essential outdoor time to 15-30 minutes",
            "indoor_recommendations": "✅ Use HEPA air purifiers. Maintain closed windows. Avoid indoor pollution sources",
            "long_term_health": "📊 Increased risk of respiratory issues with prolonged exposure"
        },
        "Very_Unhealthy": {
            "health_effects": "🟣 Health emergency conditions for all US residents: everyone may experience serious health effects from poor air quality.",
            "general_population": "🆘 All Americans should avoid all physical activity outdoors. Cancel or reschedule outdoor events nationwide. Even brief exposure can cause health issues.",
            "sensitive_groups": "🏨 US sensitive populations should remain indoors and avoid any physical exertion. Seek medical attention immediately if symptoms occur. Consider temporary relocation if air quality doesn't improve.",
            "precautions": "🚷 Use high-efficiency air purifiers in all living spaces. US residents should wear N95 masks if going outside is absolutely necessary. Create clean air rooms in homes.",
            "government_actions": "🚨 Declare federal health emergency. Implement industrial production restrictions. Close US schools and public facilities. Activate emergency shelters with air filtration.",
            "outdoor_activities": "🛑 All outdoor activities should be cancelled. Essential workers require protective equipment",
            "indoor_recommendations": "🛡️ Create clean air sanctuary rooms. Use multiple air purifiers. Seal windows thoroughly",
            "long_term_health": "💊 Significant health risks with any exposure. Medical monitoring recommended"
        }
    }
    return advice_table.get(category, advice_table["Moderate"])

def get_category_color(category: str) -> str:
    color_map = {
        "Good": "#00E400",
        "Moderate": "#FFFF00", 
        "Unhealthy_Sensitive": "#FF7E00",
        "Unhealthy": "#FF0000",
        "Very_Unhealthy": "#8F3F97"
    }
    return color_map.get(category, "#FFFF00")

def get_gemini_advice(question: str, air_quality_context: dict) -> str:
    """Get AI-powered advice from Gemini with fallback to hardcoded advice"""
    try:
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        if not gemini_api_key:
            return "❌ Gemini API key not found. Please check your .env file configuration."
        
        genai.configure(api_key=gemini_api_key)

        
        model = genai.GenerativeModel("gemini-2.5-flash")

        context_prompt = f"""
        You are an air quality expert providing advice based on EPA standards. 

        Current Air Quality Prediction:
        - Category: {air_quality_context['category']}
        - Overall AQI: {air_quality_context['overall_aqi']}
        - Pollutant Levels: {air_quality_context['pollutant_levels']}

        User Question: {question}

        Please provide specific, actionable advice related to air quality, 
        health precautions, government actions, or environmental recommendations. 
        Focus only on air quality-related topics. If the question is not related 
        to air quality, politely decline to answer.

        Keep your response concise and practical, under 200 words.
        """

        response = model.generate_content(context_prompt)
        return response.text.strip()

    except Exception as e:
       
        fallback = get_detailed_advice(air_quality_context["category"])["government_actions"]
        return f"⚠️ AI service unavailable, showing fallback advice:\n\n{fallback}"


def show_ai_chat_interface(air_quality_context: dict):
    """Show the AI chat interface for additional advice"""
    st.markdown("---")
    st.subheader("🤖 AI Air Quality Advisor")
    st.info("💬 Ask specific questions about your air quality prediction, health precautions, or government actions.")
    
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    
    if prompt := st.chat_input("Ask about air quality advice, precautions, or government actions..."):
        
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                ai_response = get_gemini_advice(prompt, air_quality_context)
                st.markdown(ai_response)
        
        
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})

def show_advice_tab():
    st.header("💡 Air Quality Advice & Recommendations")
    st.markdown("### Personalized Health Guidance Based on Your Prediction")
    
    if not st.session_state.get('prediction_made', False):
        st.warning("⚠️ Please make a prediction first to see personalized advice.")
        st.info("💡 Go to the 'Input Features' tab, enter pollutant values, and generate a prediction.")
        return
    
    model_prediction = st.session_state.get('model_prediction', {})
    if not model_prediction:
        st.error("❌ No prediction data found. Please generate a prediction first.")
        return
    
    category = model_prediction["category"]
    overall_aqi = model_prediction["overall_aqi"]
    advisory_color = get_category_color(category)
    
    
    st.markdown(f"""
    <div style='background: {advisory_color}; 
                padding: 20px; border-radius: 8px; text-align: center; color: black; margin: 20px 0;
                border: 2px solid #2c3e50;'>
        <h2 style='margin: 0; font-size: 28px; font-weight: bold;'>
            💡 Advice for: {category.replace("_", " ")} Air Quality
        </h2>
        <p style='margin: 10px 0; font-size: 18px;'>
            Overall AQI: {overall_aqi:.0f} | Based on EPA Standards
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    advice = get_detailed_advice(category)
    
    
    st.subheader("🚀 Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if category in ["Good", "Moderate"]:
            st.success("✅ Continue normal activities")
        else:
            st.warning("⚠️ Adjust outdoor plans")
    
    with col2:
        if category in ["Unhealthy", "Very_Unhealthy"]:
            st.error("❌ Limit outdoor exposure")
        else:
            st.success("✅ Safe for outdoor exercise")
    
    with col3:
        if category in ["Unhealthy_Sensitive", "Unhealthy", "Very_Unhealthy"]:
            st.info("🔒 Enhance indoor air quality")
        else:
            st.success("✅ Normal ventilation sufficient")
    
   
    st.markdown("---")
    if st.button("🤖 Get More Advice with AI", use_container_width=True):
        st.session_state.show_ai_chat = not st.session_state.get('show_ai_chat', False)
        st.rerun()
    
    
    if st.session_state.get('show_ai_chat', False):
        air_quality_context = {
            'category': category,
            'overall_aqi': overall_aqi,
            'pollutant_levels': st.session_state.input_values
        }
        show_ai_chat_interface(air_quality_context)
    
    
    st.header("📋 Detailed Recommendations")
    
    
    st.markdown(f"""
    <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; border-left: 4px solid {advisory_color}; margin: 1rem 0;">
        <h4 style="color: #2c3e50; margin: 0 0 1rem 0;">🩺 Health Effects</h4>
        <p style="margin: 0; color: #374151; line-height: 1.5;">{advice['health_effects']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    
    col1, col2 = st.columns(2)
    
    with col1:
        
        st.markdown(f"""
        <div style="background: #e3f2fd; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #2196f3;">
            <h4 style="color: #1565c0; margin: 0 0 1rem 0;">👥 For General Population</h4>
            <p style="margin: 0; color: #374151; line-height: 1.5;">{advice['general_population']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        
        st.markdown(f"""
        <div style="background: #e8f5e8; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #4caf50;">
            <h4 style="color: #2e7d32; margin: 0 0 1rem 0;">🏞️ Outdoor Activities</h4>
            <p style="margin: 0; color: #374151; line-height: 1.5;">{advice['outdoor_activities']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        
        st.markdown(f"""
        <div style="background: #fffde7; padding: 1rem; border-radius: 8px; border-left: 4px solid #ffeb3b;">
            <h4 style="color: #f57f17; margin: 0 0 1rem 0;">📈 Long-term Health Impact</h4>
            <p style="margin: 0; color: #374151; line-height: 1.5;">{advice['long_term_health']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        
        st.markdown(f"""
        <div style="background: #fff3e0; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #ff9800;">
            <h4 style="color: #e65100; margin: 0 0 1rem 0;">👨‍👩‍👧‍👦 For Sensitive Groups</h4>
            <p style="margin: 0; color: #374151; line-height: 1.5;">{advice['sensitive_groups']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        
        st.markdown(f"""
        <div style="background: #e1f5fe; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #03a9f4;">
            <h4 style="color: #0277bd; margin: 0 0 1rem 0;">🏠 Indoor Recommendations</h4>
            <p style="margin: 0; color: #374151; line-height: 1.5;">{advice['indoor_recommendations']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        
        st.markdown(f"""
        <div style="background: #f3e5f5; padding: 1rem; border-radius: 8px; border-left: 4px solid #9c27b0;">
            <h4 style="color: #7b1fa2; margin: 0 0 1rem 0;">🎯 Recommended Precautions</h4>
            <p style="margin: 0; color: #374151; line-height: 1.5;">{advice['precautions']}</p>
        </div>
        """, unsafe_allow_html=True)
    
   
    st.markdown("---")
    st.header("🆘 Emergency Preparedness")
    
    if category in ["Unhealthy", "Very_Unhealthy"]:
        st.error("""
        **🚨 High Alert Conditions Detected**
        
        Under current air quality conditions, consider these emergency measures:
        - Keep emergency medications readily accessible
        - Have a supply of N95 masks available
        - Identify clean air shelters in your community
        - Monitor local emergency alerts regularly
        """)
    
   
    st.subheader("✅ Action Checklist")
    
    if category == "Good":
        st.success("""
        - ✅ Continue all normal activities
        - ✅ Enjoy outdoor exercises and events
        - ✅ Maintain normal indoor ventilation
        - ✅ No special precautions needed
        """)
    elif category == "Moderate":
        st.info("""
        - ✅ Most people can continue normal activities
        - ⚠️ Sensitive individuals should reduce prolonged exertion
        - ✅ Generally safe for outdoor activities
        - 📝 Monitor for any unusual symptoms
        """)
    elif category == "Unhealthy_Sensitive":
        st.warning("""
        - ⚠️ Sensitive groups should reduce outdoor activities
        - ✅ General population can continue with caution
        - 🏠 Keep windows closed during peak hours
        - 😷 Consider masks for sensitive individuals
        """)
    elif category == "Unhealthy":
        st.error("""
        - ❌ Everyone should reduce outdoor exertion
        - 🏠 Sensitive groups should stay indoors
        - 😷 Wear N95 masks if going outside
        - 🔒 Use air purifiers and keep windows closed
        """)
    elif category == "Very_Unhealthy":
        st.error("""
        - 🚨 Avoid all outdoor activities
        - 🏠 Stay indoors with windows sealed
        - 😷 Essential outings require N95 masks
        - 📞 Have emergency contacts ready
        """)
    
    
    st.markdown("---")
    st.header("📚 Additional Resources")
    
    resource_col1, resource_col2 = st.columns(2)
    
    with resource_col1:
        st.markdown("""
        **🌐 Official Resources:**
        - [EPA AirNow](https://www.airnow.gov/)
        - [CDC Air Quality](https://www.cdc.gov/air/)
        - [American Lung Association](https://www.lung.org/)
        """)
    
    st.caption("💡 This advice is based on EPA Air Quality Standards and current medical guidelines. Consult healthcare providers for personalized medical advice.")