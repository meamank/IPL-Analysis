import streamlit as st
import plotly
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np

st.title('IPL Batsman Analysis')

st.write('Data used: IPL 2008-2020')

@st.cache(allow_output_mutation=True)

def load_data(nrows):
      deliveries = pd.read_csv('deliveries.csv', nrows=nrows)
      return deliveries

# Load 10,000 rows of data into the dataframe.
deliveries = load_data(193468)


#Selectbox for player
player_list = st.selectbox("Select Player", deliveries["batsman"].unique())

# filter by batsman
filter=(deliveries['batsman']== '{}'.format(player_list))
df_player=deliveries[filter]

 # Show data using Pie Chart
colors = ['#003f5c', '#58508d', '#bc5090', '#ff6361', '#ffa600']
values = df_player['dismissal_kind'].value_counts()
labels=df_player['dismissal_kind'].value_counts().index
fig = go.Figure(data=[go.Pie(labels=labels,values=values,hole=.3)])
fig.update_traces(hoverinfo='label+percent+value', textinfo='label', textfont_size=16,
                        marker=dict(colors=colors, line=dict(color='#000000', width=3)))
fig.update_layout(title="Dismissal Type",
                        titlefont={'size': 30}, )

#Plot the Pie Chart
st.plotly_chart(fig, use_container_width=True)

#Ways a batsman scores his runs
def count_runs(df_player,runs):
      return len(df_player[df_player['batsman_runs']==runs])*runs

count_runs(df_player,1)
count_runs(df_player,2)
count_runs(df_player,3)
count_runs(df_player,4)
count_runs(df_player,6)

values=[count_runs(df_player,1),count_runs(df_player,2),count_runs(df_player,3),count_runs(df_player,4),count_runs(df_player,6)]
labels=[1,2,3,4,6]
fig2 = go.Figure(data=[go.Pie(labels=labels,values=values,hole=.3)])
fig2.update_traces(hoverinfo='label+percent', textinfo='label+value', textfont_size=16,
                  marker=dict(colors=colors, line=dict(color='#000000', width=3)))
fig2.update_layout(title="Total runs Distribution",
                  titlefont={'size': 30},
                  )

#Plot the Pie Chart
st.plotly_chart(fig2, use_container_width=True)
