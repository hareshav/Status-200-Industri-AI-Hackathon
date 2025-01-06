import streamlit as st
import pandas as pd
import seaborn as sns
import pdfplumber
import re
import matplotlib.pyplot as plt
import plotly.express as px

df=pd.read_csv('bankStatements.csv')
df=df.dropna()
debit=df[df['Type']=='DR']
credit=df[df['Type']=='CR']
loan=df[df['Description'].str.contains('loan', case=False, na=False)]
cred_usage=df[df['Description'].str.contains('cred', case=False, na=False)]
income=df[df['Description'].str.contains('neft',case=False,na=False)]

def plot_debit_data(debit):
    if 'Date' not in debit.columns or 'Amount' not in debit.columns:
        st.error("Data must contain 'Date' and 'Amount' columns.")
    fig = px.line(debit, x='Date', y='Amount', title='Debit Transactions Over Time')
    fig.update_traces(line=dict(color='red'))
    st.plotly_chart(fig)
def plot_credit_data(credit):
    
    if 'Date' not in credit.columns or 'Amount' not in credit.columns:
        st.error("Data must contain 'Date' and 'Amount' columns.")
        return
    fig = px.line(credit, x='Date', y='Amount', title='Credit Transactions Over Time')
    
    st.plotly_chart(fig)
def plot_df_data(df):
    
    if 'Date' not in df.columns or 'Amount' not in df.columns:
        st.error("Data must contain 'Date' and 'Amount' columns.")
        return
    fig = px.line(df, x='Date', y='Amount', title='Amount Transactions Over Time')
    fig.update_traces(line=dict(color='red'))
    st.plotly_chart(fig)
def plot_income_data(df):
    
    if 'Date' not in df.columns or 'Amount' not in df.columns:
        st.error("Data must contain 'Date' and 'Amount' columns.")
        return
    fig = px.line(df, x='Date', y='Amount', title='Amount Transactions Over Time')
    st.plotly_chart(fig)
def plot_loan_data(df):
    
    if 'Date' not in df.columns or 'Amount' not in df.columns:
        st.error("Data must contain 'Date' and 'Amount' columns.")
        return
    fig = px.line(df, x='Date', y='Amount', title='Amount Transactions Over Time')
    st.plotly_chart(fig)
def plot_credit_and_debit_data(credit, debit):
    if 'Date' not in credit.columns or 'Amount' not in credit.columns:
        st.error("Credit data must contain 'Date' and 'Amount' columns.")
        return
    if 'Date' not in debit.columns or 'Amount' not in debit.columns:
        st.error("Debit data must contain 'Date' and 'Amount' columns.")
        return
    credit['Type'] = 'Credit'
    debit['Type'] = 'Debit'
    combined = pd.concat([credit, debit])
    fig = px.line(combined, x='Date', y='Amount', color='Type', title='Credit and Debit Transactions Over Time',color_discrete_map={'Credit': 'blue', 'Debit': 'red'})
    st.plotly_chart(fig)
def plot_transaction_type_pie_chart(df):
    if 'Type' not in df.columns:
        st.error("Data must contain 'type' column.")
        return
    
    fig = px.pie(df, names='Type', title='Transaction Type Distribution',color_discrete_map={'CR': 'blue', 'DR': 'red'})
    st.plotly_chart(fig)
# x,y=st.columns(4,1)
plot_debit_data(debit)
plot_credit_data(credit)
plot_df_data(df)
plot_income_data(income)
plot_loan_data(loan)
plot_transaction_type_pie_chart(df)
# plot_credit_and_debit_data(credit, debit)