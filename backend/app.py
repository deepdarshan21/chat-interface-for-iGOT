import logging
from flask import Flask, request
from flask_cors import CORS
from utils.chromaQueryDocuments import (
    parse_course_details,
    chroma_init,
    query_documents_local,
)

app = Flask(__name__)
cors = CORS(app)

# set up logging
app.logger.setLevel(logging.INFO)  # Set log level to INFO
handler = logging.FileHandler("app.log")  # Log to a file
app.logger.addHandler(handler)


@app.route("/api", methods=["GET"])
def health():
    return {"data": "All OK"}


@app.route("/api/chat", methods=["POST"])
def chat_response():
    request_data = request.get_json()

    # Extract the user message
    messages = request_data.get("messages", [])
    user_message = ""

    if (
        messages
        and "text" in messages[0]
        and (messages[0]["text"] != "Yes" and messages[0]["text"] != "No")
    ):
        user_message = messages[0]["text"]
    else:
        app.logger.info(f'Feedback - {messages[0]["text"]}\n')
        response_data = {
            "role": "ai",
            "text": f"Thanks recorded!",
        }
        return [response_data]

    collection = chroma_init()
    results = query_documents_local(collection, user_message)
    courses = []
    final_resp_text = ""
    j = 1
    for i in results:
        parsed_details = parse_course_details(i[0].page_content)
        name = parsed_details.get("Course Name", None)
        url = parsed_details.get("Course URL", None)
        if not name or not url:
            continue
        final_resp_text = (
            final_resp_text
            + f"{j}) <b>Course Name</b> - {name}<br><b>Course URL</b> - <a href='{url}' target='_blank'>{url}</a><br><br>"
        )
        j += 1
        courses.append({"name": name, "url": url})

    if len(courses) != 0:
        # Sample response data
        response_data = {
            "role": "ai",
            "html": f"<p>Here are the top 3 courses you should look into - <br></p>{final_resp_text}",
        }

    else:
        response_data = {
            "role": "ai",
            "text": f"No courses could be found!",
        }

    app.logger.info(f"Question - {user_message}")
    app.logger.info(f"Response - {courses}")

    return [response_data]


if __name__ == "__main__":
    app.run(debug=True)
