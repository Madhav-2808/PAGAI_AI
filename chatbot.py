import streamlit as st
from openai import ChatCompletion

# Initialize OpenAI API (replace with your key and endpoint)
API_KEY = "Use your API here"

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
    st.title("TalentScout: Hiring Assistant Chatbot")

    # Sidebar for candidate information
    st.sidebar.header("Candidate Information")
    full_name = st.sidebar.text_input("Full Name")
    email = st.sidebar.text_input("Email Address")
    phone = st.sidebar.text_input("Phone Number")
    years_experience = st.sidebar.number_input("Years of Experience", min_value=0, max_value=50, step=1)
    desired_position = st.sidebar.text_input("Desired Position(s)")
    current_location = st.sidebar.text_input("Current Location")
    tech_stack = st.sidebar.text_area(
        "Tech Stack", 
        "List the programming languages, frameworks, databases, and tools you are proficient in."
    )

    if st.sidebar.button("Submit Information"):
        if not full_name or not email or not tech_stack:
            st.sidebar.error("Please fill out all required fields.")
        else:
            st.sidebar.success("Information submitted successfully!")

    # Chat Interface
    st.header("Chat with the Assistant")
    conversation_log = st.session_state.get("conversation_log", [])

    user_input = st.text_input("Your Message")
    if st.button("Send") and user_input:
        # Display user message
        conversation_log.append({"role": "user", "content": user_input})
        st.write(f"You: {user_input}")

        # Generate response
        if user_input.lower() in ["exit", "quit"]:
            bot_response = "Thank you for chatting with TalentScout. We will review your details and get back to you!"
        elif "tech stack" in user_input.lower() and tech_stack:
            bot_response = generate_questions(tech_stack)
        else:
            # Default fallback
            bot_response = "I'm here to assist! Could you please clarify or provide more information?"

        conversation_log.append({"role": "assistant", "content": bot_response})
        st.write(f"Assistant: {bot_response}")

    # Save conversation log in session
    st.session_state["conversation_log"] = conversation_log

    # End chat button
    if st.button("End Chat"):
        st.write("Thank you for using TalentScout!")
        st.session_state["conversation_log"] = []

if __name__ == "__main__":
    main()
