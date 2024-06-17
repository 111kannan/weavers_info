import streamlit as st
import pygsheets
import pandas as pd
import time

# Authorize the pygsheets client with the service account
client = pygsheets.authorize(service_account_file="weaversproject-5f5f2f634dab.json")

# Open the Google Spreadsheet and access the specific worksheet
spreadsheet = client.open("weavers")
sheet = spreadsheet.worksheet_by_title("customers")

# App title
st.title("Shop Communication Management")

# Dropdown to select communication type
action_type = st.selectbox("Select Action Type", ["Call", "Whatsapp", "Email"])

# Initialize variable for secondary dropdown
if action_type == "Call":
    action_detail = st.selectbox("Select Call Action", ["Initiate", "Followup"])

def get_rows_to_update():
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    if action_detail == "Initiate":
        rows_to_update = df[df['Call Status'] == '']
    if action_detail == "Followup":
        rows_to_update = df[df['Call Status'].isin(['Followup-not picked', 'Followup - proceed next'])]
    return rows_to_update, df

# Initialize session state variables
if 'current_index' not in st.session_state:
    st.session_state.current_index = None

if 'df' not in st.session_state:
    st.session_state.df = None

if 'call_status' not in st.session_state:
    st.session_state.call_status = ""

# Proceed button to initiate the call and display call status update options
if st.button("Proceed"):
    rows_to_update, df = get_rows_to_update()
    if not rows_to_update.empty:
        # Get the first row to update
        row = rows_to_update.iloc[0]
        st.session_state.current_index = row.name  # Store the row index
        st.session_state.df = df
        st.markdown(f'<a href="tel:{row["Phone"]}" target="_blank">Click here to call {row["Phone"]}</a>', unsafe_allow_html=True)
        
        st.session_state.call_status_update = st.selectbox("Update Call Status", ["", "Not interested", "Followup-not picked", "Followup - proceed next"], key="call_status")
        st.write(r"Shop Name: "+ str(row["Shop_name"]))
        st.write(f"Current Status: "+ str(row["Call Status"]))
        st.write(f"Address: "+ str(row["Address"]))
        st.write(f"Website"+ str(row["Website"]))
        st.write(f"Number of google Reviews: "+ str(row["Reviews"]))

    else:
        st.info("No calls pending update.")

# Display the "Done" button only if there's a call status to update
# if st.session_state.call_status_update:
if st.session_state["call_status"]!="":
    # if st.button("Done", key=f"done_{st.session_state.current_index}"):
    cell_address = (st.session_state.current_index + 2, st.session_state.df.columns.get_loc('Call Status') + 1)  # Adjust for 1-indexed Google Sheets and header row
    sheet.update_value(cell_address, st.session_state["call_status"])
    st.success("Updated.")
    