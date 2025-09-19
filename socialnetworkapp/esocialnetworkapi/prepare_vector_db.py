from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, Docx2txtLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
from collections import Counter
from libpy import libSupport
import os
import re
import unicodedata
import numpy as np
import faiss
import tiktoken

from dotenv import load_dotenv

# Load .env
load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "esocialnetworkapi", "resources", "data")
DB_PATH = os.path.join(BASE_DIR, "esocialnetworkapi", "vectorstores", "db_faiss_1024")

MAX_TOKENS_PER_REQUEST = 300_000  # giới hạn OpenAI
encoding = tiktoken.encoding_for_model("text-embedding-3-small")

# Embedding model dùng HuggingFace
# embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Embedding model dùng OpenAI
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

def preprocess_text(text: str) -> str:
    # 1. Chuẩn hóa Unicode (loại bỏ lỗi encoding từ PDF/DOCX)
    text = unicodedata.normalize("NFC", text)

    # 2. Xóa ký tự điều khiển, ký tự không in được
    text = re.sub(r"[\x00-\x1f\x7f-\x9f]", " ", text)

    # 3. Loại bỏ bullet, ký hiệu đặc biệt thường gặp trong PDF
    text = re.sub(r"[•●▪■◆◇▶►]", " ", text)

    # 4. Loại bỏ nhiều dấu chấm hoặc ký hiệu thừa
    text = re.sub(r"\.{2,}", ".", text)   # ... → .
    text = re.sub(r"[-–—]{2,}", "-", text) # --- → -

    # 5. Loại bỏ URL, email (nếu có, tránh làm nhiễu vector)
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)
    # 6. Xóa khoảng trắng thừa, xuống dòng thừa
    text = re.sub(r"\s+", " ", text).strip()

    return text

def count_tokens(text: str) -> int:
    return len(encoding.encode(text))

# Ham 2. Tao vector DB tu cac file PDF
def create_db_from_files_openai():
    # Load PDF và DOCX
    loader_pdf = DirectoryLoader(DATA_PATH, glob="*.pdf", loader_cls=PyPDFLoader)
    loader_docx = DirectoryLoader(DATA_PATH, glob="*.docx", loader_cls=Docx2txtLoader)
    documents = loader_pdf.load() + loader_docx.load()

    # Clean text
    cleaned_documents = [
        Document(page_content=preprocess_text(doc.page_content), metadata=doc.metadata)
        for doc in documents
    ]

    # Split thành chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=128)
    chunks = text_splitter.split_documents(cleaned_documents)

    embeddings_list = []
    texts_list = []
    metadatas_list = []

    batch_texts = []
    batch_metadatas = []
    batch_tokens = 0

    for chunk in chunks:
        tokens = count_tokens(chunk.page_content)
        if batch_tokens + tokens > MAX_TOKENS_PER_REQUEST:
            # embed batch
            batch_embeddings = embedding_model.embed_documents(batch_texts)
            embeddings_list.extend(batch_embeddings)
            texts_list.extend(batch_texts)
            metadatas_list.extend(batch_metadatas)

            # reset batch
            batch_texts = []
            batch_metadatas = []
            batch_tokens = 0

        batch_texts.append(chunk.page_content)
        batch_metadatas.append(chunk.metadata)
        batch_tokens += tokens

    # embed batch cuối
    if batch_texts:
        batch_embeddings = embedding_model.embed_documents(batch_texts)
        embeddings_list.extend(batch_embeddings)
        texts_list.extend(batch_texts)
        metadatas_list.extend(batch_metadatas)

    # Chuyển sang tuple (text, embedding_vector)
    text_embeddings = list(zip(texts_list, embeddings_list))

    db = FAISS.from_embeddings(
        text_embeddings=text_embeddings,
        embedding=embedding_model,   # đối tượng embedding
        metadatas=metadatas_list
    )

    db.save_local(DB_PATH)
    print(f"FAISS DB đã lưu tại: {DB_PATH}")
    return db



# Gọi hàm
if __name__ == "__main__":
    create_db_from_files_openai()
