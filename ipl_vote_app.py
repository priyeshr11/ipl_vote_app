#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
import plotly.express as px
from collections import Counter

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
st.markdown("Pick **exactly 4 teams** you you think will finish at top 4!")
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
        # Replace spaces with underscores to keep multi-word team names together
        #word_list = [team.replace(" ", "_") for team in word_list]

       # wc_text = " ".join(word_list)
        #wc = WordCloud(width=800, height=400, background_color="white").generate(wc_text)
        wc = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(
            Counter(word_list)
        )

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
        support_counts = all_votes["Support"].value_counts().reset_index()
        support_counts.columns = ["Team", "Support Votes"]
        
        st.subheader("🗳️ IPL 2025 Most Supported team")
        #st.write(support_counts)
        fig_support = px.bar(
            support_counts,
            x="Team",
            y="Support Votes",
            color="Team",
            title="Support Votes by Team",
            text="Support Votes",
            color_discrete_sequence=px.colors.qualitative.Set3,
        )
        fig_support.update_traces(textposition='outside')
        fig_support.update_layout(showlegend=False)
        st.plotly_chart(fig_support, use_container_width=True)

        # Count predictions for winner
        prediction_counts = all_votes["Prediction"].value_counts().reset_index()
        prediction_counts.columns = ["Team", "Predicted Wins"]
        
        st.subheader("📊 IPL 2025 Win Prediction")

        fig_prediction = px.bar(
            prediction_counts,
            x="Team",
            y="Predicted Wins",
            color="Team",
            title="Predicted Winner Votes by Team",
            text="Predicted Wins",
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        fig_prediction.update_traces(textposition='outside')
        fig_prediction.update_layout(showlegend=False)
        st.plotly_chart(fig_prediction, use_container_width=True)

        # At the end of your Streamlit app (after vote logic)
        st.markdown("---")  # Just a horizontal divider

        st.subheader("👥 Participants List")

    # Remove empty or duplicate names
        participant_names = all_votes["Name"].dropna().drop_duplicates().tolist()

    # Sort alphabetically if you like
        participant_names.sort()

    # Display as a bulleted list
        for name in participant_names:
            st.markdown(f"- {name}")
    else:
            st.info("No participants yet. Be the first to vote!")

        #st.write(prediction_counts)
#else:
#    st.warning("No votes found yet.")


from datetime import datetime


DELETE_LOG = "delete_log.csv"
ADMIN_SECRET = ADMIN_PASSWORD # Change this to a secure password

# --- Admin Panel ---
with st.expander("🔐 Admin Panel (Authorised Access Only)"):
    admin_password = st.text_input("Enter admin password:", type="password")

    if admin_password == ADMIN_SECRET:
        st.success("Access granted.")

        if os.path.exists(VOTE_FILE):
            df = pd.read_csv(VOTE_FILE)

            st.subheader("🧹 Current Vote Records")
            edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
            if st.button("💾 Save Edited Table"):
                edited_df.to_csv(VOTE_FILE, index=False)
                st.success("Changes saved successfully.")

            st.markdown("---")
            st.subheader("🗑️ Delete Entry by Name")

            # Clean and drop blank names
            name_options = df["Name"].dropna().drop_duplicates().sort_values().tolist()
            name_to_delete = st.selectbox("Select name to delete:", options=[""] + name_options)

            if st.button("Delete Selected Entry"):
                if name_to_delete in df["Name"].values:
                    df = df[df["Name"] != name_to_delete]
                    df.to_csv(VOTE_FILE, index=False)

                    # Log deletion
                    log_entry = pd.DataFrame([{
                        "Name": name_to_delete,
                        "Deleted At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }])
                    if os.path.exists(DELETE_LOG):
                        log_df = pd.read_csv(DELETE_LOG)
                        log_df = pd.concat([log_df, log_entry], ignore_index=True)
                    else:
                        log_df = log_entry
                    log_df.to_csv(DELETE_LOG, index=False)

                    st.success(f"Deleted entry for '{name_to_delete}' and logged it.")
                else:
                    st.warning("Name not found in the current records.")
        else:
            st.info("No vote data found yet.")
    elif admin_password:
        st.error("Incorrect password.")
