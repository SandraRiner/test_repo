import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

df = pd.read_csv("data/CO2_per_capita.csv", sep=";")
df.columns = ['country_name','country_code','year','co2_per_capita']

st.title('Top CO2 emitters')
# st.dataframe(df)

min_year, max_year = st.slider('Choisir un intervalle de temps', min_value=1960, max_value=2011, value=(2002,2008))

def top_n_emitters(df, min_year, max_year, nb_displayed=10):
    #years filter
    filtered_years = df[(df['year']>= min_year) & (df['year']<= max_year)]
    #do the mean for each country
    country_mean = filtered_years.groupby('country_name')['co2_per_capita'].mean().reset_index()
    #sort the values and keep nb_displayed
    displayed = country_mean.sort_values(by='co2_per_capita', ascending = False).head(nb_displayed)
    #create the fig
    fig= px.bar(displayed,
                x='country_name',
                y='co2_per_capita',
                title =f"Top {nb_displayed} CO2 emitters",
                labels= {'co2_per_capita' : 'Mean of CO2 per capita', 'country_name' : 'Country'})
    return fig

top_countries = st.selectbox("Top countries emitters", [3, 5, 10, 15, 20, 30])
st.plotly_chart(top_n_emitters(df,min_year, max_year, top_countries))

df = df.dropna(subset= ["co2_per_capita"])
df = df.sort_values(by="year")
fig = px.scatter_geo(df,
                     animation_frame="year",
                     locations="country_name", 
                     color="co2_per_capita",
                     size="co2_per_capita",
                     projection="natural earth"
                     )

st.plotly_chart(fig)