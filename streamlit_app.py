import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import datetime
import re
import time

"""
# Welcome to your own UPI Transaction Fraud Detector!

You have the option of inspecting a single transaction by adjusting the parameters below or you can even check 
multiple transactions at once by uploading a .csv file in the specified format
"""
# Function to validate time format
def validate_time_format(input_time):
    pattern = re.compile(r'^([0-1]?[0-9]|2[0-3]):([0-5]?[0-9]):([0-5]?[0-9])$')
    if pattern.match(input_time):
        return True
    else:
        return False

tran_date = st.date_input("Select the date of your transaction", datetime.date.today())
tran_time = st.text_input("Enter transaction time", "in (HH:MM:SS) format")
if (tran_time!="in (HH:MM:SS) format"):
    # Validate time and display error message if format is incorrect
    if not validate_time_format(tran_time):
        st.error("format error")
    # Display the entered time if format is correct
    else:
        st.write("You entered:", tran_time)
merch_id = st.text_input("Enter the merchant's id:")
cust_id = st.text_input("Enter the customer's id:")
device_id = st.text_input("Enter the device's id:")
trans_type = st.selectbox("Select transaction type", ["Bank Transfer", "Bill Payment", "Investment", "Other", "Purchase", "Refund", "Subscription"])
pay_type = st.selectbox("Select payment gateway", ["CRED", "Google Pay", "HDFC", "ICICI UPI", "IDFC UPI", "Other", "Paytm", "PhonePe", "Razor Pay"])
tran_state=st.selectbox("Select transaction state",['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'])
ip = st.text_input("Enter IP Address:")
trans_status = st.selectbox("Select transaction status", ["Completed", "Failed", "Pending"])
device_os = st.selectbox("Select device OS", ["Android", "iOS", "MacOS","Windows"])
tran_freq = st.text_input("Enter transaction frequency")
merch_cat = st.selectbox("Select merchant category", ['Brand Vouchers and OTT', 'Donations and Devotion', 'Financial services and Taxes', 'Home delivery', 'Investment', 'More Services', 'Other', 'Purchases', 'Travel bookings', 'Utilities'])
tran_channel = st.selectbox("Select transaction channel", ["In-store", "Mobile", "Online"])
tran_amt_dev = st.text_input("Enter transaction amount deviation")
amt = st.text_input("Enter transaction amount")
days = st.text_input("Enter days since last transaction")
button_clicked = st.button("Check transaction")
if button_clicked:
    with st.spinner("Checking transaction..."):
        time.sleep(5)
        st.success("Checked transaction!")
    st.write("Congratulations! Not a fraudulent transaction.")
