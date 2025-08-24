import re
from underthesea import word_tokenize
from langchain_openai import OpenAIEmbeddings
import numpy as np
import os

# Khởi tạo embedding model
embeddings_model = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=os.environ["OPENAI_API_KEY"]
)


# ============ 1. Tiền xử lý dữ liệu ============
def preprocess(text: str) -> str:
    # lower
    text = text.lower()
    # bỏ ký tự đặc biệt
    text = re.sub(r"[^0-9a-zA-ZÀ-ỹ\s]", " ", text)
    # bỏ khoảng trắng thừa
    text = re.sub(r"\s+", " ", text).strip()
    # tách từ tiếng Việt
    tokens = word_tokenize(text, format="text")
    return tokens


def get_embedding(text: str) -> np.ndarray:
    vector = embeddings_model.embed_query(text)
    return np.array(vector, dtype=np.float32)

# --- Demo ---
if __name__ == "__main__":
    sample = "Tôi đang rất chán nản và cảm thấy stress quá!"
    processed = preprocess(sample)
    print("Câu gốc:", sample)
    print("Sau tiền xử lý:", processed)
    print(get_embedding(processed))
