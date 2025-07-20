import streamlit as st
import pandas as pd

st.title("Student Performance Analysis")

# Load the ranked DataFrame
try:
    df_ranked = pd.read_csv('/content/student_dataset.csv')
    df_ranked['Total_Marks'] = df_ranked['Math'] + df_ranked['Physics'] + df_ranked['Chemistry']
    df_ranked['Final_Rank'] = df_ranked.sort_values(by=['Total_Marks', 'Math', 'Physics', 'Chemistry'], ascending=[False, False, False, False]).reset_index().index + 1
    # Convert Roll No. and Phone No. to string for consistent comparison
    df_ranked['Roll No.'] = df_ranked['Roll No.'].astype(str)
    df_ranked['Phone_No.'] = df_ranked['Phone_No.'].astype(str)


    # Add Rank_Category
    bins = [0, 100, 500, df_ranked['Final_Rank'].max()]
    labels = ['Top 100', 'Top 500', 'Below Top 500']
    df_ranked['Rank_Category'] = pd.cut(df_ranked['Final_Rank'], bins=bins, labels=labels, include_lowest=True)

except FileNotFoundError:
    st.error("student_dataset.csv not found. Please make sure the file is in the correct location.")
    df_ranked = pd.DataFrame() # Create an empty DataFrame to prevent errors

# --- Login Section ---
st.sidebar.header("Login")
login_type = st.sidebar.radio("Select Login Type:", ("Student", "Admin"))

if login_type == "Student":
    st.sidebar.subheader("Student Login")
    student_roll_no = st.sidebar.text_input("Roll Number")
    student_phone_no = st.sidebar.text_input("Phone Number", type="password") # Added password input back
    student_login_button = st.sidebar.button("Student Login")

    if student_login_button:
        if not df_ranked.empty:
            # Check if student credentials match (using Roll Number and Phone Number)
            student_data = df_ranked[(df_ranked['Roll No.'] == student_roll_no) & (df_ranked['Phone_No.'] == student_phone_no)]


            if not student_data.empty:
                st.success(f"Welcome, {student_data['Student_Names'].iloc[0]}!")
                st.subheader("Your Performance Details:")
                # Display student's specific details in paragraph format
                student_info = student_data.iloc[0]
                st.write(f"**Name:** {student_info['Student_Names']}")
                st.write(f"**Roll Number:** {student_info['Roll No.']}")
                st.write(f"**School Name:** {student_info['School Name']}")
                st.write(f"**Math Marks:** {student_info['Math']}")
                st.write(f"**Physics Marks:** {student_info['Physics']}")
                st.write(f"**Chemistry Marks:** {student_info['Chemistry']}")
                st.write(f"**Total Marks:** {student_info['Total_Marks']}")
                st.write(f"**Final Rank:** {student_info['Final_Rank']:.0f}") # Display Final_Rank
                st.write(f"**Rank Category:** {student_info['Rank_Category']}") # Display Rank_Category
                st.write(f"**Grade:** {student_info['Grade']}")
                st.write(f"**Comment:** {student_info['Comment']}") # Added Comment
                st.write(f"**Student Address:** {student_info['Student Address']}")
                st.write(f"**Phone Number:** {student_info['Phone_No.']}") # Added Phone Number

            else:
                st.error("Invalid Roll Number or Phone Number.")
        else:
            st.warning("Data not loaded. Cannot perform login.")

elif login_type == "Admin":
    st.sidebar.subheader("Admin Login")
    admin_username = st.sidebar.text_input("Username")
    admin_password = st.sidebar.text_input("Password", type="password")
    admin_login_button = st.sidebar.button("Admin Login")

    # --- Admin Credentials (replace with secure method in production) ---
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "password123" # Replace with a strong password

    if admin_login_button:
        if admin_username == ADMIN_USERNAME and admin_password == ADMIN_PASSWORD:
            st.success("Welcome, Admin!")
            st.subheader("All Student Performance Data:")
            # Display all student data for admin, including Phone_No. and Final_Rank, excluding Initial_Rank
            if not df_ranked.empty:
                 st.dataframe(df_ranked[['Student_Names', 'School Name', 'Roll No.', 'Phone_No.', 'Math', 'Physics', 'Chemistry', 'Total_Marks', 'Final_Rank', 'Rank_Category', 'Grade', 'Comment', 'Student Address']])
            else:
                 st.info("Data not loaded. Cannot display student data.")
        else:
            st.error("Invalid Admin Username or Password.")

# --- Main Content Area (can be used for general info or visualizations before login) ---
st.subheader("Overall Student Performance Overview")
if not df_ranked.empty:
    st.write(f"Total number of students: {len(df_ranked)}")
    # Add overall visualizations here if desired (e.g., histogram of Total_Marks)
else:
    st.info("Load data to see overall performance overview.")
