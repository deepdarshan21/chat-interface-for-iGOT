import os
from langchain_groq import ChatGroq
from groq import Groq
import json
from pydantic import BaseModel


def groq_chat_intialization():
    groq_api_key = os.getenv("GROQ_API_KEY")
    model = "llama3-8b-8192"
    groq_chat = ChatGroq(groq_api_key=groq_api_key, model_name=model)
    return groq_chat


def groq_intialization():
    groq_api_key = os.getenv("GROQ_API_KEY")
    client = Groq(api_key=groq_api_key)
    return client


def question_categorization(question):
    client = groq_intialization()
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """Consider you are a sentence categorizer who has the task of categorizing a given english sentence into one of the following categories - 'course_search', 'course_summary', 'question_generation', or 'general_search'. Now to give you some more context into understanding the categories - 
                1. The first one 'course_search' implies queries that are related to user searching about the a particular course or topic within a course.
                2. The second one 'course_summary' implies queries that are related to the user asking for a course summary where the title of the course might be specified or the user may ask about the summary of his/her previous course or also about any ongoing course.
                3. The third one 'question_generation' implies queries that are related to the user asking for a questions for a course where the title of the course might be specified or the user may ask to generate questions on his/her previous course or also about any ongoing course.
                4. The fourth one 'general_search' implies queries that are related to the user asking question regarding anythin in general not specific to a course but any meaning of a term or a statement or just a normal search.
                Response Guidelines - 
                1. If you are unable to generate a relevant category for the question then simply answer politely to the best of your understanding maybe stating that you do not possess enough information on the subject.
                2. Note to only return the response as the category name as a single word string, nothing else no explaination etc.
                3. Remember that the user might not always use exact words like summary etc they can use other synonyms to ask about the summary, so in that case also make sure to only return the single word category name as the response only.""",
            },
            {
                "role": "user",
                "content": f"Now given the user query - {question}, give the one word category name.",
            },
        ],
        model="llama3-8b-8192",
    )

    final_cat = chat_completion.choices[0].message.content
    if "course_search" in final_cat:
        return "course_search"
    elif "course_summary" in final_cat:
        return "course_summary"
    elif "question_generation" in final_cat:
        return "question_generation"
    elif "general_search" in final_cat:
        return "general_search"
    else:
        return None


def get_course_title(question):
    client = groq_intialization()
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """Consider you are an assistant who is presented with a question in english asked by a user where he/she is asking for summary of a particular course (educational/professional) and your task is simply to extract the title of the course if mentioned in the english sentence provided as input. 
                Response Guidelines -
                1. If no title is present in the sentence then simply return 'NA' as the ouput nothing else.
                2. Note to only return the response as the course title as a single word string, nothing else no explaination no premise no ending etc.""",
            },
            {
                "role": "user",
                "content": f"Now given the question - {question}. give the single string course title.",
            },
        ],
        model="llama3-8b-8192",
    )

    return chat_completion.choices[0].message.content


def get_course_summary_from_description(question):
    client = groq_intialization()
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """Consider you are an assistant who is presented with a description text for a particular course and your job is to frame that back into a key pointwise format (basically a structured format) to ensure that a small summary kind of is created for the text which is pointwise and thus easy to understand. You have to return the response in a formatted vanilla html format so that it can be directly rendered.
                Response Guidelines -
                1. Return the pointwise formatted text in a proper renderable format in html.
                2. Do not return anything else like an explaination or a predicate etc. Only the html string of the course summary in points.
                """,
            },
            {
                "role": "user",
                "content": f"{question}",
            },
        ],
        model="llama3-8b-8192",
    )

    return chat_completion.choices[0].message.content


def general_search(question):
    client = groq_intialization()
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """Consider you are a helpful assistant who has the task of simply answering the queries of the user. The question asked could be any generic question related to understanding of terminologies or a meaning.
                Response Guidelines -
                1. If you are not aware or sure of the response simply return a polite response that you won't be able to answer the question. Similarly if the question seems inappropriate or insensitive or uncensored then also simply return a polite response stating you can't answer such questions.
                """,
            },
            {
                "role": "user",
                "content": f"{question}",
            },
        ],
        model="llama3-8b-8192",
    )

    return chat_completion.choices[0].message.content


def question_generation(course_description):
    client = groq_intialization()
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """Consider you are a helpful assistant who has the task of creating a multiple choice question and the corresponding 4 options out of which one has to be the coorect response and others wrong. Now the question that will be created should be picked from one of the topics present in the course description that will be provided. Keep the question of average difficulty only. 
                Response Guidelines -
                1. The response format should be a json as follows - 
                {
                    "question":"The question generated",
                    "correct_response":"the correct answer",
                    "wrong_ans_1":"the wrong option 1",
                    "wrong_ans_2":"the wrong option 2",
                    "wrong_ans_3":"the wrong option 3"
                }
                2. Do not return anything else like an explaination or a predicate etc. Only the json of the mcq as specified above in the format.
                """,
            },
            {
                "role": "user",
                "content": f"Now given the course description  - {course_description}. Generate the mcq in the given format for the course.",
            },
        ],
        model="llama3-8b-8192",
    )

    return chat_completion.choices[0].message.content
