import streamlit as st 

pg = st.navigation([st.Page("player_registration.py", title="Registration"),st.Page("main.py", title="Game Results Management")], position="sidebar")
pg.run()