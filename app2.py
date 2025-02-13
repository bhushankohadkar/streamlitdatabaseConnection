import streamlit as st
import sqlalchemy as sql
import pandas as pd
def get_connection():
    conn = st.connection(
        "sql",
        dialect="mssql",
        driver="pyodbc",
        host=st.secrets["server"],
        database=st.secrets["database"],
        username=st.secrets["username"],
        password=st.secrets["password"],
    )
    return conn

def insert_player(PlayerName, DateOfJoin):
    conn = get_connection()
    with conn.session as session:
        insert_query = sql.text("INSERT INTO Registration (PlayerName, DateOfJoin) VALUES (:P, :D);")   
        session.execute(insert_query, {"P": PlayerName, "D": DateOfJoin})
        session.commit()  # ✅ Streamlit handles session closing

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
    conn = get_connection()
    with conn.session as session:
        result = session.execute(sql.text("SELECT * FROM Registration"))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())  # ✅ Convert to DataFrame
        st.dataframe(df)

