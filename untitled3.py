# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1fiJQYIi-ULZMKFinRjAZleFulbGXAibC
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error

# Load the data
premier_league_file_path = "/content/Premier league table.xlsx"
premier_league_data = pd.read_excel(premier_league_file_path)

# Display the dataset
st.write("Chosen Dataset:")
st.dataframe(premier_league_data.head(100))

# Compute and display statistics
max_goals = premier_league_data['gf'].max()
max_goals_con = premier_league_data['ga'].max()
average_goals_scored = premier_league_data['gf'].mean()

team_with_most_goals_scored = premier_league_data[premier_league_data['gf'] == max_goals]['team'].iloc[0]
team_most_goals_conceded = premier_league_data[premier_league_data['ga'] == max_goals_con]['team'].iloc[0]
team_with_most_goals_scored_season = premier_league_data[premier_league_data['gf'] == max_goals]['season_end_year'].iloc[0]
team_most_goals_conceded_season = premier_league_data[premier_league_data['ga'] == max_goals_con]['season_end_year'].iloc[0]

st.write(f"The team that scored the most goals in one season is: **{team_with_most_goals_scored}** in the season **{team_with_most_goals_scored_season}**.")
st.write(f"The team that conceded the most goals in one season is: **{team_most_goals_conceded}** in the season **{team_most_goals_conceded_season}**.")
st.write(f"The average number of goals scored every season is: **{average_goals_scored:.2f}**.")

# Visualization: Top 5 Scoring Teams
st.write("Top 5 Scoring Teams:")
top_5_teams = premier_league_data.sort_values(by='gf', ascending=False).head(5)
fig, ax = plt.subplots()
ax.bar(top_5_teams['team'], top_5_teams['gf'], color='red', width=0.4)
ax.set_xlabel('Team')
ax.set_ylabel('Goals Scored')
ax.set_title('Top 5 Scoring Teams')
ax.set_xticklabels(top_5_teams['team'], rotation=45)
st.pyplot(fig)

# Points analysis
most_points_in_one_season = premier_league_data['points'].max()
least_points_in_one_season = premier_league_data['points'].min()

team_with_most_points = premier_league_data[premier_league_data['points'] == most_points_in_one_season]['team'].iloc[0]
team_with_least_points = premier_league_data[premier_league_data['points'] == least_points_in_one_season]['team'].iloc[0]
team_with_most_points_season = premier_league_data[premier_league_data['points'] == most_points_in_one_season]['season_end_year'].iloc[0]
team_with_least_points_season = premier_league_data[premier_league_data['points'] == least_points_in_one_season]['season_end_year'].iloc[0]

st.write(f"The team that got the most points in one season is: **{team_with_most_points}** in the season **{team_with_most_points_season}**.")
st.write(f"The team that got the least points in one season is: **{team_with_least_points}** in the season **{team_with_least_points_season}**.")

# Visualization: Teams with more than 65 points
st.write("Teams with more than 65 points in one season:")
filtered_data = premier_league_data[premier_league_data['points'] > 65]
team_max_points = filtered_data.groupby('team')['points'].max()

fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(team_max_points.index, team_max_points.values)
ax.set_xlabel('Team')
ax.set_ylabel('Points')
ax.set_title('Maximum Points per Team (Above 65)')
ax.set_xticklabels(team_max_points.index, rotation=90, ha='right')

for team, points in team_max_points.items():
    season = filtered_data[(filtered_data['team'] == team) & (filtered_data['points'] == points)]['season_end_year'].iloc[0]
    ax.text(team, points, str(season), ha='center', va='bottom')

st.pyplot(fig)

# Visualization: Top 3 Teams by Place Finishes
st.write("Top 3 Teams in First, Second, and Third Places:")
init_value = 0
dicti_FirstPlace = {}
dicti_SecondPlace = {}
dicti_ThirdPlace = {}

for index, row in premier_league_data.iterrows():
    position = row['position']
    team = row['team']

    if position == 1:
        dicti_FirstPlace[team] = dicti_FirstPlace.get(team, init_value) + 1
    elif position == 2:
        dicti_SecondPlace[team] = dicti_SecondPlace.get(team, init_value) + 1
    elif position == 3:
        dicti_ThirdPlace[team] = dicti_ThirdPlace.get(team, init_value) + 1

sorted_first = sorted(dicti_FirstPlace.items(), key=lambda item: item[1], reverse=True)
sorted_second = sorted(dicti_SecondPlace.items(), key=lambda item: item[1], reverse=True)
sorted_third = sorted(dicti_ThirdPlace.items(), key=lambda item: item[1], reverse=True)

top3_first = sorted_first[:3]
top3_second = sorted_second[:3]
top3_third = sorted_third[:3]

st.write(f"The Most 3 teams that came in the first place over the years are: {top3_first}")
st.write(f"The Most 3 teams that came in the second place over the years are: {top3_second}")
st.write(f"The Most 3 teams that came in the third place over the years are: {top3_third}")

fig, ax = plt.subplots(3, 1, figsize=(10, 15))

teams, counts = zip(*top3_first)
ax[0].bar(teams, counts, color='gold')
ax[0].set_title('Top 3 Teams in First Place')
ax[0].set_ylabel('Number of First Place Finishes')

teams, counts = zip(*top3_second)
ax[1].bar(teams, counts, color='silver')
ax[1].set_title('Top 3 Teams in Second Place')
ax[1].set_ylabel('Number of Second Place Finishes')

teams, counts = zip(*top3_third)
ax[2].bar(teams, counts, color='brown')
ax[2].set_title('Top 3 Teams in Third Place')
ax[2].set_ylabel('Number of Third Place Finishes')

st.pyplot(fig)

# Model training and evaluation
st.write("Training a Decision Tree Regressor to Predict Points:")

y = premier_league_data['points']
premier_league_columns = ['season_end_year', 'position', 'won', 'lost', 'gf', 'ga']
X = premier_league_data[premier_league_columns]

train_X, val_X, train_y, val_y = train_test_split(X, y, test_size=0.2, random_state=0)

premier_league_AImodel = DecisionTreeRegressor(random_state=1)
premier_league_AImodel.fit(train_X, train_y)

val_predictions = premier_league_AImodel.predict(val_X)
mae = mean_absolute_error(val_y, val_predictions)
st.write(f"Mean Absolute Error (MAE) is: **{mae:.2f}**")

st.write("Making predictions for the following 5 teams:")
st.write(val_X.head(5))
predicted_points = premier_league_AImodel.predict(val_X.head())
st.write("The predicted points are:")
st.write(predicted_points)
st.write('The actual points are:')
st.write(val_y.head())

# Visualize actual vs predicted points
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(val_y, val_predictions, label='Predicted Points')
ax.scatter(val_y, val_y, label='Actual Points', color='red')
ax.set_xlabel('Actual Points')
ax.set_ylabel('Predicted Points')
ax.set_title('Actual vs Predicted Points (Validation Set)')
ax.legend()
ax.grid(True)
st.pyplot(fig)