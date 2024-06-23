import streamlit as st
import pygsheets
import pandas as pd
import urllib.parse
from datetime import datetime

# Authorize Google Sheets API client
client = pygsheets.authorize(service_account_file="weaversproject-5f5f2f634dab.json")

# Open the spreadsheet
spreadsheet = client.open("weavers")

# Load the sheets
sheet_customers = spreadsheet.worksheet_by_title("customers")
sheet_credentials = spreadsheet.worksheet_by_title("credentials")

default_whatsapp_message = "Hi. This is Kannan from JNV Silks."
encoded_message_whatsapp = urllib.parse.quote(default_whatsapp_message)

call_status = ["", "Not interested", "Followup-not picked", "Followup - proceed next","Not Required"]
whatsapp_status = ["", "Sent", "Followup", "Wrong_number"]

# Function to generate WhatsApp link
def generate_whatsapp_link(phone_number, message):
    base_url = "http://wa.me/"
    encoded_message = urllib.parse.quote(message)  # URL-encode the message
    whatsapp_link = f"{base_url}{phone_number}?text={encoded_message}"
    return whatsapp_link

# Function to authenticate user
def authenticate(username, password):
    credentials = sheet_credentials.get_all_records()
    for record in credentials:
        if record['username'] == username and record['password'] == password:
            return True
    return False

# Function to get rows to update based on action type and detail
def get_rows_to_update(action_type, action_detail):
    data = sheet_customers.get_all_records()
    df = pd.DataFrame(data)
    if action_type == "Call":
        if action_detail == "Initiate":
            rows_to_update = df[df['Call Status'] == '']
        elif action_detail == "Followup":
            rows_to_update = df[df['Call Status'].isin(['Followup-not picked', 'Followup - proceed next'])]
    elif action_type == "Whatsapp":
        if action_detail == "Initiate":
            rows_to_update = df[df['Whatsapp Status'] == '']
        elif action_detail == "Followup":
            rows_to_update = df[df['Whatsapp Status'].isin(['Sent', "Wrong_number"])]

    return rows_to_update, df

# Initial state for session
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'current_index' not in st.session_state:
    st.session_state.current_index = None
if 'df' not in st.session_state:
    st.session_state.df = None
if 'call_status_update' not in st.session_state:
    st.session_state.call_status_update = ""
if "whatsapp_status_update" not in st.session_state:
    st.session_state.whatsapp_status_update = ""
if "loaded" not in st.session_state:
    st.session_state.loaded = ""
if "done" not in st.session_state:
    st.session_state.done = False
if "rows_to_update" not in st.session_state:
    st.session_state["rows_to_update"] = ""
if "phone_number1" not in st.session_state:
    st.session_state["phone_number1"] = ""
if "phone_number2" not in st.session_state:
    st.session_state["phone_number2"] = ""


# Function to show the login page
def show_login_page():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful!")
            st.rerun()  # Reload the page to transition to the main page
        else:
            st.error("Invalid username or password")

