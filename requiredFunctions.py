import streamlit as st
import plotly.express as px
import pandas as pd
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