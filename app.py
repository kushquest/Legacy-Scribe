import streamlit as st
import asyncio
import time
from datetime import datetime
from core.orchestrator import ModernizationOrchestrator
from core.config import Config
from models.schemas import CodeAnalysis

# --- PAGE SETUP ---
st.set_page_config(
    page_title="Legacy Scribe", 
    page_icon="🚀", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ADVANCED IBM BLUE CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;600;700&family=IBM+Plex+Mono&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', sans-serif;
    }

    /* Main Branding */
    .main-header { 
        text-align: left; 
        color: #0062ff;
        font-size: 3.5rem; 
        font-weight: 700; 
        margin-bottom: 0rem; 
    }
    .sub-header { color: #525252; font-size: 1.2rem; margin-bottom: 2rem; border-bottom: 2px solid #0062ff; padding-bottom: 10px; }
    
    /* Metrics & Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 4px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border-top: 4px solid #0062ff;
        margin-bottom: 1rem;
    }
    .metric-title { color: #161616; font-size: 0.9rem; font-weight: 600; text-transform: uppercase; }
    .metric-value { color: #0062ff; font-size: 1.8rem; font-weight: 700; }

    /* Modernization Console */
    .thinking-console {
        background-color: #161616;
        color: #f4f4f4;
        padding: 1.2rem;
        border-radius: 4px;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.9rem;
        margin: 1rem 0;
        border-left: 6px solid #0062ff;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "orchestrator" not in st.session_state:
    try:
        st.session_state.orchestrator = ModernizationOrchestrator()
    except Exception as e:
        st.error(f"Failed to initialize Orchestrator: {e}")
        st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## 🚀 Legacy Scribe")
    st.markdown("### Control Panel")
    
    # Dynamic Model Selection
    available_models = Config.get_available_gemini_models()
    selected_model = st.selectbox(
        "Select Model Engine", 
        available_models, 
        index=available_models.index("gemini-1.5-flash") if "gemini-1.5-flash" in available_models else 0,
        help="Select the Gemini model for analysis. Default is Gemini 1.5 Flash."
    )
    
    st.info(f"System: Vertex AI (ADC Enabled)")
    st.markdown("---")
    st.write("Legacy Scribe Agent v2.0")

# --- UI LOGIC ---
st.markdown("<h1 class='main-header'>Legacy Scribe</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>1a. Upgrading large-scale legacy systems into intelligent, scalable, future-ready platforms.</p>", unsafe_allow_html=True)

col_input, col_output = st.columns([1, 1.5])

with col_input:
    st.markdown("### Legacy Asset Input")
    legacy_type = st.selectbox("Asset Type", ["COBOL Source", "PL/I Module", "JCL Script", "Legacy SQL Schema", "Mainframe Logs"])
    code_input = st.text_area("Paste Code / Logs here:", height=500, placeholder="IDENTIFICATION DIVISION. ...", key="code_input")
    
    if st.button("Initiate Modernization Pipeline", type="primary"):
        if code_input:
            with col_output:
                console = st.empty()
                async def run_pipeline():
                    async for step in st.session_state.orchestrator.run_modernization(code_input, selected_model):
                        if isinstance(step, str):
                            console.markdown(f"<div class='thinking-console'>[SCRIBE]: {step}</div>", unsafe_allow_html=True)
                        else:
                            st.success("Modernization Strategy Generated")
                            
                            # ROI Metrics Row
                            m_col1, m_col2, m_col3 = st.columns(3)
                            with m_col1:
                                st.markdown(f"""
                                <div class='metric-card'>
                                    <div class='metric-title'>Est. Effort</div>
                                    <div class='metric-value'>{step.estimated_effort_hours} Hrs</div>
                                </div>
                                """, unsafe_allow_html=True)
                            with m_col2:
                                st.markdown(f"""
                                <div class='metric-card'>
                                    <div class='metric-title'>Mod. Cost</div>
                                    <div class='metric-value'>${step.modernization_cost_estimate:,.0f}</div>
                                </div>
                                """, unsafe_allow_html=True)
                            with m_col3:
                                st.markdown(f"""
                                <div class='metric-card'>
                                    <div class='metric-title'>Annual Savings</div>
                                    <div class='metric-value'>${step.potential_annual_savings:,.0f}</div>
                                </div>
                                """, unsafe_allow_html=True)

                            st.markdown("### System Analysis")
                            st.markdown(f"**Logic Summary:** {step.logic_summary}")
                            
                            st.error("**Identified Security Vulnerabilities**")
                            for v in step.security_vulnerabilities:
                                st.write(f"• {v}")
                            
                            st.info(f"**Target Architecture:** {step.modern_architecture_suggestion}")
                            
                            st.markdown("---")
                            st.markdown("### Refactored Implementation (Python/FastAPI)")
                            st.code(step.refactored_code_snippet, language="python")
                            
                            # Export Option
                            report_text = (
                                f"MODERNIZATION REPORT\n"
                                f"====================\n"
                                f"TIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                                f"ROI METRICS:\n"
                                f"- Estimated Effort: {step.estimated_effort_hours} hours\n"
                                f"- Modernization Cost: ${step.modernization_cost_estimate:,.2f}\n"
                                f"- Potential Annual Savings: ${step.potential_annual_savings:,.2f}\n\n"
                                f"ANALYSIS:\n{step.logic_summary}\n\n"
                                f"SECURITY:\n{', '.join(step.security_vulnerabilities)}\n\n"
                                f"ARCHITECTURE:\n{step.modern_architecture_suggestion}\n\n"
                                f"REFACTORED CODE:\n{step.refactored_code_snippet}"
                            )
                            st.download_button("Download Modernization Report", report_text, file_name=f"Legacy_Scribe_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

                asyncio.run(run_pipeline())
        else:
            st.warning("Please enter legacy code.")

with col_output:
    if not st.session_state.get('code_input'):
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-title'>System Readiness</div>
            <div class='metric-value'>AWAITING INPUT</div>
            <p style='color: #525252; margin-top: 0.5rem;'>Input legacy assets to trigger neural deconstruction and future-state mapping.</p>
        </div>
        """, unsafe_allow_html=True)
