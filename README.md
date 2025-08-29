# Course Assistant Chatbot

A Streamlit-powered teaching assistant chatbot that uses Claude AI to help students with course-related questions while maintaining academic integrity.

## Features

- 💬 Interactive chat interface for course questions
- 📚 Customizable knowledge base with course information
- 🔒 Built-in academic integrity safeguards (no complete code solutions)
- 💾 Conversation history within sessions
- 🎨 Clean, user-friendly interface
- ☁️ Easy deployment to Streamlit Cloud

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Claude API key from Anthropic

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd bantam-class-chat
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   
   Create `.streamlit/secrets.toml` (this file is gitignored for security):
   ```toml
   CLAUDE_API_KEY = "your-actual-api-key-here"
   ```

4. **Customize the knowledge base**
   
   Edit `knowledge_base.txt` with your course information:
   - Course details and schedule
   - Assignment due dates
   - Course policies
   - Office hours
   - Topics and concepts

5. **Run the app**
   ```bash
   streamlit run app.py
   ```

   The app will open in your browser at `http://localhost:8501`

## Deployment to Streamlit Cloud

### Step 1: Prepare Your Repository

1. Ensure all files are committed to GitHub (except `secrets.toml`)
2. Verify `.gitignore` includes `.streamlit/secrets.toml`
3. Push to GitHub

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Connect your GitHub repository
4. Select the branch and main file (`app.py`)

### Step 3: Configure Secrets

1. In Streamlit Cloud dashboard, go to App Settings
2. Navigate to Secrets section
3. Add your API key:
   ```toml
   CLAUDE_API_KEY = "your-actual-api-key-here"
   ```

### Step 4: Share with Students

Your app will be available at: `https://[your-app-name].streamlit.app`

## Customization Guide

### Modifying the System Prompt

Edit the `get_system_prompt()` function in `app.py` to adjust the chatbot's behavior and rules.

### Updating Course Information

Simply edit `knowledge_base.txt` with your course details. The chatbot will automatically use the updated information.

### Changing the UI

- Modify the title and headers in `app.py`
- Adjust the page configuration at the top of `app.py`
- Customize the sidebar content

## Security Considerations

- **Never commit your API key** - Always use environment variables or secrets management
- The `.gitignore` file prevents accidental commits of sensitive files
- API keys should only be added through Streamlit's secrets management when deployed

## Academic Integrity Features

The chatbot is configured to:
- Refuse to provide complete code solutions
- Guide students through concepts instead
- Encourage independent problem-solving
- Maintain clear boundaries on assignment help

## Troubleshooting

### API Key Issues
- Ensure your API key is correctly formatted
- Verify you have an active Anthropic account
- Check API usage limits

### Knowledge Base Not Loading
- Verify `knowledge_base.txt` exists in the root directory
- Check file encoding (should be UTF-8)

### Deployment Issues
- Ensure all required files are in the repository
- Verify Python version compatibility
- Check Streamlit Cloud logs for specific errors

## File Structure

```
bantam-class-chat/
├── app.py                      # Main application
├── requirements.txt            # Python dependencies
├── knowledge_base.txt          # Course information
├── README.md                   # Documentation
├── .gitignore                  # Git ignore rules
└── .streamlit/
    └── secrets.toml.example    # API key template
```

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Streamlit documentation
3. Contact your course administrator

## License

This project is designed for educational use. Feel free to modify and adapt for your courses.

---

Built with ❤️ using Streamlit and Claude AI