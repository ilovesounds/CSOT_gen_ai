# preprocess.py
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
import re

def split_by_section(text):
    pattern = r'(WALKTHROUGH|FRAMEWORK)[\s\S]*?(?=(WALKTHROUGH|FRAMEWORK|$))'
    matches = re.finditer(pattern, text, re.IGNORECASE)
    return [m.group() for m in matches]

loader = PyPDFLoader("Case Compendium.pdf")
documents = loader.load()
full_text = "\n".join([doc.page_content for doc in documents])
chunks = split_by_section(full_text)
texts = [Document(page_content=chunk) for chunk in chunks]

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-large-en",
    encode_kwargs={'normalize_embeddings': False}
)
qdrant = Qdrant.from_documents(
    texts,
    embeddings,
    url="http://localhost:6333",
    prefer_grpc=False,
    collection_name="vector_db"
)
print("Preprocessing and upload complete.")