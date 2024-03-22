import streamlit as st
from nselib import derivatives

# Title of the dashboard
st.title('Live Options Chain Dashboard')

# Fetching live options chain data
symbol = st.sidebar.selectbox('Select Symbol', ['banknifty', 'nifty', 'reliance', 'sbin'])
expiry_date = st.sidebar.date_input('Select Expiry Date')

data = derivatives.nse_live_option_chain(symbol, expiry_date.strftime('%d-%m-%Y'))

# Displaying the data in a table
st.dataframe(data)
