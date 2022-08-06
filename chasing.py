import streamlit as st
import joblib

batting_team_enc = {'Sunrisers Hyderabad': 0, 'Kings XI Punjab': 1, 'Delhi Capitals': 2, 'Royal Challengers Bangalore': 3, 'Rajasthan Royals': 4, 'Mumbai Indians': 5, 'Kolkata Knight Riders': 6, 'Chennai Super Kings': 7}
bowling_team_enc = {'Mumbai Indians': 0, 'Chennai Super Kings': 1, 'Kings XI Punjab': 2, 'Rajasthan Royals': 3, 'Kolkata Knight Riders': 4, 'Sunrisers Hyderabad': 5, 'Royal Challengers Bangalore': 6, 'Delhi Capitals': 7}
city_enc ={'Cape Town': 0, 'Nagpur': 1, 'East London': 2, 'Chennai': 3, 'Abu Dhabi': 4, 'Durban': 5, 'Dharamsala': 6, 'Mumbai': 7, 'Ahmedabad': 8, 'Chandigarh': 9, 'Cuttack': 10, 'Bloemfontein': 11, 'Delhi': 12, 'Bengaluru': 13, 'Pune': 14, 'Hyderabad': 15, 'Bangalore': 16, 'Visakhapatnam': 17, 'Kolkata': 18, 'Mohali': 19, 'Port Elizabeth': 20, 'Johannesburg': 21, 'Sharjah': 22, 'Kimberley': 23, 'Jaipur': 24, 'Centurion': 25, 'Raipur': 26, 'Indore': 27, 'Ranchi': 28}

model = joblib.load('model.pkl')

st.title("Chasing Predictor")
st.sidebar.title("Chasing Predictor")
st.sidebar.markdown("""
This app predicts the chances of a team winning a match while chasing based on the wickets left and runs left to choose along with some other features such as the city, batting team and bowling team.

This app uses a ML based algorithm to predict the chances of a team winning a match while chasing.
""")

st.subheader("Input the Match Details")
batting_team = st.selectbox("Select the Chasing(Batting) Team", list(batting_team_enc.keys()))
bowling_team = st.selectbox("Select the Defending(Bowling) Team", list(bowling_team_enc.keys()))
city = st.selectbox("Select the City", list(city_enc.keys()))
runs_left = st.number_input("Enter the Runs Left to chase", min_value=0, max_value=300)
over = st.number_input("Enter the Over Completed", min_value=0.0, max_value=20.0,format="%.1f")
wickets_left = st.number_input("Enter the Wickets Left", min_value=0, max_value=10)
total_runs =  st.number_input("Enter the Total Runs to Chase", min_value=0, max_value=300)
balls_left = 120 - over*6
current_rr = ((total_runs - runs_left)/30)*6
required_rr = (runs_left/balls_left)*6
confirm = st.button("Predict")
if confirm:
    st.header("""Match Details""")
    st.table([["Batting Team", batting_team], ["Bowling Team", bowling_team], ["City", city], ["Runs Left", runs_left], ["Over Completed", over], ["Balls Left", balls_left], ["Wickets Left", wickets_left], ["Total Runs to Chase", total_runs], ["Current RR", current_rr], ["Required RR", required_rr]])
    st.header("""Prediction""")
    result = model.predict_proba([[batting_team_enc[batting_team], bowling_team_enc[bowling_team], city_enc[city], runs_left, over, balls_left, wickets_left, total_runs, current_rr, required_rr]])
    prog_result_bat = result[0][1]
    prog_result_bowl = result[0][0]
    result = result[0][1]*100
    st.header("Winning Probability")
    st.subheader(f"{batting_team}")
    st.progress(prog_result_bat)
    st.subheader(f"{bowling_team}")
    st.progress(prog_result_bowl)
    st.subheader(f"The chances of {batting_team} chasing the score is {result}%")

