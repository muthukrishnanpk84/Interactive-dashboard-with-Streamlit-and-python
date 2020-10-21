# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 13:22:49 2020

@author: Lenovo
"""

import streamlit as st
import pandas as pd
import plotly.express as px


st.title('Sentiment Analysis of Tweets about US Airlines')
st.sidebar.title('Sentiment Analysis of Tweets about US Airlines')
st.markdown('This application is a Streamlit Dashboard to analyze the sentiment of tweets')
st.sidebar.markdown('This application is a Streamlit Dashboard to analyze the sentiment of tweets')
DATA_URL=('E:\Data science Projects\Sentiment Analysis of Tweets on US Airlines\Tweets.csv')

@st.cache(persist=True)

def load_data():
    data=pd.read_csv(DATA_URL)
    data['tweet_created']=pd.to_datetime(data['tweet_created'])
    return data
data=load_data()

st.sidebar.subheader('Show random tweets')
random_tweet=st.sidebar.radio('Sentiment',('positive','neutral','negative'))
st.sidebar.markdown(data.query('airline_sentiment==@random_tweet')[["text"]].sample(n=1).iat[0,0])
st.sidebar.markdown('### Number of tweets by sentiment')
select=st.sidebar.selectbox('Visualization type',['Histogram','Pie chart'],key=1)

sentiment_count=data['airline_sentiment'].value_counts()
st.write(sentiment_count)

sentiment_count=pd.DataFrame({'Sentiment':sentiment_count.index,'Tweets':sentiment_count.values})


if not st.sidebar.checkbox('Hide',True):
    st.markdown('Number of tweets by sentiment')
    if select == 'Histogram':
       fig=px.bar(sentiment_count,x='Sentiment',y='Tweets', color='Tweets',height=500)
       st.plotly_chart(fig)
    else:
        fig=px.pie(sentiment_count,names='Sentiment',values='Tweets')
        st.plotly_chart(fig)
        

st.sidebar.subheader("Breakdown airline tweets by sentiments")
choice=st.sidebar.multiselect('Pick the airlines',('US','United','American','Southwest','Delta','Virgin America'),key=0)

if len(choice)>0:
    choice_data=data[data.airline.isin(choice)]
    fig_choice=px.histogram(choice_data,x='airline',y='airline_sentiment',histfunc='count',color='airline_sentiment',
                            facet_col='airline_sentiment',labels={'airline_sentiment':'tweets'})
    st.plotly_chart(fig_choice)


st.sidebar.header('Word CLoud')
