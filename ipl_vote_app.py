#!/usr/bin/env python
# coding: utf-8

# In[3]:


import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

# IPL team list
teams = [
    "Chennai Super Kings", "Mumbai Indians", "Kolkata Knight Riders",
    "Sunrisers Hyderabad", "Rajasthan Royals", "Gujarat Titans",
    "Royal Challengers Bengaluru", "Delhi Capitals", "Punjab Kings",
    "Lucknow Super Giants"
]

VOTE_FILE = "votes.csv"

st.set_page_config(page_title="IPL Team Voting", layout="centered")
st.title("🏏 Vote for Your Favorite IPL Teams")
st.markdown("Pick **exactly 4 teams** you support the most!")

# User selection
selected_teams = st.multiselect("Select 4 IPL Teams:", teams, max_selections=4)

if st.button("Submit Vote"):
    if len(selected_teams) != 4:
        st.warning("Please select exactly 4 teams.")
    else:
        # Save votes to CSV
        vote_df = pd.DataFrame([selected_teams], columns=["Team1", "Team2", "Team3", "Team4"])
        if not os.path.exists(VOTE_FILE):
            vote_df.to_csv(VOTE_FILE, index=False)
        else:
            vote_df.to_csv(VOTE_FILE, mode='a', header=False, index=False)
        st.success("✅ Vote submitted anonymously!")

st.divider()
st.header("📊 Admin Panel: Generate Word Cloud")

if st.button("Generate Word Cloud"):
    if not os.path.exists(VOTE_FILE):
        st.warning("No votes found yet.")
    else:
        all_votes = pd.read_csv(VOTE_FILE)
        word_list = all_votes.values.flatten().tolist()

        wc_text = " ".join(word_list)
        wc = WordCloud(width=800, height=400, background_color="white").generate(wc_text)

        st.subheader("🖼️ Word Cloud of Team Popularity")
        fig, ax = plt.subplots()
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)


# In[ ]:




