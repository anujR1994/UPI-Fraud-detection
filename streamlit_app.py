import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import datetime
from datetime import datetime as dt
import time
import base64
import pickle 
# import subprocess
# subprocess.check_call(["pip", "install", "xgboost"])
from xgboost import XGBClassifier

"""
# Welcome to your own UPI Transaction Fraud Detector!

You have the option of inspecting a single transaction by adjusting the parameters below OR you can even check 
multiple transactions at once by uploading a .csv file in the specified format
"""

pickle_file_path = "UPI Fraud Detection Final.pkl"
# Load the saved XGBoost model from the pickle file
loaded_model = pickle.load(open(pickle_file_path, 'rb'))

tt = ["Bill Payment", "Investment", "Other", "Purchase", "Refund", "Subscription"]
pg = ["Google Pay", "HDFC", "ICICI UPI", "IDFC UPI", "Other", "Paytm", "PhonePe", "Razor Pay"]
ts = ['Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']
mc = ['Donations and Devotion', 'Financial services and Taxes', 'Home delivery', 'Investment', 'More Services', 'Other', 'Purchases', 'Travel bookings', 'Utilities']

tran_date = st.date_input("Select the date of your transaction", datetime.date.today())
if tran_date:
    selected_date = dt.combine(tran_date, dt.min.time())
    month = selected_date.month
    year = selected_date.year

tran_type = st.selectbox("Select transaction type", tt)
pmt_gateway = st.selectbox("Select payment gateway", pg)
tran_state=st.selectbox("Select transaction state",ts)
merch_cat = st.selectbox("Select merchant category", mc)

amt = st.number_input("Enter transaction amount",step=0.1)

st.write("OR")

df = pd.read_csv("sample.csv")
st.write("CSV Format:", df)

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Uploaded CSV:", df)

button_clicked = st.button("Check transaction(s)")
st.markdown(
    """
    <style>
    .stButton>button {
        position: fixed;
        bottom: 40px;
        left: 413px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
if button_clicked:
    tt_oh = []
    for i in range(len(tt)):
        tt_oh.append(0)
    pg_oh = []
    for i in range(len(pg)):
        pg_oh.append(0)
    ts_oh = []
    for i in range(len(ts)):
        ts_oh.append(0)
    mc_oh = []
    for i in range(len(mc)):
        mc_oh.append(0)
    if uploaded_file is not None:
        with st.spinner("Checking transactions..."):
            def download_csv():
                csv = df.to_csv(index=False,header=True)
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="output.csv">Download Output CSV</a>'
                return href
            df[['Month', 'Year']] = df['Date'].str.split('-', expand=True)[[1, 2]]
            df[['Month', 'Year']] = df[['Month', 'Year']].astype(int)
            df.drop(columns=['Date'], inplace=True)
            df = df.reindex(columns=['Amount', 'Year', 'Month','Transaction_Type','Payment_Gateway','Transaction_State','Merchant_Category'])
            results = []
            for index, row in df.iterrows():
                input = []
                input.append(row.values[0])
                input.append(row.values[1])
                input.append(row.values[2])
                tt_oh[tt.index(row.values[3])]=1
                pg_oh[pg.index(row.values[4])]=1
                ts_oh[ts.index(row.values[5])]=1
                mc_oh[mc.index(row.values[6])]=1
                input = input+tt_oh+pg_oh+ts_oh+mc_oh
                prediction = loaded_model.predict([input])[0]
                results.append(prediction)
            df['fraud']=results
            st.success("Checked transactions!")
            st.markdown(download_csv(), unsafe_allow_html=True)
            
    else:
        with st.spinner("Checking transaction(s)..."):
            tt_oh[tt.index(tran_type)]=1
            pg_oh[pg.index(pmt_gateway)]=1
            ts_oh[ts.index(tran_state)]=1
            mc_oh[mc.index(merch_cat)]=1
            input = []
            input.append(amt)
            input.append(year)
            input.append(month)
            input = input+tt_oh+pg_oh+ts_oh+mc_oh
            inputs = [input]
            result = loaded_model.predict(inputs)[0]
            st.success("Checked transaction!")
            if(result==0):
                st.write("Congratulations! Not a fraudulent transaction.")
            else:
                st.write("Oh no! This transaction is fraudulent.")
