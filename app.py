import streamlit as st
from transformers import pipeline
import plotly.express as px
import pandas as pd

# Set the professional look of the page
st.set_page_config(page_title="ClearSight Audit Console", layout="wide")

st.title("ClearSight Audit Console")
st.markdown("### Enterprise Risk & Compliance Assessment Framework")
st.markdown("---")

# Load the Hugging Face model
@st.cache_resource
def load_auditor():
    return pipeline("text-classification", model="unitary/toxic-bert")

auditor = load_auditor()

# The Interface
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("**Enter documentation, policies, or communications for audit:**")
    user_input = st.text_area("", height=250, placeholder="Paste text here...")
    analyze_button = st.button("Run Compliance Audit")

with col2:
    st.info("ClearSight uses advanced natural language processing to detect risk vectors, bias, and compliance liabilities in corporate text.", icon="ℹ️")

# The Logic
if analyze_button:
    if user_input.strip() == "":
        st.warning("Please enter text to audit.")
    else:
        with st.spinner("Analyzing risk vectors..."):
            # Run the AI model
            result = auditor(user_input[:512])[0] 
            label = result['label']
            score = result['score']
            
            # Calculate safe vs risk scores for the chart
            risk_score = score if label == 'toxic' else (1 - score)
            safe_score = 1 - risk_score
            
            st.markdown("---")
            st.markdown("### 📄 Official Audit Report")
            
            # Create two columns for the report and the new chart
            col3, col4 = st.columns([1, 1])
            
            with col3:
                if risk_score > 0.5:
                    st.error(f"⚠️ **HIGH RISK DETECTED**")
                    st.write(f"**Risk Confidence:** {risk_score:.2%}")
                    st.write("**Recommendation:** Text violates professional compliance standards. Immediate revision required.")
                else:
                    st.success(f"✅ **COMPLIANT**")
                    st.write(f"**Safety Confidence:** {safe_score:.2%}")
                    st.write("**Recommendation:** Text passes baseline risk assessment. Cleared for professional use.")

            with col4:
                # The New Visual Risk Heatmap
                df = pd.DataFrame({
                    "Category": ["Compliance Safety", "Liability Risk"],
                    "Score": [safe_score, risk_score]
                })
                
                fig = px.bar(df, x="Score", y="Category", orientation='h',
                             color="Category",
                             color_discrete_map={"Compliance Safety": "#00CC96", "Liability Risk": "#EF553B"},
                             title="Real-Time Risk Heatmap")
                
                fig.update_layout(xaxis_tickformat='.0%', showlegend=False, height=200)
                st.plotly_chart(fig, use_container_width=True)

            st.markdown("---")
            st.markdown("### 🚀 Share Your Certification")
            st.write("Copy the text below to showcase your proactive compliance on LinkedIn:")
            
            post_template = f"""I just ran a corporate policy through the ClearSight Audit Console. 
            
Result: {'Compliant ✅' if risk_score < 0.5 else 'Risk Flagged ⚠️'}
            
Proactive risk management is the future of enterprise operations. I built this tool using Streamlit, Plotly, and Hugging Face to automate compliance checks. 
            
Check out the live tool here: [Insert your Streamlit Link]
#RiskManagement #Compliance #SoftwareEngineering"""
            
            st.code(post_template, language="markdown")
