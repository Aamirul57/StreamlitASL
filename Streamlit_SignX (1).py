#!/usr/bin/env python
# coding: utf-8

# In[19]:


import streamlit as st
import pandas as pd
import hashlib
import random
import cv2
import numpy as np
import os

# Display current working directory
# st.write("Current working directory:", os.getcwd())

# File paths
USERS_FILE = "users.csv"
PROGRESS_FILE = "progress.csv"
SIGN_DATA_FILE = "sign_language_data.csv"

# File paths for sign language videos
SIGN_LANGUAGE_DATA = {
    "Hello": "C:/Users/Puter/Downloads/HELLO ASL.mp4",
    "Good Morning": "C:/Users/Puter/Downloads/GOODMORNING ASL.mp4",
    "Good Afternoon": "C:/Users/Puter/Downloads/GOODAFTERNOON ASL.mp4",
    "Good Evening": "C:/Users/Puter/Downloads/GOODEVENING ASL.mp4",
    "Good Night": "C:/Users/Puter/Downloads/GOODNIGHT ASL.mp4",
    "Thank You": "C:/Users/Puter/Downloads/THANKYOU.mp4",
    "Sorry": "C:/Users/Puter/Downloads/SORRY ASL.mp4",
    "Please": "C:/Users/Puter/Downloads/PLEASE ASL.mp4",
    "Yes": "C:/Users/Puter/Downloads/YES ASL.mp4",
    "No": "C:/Users/Puter/Downloads/NO ASL.mp4",
    "How Are You?": "C:/Users/Puter/Downloads/HOWAREYOU ASL.mp4",
    "My Name Is...": "C:/Users/Puter/Downloads/MYNAMEIS ASL.mp4",
    "What Is Your Name?": "C:/Users/Puter/Downloads/WHATISYOURNAME ASL.mp4",
    "I Am Deaf": "C:/Users/Puter/Downloads/IMDEAF ASL.mp4",
    "I Am Hearing": "C:/Users/Puter/Downloads/IMHEARING ASL.mp4",
    "Where Is the Toilet?": "C:/Users/Puter/Downloads/WHEREISTHETOILET ASL.mp4",
    "Help me": "C:/Users/Puter/Downloads/HELPME ASL.mp4",
    "I Love You": "C:/Users/Puter/Downloads/ILOVEYOU ASL.mp4",
    "See You Later": "C:/Users/Puter/Downloads/SEEYOULATER ASL.mp4",
    "Goodbye": "C:/Users/Puter/Downloads/GOODBYE ASL.mp4",
}

# Basic ASL alphabet
ASL_ALPHABET = {
    'A': 'C:/Users/Puter/Downloads/A ASL.mp4',
    'B': 'C:/Users/Puter/Downloads/B ASL.mp4',
    'C': 'C:/Users/Puter/Downloads/C ASL.mp4',
    'D': 'C:/Users/Puter/Downloads/D ASL.mp4',
    'E': 'C:/Users/Puter/Downloads/E ASL.mp4',
    'F': 'C:/Users/Puter/Downloads/F ASL.mp4',
    'G': 'C:/Users/Puter/Downloads/G ASL.mp4',
    'H': 'C:/Users/Puter/Downloads/H ASL.mp4',
    'I': 'C:/Users/Puter/Downloads/I ASL.mp4',
    'J': 'C:/Users/Puter/Downloads/J ASL.mp4',
    'K': 'C:/Users/Puter/Downloads/K ASL.mp4',
    'L': 'C:/Users/Puter/Downloads/L ASL.mp4',
    'M': 'C:/Users/Puter/Downloads/M ASL.mp4',
    'N': 'C:/Users/Puter/Downloads/N ASL.mp4',
    'O': 'C:/Users/Puter/Downloads/O ASL.mp4',
    'P': 'C:/Users/Puter/Downloads/P ASL.mp4',
    'Q': 'C:/Users/Puter/Downloads/Q ASL.mp4',
    'R': 'C:/Users/Puter/Downloads/R ASL.mp4',
    'S': 'C:/Users/Puter/Downloads/S ASL.mp4',
    'T': 'C:/Users/Puter/Downloads/T ASL.mp4',
    'U': 'C:/Users/Puter/Downloads/U ASL.mp4',
    'V': 'C:/Users/Puter/Downloads/V ASL.mp4',
    'W': 'C:/Users/Puter/Downloads/W ASL.mp4',
    'X': 'C:/Users/Puter/Downloads/X ASL.mp4',
    'Y': 'C:/Users/Puter/Downloads/Y ASL.mp4',
    'Z': 'C:/Users/Puter/Downloads/Z ASL.mp4'
}

# Hashing function for passwords
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# Save user data to a CSV
def save_user_data(users_data):
    users_data.to_csv(USERS_FILE, index=False)

# Load user data from a CSV
def load_user_data():
    try:
        return pd.read_csv(USERS_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["username", "password"])

# Save progress data to CSV
def save_progress_data(progress_data):
    progress_data.to_csv(PROGRESS_FILE, index=False)

# Load progress data from CSV
def load_progress_data():
    try:
        return pd.read_csv(PROGRESS_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["username", "phrase"])

# Login system
def login():
    st.title("SignX: Next-Gen Technology for Deaf Communications")
    
    users_data = load_user_data()
    
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    hashed_password = hash_password(password)

    if st.button("Login"):
        if username in users_data['username'].values:
            stored_password = users_data[users_data['username'] == username]['password'].values[0]
            if stored_password == hashed_password:
                st.success(f"Welcome back, {username}!")
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
            else:
                st.error("Invalid password")
        else:
            st.error("Username not found")