# Function to show the shop communication management page
def show_shop_communication_page():
    st.title("Shop Communication Management")
    st.write(f"Logged in as: {st.session_state.username}")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()  # Reload the page to transition back to the login page

    action_type = st.selectbox("Select Action Type", ["Call", "Whatsapp", "Email"])

    if action_type == "Call":
        action_detail = st.selectbox("Select Call Action", ["Initiate", "Followup"])

    if action_type == "Whatsapp":
        action_detail = st.selectbox("Select Whatsapp Action", ["Initiate", "Followup"])

    # Proceed button to initiate the call and display call status update options
    if st.button("Proceed"):
        st.session_state["loaded"] = True
        st.session_state["done"] = False
        rows_to_update, df = get_rows_to_update(action_type, action_detail)
        st.session_state["rows_to_update"] = rows_to_update
        st.session_state.df = df
        if rows_to_update.empty:
            st.session_state["loaded"] = ""
            st.info("No Data Available...")

    if st.session_state["loaded"]:
        rows_to_update = st.session_state["rows_to_update"]
        df = st.session_state["df"]
        if not st.session_state["done"]:
            button_placeholder = st.empty()
            if button_placeholder.button("Complete"):
                st.session_state["loaded"] = False
                st.session_state["call_status_update"] = ""
                st.session_state["whatsapp_status_update"] = ""
                st.session_state["done"] = True
                st.session_state["phone_number1"] = ""
                st.session_state["phone_number2"] = ""
                button_placeholder.empty()
        
        if st.session_state["loaded"]:
            if not rows_to_update.empty:
                row = rows_to_update.iloc[0]
                st.session_state.current_index = row.name  # Store the row index
                st.markdown(f'<a href="tel:{row["Phone"]}" target="_blank">Click here to call {row["Phone"]}</a>', unsafe_allow_html=True)
                whatsapp_link = generate_whatsapp_link(row["Phone"], default_whatsapp_message)
                st.markdown(f'<a href="{whatsapp_link}" target="_blank">Click here to Whatsapp {row["Phone"]}</a>', unsafe_allow_html=True)
                
                if row["Phone number1"]:
                    st.markdown(f'<a href="tel:{row["Phone number1"]}" target="_blank">Click here to call {row["Phone number1"]}</a>', unsafe_allow_html=True)
                    whatsapp_link = generate_whatsapp_link(row["Phone number1"], default_whatsapp_message)
                    st.markdown(f'<a href="{whatsapp_link}" target="_blank">Click here to Whatsapp {row["Phone number1"]}</a>', unsafe_allow_html=True)
                
                if row["Phone number2"]:
                    st.markdown(f'<a href="tel:{row["Phone number2"]}" target="_blank">Click here to call {row["Phone number2"]}</a>', unsafe_allow_html=True)
                    whatsapp_link = generate_whatsapp_link(row["Phone number2"], default_whatsapp_message)
                    st.markdown(f'<a href="{whatsapp_link}" target="_blank">Click here to Whatsapp {row["Phone number2"]}</a>', unsafe_allow_html=True)

                st.write(f"Shop Name: {row['Shop_name']}")
                st.write(f"Initial Status: {row['Call Status']}")
                st.write(f"Address: {row['Address']}")
                st.write(f"Website: {row['Website']}")
                st.write(f"Number of Google Reviews: {row['Reviews']}")

                if st.session_state["call_status_update"] == "":
                    if st.selectbox("Update Call Status", call_status, key="call_status"):
                        st.session_state["call_status_update"] = st.session_state["call_status"]
                        cell_address = (st.session_state.current_index + 2, st.session_state.df.columns.get_loc('Call Status') + 1)  # Adjust for 1-indexed Google Sheets and header row
                        sheet_customers.update_value(cell_address, st.session_state["call_status"])
                        st.success("Call Status Updated.")
                else:
                    new_call_status = st.selectbox("Update Call Status", call_status, key="call_status")
                    if st.session_state["call_status_update"] != new_call_status:
                        st.session_state["call_status_update"] = new_call_status
                        cell_address = (st.session_state.current_index + 2, st.session_state.df.columns.get_loc('Call Status') + 1)  # Adjust for 1-indexed Google Sheets and header row
                        sheet_customers.update_value(cell_address, st.session_state["call_status"])
                        st.success("Call Status Updated.")

                if st.session_state["whatsapp_status_update"] == "":
                    if st.selectbox("Update Whatsapp Status", whatsapp_status, key="whatsapp_status"):
                        st.session_state["whatsapp_status_update"] = st.session_state["whatsapp_status"]
                        cell_address = (st.session_state.current_index + 2, st.session_state.df.columns.get_loc('Whatsapp Status') + 1)  # Adjust for 1-indexed Google Sheets and header row
                        sheet_customers.update_value(cell_address, st.session_state["whatsapp_status"])
                        st.success("Whatsapp Status Updated.")
                else:
                    new_whatsapp_status = st.selectbox("Update Whatsapp Status", whatsapp_status, key="whatsapp_status")
                    if st.session_state["whatsapp_status_update"] != new_whatsapp_status:
                        st.session_state["whatsapp_status_update"] = new_whatsapp_status
                        cell_address = (st.session_state.current_index + 2, st.session_state.df.columns.get_loc('Whatsapp Status') + 1)  # Adjust for 1-indexed Google Sheets and header row
                        sheet_customers.update_value(cell_address, st.session_state["whatsapp_status"])
                        st.success("Whatsapp Status Updated.")
                    
                if st.session_state["phone_number1"] == "":
                    phone_nm1 = st.text_input("Phone_number1",value=row["Phone number1"])
                    if phone_nm1!=row["Phone number1"]:
                        st.session_state["phone_number1"] = phone_nm1
                        cell_address = (st.session_state.current_index + 2, st.session_state.df.columns.get_loc('Phone number1') + 1)
                        sheet_customers.update_value(cell_address, st.session_state["phone_number1"])
                        st.success("phone number1 Updated.")
                else:
                    phone_nm1 = st.text_input("Phone_number1",value = st.session_state["phone_number1"])
                    if phone_nm1!=st.session_state["phone_number1"]:
                        st.session_state["phone_number1"] = phone_nm1
                        cell_address = (st.session_state.current_index + 2, st.session_state.df.columns.get_loc('Phone number1') + 1)  # Adjust for 1-indexed Google Sheets and header row
                        sheet_customers.update_value(cell_address, st.session_state["phone_number1"])
                        st.success("phone number1 Updated")
                
                if st.session_state["phone_number2"] == "":
                    phone_nm1 = st.text_input("Phone_number2",value=row["Phone number2"])
                    if phone_nm1!=row["Phone number2"]:
                        st.session_state["phone_number2"] = phone_nm1
                        cell_address = (st.session_state.current_index + 2, st.session_state.df.columns.get_loc('Phone number2') + 1)
                        sheet_customers.update_value(cell_address, st.session_state["phone_number2"])
                        st.success("phone number2 Updated.")
                else:
                    phone_nm1 = st.text_input("Phone_number2",value = st.session_state["phone_number2"])
                    if phone_nm1!=st.session_state["phone_number2"]:
                        st.session_state["phone_number2"] = phone_nm1
                        cell_address = (st.session_state.current_index + 2, st.session_state.df.columns.get_loc('Phone number2') + 1)
                        sheet_customers.update_value(cell_address, st.session_state["phone_number2"])
                        st.success("phone number2 Updated")

