import streamlit as st
import anthropic
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="Course Logistics Assistant",
    page_icon="📋",
    layout="centered"
)

# Initialize Claude client with error handling
@st.cache_resource
def init_claude_client():
    try:
        api_key = st.secrets.get("CLAUDE_API_KEY")
        if not api_key:
            st.error("Claude API key not found. Please add it to your Streamlit secrets.")
            st.stop()
        return anthropic.Anthropic(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialize Claude client: {str(e)}")
        st.stop()

# Load knowledge base with error handling
@st.cache_data
def load_knowledge_base():
    knowledge_file = 'knowledge_base.txt'
    if not os.path.exists(knowledge_file):
        return """No knowledge base file found. 
        Please create a 'knowledge_base.txt' file with your course information."""
    
    try:
        with open(knowledge_file, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        st.error(f"Error loading knowledge base: {str(e)}")
        return "Error loading knowledge base."

# Initialize client and knowledge
client = init_claude_client()
knowledge = load_knowledge_base()

# Customizable system prompt
def get_system_prompt():
    return f"""You are a course logistics assistant. Your ONLY role is to answer questions about course logistics, policies, and administrative information.

You have access to the following course information:

{knowledge}

CRITICAL INSTRUCTIONS - YOU MUST FOLLOW THESE:

1. ONLY answer questions about:
   - Course schedule and due dates
   - Grading policies and breakdown
   - Assignment submission procedures
   - Office hours and contact information
   - Attendance and late work policies
   - Exam dates and locations
   - Course resources and materials
   - Administrative procedures
   - Any information explicitly in the knowledge base above

2. For ANY technical, programming, or conceptual questions:
   - Politely redirect: "I'm a logistics assistant and can only help with course policies, schedules, and administrative questions. For technical help, please attend office hours or post in the course forum."

3. When answering logistics questions:
   - Be direct and cite specific policies
   - Reference exact dates and times
   - Quote policies verbatim when important
   - If the information isn't in your knowledge base, say: "I don't have that information in the syllabus. Please check with the instructor."

4. Do NOT:
   - Provide programming help or code examples
   - Explain technical concepts
   - Help with homework problems
   - Give study advice beyond what's in the syllabus
   - Make up information not in your knowledge base

Remember: You are a syllabus and logistics expert ONLY. Stay strictly within this role.

Current date/time: {datetime.now().strftime("%Y-%m-%d %H:%M")}
"""

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_count" not in st.session_state:
    st.session_state.conversation_count = 0

# Header and instructions
st.title("📋 Course Logistics Assistant")
st.markdown("*Quick answers to syllabus, schedule, and policy questions*")

# Sidebar with information
with st.sidebar:
    st.header("ℹ️ What I Can Help With")
    st.markdown("""
    **✅ I can answer:**
    - When are assignments due?
    - What's the late work policy?
    - When are office hours?
    - How much is the final worth?
    - When is the midterm?
    - How do I submit assignments?
    - What's the attendance policy?
    
    **❌ I cannot help with:**
    - Programming questions
    - Homework problems
    - Technical concepts
    - Code debugging
    
    *For technical help, please attend office hours or use the course forum.*
    """)
    
    # Clear conversation button
    if st.button("🔄 Clear Conversation"):
        st.session_state.messages = []
        st.session_state.conversation_count += 1
        st.rerun()
    
    # Display conversation stats
    st.divider()
    st.caption(f"Messages in conversation: {len(st.session_state.messages)}")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input and processing
if prompt := st.chat_input("Ask about due dates, policies, office hours..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Prepare messages for API
                api_messages = []
                for msg in st.session_state.messages:
                    api_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
                
                # Get response from Claude
                response = client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=2000,
                    temperature=0.7,
                    system=get_system_prompt(),
                    messages=api_messages
                )
                
                # Extract and display response
                answer = response.content[0].text
                st.markdown(answer)
                
                # Add to message history
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
            except anthropic.APIError as e:
                st.error(f"API Error: {str(e)}")
                st.info("Please check your API key and try again.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Please try again or contact support if the issue persists.")

# Footer
st.divider()
st.caption("📋 This bot only answers logistics questions. For technical help, visit office hours.")