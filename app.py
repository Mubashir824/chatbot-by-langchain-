from flask import Flask, render_template, request, redirect, url_for
from chatbox import db, ChatHistory, get_chat_response

app = Flask(__name__)

# Configure Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create database automatically if not exist
with app.app_context():
    db.create_all()

# Home page - just display empty chat
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# Chat page - process user input and show bot response
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    bot_response = get_chat_response(user_input)

    # Save to database
    new_chat = ChatHistory(user_input=user_input, chatbot_response=bot_response)
    db.session.add(new_chat)
    db.session.commit()

    return render_template('index.html', user_input=user_input, bot_response=bot_response)

if __name__ == "__main__":
    app.run(debug=True)
