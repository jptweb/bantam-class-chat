import streamlit as st
import anthropic
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="Course Assistant",
    page_icon="📚",
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
    return f"""You are a helpful teaching assistant for this course. 
You have access to the following course information:

{knowledge}

CRITICAL ACADEMIC INTEGRITY RULES - YOU MUST FOLLOW THESE:
1. NEVER provide complete, runnable code solutions
2. When asked for code examples, ONLY provide:
   - Conceptual explanations of how to approach the problem
   - Pseudocode showing the logic (not actual syntax)
   - Small syntax examples (max 2-3 lines) to illustrate a specific concept
   - Comments explaining what each step should do
3. If a student asks for a function or complete code:
   - Explain the CONCEPT of what the function should do
   - Describe the STEPS in plain English
   - DO NOT write the actual function
4. Acceptable response for "write a function to add two numbers":
   - "To add two numbers, you'll need to: 1) Define a function with two parameters, 2) Use the addition operator, 3) Return the result"
   - NOT acceptable: Actually writing def add(a, b): return a + b
5. Always encourage students to write their own code
6. For specific dates, policies, or administrative questions, refer to the information provided
7. If information is not in your knowledge base, direct students to the instructor or syllabus

Remember: You're here to TEACH concepts, not to provide code solutions.

Current date/time: {datetime.now().strftime("%Y-%m-%d %H:%M")}
"""

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_count" not in st.session_state:
    st.session_state.conversation_count = 0

# Header and instructions
st.title("📚 Course Assistant")
st.markdown("*Your AI teaching assistant for course questions and concept explanations*")

# Sidebar with information
with st.sidebar:
    st.header("ℹ️ How to Use")
    st.markdown("""
    - Ask about course policies
    - Get help understanding concepts
    - Clarify assignment requirements
    - Review course schedule
    
    **Note:** I won't provide complete code solutions, but I'll help you understand the concepts!
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
if prompt := st.chat_input("Ask me about the course..."):
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
st.caption("💡 Remember: Learning happens through understanding, not copying!")