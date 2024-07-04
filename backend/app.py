from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
cors = CORS(app)


@app.route("/chat", methods=["POST"])
def chat_response():
    request_data = request.get_json()

    # Extract the user message
    messages = request_data.get("messages", [])
    user_message = ""
    if messages and "text" in messages[0]:
        user_message = messages[0]["text"]

    # Sample response data
    response_data = {
        "role": "ai",
        "text": f"Received your query: {user_message}. Here's a sample response.",
    }
    feedback = {"role": "ai", "text": "feedback"}

    return [response_data, feedback]


if __name__ == "__main__":
    app.run(debug=True)
