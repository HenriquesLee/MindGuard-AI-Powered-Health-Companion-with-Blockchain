import streamlit as st
import pandas as pd
from blockchain import Blockchain
from db import initialize_db, create_user, get_user, get_all_blocks, add_block_to_db, get_user_blocks, add_post_block, get_post_blocks, add_comment, get_comments_for_post, add_like, count_likes, user_has_liked,get_all_posts
from user_auth import authenticate_user, get_current_user, register_user
from mental_health_ai import mental_health_chat, analyze_nutrition, analyze_fitness
from hashlib import sha256

# Initialize the SQLite database and blockchain
initialize_db()
blockchain = Blockchain()

# Hash function for data encryption
def hash_data(data):
    return sha256(data.encode()).hexdigest()

# User session management
if "username" not in st.session_state:
    st.session_state["username"] = None

# Set the background image using HTML and CSS
background_image = """
<style>
[data-testid="stAppViewContainer"] {
    background: url("https://media1.tenor.com/m/eSK4SyEXPr4AAAAC/anime-himmel.gif") no-repeat center center fixed;
    background-size: cover;
}

[data-testid="stSidebarContent"] {
    background-image: linear-gradient(to bottom right, #290e47, #341c5c);
}

[data-testid="stHeader"] {
    background-color: rgba(0, 0, 0, 0);
}

</style>
"""
st.markdown(background_image, unsafe_allow_html=True)

# Add the logo at the top of the app
st.image("/content/MindGuard.png", width=150)  # Adjust width as needed


# User Authentication
st.title("MindGuard: AI-Powered Health Companion with Blockchain")

if st.session_state["username"] is None:
    # Toggle between login and signup
    mode = st.radio("Select Mode:", ["Sign In", "Login"])

    if mode == "Sign In":
        st.subheader("Sign In")
        username = st.text_input("Username", "")
        password = st.text_input("Password", type="password")
        if st.button("Sign In"):
            user = get_user(username)
            if user and authenticate_user(username, password):
                st.session_state["username"] = username
                st.success(f"Welcome, {username}!")
                st.rerun()
            else:
                st.error("Invalid username or password.")

    elif mode == "Login":
        st.subheader("Login")
        new_username = st.text_input("New Username", "")
        email = st.text_input("Email (Gmail)", "")
        password = st.text_input("Password", type="password")
        if st.button("Submit"):
            if email.endswith("@gmail.com"):
                try:
                    register_user(new_username, password)
                    st.success("User created successfully! You can now sign in.")
                except Exception as e:
                    st.error("Error creating user: " + str(e))
            else:
                st.error("Please enter a valid Gmail address.")
else:
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select a section", ["Mental Health Check-in", "Nutrition Tracker", "Fitness Tracker", "Community Feed", "Your Personal Blockchain", "Global Blockchain", "Logout"])

    user = get_current_user(st.session_state["username"])

    if user is not None:
        if page == "Mental Health Check-in":
            st.subheader("AI-Powered Mental Health Check-in")
            user_input = st.text_input("How are you feeling today?", "")

            if st.button("Submit"):
                ai_response = mental_health_chat(user_input)
                st.write(ai_response)

                # Save mood and encrypt data
                action_data = f"Mental health check-in: {user_input}, AI response: {ai_response}"
                blockchain.add_block(user["username"], action_data)
                add_block_to_db(user["username"], action_data)

        elif page == "Nutrition Tracker":
            st.subheader("Nutrition Tracker")
            food_item = st.text_input("Enter the food item:", "")
            quantity = st.text_input("Enter the quantity:", "")

            if st.button("Analyze"):
                nutrition_response = analyze_nutrition(food_item, quantity)
                st.write(nutrition_response)

                # Encrypt and create a block for the nutrition analysis
                action_data = f"Nutrition analysis: {food_item}, Quantity: {quantity}, AI response: {nutrition_response}"
                blockchain.add_block(user["username"], action_data)
                add_block_to_db(user["username"], action_data)

        elif page == "Fitness Tracker":
            st.subheader("Fitness Tracker")
            activity = st.text_input("Enter the activity (e.g., running, weightlifting):", "")
            duration = st.text_input("Duration:", "")

            if st.button("Analyze"):
                fitness_response = analyze_fitness(activity, duration)
                st.write(fitness_response)

                # Encrypt and create a block for the fitness analysis
                action_data = f"Fitness analysis: {activity}, Duration: {duration}, AI response: {fitness_response}"
                blockchain.add_block(user["username"], action_data)
                add_block_to_db(user["username"], action_data)

        elif page == "Your Personal Blockchain":
            st.subheader("Your Personal Blockchain")
            personal_blocks = get_user_blocks(user["username"])

            if personal_blocks:
                data = [{"Block ID": hash_data(str(block['id'])),
                         "Hashed Data": hash_data(block['action_data']),
                         "Timestamp": hash_data(block['timestamp'])} for block in personal_blocks]

                df = pd.DataFrame(data)
                st.dataframe(df)
            else:
                st.write("No blocks found for your personal blockchain.")

        elif page == "Global Blockchain":
            st.subheader("Global Blockchain")
            global_blocks = get_all_blocks()

            if global_blocks:
                data = [{"Block ID": hash_data(str(block['id'])),
                         "Hashed Data": hash_data(block['action_data']),
                         "Timestamp": hash_data(block['timestamp'])} for block in global_blocks]

                df = pd.DataFrame(data)
                st.dataframe(df)
            else:
                st.write("No global blocks available.")

        # Existing code for Community Posts
        elif page == "Community Feed":
            st.subheader("Community Feed")
            post_content = st.text_input("What's on your mind?")
            
            if st.button("Post"):
                if post_content:
                    add_post_block(user["username"], post_content)  # No need to pass block_id
                    st.success("Post added!")
                    st.rerun()  # Refresh to show new post
                else:
                    st.error("Please enter some content.")
            
            # Display all posts
            posts = get_all_posts()
            
            for post in posts:
                st.write(f"**{post['content']}**")
                st.write(f"*Posted on: {post['timestamp']}*")
                
                comment_input = st.text_input("Add a comment:", key=post['post_id'])
                if st.button("Comment", key=f"comment_{post['post_id']}"):
                    if comment_input:
                        add_comment(post['post_id'], user["username"], comment_input)
                        st.success("Comment added!")
                        st.rerun()  # Refresh to show new comment
                    else:
                        st.error("Please enter a comment.")
                
                # Display comments for each post
                comments = get_comments_for_post(post['post_id'])
                for comment in comments:
                    st.write(f"{comment['username']}: {comment['content']} (Posted on: {comment['timestamp']})")


        elif page == "Logout":  
            st.subheader("Farewell for now, we’ll miss your vibes! Come back soon!🎉")      
            if st.button("Logout"):
                st.session_state["username"] = None
                st.rerun()
