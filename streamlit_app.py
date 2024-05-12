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
# def validate_time_format(input_time):
#     pattern = re.compile(r'^([0-1]?[0-9]|2[0-3]):([0-5]?[0-9]):([0-5]?[0-9])$')
#     if pattern.match(input_time):
#         return True
#     else:
#         return False

tran_date = st.date_input("Select the date of your transaction", datetime.date.today())
if tran_date:
    selected_date = datetime.strptime(str(tran_date), '%Y-%m-%d')
    month = selected_date.strftime("%B")
    year = selected_date.year

    st.write("Month:", month)
    st.write("Year:", year)
# tran_time = st.text_input("Enter transaction time", "in (HH:MM:SS) format")
# if (tran_time!="in (HH:MM:SS) format"):
#     # Validate time and display error message if format is incorrect
#     if not validate_time_format(tran_time):
#         st.error("format error")
#     # Display the entered time if format is correct
#     else:
#         st.write("You entered:", tran_time)
# merch_id = st.text_input("Enter the merchant's id:")
# cust_id = st.text_input("Enter the customer's id:")
# device_id = st.text_input("Enter the device's id:")
trans_type = st.selectbox("Select transaction type", ["Bank Transfer", "Bill Payment", "Investment", "Other", "Purchase", "Refund", "Subscription"])
pmt_gateway = st.selectbox("Select payment gateway", ["CRED", "Google Pay", "HDFC", "ICICI UPI", "IDFC UPI", "Other", "Paytm", "PhonePe", "Razor Pay"])
tran_state=st.selectbox("Select transaction state",['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'])
tran_city=st.selectbox("Select transaction city",['Agartala', 'Agra', 'Ahmedabad', 'Ahmednagar', 'Aizawl', 'Ajmer', 'Akola', 'Alappuzha', 'Aligarh', 'Allahabad', 'Alwar', 'Amaravati', 'Ambala', 'Ambarnath', 'Ambattur', 'Amravati', 'Amritsar', 'Amroha', 'Anand', 'Anantapur', 'Anantapuram', 'Arrah', 'Asansol', 'Aurangabad', 'Avadi', 'Bahraich', 'Ballia', 'Bally', 'Bangalore', 'Baranagar', 'Barasat', 'Bardhaman', 'Bareilly', 'Bathinda', 'Begusarai', 'Belgaum', 'Bellary', 'Berhampore', 'Berhampur', 'Bettiah', 'Bhagalpur', 'Bhalswa Jahangir Pur', 'Bharatpur', 'Bhatpara', 'Bhavnagar', 'Bhilai', 'Bhilwara', 'Bhimavaram', 'Bhind', 'Bhiwandi', 'Bhiwani', 'Bhopal', 'Bhubaneswar', 'Bhusawal', 'Bidar', 'Bidhannagar', 'Bihar Sharif', 'Bijapur', 'Bikaner', 'Bilaspur', 'Bokaro', 'Bongaigaon', 'Bulandshahr', 'Burhanpur', 'Buxar', 'Chandigarh', 'Chandrapur', 'Chapra', 'Chennai', 'Chinsurah', 'Chittoor', 'Coimbatore', 'Cuttack', 'Danapur', 'Darbhanga', 'Davanagere', 'Dehradun', 'Dehri', 'Delhi', 'Deoghar', 'Dewas', 'Dhanbad', 'Dharmavaram', 'Dhule', 'Dibrugarh', 'Dindigul', 'Durg', 'Durgapur', 'Eluru', 'Erode', 'Etawah', 'Faridabad', 'Farrukhabad', 'Fatehpur', 'Firozabad', 'Gandhidham', 'Gandhinagar', 'Gangtok', 'Gaya', 'Ghaziabad', 'Giridih', 'Gopalpur', 'Gorakhpur', 'Gudivada', 'Gulbarga', 'Guna', 'Guntakal', 'Guntur', 'Gurgaon', 'Guwahati', 'Gwalior', 'Hajipur', 'Haldia', 'Hapur', 'Haridwar', 'Hazaribagh', 'Hindupur', 'Hospet', 'Hosur', 'Howrah', 'Hubliâ€“Dharwad', 'Hyderabad', 'Ichalkaranji', 'Imphal', 'Indore', 'Jabalpur', 'Jaipur', 'Jalandhar', 'Jalgaon', 'Jalna', 'Jamalpur', 'Jammu', 'Jamnagar', 'Jamshedpur', 'Jaunpur', 'Jehanabad', 'Jhansi', 'Jodhpur', 'Jorhat', 'Junagadh', 'Kadapa', 'Kakinada', 'Kalyan-Dombivli', 'Kamarhati', 'Kanpur', 'Karaikudi', 'Karawal Nagar', 'Karimnagar', 'Karnal', 'Katihar', 'Katni', 'Kavali', 'Khammam', 'Khandwa', 'Kharagpur', 'Khora ', 'Kirari Suleman Nagar', 'Kishanganj', 'Kochi', 'Kolhapur', 'Kolkata', 'Kollam', 'Korba', 'Kota', 'Kottayam', 'Kozhikode', 'Kulti', 'Kumbakonam', 'Kurnool', 'Latur', 'Loni', 'Lucknow', 'Ludhiana', 'Machilipatnam', 'Madanapalle', 'Madhyamgram', 'Madurai', 'Mahbubnagar', 'Maheshtala', 'Malda', 'Malegaon', 'Mangalore', 'Mango', 'Mathura', 'Mau', 'Medininagar', 'Meerut', 'Mehsana', 'Mira-Bhayandar', 'Miryalaguda', 'Mirzapur', 'Moradabad', 'Morbi', 'Morena', 'Motihari', 'Mumbai', 'Munger', 'Muzaffarnagar', 'Muzaffarpur', 'Mysore', 'Nadiad', 'Nagaon', 'Nagercoil', 'Nagpur', 'Naihati', 'Nanded', 'Nandyal', 'Nangloi Jat', 'Narasaraopet', 'Nashik', 'Navi Mumbai', 'Nellore', 'New Delhi', 'Nizamabad', 'Noida', 'North Dumdum', 'Ongole', 'Orai', 'Ozhukarai', 'Pali', 'Pallavaram', 'Panchkula', 'Panihati', 'Panipat', 'Panvel', 'Parbhani', 'Patiala', 'Patna', 'Phagwara', 'Phusro', 'Pimpri-Chinchwad', 'Pondicherry', 'Proddatur', 'Pudukkottai', 'Pune', 'Purnia', 'Raebareli', 'Raichur', 'Raiganj', 'Raipur', 'Rajahmundry', 'Rajkot', 'Rajpur Sonarpur', 'Ramagundam', 'Ramgarh', 'Rampur', 'Ranchi', 'Ratlam', 'Raurkela Industrial Township', 'Rewa', 'Rohtak', 'Rourkela', 'Sagar', 'Saharanpur', 'Saharsa', 'Salem', 'Sambalpur', 'Sambhal', 'Sangli-Miraj & Kupwad', 'Sasaram', 'Satara', 'Satna', 'Secunderabad', 'Serampore', 'Shahjahanpur', 'Shimla', 'Shimoga', 'Shivpuri', 'Sikar', 'Silchar', 'Siliguri', 'Singrauli', 'Sirsa', 'Siwan', 'Solapur', 'Sonipat', 'South Dumdum', 'Sri Ganganagar', 'Srikakulam', 'Srinagar', 'Sultan Pur Majra', 'Surat', 'Surendranagar Dudhrej', 'Suryapet', 'Tadepalligudem', 'Tadipatri', 'Tenali', 'Tezpur', 'Thane', 'Thanjavur', 'Thiruvananthapuram', 'Thoothukudi', 'Thrissur', 'Tinsukia', 'Tiruchirappalli', 'Tirunelveli', 'Tirupati', 'Tiruppur', 'Tiruvottiyur', 'Tumkur', 'Udaipur', 'Udupi', 'Ujjain', 'Ulhasnagar', 'Uluberia', 'Unnao', 'Vadodara', 'Varanasi', 'Vasai-Virar', 'Vellore', 'Vijayanagaram', 'Vijayawada', 'Visakhapatnam', 'Warangal', 'Yamunanagar'])
# ip = st.text_input("Enter IP Address:")
# trans_status = st.selectbox("Select transaction status", ["Completed", "Failed", "Pending"])
# device_os = st.selectbox("Select device OS", ["Android", "iOS", "MacOS","Windows"])
# tran_freq = st.text_input("Enter transaction frequency")
merch_cat = st.selectbox("Select merchant category", ['Brand Vouchers and OTT', 'Donations and Devotion', 'Financial services and Taxes', 'Home delivery', 'Investment', 'More Services', 'Other', 'Purchases', 'Travel bookings', 'Utilities'])
# tran_channel = st.selectbox("Select transaction channel", ["In-store", "Mobile", "Online"])
# tran_amt_dev = st.text_input("Enter transaction amount deviation")
amt = st.text_input("Enter transaction amount")
# days = st.text_input("Enter days since last transaction")
button_clicked = st.button("Check transaction")
if button_clicked:
    with st.spinner("Checking transaction..."):
        time.sleep(5)
        st.success("Checked transaction!")
    st.write("Congratulations! Not a fraudulent transaction.")
