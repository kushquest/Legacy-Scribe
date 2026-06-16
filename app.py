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

# --- RATE LIMITING & ABUSE PREVENTION ---
MAX_QUERIES_PER_SESSION = 3
GLOBAL_QUERIES_PER_HOUR = 30

@st.cache_resource
def get_global_rate_limiter():
    return {"count": 0, "reset_time": time.time() + 3600}

global_usage = get_global_rate_limiter()
if time.time() > global_usage["reset_time"]:
    global_usage["count"] = 0
    global_usage["reset_time"] = time.time() + 3600

if "session_queries" not in st.session_state:
    st.session_state.session_queries = 0

# --- SIDEBAR ---
# Removed per user request

# --- UI LOGIC ---
st.markdown("<h1 class='main-header'>Legacy Scribe</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Upgrading large-scale legacy systems into intelligent, scalable, future-ready platforms.</p>", unsafe_allow_html=True)

col_input, col_output = st.columns([1, 1.5])

with col_input:
    st.markdown("### Legacy Asset Input")
    
    with st.expander("💡 View Copy-Paste Examples"):
        st.markdown("**1. COBOL Source**")
        st.code('''IDENTIFICATION DIVISION.
PROGRAM-ID. CALC-TAX.
DATA DIVISION.
WORKING-STORAGE SECTION.
01  WS-SALARY   PIC 9(5)V99.
01  WS-TAX      PIC 9(5)V99.
PROCEDURE DIVISION.
    COMPUTE WS-TAX = WS-SALARY * 0.15.
    DISPLAY "TAX IS: " WS-TAX.
    STOP RUN.''', language="cobol")
        
        st.markdown("**2. PL/I Module**")
        st.code('''FETCH_DATA: PROC OPTIONS(MAIN);
  DCL CUST_ID CHAR(5);
  DCL CUST_NAME CHAR(30);
  EXEC SQL SELECT NAME INTO :CUST_NAME FROM CUSTOMERS WHERE ID = :CUST_ID;
  PUT SKIP LIST('Customer: ', CUST_NAME);
END FETCH_DATA;''', language="pli")
        
        st.markdown("**3. JCL Script**")
        st.code('''//BACKUP JOB (123),'SYS BACKUP',CLASS=A,MSGCLASS=X
//STEP1    EXEC PGM=IEBGENER
//SYSPRINT DD  SYSOUT=*
//SYSUT1   DD  DSN=PROD.DATA.MASTER,DISP=SHR
//SYSUT2   DD  DSN=BACKUP.DATA.MASTER,DISP=(NEW,CATLG,DELETE),
//             SPACE=(CYL,(50,10),RLSE),UNIT=SYSDA
//SYSIN    DD  DUMMY''', language="jcl")

        st.markdown("**4. Legacy SQL Schema**")
        st.code('''CREATE TABLE EMP_MAST (
  EMP_NO NUMBER(4) PRIMARY KEY,
  ENAME VARCHAR2(10),
  JOB VARCHAR2(9),
  MGR NUMBER(4),
  HIREDATE DATE,
  SAL NUMBER(7,2),
  COMM NUMBER(7,2),
  DEPTNO NUMBER(2)
);''', language="sql")

        st.markdown("**5. Mainframe Logs**")
        st.code('''+DFHAP0001 2026-06-16 10:00:00 CICSHTK1 An abend (code 0C4) has occurred at offset X'000A42' in module PROG7B.
IEA995I SYMPTOM DUMP OUTPUT
USER COMPLETION CODE=4038 REASON CODE=00000001
TIME=10.05.01  SEQ=00045  CPU=0000  ASID=002B''', language="text")

    legacy_type = st.selectbox("Asset Type", ["COBOL Source", "PL/I Module", "JCL Script", "Legacy SQL Schema", "Mainframe Logs"])
    code_input = st.text_area("Paste Code / Logs here:", height=400, placeholder="IDENTIFICATION DIVISION. ...", key="code_input")
    
    if st.button("Initiate Modernization Pipeline", type="primary"):
        if global_usage["count"] >= GLOBAL_QUERIES_PER_HOUR:
            st.error("🛑 **Global Capacity Reached:** The application is currently receiving too many requests. Please try again later to prevent abuse.")
        elif st.session_state.session_queries >= MAX_QUERIES_PER_SESSION:
            st.error(f"🛑 **Session Limit Reached:** To prevent abuse, each user session is limited to {MAX_QUERIES_PER_SESSION} queries. Thank you for testing Legacy Scribe!")
        elif code_input:
            # Increment counts to track usage
            st.session_state.session_queries += 1
            global_usage["count"] += 1
            with col_output:
                console = st.empty()
                async def run_pipeline():
                    async for step in st.session_state.orchestrator.run_modernization(code_input):
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
