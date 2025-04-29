# chatbox.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from langchain.schema import HumanMessage
db = SQLAlchemy()

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_input = db.Column(db.String(500))
    chatbot_response = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ChatHistory {self.user_input}>'

# ------------------------------------------
# LangChain imports
import getpass
import os

# Set Google Gemini API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyArw_yFn6u21fFjDBR4vz1IyIlpXGJCXZQ"

from langchain.chat_models import init_chat_model
from langchain.agents import initialize_agent, Tool

# Initialize Gemini model
llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai")

# Define the tool
def call_llm_with_human_message(input_str):
    return llm.invoke(input_str)

tools = [
    Tool(
        name="Gemini",
        func=call_llm_with_human_message,  # Use the wrapper function here
        description="Use this tool to generate answers from Google's Gemini model"
    )
]


# Create agent
agent = initialize_agent(tools, llm, agent_type="zero-shot-react-description", verbose=True)

# ------------------------------------------

# Final get_chat_response() function
from langchain.schema import HumanMessage

def get_chat_response(user_input):
 
    # Proceed with the agent's response generation
    response = agent.run(user_input)
    return response

