import streamlit as st
import pandas as pd
import pyodbc 


@st.cache_resource
def init_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        + st.secrets["server"]
        + ";DATABASE="
        + st.secrets["database"]
        + ";UID="
        + st.secrets["username"]
        + ";PWD="
        + st.secrets["password"]
    )

conn = init_connection()

@st.cache_data(ttl=600)
def insert_player(PlayerName, DateOfJoin):
    cursor = conn.cursor()
    
    # Convert DateOfJoin to string (YYYY-MM-DD) for SQL Server
    DateOfJoin_str = DateOfJoin.strftime('%Y-%m-%d')
    
    query = "INSERT INTO Registration (PlayerName, DateOfJoin) VALUES (?, ?)"
    cursor.execute(query, (PlayerName, DateOfJoin_str))
    
    conn.commit()
    cursor.close()  # Close cursor, but keep the connection open

def fetch_players():
    query = "SELECT * FROM Registration"
    df = pd.read_sql(query, conn)  # Use the global connection
    return df

st.set_page_config(page_title="Register Player", page_icon="📝")

st.title("📝 Register New Player")

# Input Fields
PlayerName = st.text_input("Enter Player Name")

# Manual Date Picker (Calendar)
DateOfJoin = st.date_input("Select Registration Date")  # User must choose a date


if st.button("Register Player"):
    # st.text(DateOfJoin)
    if PlayerName and DateOfJoin:
        insert_player(PlayerName, DateOfJoin)
        st.success(f"✅ Player '{PlayerName}' registered successfully on {DateOfJoin}!")
    else:
        pass
        st.warning("⚠️ Please enter a player name and select a registration date.")


if st.button("Show Players"):
    df = fetch_players()  # Fetch players from DB
    st.dataframe(df)  # Display in Streamlit UI
