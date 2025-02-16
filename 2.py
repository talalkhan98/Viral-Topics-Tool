import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit_authenticator as stauth

# User authentication setup
names = ['User  1', 'User  2']
usernames = ['user1', 'user2']
passwords = ['password1', 'password2']

authenticator = stauth.Authenticate(names, usernames, passwords, 'some_cookie_name', 'some_signature_key', cookie_expiry_days=30)

# Login
name, authentication_status = authenticator.login('Login', 'main')

if authentication_status:
    st.write(f'Welcome {name}')

    # Sidebar for user input
    st.sidebar.header("User  Input")
    
    # Function to get user input
    def get_user_input():
        niche = st.sidebar.text_input("Enter Niche:")
        return niche

    # Main function to run the app
    def main():
        niche = get_user_input()
        
        if niche:
            st.write(f"You entered: {niche}")
            analyze_niche(niche)

    # Function to analyze the niche
    def analyze_niche(niche):
        st.write(f"Analyzing the niche: {niche}")
        
        # Example data for visualization
        data = {
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
            'Views': np.random.randint(1000, 5000, size=5),
            'Engagement': np.random.rand(5)
        }
        
        df = pd.DataFrame(data)
        
        # Plotting the data
        st.subheader("Niche Performance Over Time")
        fig, ax = plt.subplots()
        sns.lineplot(data=df, x='Month', y='Views', ax=ax, marker='o')
        ax.set_title(f"Views for {niche} Over Time")
        ax.set_xlabel("Month")
        ax.set_ylabel("Number of Views")
        st.pyplot(fig)

        # Comment section
        st.subheader("Community Comments")
        comments = st.text_area("Leave a comment:")
        if st.button("Submit"):
            if comments:
                st.success("Comment submitted!")
                st.write(f"Comment: {comments}")
            else:
                st.warning("Please enter a comment.")

    main()

else:
    st.warning("Please enter your username and password.")
