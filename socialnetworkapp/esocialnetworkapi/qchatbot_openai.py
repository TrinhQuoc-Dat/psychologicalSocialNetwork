from langchain_openai import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Sử dụng ChatGPT (GPT-4 hoặc 3.5)
def load_llm():
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
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
        return_source_documents=True, # để log context
        chain_type_kwargs={'prompt': prompt}
    )
    return llm_chain

# Tải vector DB
def read_vectors_db():
    embedding_model = OpenAIEmbeddings()  # hoặc giữ nguyên nếu bạn đã dùng embedding cũ
    db = FAISS.load_local("vectorstores/db_faiss", embedding_model, allow_dangerous_deserialization=True)
    return db


# === Chạy thử ===
if __name__ == "__main__":
    # import faiss
    # index = faiss.read_index("vectorstores/db_faiss/index.faiss")
    # print("FAISS dimension:", index.d)
    pass
    TEMPLATE = """Trả lời câu hỏi sau dựa trên ngữ cảnh được cung cấp. 
    Nếu không có thông tin, hãy trả lời "Tôi không chắc chắn".
    Context: {context}
    Question: {question}
    Answer:"""

    llm = load_llm()
    prompt = create_prompt(TEMPLATE)
    db = read_vectors_db()

    qa_chain = create_qa_chain(prompt, llm, db)

    # Ví dụ truy vấn
    query = "Các giai đoạn phát triển tâm lý theo Freud là gì?"
    result = qa_chain.invoke({"query": query})

    print("=== Trả lời ===")
    print(result["result"])  # câu trả lời
    print("\n=== Nguồn tham chiếu ===")
    for doc in result["source_documents"]:
        print(f"- {doc.metadata.get('source', 'unknown')}")


