# FinTrack - Financial Tracking and Loan Assessment

## Overview
FinTrack is a Streamlit-based application designed to help users efficiently track finances, assess loans, and analyze bank transactions. It provides credit risk scoring, bank loan comparisons, and visualizations for better financial insights.

## Features
- Credit risk assessment based on user-provided financial parameters.
- Loan eligibility recommendations from major banks.
- Interactive visualizations of credit and debit transactions.
- Bank statement uploads and analysis.
- Integrated chatbot for financial queries.
  
## Workflow
![flowchart](https://github.com/user-attachments/assets/f2538b83-d49f-46ad-9b85-f6b252080aab)

## Installation

### Prerequisites
- Python 3.9+
- Streamlit
- Required Python packages listed in `requirements.txt`

### Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   streamlit run backend1.py
   ```

## Usage
1. Launch the application.
2. Upload a bank statement (CSV format) in the sidebar.
3. Provide loan details like amount, interest rate, collateral value, etc.
4. Analyze the results including risk score, recommended banks, and transaction breakdowns.
5. Use the chatbot for additional queries.

## Configuration
Set the API key for Google Generative AI:
```python
import google.generativeai as genai
genai.configure(api_key="YOUR_API_KEY")
```

## Visualizations
The app generates the following charts and graphs:
- Credit and debit data trends.
- Transaction type distribution pie charts.
- Loan data breakdown.

## Recommendations
The app evaluates loan eligibility based on:
- Debt-to-Income Ratio (DTI)
- Collateral Coverage Ratio (CCR)
- Loan-to-Income Ratio (LTI)
- Credit Risk Score

### Bank Loan Details
- Displays interest rates, tenure, and eligibility criteria from top banks.
- Ranks banks based on user's financial parameters.

## Chatbot
- Integrated financial assistant powered by Google's Gemini model.
- Provides quick responses to financial queries.

## Contributing
1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Submit a pull request.

## Contributors
- Mohamed Abubakkar S
- Darshika R K
- Janani M
