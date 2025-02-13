import streamlit as st
import sqlalchemy as sql

def get_connection():
    conn = st.connection(
        "sql",
        dialect="mssql",
        driver="pyodbc",
        host="tcp:bhushankoahadkar.database.windows.net,1433",
        database="Game",
        username="bhushankohadkar",
        password = "Bhushank@11",
        query={
            "driver": "ODBC Driver 18 for SQL Server",
            "encrypt": "yes",
        },
    )
    return conn


# PlayerName = st.text_input("Enter Player Name")
# DateOfJoin = st.date_input("Select Registration Date")
# if st.button("Register Player"):
#     with conn.session as session:
#         insert_query = sql.text("INSERT INTO Registration (PlayerName,DateOfJoin) VALUES (:P,:D);")   
#         session.execute(insert_query, {"P" : PlayerName, "D" : DateOfJoin})
#         session.commit()
#         st.success(f"�� Player '{PlayerName}' registered successfully!")
#         session.close()
        # df = session.execute(text("SELECT * FROM Registration")).fetchall()
        # st.dataframe(df)
     


# if st.button("Register Player"):
# df = conn.query("select * from Registration")
# st.dataframe(df)


def insert_player(PlayerName, DateOfJoin):
    conn = get_connection()
    with conn.session as session:
        insert_query = sql.text("INSERT INTO Registration (PlayerName,DateOfJoin) VALUES (:P,:D);")   
        session.execute(insert_query, {"P" : PlayerName, "D" : DateOfJoin})
        session.commit()
        session.close()
    

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

if st.button("show Player"):
    conn = get_connection()
    with conn.session as session:
        df = session.execute(sql.text("SELECT * FROM Registration")).fetchall()
        st.dataframe(df)