import streamlit as st
from constants import currency_list
from currency_convertor import get_exchange_rate, convert_currency
import datetime
#import humanize

# Set the title of the Streamlit app
st.title(':dollar: Currency Converter')

# Description text to help the user understand the input requirements
st.markdown('Enter the amount and choose the currencies to see the conversion result.')

# Select the base currency and target currency from predefined currency lists
base_currency = st.selectbox('Base Currency', currency_list, index=currency_list.index("IRR"))
target_currency = st.selectbox('Target Currency', currency_list, index=currency_list.index("USD"))

# Input field for the amount the user wants to convert
amount = st.number_input('Enter the amount:', value=1.0)

# Check if the user has entered a valid amount and selected currencies
if amount > 0 and base_currency and target_currency:
    # Fetch exchange rate and the last update time
    exchange_rate, time_update = get_exchange_rate(base_currency, target_currency)
    
    # Calculate the time since the exchange rate was last updated
    time_diff = datetime.datetime.now() - datetime.datetime.fromtimestamp(time_update)
    #time_ago = humanize.naturaltime(time_diff)

    # If the exchange rate was successfully retrieved, show the conversion result
    if exchange_rate:
        convert_result = convert_currency(amount, exchange_rate)
        
        # Display exchange rate and when it was last updated
        st.success(f"✅ Exchange Rate: {exchange_rate:.4f} (Last updated: {time_diff})")
        
        # Layout for displaying conversion metrics in a row
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Base Currency", value=f"{amount:.2f} {base_currency}")
        
        # Display a right arrow icon between the base and target currency values
        col2.markdown("<h1 style='text-align: center;color: green; margin: 0;'>&#8594;</h1>", unsafe_allow_html=True)
        
        # Show the result of the currency conversion
        col3.metric(label="Target Currency", value=f"{convert_result:.2f} {target_currency}")
    else:
        st.error("Error: Unable to fetch the exchange rate. Please try again.")