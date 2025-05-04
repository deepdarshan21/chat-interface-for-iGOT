from chromaDataLoader import query_documents_local, collection
from groqLoader import question_generation
import json

# Define synthetic queries and course descriptions
synthetic_queries = [
    "What are the prerequisites for the AWS Elastic Beanstalk course?",
    "Can you summarize the course on Data Science with Python?",
    "What is the duration of the Machine Learning course?",
    "List some advanced topics covered in the Kubernetes course.",
    "Are there any beginner-friendly courses on Cloud Computing?"
]

course_descriptions = [
    "This course covers the basics of AWS Elastic Beanstalk, including deployment, scaling, and monitoring of applications.",
    "Learn the fundamentals of Data Science with Python, including data visualization, statistical analysis, and machine learning.",
    "An advanced course on Kubernetes, focusing on container orchestration, scaling, and deployment strategies.",
    "Introduction to Cloud Computing, covering key concepts, service models, and popular platforms like AWS and Azure."
]

# Generate synthetic queries and responses
synthetic_data = []
for query in synthetic_queries:
    response = query_documents_local(collection, query)
    synthetic_data.append({"query": query, "response": response})

# Generate synthetic MCQs
synthetic_mcqs = []
for description in course_descriptions:
    mcq = question_generation(description)
    synthetic_mcqs.append({"course_description": description, "mcq": mcq})

# Save combined synthetic data to a JSON file
combined_data = {"queries": synthetic_data, "mcqs": synthetic_mcqs}
with open("synthetic_data.json", "w") as f:
    json.dump(combined_data, f, indent=4)

print("Full synthetic data generated and saved to synthetic_data.json")