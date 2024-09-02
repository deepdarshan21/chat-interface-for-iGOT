import logging
from flask import Flask, request
from flask_cors import CORS
from utils.chromaQueryDocuments import (
    parse_course_details,
    chroma_init,
    query_documents_local,
)
from utils.groqLoader import (
    groq_chat_intialization,
    question_categorization,
    get_course_title,
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

    category = question_categorization(user_message)
    print(category)

    if category == "course_search":
        collection = chroma_init()
        results = query_documents_local(collection, user_message, 3)
        courses = []
        final_resp_text = ""
        j = 1
        for i in results:
            parsed_details = parse_course_details(i[0].page_content)
            name = parsed_details.get("Course Name", None)
            url = parsed_details.get("Course URL", None)
            rating = parsed_details.get("Course Rating", None)
            if not name or not url or not rating:
                continue
            final_resp_text = (
                final_resp_text
                + f"{j}) <b>Course Name</b> - {name}<br><b>Course URL</b> - <a href='{url}' target='_blank'>{url}</a><br> <b>Course Rating</b> - {rating}<br><br>"
            )
            j += 1
            courses.append({"name": name, "url": url, "rating": rating})

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
    elif category == "course_summary":
        collection = chroma_init()
        course_title = get_course_title(user_message)
        if course_title == "NA":
            default_current_course = "Anti-Racism I"
        else:
            default_current_course = course_title

        # rag based fetching top 1 course that matches this title and thus getting the summary of that course
        results = query_documents_local(collection, default_current_course, 1)
        if len(results) == 0:
            response_data = {
                "role": "ai",
                "text": f"No courses could be found!",
            }
        else:
            parsed_details = parse_course_details(results[0][0].page_content)
            name = parsed_details.get("Course Name", None)
            description = parsed_details.get("Course Description", None)

            response_data = {
                "role": "ai",
                "html": f"<p>This is the course name - <br>{name}<br></p> And here is the summary - <br>{description}",
            }
        return [response_data]
    elif category == "question_generation":
        response_data = {
            "role": "ai",
            "text": f"question generation",
        }
        return [response_data]
    elif category == "general_search":
        response_data = {
            "role": "ai",
            "text": f"general search",
        }
        return [response_data]
    else:
        response_data = {
            "role": "ai",
            "text": f"{category}",
        }
        return [response_data]


if __name__ == "__main__":
    app.run(debug=True)
