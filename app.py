import streamlit as st

with st.form("my_form"):
   st.write("PAPAA - PriorAuth Patient Access API")
   entence = st.text_input('Put your JSON here')
   my_color = st.selectbox('Pick a profile', ['Claim','ClaimResponse','Patient','Practitioner'])
   st.form_submit_button('Submit')

# This is outside the form
st.write(entence)
st.write(my_color)