# Sign-up system
def sign_up():
    st.subheader("Sign Up")
    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if password == confirm_password:
            users_data = load_user_data()
            if username not in users_data['username'].values:
                hashed_password = hash_password(password)
                new_user = pd.DataFrame([[username, hashed_password]], columns=["username", "password"])
                users_data = pd.concat([users_data, new_user], ignore_index=True)
                save_user_data(users_data)
                st.success("Account created successfully! Please log in.")
            else:
                st.error("Username already exists!")
        else:
            st.error("Passwords do not match")

# Training module
def training():
    st.subheader("Sign Language Training")
    for phrase, video in SIGN_LANGUAGE_DATA.items():
        st.write(f"Phrase: {phrase}")
        try:
            st.video(video)
        except Exception as e:
            st.error(f"Error loading video: {str(e)}")
        if st.button(f"Mark {phrase} as learned"):
            track_progress(st.session_state['username'], phrase)

# ASL alphabet training
def asl_alphabet_training():
    st.subheader("Learn the ASL Alphabet")
    for letter, video in ASL_ALPHABET.items():
        st.write(f"Letter: {letter}")
        try:
            st.video(video)
        except Exception as e:
            st.error(f"Error loading video: {str(e)}")
        if st.button(f"Mark {letter} as learned"):
            track_progress(st.session_state['username'], letter)

# Performance tracking
def track_progress(username, phrase):
    progress_data = load_progress_data()
    new_entry = pd.DataFrame([[username, phrase]], columns=["username", "phrase"])
    progress_data = pd.concat([progress_data, new_entry], ignore_index=True)
    save_progress_data(progress_data)
    st.success(f"{phrase} marked as learned!")

# Display user progress with "Completion Rate" in the table
def show_progress(username):
    st.subheader("Your Learning Progress")
    progress_data = load_progress_data()
    user_progress = progress_data[progress_data['username'] == username]
    
    total_phrases_available = 20  # Set the total number of available phrases/signs
    
    if user_progress.empty:
        st.write("No progress yet.")
    else:
        # Count the number of unique phrases learned by the user
        unique_phrases_learned = user_progress['phrase'].nunique()
        completion_rate = (unique_phrases_learned / total_phrases_available) * 100
        
        # Display completion message
        st.write(f"You have completed {unique_phrases_learned} out of {total_phrases_available} phrases "
                 f"({completion_rate:.1f}% complete).")
        
        # Add completion rate column instead of 'language'
        user_progress['completion_rate'] = f"{completion_rate:.1f}%"
        
        # Display the progress table with 'completion_rate' and 'phrase'
        st.table(user_progress[['username', 'completion_rate', 'phrase']])

# Evaluation module
def evaluation():
    st.subheader("Sign Language Evaluation")
    st.write("Watch the sign and identify it.")
    
    # Randomly select a phrase and the corresponding video
    random_phrase = random.choice(list(SIGN_LANGUAGE_DATA.keys()))
    video_url = SIGN_LANGUAGE_DATA[random_phrase]
    
    # Display the video
    st.video(video_url)
    
    # Input field for user's answer
    answer = st.text_input("What is the phrase?")
    
    if st.button("Submit"):
        # Normalize the user's answer
        normalized_answer = answer.strip().lower()
        normalized_correct_answer = random_phrase.strip().lower()
        
        # Debugging output to check the user's answer and the correct answer
        st.write(f"Your answer: '{normalized_answer}', Correct answer: '{normalized_correct_answer}'")
        
        # Check if the normalized answer matches the selected phrase
        if normalized_answer == normalized_correct_answer:
            st.success("Correct!")
            track_progress(st.session_state['username'], random_phrase)
        else:
            st.error("Try again!")

# Surprise feature: Sign with a Friend
def sign_with_friend():
    st.subheader("Sign with a Friend")
    st.write("Send a sign phrase to your friend and see if they can interpret it correctly!")

    friend_username = st.text_input("Friend's Username")
    phrase_to_send = st.selectbox("Select a phrase to send", list(SIGN_LANGUAGE_DATA.keys()))
    
    if st.button("Send Sign"):
        st.success(f"Sign '{phrase_to_send}' sent to {friend_username}!")

# Camera feature for sign detection
def sign_detection():
    st.subheader("Sign Detection Camera")
    st.write("Point your camera to detect ASL signs.")
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("Could not open webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to capture video")
            break
        
        # Display the resulting frame
        st.image(frame, channels="BGR")
        
        # Add sign detection logic here
        st.write("This is where sign detection logic would go.")

        if st.button("Stop"):
            break

    cap.release()
    cv2.destroyAllWindows()

# Main app flow
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.sidebar.title("SignX: Next-Gen Technology for Deaf Communications")
    login_option = st.sidebar.selectbox("Login or Sign Up", ["Login", "Sign Up"])

    if login_option == "Login":
        login()
    else:
        sign_up()
else:
    st.sidebar.title(f"Welcome, {st.session_state['username']}")
    action = st.sidebar.selectbox("Action", ["Training", "ASL Alphabet", "Your Progress", "Evaluation", "Sign with a Friend", "Sign Detection", "Logout"])

    # Action handling
    if action == "Training":
        training()
    elif action == "ASL Alphabet":
        asl_alphabet_training()
    elif action == "Your Progress":
        show_progress(st.session_state['username'])
    elif action == "Evaluation":
        evaluation()
    elif action == "Sign with a Friend":
        sign_with_friend()
    elif action == "Sign Detection":
        sign_detection()
    elif action == "Logout":
        st.session_state['logged_in'] = False
        st.session_state['username'] = None
        st.success("Logged out successfully!")


# In[ ]:





# In[ ]:





# In[ ]:




