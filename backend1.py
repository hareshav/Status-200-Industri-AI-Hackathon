import google.generativeai as genai
import re
import streamlit as st
import json
import streamlit as st
import pandas as pd
import seaborn as sns
import pdfplumber
import re
import matplotlib.pyplot as plt
import plotly.express as px
from requiredFunctions import plot_credit_and_debit_data,plot_credit_data,plot_df_data,plot_debit_data,plot_loan_data,plot_transaction_type_pie_chart,plot_income_data
# Configure the API key
st.set_page_config(layout="wide")
genai.configure(api_key="AIzaSyBQfOqo8xW9ImnOVqQs-wX4f5kTsbFXQgM")
model = genai.GenerativeModel('gemini-1.5-flash')
chat_no={
    "HDFC Bank": "70700 22222",
    "ICICI Bank": "8640086400",
    "Axis Bank": "7036165000",
    "State Bank of India (SBI)": "9022690226",
    "Bajaj Finserv":"8698010101"
}
st.title('📊 FinTrack')
st.subheader('Tracking finances and loans efficiently.')
x,z=st.columns([3,1])
# Define the parameters for the content generation
with z:
    loan_type = st.selectbox("Loan Type", ["Personal Loan", "Home Loan"], index=0)
    amount_requested = st.slider("Amount Requested ($)", min_value=0, max_value=1000000, value=300000, step=5000)
    interest_rate = st.slider("Interest Rate (%)", min_value=0.0, max_value=20.0, value=5.5, step=0.1, format="%.2f %%")
    collateral_value = st.slider("Collateral Value ($)", min_value=0, max_value=500000, value=60000, step=1000)
    employment_status = st.selectbox("Employment Status", ["Full-time", "Part-time", "Self-employed", "Unemployed"], index=0)
    monthly_income = st.slider("Monthly Income ($)", min_value=0, max_value=100000, value=25000, step=1000)
    loan_purpose = st.text_input("Loan Purpose", value="Home Renovation")
    loan_duration = st.slider("Loan Duration (Months)", min_value=1, max_value=120, value=24, step=1)
    current_debt = st.slider("Current Debt ($)", min_value=0, max_value=200000, value=10000, step=500)
    credit_score = st.slider("Credit Score", min_value=300, max_value=850, value=800, step=10)
monthly_payment = (amount_requested * (interest_rate / 100 / 12)) / (1 - (1 + interest_rate / 100 / 12)**(-loan_duration))
DTI = (current_debt + monthly_payment) / monthly_income
CCR = collateral_value / amount_requested
LTI = amount_requested / (monthly_income * 12)

# Scoring Components
credit_score_scaled = (credit_score - 300) / 550 * 100
DTI_score = max(0, 100 - (DTI * 100))  # Lower DTI is better
CCR_score = min(100, CCR * 100)       # Higher collateral coverage is better
LTI_score = max(0, 100 - (LTI * 100)) # Lower loan-to-income ratio is better
employment_score = {"Full-time": 100, "Part-time": 80, "Self-employed": 70, "Unemployed": 30}[employment_status]

# Weighted Score Calculation
final_score = (
    0.35 * credit_score_scaled +
    0.20 * DTI_score +
    0.15 * CCR_score +
    0.15 * LTI_score +
    0.10 * employment_score +
    0.05 * 100  # Assuming loan purpose is always acceptable
)

# Construct the dynamic prompt
prompt = f"""
The credit score is determined by evaluating the following factors:
- Amount Requested: ${amount_requested}
- Interest Rate: {interest_rate}%
- Collateral Value: ${collateral_value}
- Employment Status: {employment_status}
- Monthly Income: ${monthly_income}
- Loan Purpose: {loan_purpose}
- Loan Duration: {loan_duration} months
- Current Debt: ${current_debt}

Explain how these parameters influence in 4 to 5 lines in plain text
"""

