from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from difflib import SequenceMatcher
from dotenv import load_dotenv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "esocialnetworkapi\\vectorstores", "db_faiss")
print("BASE_DIR", DB_PATH)

# Load .env
load_dotenv()
FAQ = {
    "xin chào": "Xin chào bạn! Tôi có thể giúp gì?999999999",
    "giờ làm việc": "Chúng tôi làm việc từ 8h00 đến 17h30, từ thứ 2 đến thứ 6.",
    "liên hệ": "Bạn có thể liên hệ qua hotline 1900-xxxx hoặc email support@example.com",
}
# Hàm tìm câu trả lời FAQ theo độ giống nhau
def find_faq_answer(query, threshold=0.7):
    for q, ans in FAQ.items():
        ratio = SequenceMatcher(None, query.lower(), q).ratio()
        if ratio >= threshold:
            return ans
    return None

# Hàm xử lý 1 câu hỏi
def answer_query(qa_chain, query):
    faq_answer = find_faq_answer(query)
    if faq_answer:
        data = {}
        data["result"] = faq_answer
        data["question"] = False
        return data
    else:
        return ask_ai(qa_chain, query)


# Sử dụng ChatGPT (GPT-4 hoặc 3.5)
def load_llm():
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",   # vẫn dùng GPT-4o-mini để trả lời
        temperature=0.01,
        openai_api_key=os.environ["OPENAI_API_KEY"]
    )
    return llm

# Prompt template cho RAG
def create_prompt(template):
    return PromptTemplate(template=template, input_variables=["context", "question"])

# Tạo RetrievalQA chain
def create_qa_chain(prompt, llm, db):
    llm_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True,  # để log context
        chain_type_kwargs={'prompt': prompt}
    )
    return llm_chain

# Tải vector DB (sử dụng HuggingFaceEmbeddings giống lúc tạo)
def read_vectors_db():
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.load_local(DB_PATH, embedding_model, allow_dangerous_deserialization=True)
    return db


# Hàm gọi AI (LLM) nếu không có trong FAQ
def ask_ai(qa_chain, query):
    return qa_chain.invoke({"query": query})


# === Chạy thử ===
if __name__ == "__main__":

    TEMPLATE = """Sử dụng thông tin sau đây để trả lời câu hỏi. Nếu không có câu trả lời hãy tự sinh ra câu trả lời.".
    Context: {context}
    Question: {question}
    Answer:"""

    llm = load_llm()
    prompt = create_prompt(TEMPLATE)
    db = read_vectors_db()

    qa_chain = create_qa_chain(prompt, llm, db)

    while True:
        query = input("Nhập câu hỏi: ")
        if query.lower().strip() == "exit":
            print("Thoát chương trình.")
            break

        result = answer_query(qa_chain, query)
        print(result)
        print("\n=== Trả lời ===")
        print(result["result"])
        if "question" not in result or result["question"] == True:
            print("\n=== Nguồn tham chiếu ===")
            for doc in result["source_documents"]:
                print(f"- {doc.metadata.get('source', 'unknown')}")
            print("\n----------------------\n")