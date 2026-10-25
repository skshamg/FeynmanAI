import json
import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ServerError
import streamlit as st

# 1. Load API Key & Setup Client
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY is missing from your .env file!")
    st.stop()

client = genai.Client(api_key=api_key)

# 2. Page Configuration
st.set_page_config(
    page_title="FeynmanAI | Socratic Inversion Engine",
    page_icon="🧠",
    layout="wide",
)

# 3. Session State Initialization
if "topic" not in st.session_state:
    st.session_state.topic = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "tutor_history" not in st.session_state:
    st.session_state.tutor_history = []
if "comprehension_score" not in st.session_state:
    st.session_state.comprehension_score = 15
if "feedback" not in st.session_state:
    st.session_state.feedback = "Session started. Alex is waiting for your opening explanation."

# 4. Agent Prompts
ALEX_SYSTEM_INSTRUCTION = """
You are Alex, an inquisitive and slightly confused high school student trying to learn a STEM concept.
The user is your teacher using the Feynman Technique.

Rules for Alex:
1. Speak informally and concisely (maximum 2-3 sentences per turn).
2. Never act like an AI or an all-knowing assistant. You are a curious peer.
3. Express realistic intuitive misconceptions (e.g., 'Wait, why is orbital energy negative? Does that mean an electron in n=1 has less than zero energy?').
4. Ask one sharp question that forces the teacher to clarify the physical intuition behind the equations or concepts.
"""

TUTOR_SYSTEM_INSTRUCTION = """
You are an expert, encouraging STEM professor and mentor in the style of Richard Feynman.
The user is asking you for explanations, formula derivations, intuition, or quick conceptual brainstorming.
Format mathematical equations cleanly using standard LaTeX enclosed in $ or $$.
Be clear, intuitive, and concise. Avoid unnecessary preamble.
"""

EVALUATOR_SYSTEM_INSTRUCTION = """
You are an expert pedagogy evaluator for STEM subjects.
Analyze the user's explanation to Alex and return ONLY a valid JSON object.

Format strictly as:
{
  "comprehension_score": <integer from 0 to 100>,
  "feedback": "<one concise sentence diagnosing the user's explanation or noting jargon>"
}
"""

ACTIVE_MODEL = "gemini-3.8-flash"

def call_gemini_with_retry(contents, config, max_retries=3):
    """Retries cleanly if Google's servers experience a temporary 503 spike."""
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=ACTIVE_MODEL,
                contents=contents,
                config=config,
            )
            return response
        except ServerError as e:
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                raise e

def generate_alex_response(topic, history, user_input):
    """Generates Alex's conversational response with inquisitive misconceptions."""
    conversation_context = f"Topic: {topic}\n\nRecent Dialogue:\n"
    for msg in history[-6:]:
        conversation_context += f"{msg['role']}: {msg['content']}\n"
    conversation_context += f"User (Teacher): {user_input}\nAlex:"

    response = call_gemini_with_retry(
        contents=conversation_context,
        config=types.GenerateContentConfig(
            system_instruction=ALEX_SYSTEM_INSTRUCTION,
            temperature=0.7,
        ),
    )
    return response.text.strip()

def generate_tutor_response(topic, history, user_input):
    """Generates standard mentor/tutor assistance."""
    conversation_context = f"Topic: {topic}\n\nRecent Dialogue:\n"
    for msg in history[-6:]:
        conversation_context += f"{msg['role']}: {msg['content']}\n"
    conversation_context += f"User: {user_input}\nTutor:"

    response = call_gemini_with_retry(
        contents=conversation_context,
        config=types.GenerateContentConfig(
            system_instruction=TUTOR_SYSTEM_INSTRUCTION,
            temperature=0.4,
        ),
    )
    return response.text.strip()

def evaluate_explanation(topic, user_input, current_score):
    """Silently scores the user's explanation and updates the comprehension meter."""
    prompt = f"""
    Topic: {topic}
    Current Comprehension Score: {current_score}%
    Latest User Explanation: "{user_input}"
    
    If the explanation uses intuitive analogies or clarifies underlying mechanics, increase the score.
    If it is vague, purely memorized jargon, or logically wrong, lower the score slightly or keep it unchanged.
    """
    response = call_gemini_with_retry(
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=EVALUATOR_SYSTEM_INSTRUCTION,
            response_mime_type="application/json",
            temperature=0.2,
        ),
    )
    data = json.loads(response.text)
    return data.get("comprehension_score", current_score), data.get("feedback", "Explanation processed.")

# 5. UI Layout: Sidebar (HUD & State)
with st.sidebar:
    st.header("🎛️ Session Controls")
    input_topic = st.text_input(
        "Enter Concept to Teach:",
        placeholder="e.g. Bohr's Model & de Broglie Wavelength",
    )
    
    if st.button("Start New Session", use_container_width=True):
        if input_topic.strip():
            st.session_state.topic = input_topic.strip()
            st.session_state.chat_history = []
            st.session_state.tutor_history = []
            st.session_state.comprehension_score = 15
            st.session_state.feedback = f"Alex is ready to learn about {input_topic}."
            st.rerun()

    st.markdown("---")
    st.subheader("📊 Alex's Comprehension")
    st.progress(st.session_state.comprehension_score / 100)
    st.metric("Comprehension Level", f"{st.session_state.comprehension_score}%")
    
    st.markdown("**Pedagogical Feedback:**")
    st.info(st.session_state.feedback)

# 6. UI Layout: Main Stage (Classroom)
st.title("🎓 FeynmanAI Studio")

# Mode Selector
mode = st.radio(
    "Active Mode:",
    ["🧠 Feynman Inversion Mode (Teach Alex)", "💡 Standard Tutor / Brainstorm Mode"],
    horizontal=True,
)

if not st.session_state.topic:
    st.info("👈 Enter a topic in the sidebar and hit **Start New Session** to begin.")
else:
    st.markdown(f"**Current Subject:** `{st.session_state.topic}`")

    if "Feynman Inversion" in mode:
        st.caption("You are the Teacher. Alex is your student. Explain the intuition behind the concept.")
        
        # Render Feynman dialogue history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        user_input = st.chat_input("Teach Alex...")
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.write(user_input)

            with st.spinner("Alex is thinking..."):
                try:
                    alex_reply = generate_alex_response(
                        st.session_state.topic, st.session_state.chat_history, user_input
                    )
                    st.session_state.chat_history.append({"role": "assistant", "content": alex_reply})

                    new_score, feedback = evaluate_explanation(
                        st.session_state.topic, user_input, st.session_state.comprehension_score
                    )
                    st.session_state.comprehension_score = new_score
                    st.session_state.feedback = feedback
                    st.rerun()
                except Exception as e:
                    st.error(f"Execution Error: {e}")

    else:
        st.caption("You are studying. Ask the AI Tutor to explain formulas, derivations, or practice questions.")
        
        # Render Tutor dialogue history
        for message in st.session_state.tutor_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        tutor_input = st.chat_input("Ask a doubt or request a derivation...")
        if tutor_input:
            st.session_state.tutor_history.append({"role": "user", "content": tutor_input})
            with st.chat_message("user"):
                st.write(tutor_input)

            with st.spinner("Tutor is answering..."):
                try:
                    tutor_reply = generate_tutor_response(
                        st.session_state.topic, st.session_state.tutor_history, tutor_input
                    )
                    st.session_state.tutor_history.append({"role": "assistant", "content": tutor_reply})
                    st.rerun()
                except Exception as e:
                    st.error(f"Execution Error: {e}")