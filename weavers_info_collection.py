import streamlit as st
import pygsheets

# Authorize pygsheets with the service account file
client = pygsheets.authorize(service_account_file="weaversproject-5f5f2f634dab.json")
# Open the spreadsheet
spreadsheet = client.open("weavers")
# Select the first sheet
sheet = spreadsheet.sheet1

# Set up the page configuration
st.set_page_config(page_title="Weaver's Community", page_icon="🧵", layout="centered")

# Custom CSS to enhance the appearance
st.markdown("""
    <style>
        .main {
            background-color: #f6fabb;
            color: #4b4b4b;
        }
        .title {
            font-size: 2.5em;
            color: #8a2be2;
            text-align: center;
            font-family: 'Georgia', serif;
            margin-top: 0;
        }
        .subtitle {
            font-size: 1.5em;
            color: #555;
            text-align: center;
            margin-bottom: 50px;
            font-family: 'Arial', sans-serif;
        }
        .form-container {
            background: white;
            padding: 2em;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin-top: 30px;
        }
        .stButton button {
            background: linear-gradient(90deg, #8a2be2, #6a0dad);
            border: none;
            color: white;
            padding: 10px 20px;
            font-size: 1.2em;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        .stButton button:hover {
            background: linear-gradient(90deg, #6a0dad, #8a2be2);
        }
        .success-message {
            font-size: 1.2em;
            color: #2ecc71;
            text-align: center;
        }
        .error-message {
            font-size: 1.2em;
            color: #e74c3c;
            text-align: center;
        }
        .content {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            margin-bottom: 30px;
        }
        .content h2 {
            color: #8a2be2;
        }
        .logo {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 50%;
        }
        .center {
            display: flex;
            justify-content: center;
            align-items: center;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for form fields if not already set
if "weaver_name" not in st.session_state:
    st.session_state["weaver_name"] = ""
if "address" not in st.session_state:
    st.session_state["address"] = ""
if "weaving_type" not in st.session_state:
    st.session_state["weaving_type"] = "Korvai"
if "whatsapp_number" not in st.session_state:
    st.session_state["whatsapp_number"] = ""
if "phone_number" not in st.session_state:
    st.session_state["phone_number"] = ""
if "email_address" not in st.session_state:
    st.session_state["email_address"] = ""
if "form_submitted" not in st.session_state:
    st.session_state["form_submitted"] = False

# Function to clear form fields
def clear_form():
    st.session_state["weaver_name"] = ""
    st.session_state["address"] = ""
    st.session_state["weaving_type"] = "Korvai"
    st.session_state["whatsapp_number"] = ""
    st.session_state["phone_number"] = ""
    st.session_state["email_address"] = ""

# Function to handle form submission
def submit_form():
    # Check mandatory fields
    if st.session_state["weaver_name"] and st.session_state["address"] and st.session_state["weaving_type"] and st.session_state["whatsapp_number"] and st.session_state["phone_number"]:
        # Append data to Google Sheet
        sheet.append_table(values=[
            st.session_state["weaver_name"], 
            st.session_state["address"], 
            st.session_state["weaving_type"], 
            st.session_state["whatsapp_number"], 
            st.session_state["phone_number"], 
            st.session_state["email_address"]
        ])
        # Set form submission state
        st.session_state["form_submitted"] = True
        # Clear form fields
        clear_form()
    else:
        st.error("Please fill in all mandatory fields.")

# Display success message if form is submitted
if st.session_state["form_submitted"]:
    st.markdown('<div class="center">', unsafe_allow_html=True)
    # st.image("logo.png", width=200)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<h1 class='title'>Welcome to the Weaver's Community</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Join us and help build a stronger, connected community of weavers</p>", unsafe_allow_html=True)
    st.markdown("<p class='success-message'>🌟 Your information has been successfully added! Thank you for joining our community. 🌟</p>", unsafe_allow_html=True)
else:
    # Logo and application title
    st.markdown('<div class="center">', unsafe_allow_html=True)
    # st.image("logo.png", width=200)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<h1 class='title'>Welcome to the Weaver's Community</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Join us and help build a stronger, connected community of weavers</p>", unsafe_allow_html=True)

    # Content about the community
    st.markdown("""
    <div class='content'>
        <h2>About Us</h2>
        <p>Weavers Community is dedicated to supporting and promoting the art of weaving. Our goal is to connect weavers from around the world, share knowledge, and provide a platform to showcase and sell their beautiful creations.</p>
        <p>By joining our community, you'll have access to resources, workshops, and a network of fellow weavers. Together, we can keep the tradition of weaving alive and thriving.</p>
    </div>
    """, unsafe_allow_html=True)

    # Form to get user input
    with st.form("weaver_form"):
        # st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        weaver_name = st.text_input("Weaver's Name", key="weaver_name")
        address = st.text_area("Address", key="address")
        weaving_type = st.selectbox("Weaving Type", ["Korvai", "Ettukol", "Dharmavaram","Thallu Machine Korvai"], key="weaving_type")
        whatsapp_number = st.text_input("WhatsApp Number", key="whatsapp_number")
        phone_number = st.text_input("Phone Number", key="phone_number")
        email_address = st.text_input("Email Address (Optional)", key="email_address")
        submit = st.form_submit_button("Submit", on_click=submit_form)

        st.markdown("</div>", unsafe_allow_html=True)

# To run the streamlit app, save this script and run `streamlit run script_name.py` in the terminal.
