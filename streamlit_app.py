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

pickle_file_path = "UPI Fraud Detection updated.pkl"
# Load the saved XGBoost model from the pickle file
loaded_model = pickle.load(open(pickle_file_path, 'rb'))

tt = ["Bill Payment", "Investment", "Other", "Purchase", "Refund", "Subscription"]
pg = ["Google Pay", "HDFC", "ICICI UPI", "IDFC UPI", "Other", "Paytm", "PhonePe", "Razor Pay"]
tc = ['Agartala', 'Agra', 'Ahmedabad', 'Ahmednagar', 'Aizawl', 'Ajmer', 'Akola', 'Alappuzha', 'Aligarh', 'Allahabad', 'Alwar', 'Amaravati', 'Ambala', 'Ambarnath', 'Ambattur', 'Amravati', 'Amritsar', 'Amroha', 'Anand', 'Anantapur', 'Anantapuram', 'Arrah', 'Asansol', 'Aurangabad', 'Avadi', 'Bahraich', 'Ballia', 'Bally', 'Bangalore', 'Baranagar', 'Barasat', 'Bardhaman', 'Bareilly', 'Bathinda', 'Begusarai', 'Belgaum', 'Bellary', 'Berhampore', 'Berhampur', 'Bettiah', 'Bhagalpur', 'Bhalswa Jahangir Pur', 'Bharatpur', 'Bhatpara', 'Bhavnagar', 'Bhilai', 'Bhilwara', 'Bhimavaram', 'Bhind', 'Bhiwandi', 'Bhiwani', 'Bhopal', 'Bhubaneswar', 'Bhusawal', 'Bidar', 'Bidhannagar', 'Bihar Sharif', 'Bijapur', 'Bikaner', 'Bilaspur', 'Bokaro', 'Bongaigaon', 'Bulandshahr', 'Burhanpur', 'Buxar', 'Chandigarh', 'Chandrapur', 'Chapra', 'Chennai', 'Chinsurah', 'Chittoor', 'Coimbatore', 'Cuttack', 'Danapur', 'Darbhanga', 'Davanagere', 'Dehradun', 'Dehri', 'Delhi', 'Deoghar', 'Dewas', 'Dhanbad', 'Dharmavaram', 'Dhule', 'Dibrugarh', 'Dindigul', 'Durg', 'Durgapur', 'Eluru', 'Erode', 'Etawah', 'Faridabad', 'Farrukhabad', 'Fatehpur', 'Firozabad', 'Gandhidham', 'Gandhinagar', 'Gangtok', 'Gaya', 'Ghaziabad', 'Giridih', 'Gopalpur', 'Gorakhpur', 'Gudivada', 'Gulbarga', 'Guna', 'Guntakal', 'Guntur', 'Gurgaon', 'Guwahati', 'Gwalior', 'Hajipur', 'Haldia', 'Hapur', 'Haridwar', 'Hazaribagh', 'Hindupur', 'Hospet', 'Hosur', 'Howrah', 'Hubliâ€“Dharwad', 'Hyderabad', 'Ichalkaranji', 'Imphal', 'Indore', 'Jabalpur', 'Jaipur', 'Jalandhar', 'Jalgaon', 'Jalna', 'Jamalpur', 'Jammu', 'Jamnagar', 'Jamshedpur', 'Jaunpur', 'Jehanabad', 'Jhansi', 'Jodhpur', 'Jorhat', 'Junagadh', 'Kadapa', 'Kakinada', 'Kalyan-Dombivli', 'Kamarhati', 'Kanpur', 'Karaikudi', 'Karawal Nagar', 'Karimnagar', 'Karnal', 'Katihar', 'Katni', 'Kavali', 'Khammam', 'Khandwa', 'Kharagpur', 'Khora ', 'Kirari Suleman Nagar', 'Kishanganj', 'Kochi', 'Kolhapur', 'Kolkata', 'Kollam', 'Korba', 'Kota', 'Kottayam', 'Kozhikode', 'Kulti', 'Kumbakonam', 'Kurnool', 'Latur', 'Loni', 'Lucknow', 'Ludhiana', 'Machilipatnam', 'Madanapalle', 'Madhyamgram', 'Madurai', 'Mahbubnagar', 'Maheshtala', 'Malda', 'Malegaon', 'Mangalore', 'Mango', 'Mathura', 'Mau', 'Medininagar', 'Meerut', 'Mehsana', 'Mira-Bhayandar', 'Miryalaguda', 'Mirzapur', 'Moradabad', 'Morbi', 'Morena', 'Motihari', 'Mumbai', 'Munger', 'Muzaffarnagar', 'Muzaffarpur', 'Mysore', 'Nadiad', 'Nagaon', 'Nagercoil', 'Nagpur', 'Naihati', 'Nanded', 'Nandyal', 'Nangloi Jat', 'Narasaraopet', 'Nashik', 'Navi Mumbai', 'Nellore', 'New Delhi', 'Nizamabad', 'Noida', 'North Dumdum', 'Ongole', 'Orai', 'Ozhukarai', 'Pali', 'Pallavaram', 'Panchkula', 'Panihati', 'Panipat', 'Panvel', 'Parbhani', 'Patiala', 'Patna', 'Phagwara', 'Phusro', 'Pimpri-Chinchwad', 'Pondicherry', 'Proddatur', 'Pudukkottai', 'Pune', 'Purnia', 'Raebareli', 'Raichur', 'Raiganj', 'Raipur', 'Rajahmundry', 'Rajkot', 'Rajpur Sonarpur', 'Ramagundam', 'Ramgarh', 'Rampur', 'Ranchi', 'Ratlam', 'Raurkela Industrial Township', 'Rewa', 'Rohtak', 'Rourkela', 'Sagar', 'Saharanpur', 'Saharsa', 'Salem', 'Sambalpur', 'Sambhal', 'Sangli-Miraj & Kupwad', 'Sasaram', 'Satara', 'Satna', 'Secunderabad', 'Serampore', 'Shahjahanpur', 'Shimla', 'Shimoga', 'Shivpuri', 'Sikar', 'Silchar', 'Siliguri', 'Singrauli', 'Sirsa', 'Siwan', 'Solapur', 'Sonipat', 'South Dumdum', 'Sri Ganganagar', 'Srikakulam', 'Srinagar', 'Sultan Pur Majra', 'Surat', 'Surendranagar Dudhrej', 'Suryapet', 'Tadepalligudem', 'Tadipatri', 'Tenali', 'Tezpur', 'Thane', 'Thanjavur', 'Thiruvananthapuram', 'Thoothukudi', 'Thrissur', 'Tinsukia', 'Tiruchirappalli', 'Tirunelveli', 'Tirupati', 'Tiruppur', 'Tiruvottiyur', 'Tumkur', 'Udaipur', 'Udupi', 'Ujjain', 'Ulhasnagar', 'Uluberia', 'Unnao', 'Vadodara', 'Varanasi', 'Vasai-Virar', 'Vellore', 'Vijayanagaram', 'Vijayawada', 'Visakhapatnam', 'Warangal', 'Yamunanagar']
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
tran_city=st.selectbox("Select transaction city",tc)
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
    tc_oh = []
    for i in range(len(tc)):
        tc_oh.append(0)
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
            df = df.reindex(columns=['Amount', 'Year', 'Month','Transaction_Type','Payment_Gateway','Transaction_City','Transaction_State','Merchant_Category'])
            results = []
            for index, row in df.iterrows():
                input = []
                input.append(row.values[0])
                input.append(row.values[1])
                input.append(row.values[2])
                tt_oh[tt.index(row.values[3])]=1
                pg_oh[pg.index(row.values[4])]=1
                tc_oh[tc.index(row.values[5])]=1
                ts_oh[ts.index(row.values[6])]=1
                mc_oh[mc.index(row.values[7])]=1
                input = input+tt_oh+pg_oh+tc_oh+ts_oh+mc_oh
                prediction = loaded_model.predict([input])[0]
                results.append(prediction)
            df['fraud']=results
            st.success("Checked transactions!")
            st.markdown(download_csv(), unsafe_allow_html=True)
            
    else:
        with st.spinner("Checking transaction(s)..."):
            tt_oh[tt.index(tran_type)]=1
            pg_oh[pg.index(pmt_gateway)]=1
            tc_oh[tc.index(tran_city)]=1
            ts_oh[ts.index(tran_state)]=1
            mc_oh[mc.index(merch_cat)]=1
            input = []
            input.append(amt)
            input.append(year)
            input.append(month)
            input = input+tt_oh+pg_oh+tc_oh+ts_oh+mc_oh
            inputs = [input]
            result = loaded_model.predict(inputs)[0]
            st.success("Checked transaction!")
            if(result==0):
                st.write("Congratulations! Not a fraudulent transaction.")
            else:
                st.write("Oh no! This transaction is fraudulent.")