# Define bank loan details
bank_loans = {
    "HDFC Bank": {
        "Personal Loan": {
            "loan_amount": "₹50,000 to ₹40 lakhs",
            "tenure": "1 to 5 years",
            "interest_rate": "10.50% to 18% p.a.",
            "eligibility": "Salaried individuals with minimum income ₹25,000/month",
            "credit_score": "750+ preferred"
        },
        "Home Loan": {
            "loan_amount": "Up to 90% of property value",
            "tenure": "Up to 30 years",
            "interest_rate": "8.50% to 9.60% p.a.",
            "eligibility": "Salaried or self-employed with income of ₹25,000+/month",
            "credit_score": "700+"
        }
    },
    "State Bank of India (SBI)": {
        "Personal Loan": {
            "loan_amount": "₹25,000 to ₹20 lakhs",
            "tenure": "Up to 6 years",
            "interest_rate": "10.90% to 12.90% p.a.",
            "eligibility": "Minimum monthly income ₹15,000 (salaried or pensioners)",
            "credit_score": "700+ preferred"
        },
        "Home Loan": {
            "loan_amount": "₹5 lakhs to ₹10 crores",
            "tenure": "Up to 30 years",
            "interest_rate": "9.15% to 9.75% p.a.",
            "eligibility": "Minimum monthly income ₹25,000",
            "credit_score": "700+"
        }
    },
    "ICICI Bank": {
        "Personal Loan": {
            "loan_amount": "₹50,000 to ₹50 lakhs",
            "tenure": "1 to 6 years",
            "interest_rate": "10.99% to 16.50% p.a.",
            "eligibility": "Salaried individuals earning ₹25,000+/month",
            "credit_score": "750+"
        },
        "Home Loan": {
            "loan_amount": "₹1 lakh to ₹50 lakhs",
            "tenure": "Up to 30 years",
            "interest_rate": "8.50% to 9.75% p.a.",
            "eligibility": "Salaried or self-employed with regular income",
            "credit_score": "700+"
        }
    },
    "Axis Bank": {
        "Personal Loan": {
            "loan_amount": "₹50,000 to ₹40 lakhs",
            "tenure": "1 to 5 years",
            "interest_rate": "10.50% to 18% p.a.",
            "eligibility": "Salaried individuals with minimum income ₹25,000/month",
            "credit_score": "750+ preferred"
        },
        "Home Loan": {
            "loan_amount": "₹1 lakh to ₹5 crores",
            "tenure": "Up to 30 years",
            "interest_rate": "8.60% to 9.85% p.a.",
            "eligibility": "Salaried or self-employed with regular income",
            "credit_score": "700+"
        }
    },
    "Bajaj Finserv": {
        "Personal Loan": {
            "loan_amount": "₹50,000 to ₹25 lakhs",
            "tenure": "1 to 5 years",
            "interest_rate": "11% to 16% p.a.",
            "eligibility": "Salaried individuals with income of ₹20,000+/month",
            "credit_score": "750+ preferred"
        },
        "Home Loan": {
            "loan_amount": "₹10 lakhs to ₹5 crores",
            "tenure": "Up to 15 years",
            "interest_rate": "8.50% to 11% p.a.",
            "eligibility": "Salaried or self-employed with property ownership",
            "credit_score": "750+ preferred"
        }
    }
}

# Function to calculate the best loan options
def recommend_loan(bank_loans, loan_type, requested_amount, monthly_income, credit_score):
    model2 = genai.GenerativeModel('gemini-1.5-flash',
                              generation_config={"response_mime_type": "application/json"})
    recommend={}
    for i in bank_loans.keys():
        prompt=f"""
        from the below parameters the based on this give the matching rate (The value between  1 to 10 ) . this is the eligiblity criteria 
        {bank_loans[i][loan_type]} and this is current criteria {requested_amount}{monthly_income}{credit_score} 0-1 rating in json with key as matching_rate
        """
        data=model2.generate_content(prompt).text
        data=json.loads(data)
        recommend[i]=data['matching_rate']
    # Sort banks based on preference (just a placeholder here)
    recommend=sorted(recommend, key=recommend.get, reverse=True)
    
    return recommend
# Example user input
loan_type = "Personal Loan"
requested_amount = amount_requested
monthly_income = monthly_income
credit_score = credit_score
uploaded_file = st.sidebar.file_uploader("Upload Bank Statements", type=["csv"])
with z:
    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)
        df=df.dropna()
        debit=df[df['Type']=='DR']
        credit=df[df['Type']=='CR']
        loan=df[df['Description'].str.contains('loan', case=False, na=False)]
        cred_usage=df[df['Description'].str.contains('cred', case=False, na=False)]
        income=df[df['Description'].str.contains('neft',case=False,na=False)]
    if st.button("Get Recommended Banks"):
        with x:
            if uploaded_file is None:
                st.error("Please upload a bank statements file.")
                st.stop()
            st.write("### Credit Risk Assessment")
            st.write(f"**Debt-to-Income Ratio (DTI):** {DTI:.2f}")
            st.write(f"**Collateral Coverage Ratio (CCR):** {CCR:.2f}")
            st.write(f"**Loan-to-Income Ratio (LTI):** {LTI:.2f}")
            st.write(f"**Estimated Monthly Payment:** ${monthly_payment:.2f}")
            st.write(f"**Credit Risk Score:** {final_score:.2f} / 100")

            # Risk Level
            if final_score >= 70:
                st.success("Low Risk - Likely to be approved")
            elif final_score >= 50:
                st.warning("Moderate Risk - May require additional checks")
            else:
                st.error("High Risk - Likely to be declined")
            data=model.generate_content(prompt).text
            st.write(data)
            recommended_banks = recommend_loan(bank_loans, loan_type, amount_requested, monthly_income, credit_score)
            st.write("Recommended Banks for your Loan Type From High Probable To Low Probable:")
            for i in recommended_banks:
                st.write(i,chat_no[i])
            j,k=st.columns([2,2])
            with j:
                plot_debit_data(debit)
                plot_credit_data(credit)
            with k:
                plot_df_data(df)

                plot_transaction_type_pie_chart(df)
chatbot_model=genai.GenerativeModel('gemini-1.5-flash')

st.sidebar.title("Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.sidebar.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for user query
user_input = st.sidebar.text_input("Ask something:")

# Process User Input
if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Simulated bot response
    response = chatbot_model.generate_content(f"you are now a financial assistant answer the question below in 3 lines {user_input}").text
    st.session_state.messages.append({"role": "bot", "content": response})

    # Display the bot response
    with st.sidebar.chat_message("bot"):
        st.markdown(response)