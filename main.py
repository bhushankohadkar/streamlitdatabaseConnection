import streamlit as st
import pandas as pd
import pyodbc
import datetime 


st.set_page_config(page_title="Game Management", page_icon="🎮")

# @st.cache_resource
def init_connection():
    # return pyodbc.connect(
    #     "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
    #     + st.secrets["server"]
    #     + ";DATABASE="
    #     + st.secrets["database"]
    #     + ";UID="
    #     + st.secrets["username"]
    #     + ";PWD="
    #     + st.secrets["password"]
    # )
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=tcp:bhushankoahadkar.database.windows.net,1433;"
        "DATABASE=Game;"
        "UID=bhushankohadkar;"
        "PWD=Bhushank@11;"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

conn = init_connection()


# Function to fetch registered players from Registration table
def get_registered_players():
    query = "SELECT ID, PlayerName FROM Registration ORDER BY PlayerName"
    df = pd.read_sql(query, conn)
    # conn.close()
    return df

# Function to insert game results
def insert_game_result(MatchID, player_id, PlayerName, kills, deaths, score, game_winner, total_score, tokens):
    cursor = conn.cursor()
    query = """INSERT INTO MatchDetails (MatchID, PlayerID, PlayerName, Kills, Deaths, Score, GameWinner, TotalScore, Tokens)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    cursor.execute(query, (MatchID, player_id, PlayerName, kills, deaths, score, game_winner, total_score, tokens))
    
    conn.commit()
    cursor.close()
    # conn.close()

# Function to fetch match results
def get_game_results():
    query = """SELECT m.MatchID, r.PlayerName, m.Kills, m.Deaths, m.Score, m.GameWinner, m.TotalScore, m.Tokens
               FROM MatchDetails m
               JOIN Registration r ON m.PlayerID = r.ID
               ORDER BY m.MatchID DESC"""
    df = pd.read_sql(query, conn)
    # conn.close()
    return df


st.title("🎮 Game Results Management")

# Load registered players for selection
players_df = get_registered_players()
if players_df.empty:
    st.warning("⚠ No players found. Please register players first!")
    st.stop()

# Dropdown: Select Player
player_options = {row["PlayerName"]: row["ID"] for _, row in players_df.iterrows()}  # Dictionary {PlayerName: PlayerID}

#match master
col1, col2, col3, col4 = st.columns(4)
with col1:
    MatchID = st.number_input("Match Number", min_value=1, step=1)
with col2:
    MatchDate = st.date_input("Select Match Date")
with col3:
    st.selectbox(
        "Select the map",
        ("Outpost","Catacombs","Sub division","Undermine","Cliff hanger","Overseer","Prymid","Snowblind",
        "Hightower","No Escape","Bottleneck","So long","Lunarcy","Suspension","Crossfire","Icebox"),
    )
with col4:
    TimeDuration = st.time_input("Select Time Duration", datetime.time(4, 0))


# Form to insert game data
with st.form("game_result_form"):
    MatchID = st.number_input("Match Number", min_value=1, step=1)
    PlayerName = st.selectbox("Select Player", list(player_options.keys()))  # Display Player Names
    player_id = player_options[PlayerName]  # Fetch corresponding PlayerID
    kills = st.number_input("Kills", min_value=0)
    deaths = st.number_input("Deaths", min_value=0)
    score = kills - deaths  # Auto-calculate score
    game_winner = st.text_input("Game Winner")
    total_score = st.number_input("Total Score", min_value=0)
    tokens = st.number_input("Tokens", min_value=0)

    submitted = st.form_submit_button("Add Game Result")
    if submitted:
        insert_game_result(MatchID, player_id, PlayerName, kills, deaths, score, game_winner, total_score, tokens)
        st.success(f"✅ Game result for {PlayerName} (Match {MatchID}) added!")

# Display game results
st.subheader("📊 Game Results Table")
game_results_df = get_game_results()
st.dataframe(game_results_df)
