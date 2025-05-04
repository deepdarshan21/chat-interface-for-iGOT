from chromaDataLoader import query_documents_local, collection

# Define synthetic queries
synthetic_queries = [
    "What are the prerequisites for the AWS Elastic Beanstalk course?",
    "Can you summarize the course on Data Science with Python?",
    "What is the duration of the Machine Learning course?",
    "List some advanced topics covered in the Kubernetes course.",
    "Are there any beginner-friendly courses on Cloud Computing?"
]

# Generate synthetic responses
synthetic_data = []
for query in synthetic_queries:
    response = query_documents_local(collection, query)
    synthetic_data.append({"query": query, "response": response})

# Save synthetic data to a JSON file
import json
with open("synthetic_course_queries.json", "w") as f:
    json.dump(synthetic_data, f, indent=4)

print("Synthetic data generated and saved to synthetic_course_queries.json")