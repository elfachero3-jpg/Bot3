# --- UI Styling Component --------------------------------------------------
import streamlit as st

def inject_custom_css():
    """Inject custom CSS for app styling - light mode only with fixed tab fonts"""
    
    st.markdown("""
    <style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    /* Main app background */
    .stApp { 
        background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%); 
    }
    
    /* Header styling */
    .main-header { 
        text-align: center; 
        color: #2c3e50; 
        padding: 20px 0 20px 0; 
        animation: fadeInDown 0.8s ease; 
    }
    .main-header h1 { 
        font-size: 2.5rem; 
        font-weight: 600; 
        margin-bottom: 10px; 
    }
    .main-header p { 
        font-size: 1.1rem; 
        opacity: 0.85; 
        color: #546e7a; 
    }
    .creator-text { 
        font-size: 0.9rem; 
        margin-top: 5px; 
        opacity: 0.75; 
        color: #607d8b; 
    }
    
    /* CHROME-STYLE TAB STYLING WITH FIXED FONT SIZE */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #dadce0;
        padding: 8px 8px 0 8px;
        border-radius: 8px 8px 0 0;
        margin-bottom: 0;
        border-bottom: none;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        padding: 0 30px;
        background-color: #dadce0;
        border-radius: 8px 8px 0 0;
        font-size: 1.2rem !important;
        font-weight: 500;
        color: #5f6368;
        border: none;
        position: relative;
        margin-bottom: 0;
        transition: all 0.2s ease;
        box-shadow: none;
    }
    
    .stTabs [data-baseweb="tab"] * {
        font-size: 1.2rem !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #e8eaed;
        color: #202124;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #202124 !important;
        font-weight: 600;
        border-radius: 8px 8px 0 0;
        box-shadow: none;
        z-index: 10;
        border-bottom: 2px solid #ffffff;
    }
    
    /* Remove the horizontal line below tabs */
    .stTabs [data-baseweb="tab-list"]::after {
        display: none;
    }
    
    .stTabs [data-baseweb="tab-border"] {
        display: none;
    }
    
    .stTabs [data-baseweb="tab-highlight"] {
        display: none;
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 30px;
        background: #ffffff;
        border-radius: 0 8px 8px 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        padding: 30px 20px;
        margin-top: 0;
    }
    
    /* Button styling */
    .stButton > button { 
        background: #37474f; 
        color: white; 
        border: none; 
        padding: 15px 40px; 
        font-size: 1.1rem; 
        font-weight: 600; 
        border-radius: 8px; 
        width: 100%; 
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15); 
        transition: all 0.3s ease; 
    }
    .stButton > button:hover { 
        background: #455a64; 
        transform: translateY(-2px); 
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2); 
    }
    
    /* Download button styling */
    .stDownloadButton > button { 
        background: #2e7d32 !important; 
        color: white !important; 
        border: none; 
        padding: 15px 40px; 
        font-size: 1.1rem; 
        font-weight: 600; 
        border-radius: 8px; 
        width: 100%; 
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15); 
    }
    .stDownloadButton > button:hover { 
        background: #388e3c !important; 
        transform: translateY(-2px); 
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2); 
    }
    
    /* Input status box */
    .input-status { 
        background: #ffffff; 
        padding: 15px; 
        border-radius: 8px; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.1); 
        margin: 10px 0; 
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Animation */
    @keyframes fadeInDown { 
        from { opacity: 0; transform: translateY(-30px); } 
        to { opacity: 1; transform: translateY(0); } 
    }
    </style>
    """, unsafe_allow_html=True)
