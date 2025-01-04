import streamlit as st
from openai import ChatCompletion

# Initialize OpenAI API (replace with your key and endpoint)
API_KEY = "your_openai_api_key"

# Function to generate technical questions based on tech stack
def generate_questions(tech_stack):
    prompt = (
        f"You are an expert in technical hiring. Generate 3-5 technical questions tailored for the following tech stack: {tech_stack}. "
        "Make sure the questions assess fundamental and advanced proficiency."
    )
    response = ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# Streamlit UI
def main():
    st.set_page_config(page_title="TalentScout Hiring Assistant", layout="centered")

    st.title("TalentScout: Hiring Assistant Chatbot")
    st.markdown(
        """
        Welcome to TalentScout, your virtual hiring assistant. Please provide your details and engage in a conversation to get started.
        """
    )

    # Tabs for better organization
    tab1, tab2 = st.tabs(["Candidate Information", "Chatbot"])

    # Tab 1: Candidate Information
    with tab1:
        st.header("Candidate Information")
        full_name = st.text_input("Full Name", placeholder="Enter your full name")
        email = st.text_input("Email Address", placeholder="Enter a valid email")
        phone = st.text_input("Phone Number", placeholder="Enter your phone number")
        years_experience = st.number_input("Years of Experience", min_value=0, max_value=50, step=1)
        desired_position = st.text_input("Desired Position(s)", placeholder="e.g., Software Engineer")
        current_location = st.text_input("Current Location", placeholder="City, Country")
        tech_stack = st.text_area(
            "Tech Stack", 
            placeholder="List programming languages, frameworks, databases, and tools (e.g., Python, Django, PostgreSQL)"
        )

        if st.button("Submit Information"):
            if not full_name or not email or not tech_stack:
                st.error("Please fill out all required fields.")
            else:
                st.success("Information submitted successfully! Proceed to the chatbot tab.")

    # Tab 2: Chatbot Interaction
    with tab2:
        st.header("Chat with the Assistant")
        st.markdown("Engage in a conversation with the assistant to receive tailored questions.")

        conversation_log = st.session_state.get("conversation_log", [])

        user_input = st.text_input("Your Message", placeholder="Type your message here")
        if st.button("Send") and user_input:
            # Display user message
            conversation_log.append({"role": "user", "content": user_input})
            st.write(f"**You**: {user_input}")

            # Generate response
            if user_input.lower() in ["exit", "quit"]:
                bot_response = "Thank you for chatting with TalentScout. We will review your details and get back to you!"
            elif "tech stack" in user_input.lower() and tech_stack:
                bot_response = generate_questions(tech_stack)
            else:
                # Default fallback
                bot_response = "I'm here to assist! Could you please clarify or provide more information?"

            conversation_log.append({"role": "assistant", "content": bot_response})
            st.write(f"**Assistant**: {bot_response}")

        # Save conversation log in session
        st.session_state["conversation_log"] = conversation_log

        if st.button("End Chat"):
            st.write("Thank you for using TalentScout! The chat has been reset.")
            st.session_state["conversation_log"] = []

if __name__ == "__main__":
    main()
