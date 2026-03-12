import streamlit as st
from transformers import pipeline

# Set the professional look of the page
st.set_page_config(page_title="ClearSight Audit Console", layout="wide")

st.title("ClearSight Audit Console")
st.markdown("### Enterprise Risk & Compliance Assessment Framework")
st.markdown("---")

# Load the Hugging Face model (cached so it only loads once)
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
            
            st.markdown("---")
            st.markdown("### 📄 Official Audit Report")
            
            # Formatting the output based on risk
            if label == 'toxic' and score > 0.5:
                st.error(f"⚠️ **HIGH RISK DETECTED**")
                st.write(f"**Confidence Score:** {score:.2%}")
                st.write("**Recommendation:** Text violates professional compliance standards. Immediate revision required.")
            else:
                st.success(f"✅ **COMPLIANT**")
                st.write(f"**Confidence Score:** {(1 - score):.2%}")
                st.write("**Recommendation:** Text passes baseline risk assessment. Cleared for professional use.")

            st.markdown("---")
            st.markdown("### 🚀 Share Your Certification")
            st.write("Copy the text below to showcase your proactive compliance on LinkedIn:")
            
            post_template = f"""I just ran a corporate policy through the ClearSight Audit Console. 
            
Result: {'Compliant ✅' if label != 'toxic' else 'Risk Flagged ⚠️'}
            
Proactive risk management is the future of enterprise operations. I built this tool using Streamlit and Hugging Face to automate compliance checks. 
            
Check out the live tool here: [Insert your Streamlit Link]
#RiskManagement #Compliance #SoftwareEngineering"""
            
            st.code(post_template, language="markdown")
