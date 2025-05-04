from groqLoader import question_generation

# Define synthetic course descriptions
course_descriptions = [
    "This course covers the basics of AWS Elastic Beanstalk, including deployment, scaling, and monitoring of applications.",
    "Learn the fundamentals of Data Science with Python, including data visualization, statistical analysis, and machine learning.",
    "An advanced course on Kubernetes, focusing on container orchestration, scaling, and deployment strategies.",
    "Introduction to Cloud Computing, covering key concepts, service models, and popular platforms like AWS and Azure."
]

# Generate synthetic MCQs
synthetic_mcqs = []
for description in course_descriptions:
    mcq = question_generation(description)
    synthetic_mcqs.append({"course_description": description, "mcq": mcq})

# Save synthetic MCQs to a JSON file
import json
with open("synthetic_mcqs.json", "w") as f:
    json.dump(synthetic_mcqs, f, indent=4)

print("Synthetic MCQs generated and saved to synthetic_mcqs.json")