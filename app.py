import streamlit as st
from dotenv import load_dotenv
import logging

#import pages
from modules.prediction import prediction
from modules.visualizations import create_visualization

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Configure page
    st.set_page_config(
        page_title="Student Performance Analysis",
        page_icon="🎓",
        layout="wide"
    )
    # Sidebar navigation
    page = st.sidebar.radio(
        "Go to:",
        ["🔮 Make Predictions", "📊 Data Visualizations"]
    )
    
    if page == "🔮 Make Predictions":
        prediction()

    elif page == "📊 Data Visualizations":
        create_visualization()

if __name__ == "__main__":
    main()
