from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from difflib import SequenceMatcher
from esocialnetworkapi.libpy import libSupport
from dotenv import load_dotenv
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "esocialnetworkapi\\vectorstores", "db_faiss")
DATA_PATH = os.path.join(BASE_DIR, "esocialnetworkapi\\resources\data")

# Load .env
load_dotenv()

FAQ = libSupport.getFile(DATA_PATH + "\question.json")
if FAQ != None:
    FAQ = libSupport.json_load(FAQ)

data_query = libSupport.getFile(DATA_PATH + "\\trangtamly_dataset.json")
if data_query != None:
    data_query = libSupport.json_load(data_query)

# Hàm tìm câu trả lời FAQ theo độ giống nhau
def find_faq_answer(query, threshold=0.85):
    for q, ans in FAQ.items():
        ratio = SequenceMatcher(None, query.lower(), q).ratio()
        if ratio >= threshold:
            return ans
    return None

# Hàm tìm bộ câu hỏi và câu trả lời khá tương đồng
def find_data_answer(query, threshold=0.75):
    for q, ans in data_query.items():
        ratio = SequenceMatcher(None, query.lower(), q).ratio()
        if ratio >= threshold:
            return ans
    return None

# Hàm xử lý 1 câu hỏi
def answer_query(qa_chain, query, llm):
    faq_answer = find_faq_answer(query)
    if faq_answer:
        data = {}
        data["result"] = faq_answer
        data["question"] = False
        return data
    else:
        data_answer = find_data_answer(query=query)
        if data_answer:
            # gửi dữ liệu lên chatgpt để trả lời
            result = ask_ai_content(data_answer=data_answer, query=query, llm=llm)

            return {
                "result": result.content,
                "question": False,
            }
        return ask_ai(qa_chain, query)


def ask_ai_content(data_answer, query, llm):
    template = """Sử dụng thông tin sau đây để trả lời câu hỏi của người dùng.
                Nếu không có câu trả lời chính xác thì hãy tự tổng hợp câu trả lời dựa trên thông tin.

                Thông tin (context): 
                {context}

                Câu hỏi: {question}

                Trả lời:"""
    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )

    chain = prompt | llm
    result = chain.invoke({"context": data_answer, "question": query})
    return result

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
    pass

    # TEMPLATE = """Sử dụng thông tin sau đây để trả lời câu hỏi. Nếu không có câu trả lời hãy tự sinh ra câu trả lời.".
    # Context: {context}
    # Question: {question}
    # Answer:"""

    # llm = load_llm()
    # prompt = create_prompt(TEMPLATE)
    # db = read_vectors_db()

    # qa_chain = create_qa_chain(prompt, llm, db)

    # while True:
    #     query = input("Nhập câu hỏi: ")
    #     if query.lower().strip() == "exit":
    #         print("Thoát chương trình.")
    #         break

    #     result = answer_query(qa_chain, query)
    #     print(result)
    #     print("\n=== Trả lời ===")
    #     print(result["result"])
    #     if "question" not in result or result["question"] == True:
    #         print("\n=== Nguồn tham chiếu ===")
    #         for doc in result["source_documents"]:
    #             print(f"- {doc.metadata.get('source', 'unknown')}")
    #         print("\n----------------------\n")