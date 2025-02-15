import streamlit as st
import pandas as pd
import pyodbc


st.set_page_config(page_title="Game Management", page_icon="🎮")

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


# Function to fetch registered players from Registration table
def get_registered_players():
    query = "SELECT ID, PlayerName FROM Registration ORDER BY PlayerName"
    df = pd.read_sql(query, conn)
    # conn.close()
    return df

# Function to insert game results
def insert_game_result(match_number, player_id, kills, deaths, score, game_winner, total_score, tokens):
    cursor = conn.cursor()
    query = """INSERT INTO MatchResults (MatchNumber, PlayerID, Kills, Deaths, Score, GameWinner, TotalScore, Tokens)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
    cursor.execute(query, (match_number, player_id, kills, deaths, score, game_winner, total_score, tokens))
    
    conn.commit()
    cursor.close()
    # conn.close()

# Function to fetch match results
def get_game_results():
    query = """SELECT m.MatchNumber, r.PlayerName, m.Kills, m.Deaths, m.Score, m.GameWinner, m.TotalScore, m.Tokens
               FROM MatchResults m
               JOIN Registration r ON m.PlayerID = r.ID
               ORDER BY m.MatchNumber DESC"""
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

# Form to insert game data
with st.form("game_result_form"):
    match_number = st.number_input("Match Number", min_value=1, step=1)
    selected_player_name = st.selectbox("Select Player", list(player_options.keys()))  # Display Player Names
    player_id = player_options[selected_player_name]  # Fetch corresponding PlayerID
    kills = st.number_input("Kills", min_value=0)
    deaths = st.number_input("Deaths", min_value=0)
    score = kills - deaths  # Auto-calculate score
    game_winner = st.text_input("Game Winner")
    total_score = st.number_input("Total Score", min_value=0)
    tokens = st.number_input("Tokens", min_value=0)

    submitted = st.form_submit_button("Add Game Result")
    if submitted:
        insert_game_result(match_number, player_id, kills, deaths, score, game_winner, total_score, tokens)
        st.success(f"✅ Game result for {selected_player_name} (Match {match_number}) added!")

# Display game results
st.subheader("📊 Game Results Table")
game_results_df = get_game_results()
st.dataframe(game_results_df)
