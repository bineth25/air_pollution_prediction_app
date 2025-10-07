import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

def get_aqi_color(category: str) -> str:
    color_map = {
        "Good": "#00E400",
        "Moderate": "#FFFF00",
        "Unhealthy_Sensitive": "#FF7E00",
        "Unhealthy": "#FF0000",
        "Very_Unhealthy": "#8F3F97"
    }
    return color_map.get(category, "#FFFF00")

def show_analytics_tab():
    st.header("📊 Air Quality Analytics")
    
    if not st.session_state.get('prediction_made', False):
        st.warning("⚠️ Make a prediction first to see analytics.")
        return
    
    model_prediction = st.session_state.get('model_prediction', {})
    if not model_prediction:
        st.error("❌ No prediction data found.")
        return
    
    category = model_prediction["category"]
    current_aqi = model_prediction["overall_aqi"]
    input_values = st.session_state.input_values
    location_info = st.session_state.get('location_info', {'region': 'United States', 'city': 'Not specified'})
    

    st.subheader("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        avg_aqi = sum(input_values.values()) / len(input_values)
        st.metric("Average AQI", f"{avg_aqi:.1f}")
    with col2:
        dominant_pollutant = max(input_values, key=input_values.get)
        st.metric("Primary Pollutant", dominant_pollutant.split()[0])
    with col3:
        risk_level = "High" if current_aqi > 150 else "Medium" if current_aqi > 100 else "Low"
        st.metric("Risk Level", risk_level)
    with col4:
        st.metric("Category", category.replace("_", " "))
    
 
    st.subheader("Predicted Pollutant Breakdown")
    
    pollutant_data = [{"Pollutant": k, "AQI Value": f"{v:.1f}"} for k, v in input_values.items()]
    pollutant_df = pd.DataFrame(pollutant_data)
    st.dataframe(pollutant_df, use_container_width=True, hide_index=True)
    
   
    fig_bar = px.bar(
        x=list(input_values.keys()), 
        y=list(input_values.values()),
        title="Predicted Pollutant Metrics",
        color=list(input_values.keys()),
        color_discrete_sequence=px.colors.qualitative.Set2,
        labels={'x': 'Pollutant', 'y': 'AQI Value'}
    )
    fig_bar.update_layout(showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)
    
  
    st.subheader("AQI Indicator")
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=current_aqi,
        title={'text': f"AQI: {category.replace('_', ' ')}"},
        gauge={
            'axis': {'range': [0, 300]},
            'bar': {'color': get_aqi_color(category)},
            'steps': [
                {'range': [0, 50], 'color': "#00E400"},
                {'range': [50, 100], 'color': "#FFFF00"},
                {'range': [100, 150], 'color': "#FF7E00"},
                {'range': [150, 200], 'color': "#FF0000"},
                {'range': [200, 300], 'color': "#8F3F97"}
            ]
        }
    ))
    st.plotly_chart(fig_gauge, use_container_width=True)
    
  
    st.subheader("📈 Historical vs Current AQI")
    try:
        df = pd.read_csv("data/US_air_pollution_dataset_2000_2023.csv")
        df["Date"] = pd.to_datetime(df["Date"])
        
        if "Overall_AQI" not in df.columns:
            df["Overall_AQI"] = df[["O3 AQI", "CO AQI", "SO2 AQI", "NO2 AQI"]].max(axis=1)

        city = location_info["city"].replace(" City", "")
        state = location_info["region"].replace(" State", "").replace(" County", "")

        hist = df[(df["City"] == city) & (df["State"] == state)]
        hist = hist[hist["Date"].dt.year >= 2015]

        if not hist.empty:
            hist = hist.groupby("Date")["Overall_AQI"].mean().reset_index()

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=hist["Date"], y=hist["Overall_AQI"],
                mode="lines", name="Historical AQI",
                line=dict(color="blue", width=2)
            ))
            fig.add_trace(go.Scatter(
                x=[pd.Timestamp.today().normalize()],
                y=[current_aqi],
                mode="markers+text",
                name="Current Prediction",
                text=[f"Pred: {current_aqi:.0f}"],
                textposition="top center",
                marker=dict(color=get_aqi_color(category), size=12, symbol="star")
            ))
            fig.update_layout(title=f"Historical AQI vs Current Prediction ({city}, {state})",
                              xaxis_title="Date", yaxis_title="AQI")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(f"No historical data available for {city}, {state}.")
    except Exception as e:
        st.error(f"Error loading historical data: {e}")
    
  
    st.subheader("📥 Download Analytics Report")
    
    col1, col2, col3 = st.columns([190, 160, 80])
    with col2:
        if st.button("Download PDF Report"):
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []

            title_style = styles['Heading1']
            title_style.alignment = 1
            story.append(Paragraph("AIR QUALITY ANALYTICS REPORT", title_style))
            story.append(Spacer(1, 20))
            
            summary_data = [
                ["Location", f"{location_info['city']}, {location_info['region']}"],
                ["Predicted AQI Category", category.replace('_', ' ')],
                ["Overall AQI", f"{current_aqi:.1f}"],
                ["Report Date", pd.Timestamp.today().strftime("%Y-%m-%d")]
            ]
            
            summary_table = Table(summary_data, colWidths=[200, 200])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.lightblue),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.white)
            ]))
            story.append(summary_table)
            story.append(Spacer(1, 20))

            heading_style = styles['Heading2']
            story.append(Paragraph("KEY PERFORMANCE INDICATORS", heading_style))
            story.append(Spacer(1, 12))
            
            metrics_data = [
                ["Metric", "Value", "Status"],
                ["Average AQI", f"{avg_aqi:.1f}", "Good" if avg_aqi <= 50 else "Moderate" if avg_aqi <= 100 else "Poor"],
                ["Primary Pollutant", dominant_pollutant.split()[0], "Dominant"],
                ["Risk Level", risk_level, "⚠️" if risk_level == "High" else "ℹ️" if risk_level == "Medium" else "✅"],
                ["Classification", "If-Else AQI Logic", "Rule-based Category"]
            ]
            
            metrics_table = Table(metrics_data, colWidths=[150, 120, 100])
            metrics_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.steelblue)
            ]))
            story.append(metrics_table)
            story.append(Spacer(1, 20))

            story.append(Paragraph("POLLUTANT BREAKDOWN", heading_style))
            story.append(Spacer(1, 12))
            pollutant_data = [["Pollutant", "AQI Value"]] + [[k, f"{v:.1f}"] for k, v in input_values.items()]
            pollutant_table = Table(pollutant_data, colWidths=[250, 150])
            pollutant_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.green)
            ]))
            story.append(pollutant_table)
            story.append(Spacer(1, 20))

            story.append(Paragraph("Classification Method", heading_style))
            story.append(Spacer(1, 12))
            story.append(Paragraph("""
            Air Quality Category is determined using <b>EPA standard AQI thresholds</b> with 
            <b>if-else conditional logic</b> instead of a separate machine learning classifier.
            This ensures transparent, explainable results aligned with standard public health criteria.
            """, styles['BodyText']))
            story.append(Spacer(1, 20))

            footer_style = styles['Italic']
            footer_style.alignment = 1
            story.append(Paragraph("Generated by Air Quality Analytics System", footer_style))
            story.append(Paragraph(f"Report generated on: {pd.Timestamp.today().strftime('%Y-%m-%d %H:%M:%S')}", footer_style))

            doc.build(story)
            st.download_button(
                label="📥 Download PDF Report",
                data=buffer.getvalue(),
                file_name="air_quality_report.pdf",
                mime="application/pdf"
            )
