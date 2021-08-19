from os import write
import streamlit as st
import plotly
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

@st.cache(allow_output_mutation=True)

def load_data(nrows):
      deliveries = pd.read_csv('deliveries.csv', nrows=nrows)
      return deliveries
def load_data2(nrows):
      matches = pd.read_csv('matches.csv', nrows=nrows)
      return matches
# Load 10,000 rows of data into the dataframe.
deliveries = load_data(193468)
matches = load_data2(900)

with st.sidebar:
      st.title('IPL Batsman Analysis')
      st.write('Data used: IPL 2008-2020')
      #Selectbox for player
      player_list = st.selectbox("Select Player", deliveries["batsman"].unique())

      # filter by batsman for deliveries dataframe
      filter_deliveries=(deliveries['batsman']== '{}'.format(player_list))
      df_deliveries_player=deliveries[filter_deliveries]

      # filter by batsman for matches dataframe
      filter_matches=(matches['player_of_match']== '{}'.format(player_list))
      df_matches_player=matches[filter_matches]
      
      #Total matches played
      total_matches = df_deliveries_player['id'].nunique()
      st.markdown("- **Matches: {}**".format(total_matches))
      #Total balls played
      total_balls = df_deliveries_player['ball'].count()
      st.markdown("- **Balls Played: {}**".format(total_balls))
      #Total Runs scored
      total_runs = df_deliveries_player['batsman_runs'].sum()
      st.markdown("- **Runs: {}**".format(total_runs))
      #Show MOM data
      mom_value = df_matches_player['player_of_match'].value_counts()
      try:
            st.markdown("- **Man of the Match: {}**" .format(mom_value[0]))
      except IndexError:
            st.markdown('- **Man of the Match: 0**')

#structure the page
dismissal_type, runs_contribution = st.columns(2)

with dismissal_type:
      # Show data using Pie Chart
      colors = ['#003f5c', '#58508d', '#bc5090', '#ff6361', '#ffa600']
      values = df_deliveries_player['dismissal_kind'].value_counts()
      labels=df_deliveries_player['dismissal_kind'].value_counts().index
      fig = go.Figure(data=[go.Pie(labels=labels,values=values,hole=.3)])
      fig.update_traces(hoverinfo='label+percent+value', textinfo='label', textfont_size=12,
                              marker=dict(colors=colors, line=dict(color='#000000', width=3)))
      fig.update_layout(title="Dismissal Type",
                              titlefont={'size': 24}, )

      #Plot the Pie Chart
      st.plotly_chart(fig, use_container_width=True)

with runs_contribution:
      #Ways a batsman scores his runs
      def count_runs(df_deliveries_player,runs):
            return len(df_deliveries_player[df_deliveries_player['batsman_runs']==runs])*runs

      count_runs(df_deliveries_player,1)
      count_runs(df_deliveries_player,2)
      count_runs(df_deliveries_player,3)
      count_runs(df_deliveries_player,4)
      count_runs(df_deliveries_player,6)

      values=[count_runs(df_deliveries_player,1),count_runs(df_deliveries_player,2),count_runs(df_deliveries_player,3),count_runs(df_deliveries_player,4),count_runs(df_deliveries_player,6)]
      labels=[1,2,3,4,6]
      fig2 = go.Figure(data=[go.Pie(labels=labels,values=values,hole=.3)])
      fig2.update_traces(hoverinfo='label+percent', textinfo='label+value', textfont_size=16,
                        marker=dict(colors=colors, line=dict(color='#000000', width=3)))
      fig2.update_layout(title="Total runs Distribution",
                        titlefont={'size': 24},
                        )

      #Plot the Pie Chart
      st.plotly_chart(fig2, use_container_width=True)

# Number of matches played against each teams
number_of_matches = df_deliveries_player.groupby(['bowling_team'])['id'].nunique().reset_index().rename(columns={'bowling_team':'Team', 'id':'No. of matches'})
number_of_matches = number_of_matches.sort_values(by='No. of matches',ascending=True)
#Plot the chart
values = df_deliveries_player.groupby(['bowling_team'])['id'].nunique()
labels=df_deliveries_player.groupby(['bowling_team'])['id'].nunique().index
fig3 = px.bar(number_of_matches, x='Team', y='No. of matches', 
                                                            hover_data=['Team', 'No. of matches'], color='No. of matches',)
fig3.update_layout(title="Number of matches played against each team",
                        titlefont={'size': 24},
                        )
st.plotly_chart(fig3, use_container_width=True)