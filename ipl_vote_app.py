#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
ADMIN_PASSWORD = "aplipublic2013"
# IPL team list
teams = [
    "Chennai Super Kings", "Mumbai Indians", "Kolkata Knight Riders",
    "Sunrisers Hyderabad", "Rajasthan Royals", "Gujarat Titans",
    "Royal Challengers Bengaluru", "Delhi Capitals", "Punjab Kings",
    "Lucknow Super Giants"
]

VOTE_FILE = "votes.csv"

st.set_page_config(page_title="IPL Team Voting", layout="centered")
st.title("🏏 Welcome to Vote Your Favorite IPL Teams")
st.subheader("This experience is all crafted with care by Priyesh. Enjoy the fun and vote away!")

# Step 1: Collect user information (name and team)
name = st.text_input("What's your name?")

# Step 2: User selection for team prediction and support
prediction = st.selectbox("Who do you think will win IPL 2025?", teams)
support = st.selectbox("Which team do you support this season?", teams)

# Step 3: User selection for 4 teams
st.markdown("Pick **exactly 4 teams** you support the most!")
selected_teams = st.multiselect("Select 4 IPL Teams:", teams, max_selections=4)

# Handle submission
if st.button("Submit Vote"):
    if len(selected_teams) != 4 or not name:
        st.warning("Please select exactly 4 teams and provide your name.")
    else:
        # Store the votes
        vote_data = {
            "Name": name,
            "Prediction": prediction,
            "Support": support,
            "Team1": selected_teams[0],
            "Team2": selected_teams[1],
            "Team3": selected_teams[2],
            "Team4": selected_teams[3]
        }

        # Check if the file exists, if not create it
        if not os.path.exists(VOTE_FILE):
            df = pd.DataFrame([vote_data])
            df.to_csv(VOTE_FILE, index=False)
        else:
            # Append vote to the CSV file
            df = pd.read_csv(VOTE_FILE)
            new_vote_df = pd.DataFrame([vote_data])
            df = pd.concat([df, new_vote_df], ignore_index=True)
            df.to_csv(VOTE_FILE, index=False)
        
        st.success(f"✅ Vote submitted successfully, {name}!")
        
st.divider()

# Admin Password Input for Reset
admin_password = st.text_input("Enter admin password to reset results", type="password")

if admin_password == ADMIN_PASSWORD:
    if st.button("Reset Results"):
        if os.path.exists(VOTE_FILE):
            os.remove(VOTE_FILE)
            st.success("🧹 Results have been reset!")
        else:
            st.warning("No results found to reset.")
else:
    if admin_password:
        st.warning("Incorrect password! Only the admin can reset the results.")

# Step 4: Admin Panel - Generate Word Cloud
st.divider()
st.header("📊 Users Choice: Top four teams")

if st.button("Generate Word Cloud"):
    if not os.path.exists(VOTE_FILE):
        st.warning("No votes found yet.")
    else:
        all_votes = pd.read_csv(VOTE_FILE)
        word_list = all_votes[["Team1", "Team2", "Team3", "Team4"]].values.flatten().tolist()

        wc_text = " ".join(word_list)
        wc = WordCloud(width=800, height=400, background_color="white").generate(wc_text)

        st.subheader("🖼️ Word Cloud of Team Popularity")
        fig, ax = plt.subplots()
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)

# Step 5: Display Vote Counts for each Team and Prediction
if st.button("Show Vote Counts"):
    if os.path.exists(VOTE_FILE):
        all_votes = pd.read_csv(VOTE_FILE)

        # Count votes for each team
        support_counts = all_votes["Support"].value_counts()
        st.subheader("🗳️ IPL 2025 Most Supported team")
        st.write(support_counts)

        # Count predictions for winner
        prediction_counts = all_votes["Prediction"].value_counts()
        st.subheader("📊 IPL 2025 Win Prediction")
        st.write(prediction_counts)
    else:
        st.warning("No votes found yet.")