# Function to show the transaction details page

def show_transaction_page():
    st.title("Transaction Details")
    st.write(f"Logged in as: {st.session_state.username}")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()  # Reload the page to transition back to the login page

    # Load the account sheet specific to the logged-in user
    try:
        sheet_account = spreadsheet.worksheet_by_title(f"Accounts-{st.session_state.username}")
    except pygsheets.WorksheetNotFound:
        st.error("Account sheet not found for this user.")
        return

    data = sheet_account.get_all_records()
    df = pd.DataFrame(data)

    # Add a new transaction
    st.subheader("Add New Transaction")
    with st.form(key='add_transaction_form'):
        date = st.date_input("Date", value=datetime.now().date(), key='add_date')
        description = st.text_area("Description", key='add_description')
        # amount = st.number_input("Amount", min_value=0.0, step=0.01, format="%.2f", key='add_amount')
        amount =  st.text_area("Amount", key='add_amount')
        trans_type = st.selectbox("Type", ["Credit", "Debit"], key='add_type')
        if st.form_submit_button("Add Transaction"):
            new_transaction = [
                date.strftime("%Y-%m-%d"),
                description,
                amount,
                trans_type
            ]
            try:
                sheet_account.append_table(new_transaction, start='A2', end=None, dimension='ROWS', overwrite=False)
            except:
                pass
            st.success("Transaction added successfully.")
            st.rerun()  # Reload the page to show the updated data

    # Modify an existing transaction
    st.subheader("Modify Transaction")
    if not df.empty:
        selected_index = st.selectbox("Select Transaction to Modify", df.index, key='modify_select_index')
        selected_transaction = df.loc[selected_index]

        date = st.date_input("Date", value=datetime.strptime(selected_transaction["Date"], "%Y-%m-%d").date(), key='modify_date')
        description = st.text_area("Description", value=selected_transaction["Description"], key='modify_description')
        # amount = st.number_input("Amount", min_value=0.0, step=0.01, format="%.2f", value=float(selected_transaction["Amount"]), key='modify_amount')
        amount = st.text_area("Amount",value=selected_transaction["Amount"],key="modify_amount")
        trans_type = st.selectbox("Type", ["Credit", "Debit"], index=["Credit", "Debit"].index(selected_transaction["Type"]), key='modify_type')

        if st.button("Update Transaction", key='update_transaction'):
            # Update the dataframe
            df.at[selected_index, "Date"] = date.strftime("%Y-%m-%d")
            df.at[selected_index, "Description"] = description
            df.at[selected_index, "Amount"] = amount
            df.at[selected_index, "Type"] = trans_type

            # Update the specific row in the Google Sheet
            sheet_account.update_row(selected_index + 2, df.loc[selected_index].values.tolist())  # +2 to account for header and 0-based index
            st.success("Transaction updated successfully.")
            st.rerun()  # Reload the page to show the updated data
    else:
        st.info("No transactions to modify.")

    # Show top transactions
    st.subheader("Top Transactions")
    top_n = st.number_input("Number of Transactions to Show", min_value=1, step=1, value=5, key='top_n')
    # sorted_df = df.sort_values(by=["Amount"], ascending=False).head(top_n)
    sorted_df = df.tail(top_n)
    st.dataframe(sorted_df)

    # Calculate totals
    st.subheader("Total Credits and Debits")
    total_credit = df[df["Type"] == "Credit"]["Amount"].sum()
    total_debit = df[df["Type"] == "Debit"]["Amount"].sum()
    st.write(f"Total Credit: {total_credit}")
    st.write(f"Total Debit: {total_debit}")

# Determine which page to show
if not st.session_state.logged_in:
    show_login_page()
else:
    page = st.sidebar.selectbox("Select Page", ["Shop Communication", "Transaction Details"])
    if page == "Shop Communication":
        show_shop_communication_page()
    elif page == "Transaction Details":
        show_transaction_page()
