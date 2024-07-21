from langchain.document_loaders import CSVLoader
import os
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma


def create_collection_local(client, collection_name, embedding_function):
    collection = client.create_collection(
        name=collection_name, embedding_function=embedding_function
    )
    return collection


def add_documents_local(collection, document, id):
    collection.add_documents(documents=document, ids=id)
    collection.persist()


def query_documents_local(collection, question):
    results = collection.similarity_search_with_score(query=question, k=2)
    return results


embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
# BAAI/bge-large-en-v1.5

loader = CSVLoader("./data/Coursera.csv", encoding="windows-1252")
documents = loader.load()


persist_directory = "./db"
if not os.path.exists(persist_directory):
    os.makedirs(persist_directory)

collection = Chroma(
    collection_name="courses",
    embedding_function=embedding_function,
    persist_directory=persist_directory,
)


def split_documents(documents, chunk_size=166):
    return [documents[i : i + chunk_size] for i in range(0, len(documents), chunk_size)]


split_docs = split_documents(documents)
for i, chunk in enumerate(split_docs):
    start_index = sum(len(split_docs[j]) for j in range(i))
    indices = list(range(start_index, start_index + len(chunk)))
    indices_str = list(map(str, indices))
    add_documents_local(collection, chunk, list(indices_str))


query = "give some course details about AWS Elastic beanstalk?"
print(query_documents_local(collection, query))
