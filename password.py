import streamlit as st
import re
import random
import string

def check_password_strength(password):
    common_passwords = ["123456", "password", "123456789", "12345678", "12345", "1234567", "qwerty", "abcdef", "password1", "admin"]
    
    if password in common_passwords:
        return 0, ["❌ This password is too common. Choose a more secure one."], len(password)
    
    score = 0
    feedback = []
    
    # Length Check
    password_length = len(password)
    if password_length >= 8:
        score += 1
    else:
        feedback.append("🔴 Increase the password length to at least 8 characters.")
    
    # Uppercase Check
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("🔤 Include at least one uppercase letter.")
    
    # Lowercase Check
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("🔡 Include at least one lowercase letter.")
    
    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("🔢 Include at least one digit (0-9).")
    
    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("✨ Include at least one special character (!@#$%^&*).")
    
    return score, feedback, password_length

def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(length))

# Password history storage
if "password_history" not in st.session_state:
    st.session_state.password_history = []

# Streamlit UI
st.markdown("""
    <h1 style='text-align: center;'>🔐 Password Strength Meter</h1>
""", unsafe_allow_html=True)

st.write("### 🔑 Type your password below to analyze its strength:")
password = st.text_input("Enter Password:", type="password")

st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #45a049;
    }
    </style>
    """, unsafe_allow_html=True)

if st.button("🔍 Check Strength"):
    if password:
        score, feedback, password_length = check_password_strength(password)
        
        st.write(f"🔢 Password Length: {password_length} characters")
        
        if score == 0:
            st.error("❌ This password is too common. Choose a more secure one.")
        elif score <= 2:
            st.warning("⚠ Weak Password")
        elif score <= 4:
            st.info("🟡 Moderate Password")
        else:
            st.success("✅ Strong Password")
        
        if feedback:
            st.write("### 💡 Suggestions to Improve Your Password:")
            for tip in feedback:
                st.write(f"- {tip}")
        
        # Store password in history (only store last 5 passwords for security reasons)
        st.session_state.password_history.append(password)
        if len(st.session_state.password_history) > 5:
            st.session_state.password_history.pop(0)
    else:
        st.warning("⚠ Please enter a password to check its strength.")

# Choose password length
password_length = st.number_input("🔢 Choose password length:", min_value=8, max_value=32, value=12)

st.write("### 🔑 Need a Strong Password? Click Below!")
if st.button("🔄 Generate Strong Password"):
    strong_password = generate_strong_password(password_length)
    st.code(strong_password, language='text')

# Sidebar with app information
st.sidebar.title("ℹ️ About This App")
st.sidebar.info(
    "🔍 This Password Strength Meter evaluates the security of your passwords based on length, character variety, and complexity. "
    "🛡️ It provides feedback for improvement and can generate strong passwords for you."
)

# Sidebar with password requirements
st.sidebar.title("🔹 Requirements")
st.sidebar.markdown(
    "**1️⃣ Password Strength Criteria**\n\n"
    "🔒 A strong password should:\n"
    "- ✅ Be at least 8 characters long\n"
    "- 🔠 Contain uppercase & lowercase letters\n"
    "- 🔢 Include at least one digit (0-9)\n"
    "- ✨ Have one special character (!@#$%^&*)"
)

# Sidebar password history
st.sidebar.title("📜 Password History")
if st.session_state.password_history:
    for i, past_password in enumerate(reversed(st.session_state.password_history), 1):
        st.sidebar.text(f"{i}. {past_password}")
