import streamlit as st
import pandas as pd
import hashlib
import random
import cv2
import numpy as np

# File paths
USERS_FILE = "users.csv"
PROGRESS_FILE = "progress.csv"
SIGN_DATA_FILE = "sign_language_data.csv"

# Sign language data for training
SIGN_LANGUAGE_DATA = {
    "Hello": "https://files.fm/f/7yebgh6a3c?fk=9c466d1d",
    "Good Morning": "videos/good_morning_asl.mp4",
    "Good Afternoon": "videos/good_afternoon_asl.mp4",
    "Good Evening": "videos/good_evening_asl.mp4",
    "Good Night": "videos/good_night_asl.mp4",
    "Thank You": "videos/thank_you_asl.mp4",
    "Sorry": "videos/sorry_asl.mp4",
    "Please": "videos/please_asl.mp4",
    "Yes": "videos/yes_asl.mp4",
    "No": "videos/no_asl.mp4",
    "How Are You?": "videos/how_are_you_asl.mp4",
    "My Name Is...": "videos/my_name_is_asl.mp4",
    "What Is Your Name?": "videos/what_is_your_name_asl.mp4",
    "I Am Deaf": "videos/i_am_deaf_asl.mp4",
    "I Am Hearing": "videos/i_am_hearing_asl.mp4",
    "Where Is the Toilet?": "videos/where_is_the_toilet_asl.mp4",
    "Help": "videos/help_asl.mp4",
    "I Love You": "videos/i_love_you_asl.mp4",
    "See You Later": "videos/see_you_later_asl.mp4",
    "Goodbye": "videos/goodbye_asl.mp4",
}


# Basic ASL alphabet
ASL_ALPHABET = {
    'A': 'asl_alphabet_a.mp4',
    'B': 'asl_alphabet_b.mp4',
    'C': 'asl_alphabet_c.mp4',
    'D': 'asl_alphabet_d.mp4',
    'E': 'asl_alphabet_e.mp4',
    'F': 'asl_alphabet_f.mp4',
    'G': 'asl_alphabet_g.mp4',
    'H': 'asl_alphabet_h.mp4',
    'I': 'asl_alphabet_i.mp4',
    'J': 'asl_alphabet_j.mp4',
    'K': 'asl_alphabet_k.mp4',
    'L': 'asl_alphabet_l.mp4',
    'M': 'asl_alphabet_m.mp4',
    'N': 'asl_alphabet_n.mp4',
    'O': 'asl_alphabet_o.mp4',
    'P': 'asl_alphabet_p.mp4',
    'Q': 'asl_alphabet_q.mp4',
    'R': 'asl_alphabet_r.mp4',
    'S': 'asl_alphabet_s.mp4',
    'T': 'asl_alphabet_t.mp4',
    'U': 'asl_alphabet_u.mp4',
    'V': 'asl_alphabet_v.mp4',
    'W': 'asl_alphabet_w.mp4',
    'X': 'asl_alphabet_x.mp4',
    'Y': 'asl_alphabet_y.mp4',
    'Z': 'asl_alphabet_z.mp4'
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
            hashed_password = hash_password(password)
            new_user = pd.DataFrame([[username, hashed_password]], columns=["username", "password"])
            users_data = pd.concat([users_data, new_user], ignore_index=True)
            save_user_data(users_data)
            st.success("Account created successfully! Please log in.")
        else:
            st.error("Passwords do not match")

# Training module
def training():
    st.subheader("Sign Language Training")
    for phrase, video in SIGN_LANGUAGE_DATA.items():
        st.write(f"Phrase: {phrase}")
        st.video(video)
        if st.button(f"Mark {phrase} as learned"):
            track_progress(st.session_state['username'], phrase)

# ASL alphabet training
def asl_alphabet_training():
    st.subheader("Learn the ASL Alphabet")
    for letter, video in ASL_ALPHABET.items():
        st.write(f"Letter: {letter}")
        st.video(video)
        if st.button(f"Mark {letter} as learned"):
            track_progress(st.session_state['username'], letter)

# Performance tracking
def track_progress(username, phrase):
    progress_data = load_progress_data()
    new_entry = pd.DataFrame([[username, phrase]], columns=["username", "phrase"])
    progress_data = pd.concat([progress_data, new_entry], ignore_index=True)
    save_progress_data(progress_data)
    st.success(f"{phrase} marked as learned!")

# Display user progress
def show_progress(username):
    st.subheader("Your Learning Progress")
    progress_data = load_progress_data()
    user_progress = progress_data[progress_data['username'] == username]
    st.table(user_progress)

# Evaluation module
def evaluation():
    st.subheader("Sign Language Evaluation")
    st.write("Watch the sign and identify it.")
    
    random_phrase = random.choice(list(SIGN_LANGUAGE_DATA.keys()))
    st.video(SIGN_LANGUAGE_DATA[random_phrase])
    
    answer = st.text_input("What is the phrase?")
    
    if st.button("Submit"):
        if answer.lower() == random_phrase.lower():
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

    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to capture video")
            break
        
        # Display the resulting frame
        st.image(frame, channels="BGR")
        
        # Add sign detection logic here
        # For demonstration, we will just show a message.
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
    action = st.sidebar.selectbox("Action", ["Training", "ASL Alphabet", "Evaluation", "View Progress", "Sign with a Friend", "Sign Detection", "Logout"])

    if action == "Training":
        training()

    elif action == "ASL Alphabet":
        asl_alphabet_training()

    elif action == "Evaluation":
        evaluation()

    elif action == "View Progress":
        show_progress(st.session_state['username'])

    elif action == "Sign with a Friend":
        sign_with_friend()

    elif action == "Sign Detection":
        sign_detection()

    elif action == "Logout":
        st.session_state['logged_in'] = False
        st.session_state['username'] = None
        st.success("Logged out successfully!")
