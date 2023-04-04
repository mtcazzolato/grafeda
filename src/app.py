# Author: Mirela Cazzolato
# Date: March 2023
# =======================================================================

import streamlit as st

from dashboard import launch_dashboard

# Change page width and configure on load
st.set_page_config(layout="wide",
                   page_icon="🔬",
                   page_title="GraF-EDA",
                   initial_sidebar_state="auto"
)

with st.sidebar:
    st.write(
        """
        # 🔬 GraF-EDA
        EDA and visualization EHR graphs.
        """
    )
    
launch_dashboard()

