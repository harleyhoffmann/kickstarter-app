# -*- coding: utf-8 -*-
"""
Sample streamlit file
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import pickle

@st.cache
def load_data(number_input):
    df = pd.read_csv('https://raw.githubusercontent.com/JonathanBechtel/dat-02-22/main/ClassMaterial/Unit3/data/ks2.csv', nrows=number_input)
    return df

df = pd.read_csv('https://raw.githubusercontent.com/JonathanBechtel/dat-02-22/main/ClassMaterial/Unit3/data/ks2.csv', nrows=2000)


@st.cache
def group_data(x_val, y_val):
    grouping = df.groupby(x_val)[y_val].mean()
    return grouping

@st.cache
def filter_strip_data(x_val, y_val):
    strip_data
    
def load_model():
    with open('mod.pkl', 'rb') as mod:
        pipe = pickle.load(mod)
        
    return pipe

section = st.sidebar.radio('App Section', ['Data Explorer', 'Model Explorer'])

num_rows = st.sidebar.number_input('Number of rows to load', min_value=1000, value=1000, step=1000)



df = load_data(num_rows)

if section == 'Data Explorer':
    
    chart_type = st.sidebar.selectbox('Chart Type',['Bar','Line','Strip'])
    x_axis = st.sidebar.selectbox('X Axis', ['category','main_category','country'])
    y_axis = st.sidebar.selectbox('Y Axis', ['state','goal'])
    st.header("Exploring Kickstart Campaigns! (by Harley Hoffmann)")
    st.subheader("Summary")
    st.text("Use this area to explore the data within the Kickstarter dataset.")
    st.text("This was based on historical Kickstarter campaigns and their funding amounts.")
    st.text("The goal here is to determine the success rate of a particular campaign.")
    st.text("Success is based on their category, main_category, and funding amount.")
    st.text("Visit the Model Explorer section to see possible success percentages.")
    st.text("Model Used: XGBClassifier")
    st.write(df)
    
    if chart_type == 'Bar':
        grouped_data = group_data(x_axis, y_axis)
        st.bar_chart(grouped_data)
    elif chart_type == 'Line':
        grouped_data = group_data(x_axis, y_axis)
        st.line_chart(grouped_data) 
        
    elif chart_type == 'Strip':
        result = df[[x_axis, y_axis]]
        fig = px.strip(result, x=x_axis, y=y_axis, color=x_axis)
        st.plotly_chart(fig)



elif section == 'Model Explorer':
    st.header('Make Predictions With Your Model Here')
    st.text("Use this area to explore different campaign types.")
    st.text("Select different categories, main_categories, and funding amounts.")
    st.text("View their percentage chance of success. Enjoy!")
    mod = load_model()
    
    category = st.sidebar.selectbox('Category', df['category'].unique())
    main_category = st.sidebar.selectbox('Main Category', df['main_category'].unique())
    goal = st.sidebar.number_input('Enter Your Funding Amount', min_value=0, value=1000, step=500)
    

    sample = pd.DataFrame({
       'category': [category],
       'main_category': [main_category],
       'goal': [goal]
       })
    
    
    prediction = mod.predict_proba(sample)
    positive_prob = prediction[0][1]
   
    
    
    st.title(f"Predicted Probability of Campaign Successs: {positive_prob:.2%}")