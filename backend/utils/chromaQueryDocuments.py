import os
import re
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma

def query_documents_local(collection, question, k):
    results = collection.similarity_search_with_score(query=question, k=k)
    return results


def parse_course_details(course_details):
    # Define regex patterns for each field
    patterns = {
        "Course Name": r"Course Name: (.*)",
        "University": r"University: (.*)",
        "Difficulty Level": r"Difficulty Level: (.*)",
        "Course Rating": r"Course Rating: (.*)",
        "Course URL": r"Course URL: (.*)",
        "Course Description": r"Course Description: (.*)",
        "Skills": r"Skills: (.*)",
    }

    # Dictionary to hold the parsed details
    parsed_details = {}

    # Extract each detail using regex
    for key, pattern in patterns.items():
        match = re.search(pattern, course_details)
        if match:
            parsed_details[key] = match.group(1).strip()

    return parsed_details


def chroma_init():
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    persist_directory = "./db"
    if not os.path.exists(persist_directory):
        os.makedirs(persist_directory)

    collection = Chroma(
        collection_name="courses",
        embedding_function=embedding_function,
        persist_directory=persist_directory,
    )

    return collection