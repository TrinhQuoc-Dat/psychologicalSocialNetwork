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
DB_PATH = os.path.join(BASE_DIR, "esocialnetworkapi", "vectorstores", "db_faiss")
DATA_PATH = os.path.join(BASE_DIR, "esocialnetworkapi", "resources", "data")
FAQ_PATH = os.path.join(DATA_PATH, "question.json")

# Load .env
load_dotenv()

FAQ = libSupport.getFile(FAQ_PATH)
if FAQ != None:
    FAQ = libSupport.json_load(FAQ)

data_query = libSupport.getFile(os.path.join(DATA_PATH, "trangtamly_dataset.json"))
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
def find_data_answer_vector(query, threshold=0.5):
    for q, ans in data_query.items():
        ratio = SequenceMatcher(None, query.lower(), q).ratio()
        if ratio >= threshold:
            return ans
    return None

# Hàm xử lý 1 câu hỏi
def answer_query(query, llm, template, qa_chain):
    faq_answer = find_faq_answer(query)
    if faq_answer:
        data = {}
        data["result"] = faq_answer
        data["question"] = False
        return data
    else:
        data_answer = find_data_answer_vector(query=query)
        # tìm trong vector DB gốc
        rag_context = ""
        rag_result = qa_chain.invoke({"query": query})
       
        if "source_documents" in rag_result:
            rag_context = "\n".join([
                " ".join(doc.page_content.split())
                for doc in rag_result["source_documents"]
            ])

        if data_answer or rag_context:
            context = ""
            if data_answer:
                context += f"\n[Dữ liệu Từ 1 cá nhân viết ]\n{data_answer}"
            if rag_context:
                context += f"\n[Dữ liệu Gốc]\n{rag_context}"

            # dev
            print("\n=== Nguồn tham chiếu ===")
            for doc in rag_result["source_documents"]:
                print(f"- {doc.metadata.get('source', 'unknown')}")
            print("\n----------------------\n")
            print("context", context)
            
            result = ask_ai_content(context=context, query=query, llm=llm, template=template)
            return {"result": result.content, "question": False}

        return rag_result


def ask_ai_content(context, query, llm, template):
    prompt = create_prompt(template=template)
    chain = prompt | llm
    result = chain.invoke({"context": context, "question": query})
    return result

# Sử dụng ChatGPT (GPT-4 hoặc 3.5)
def load_llm():
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",   # vẫn dùng GPT-4o-mini để trả lời
        temperature=0.01
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
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
    db = FAISS.load_local(DB_PATH, embedding_model, allow_dangerous_deserialization=True)
    return db

# === Chạy thử ===
if __name__ == "__main__":
    pass

    # TEMPLATE = """
    #     Bạn là một chuyên gia tâm lý. Hãy dựa vào context để trả lời ngắn gọn, rõ ràng (tối đa 3-5 câu), phù hợp với câu hỏi người dùng.  
    #     Yêu cầu:
    #     1. Đồng cảm với cảm xúc của người dùng, giọng văn nhẹ nhàng, không phán xét. 
    #     2. Nếu không có đủ thông tin, hãy thừa nhận và đưa ra lời khuyên tổng quát.
    #     3. Nếu phát hiện người dùng người dùng bị stress, căng thẳng, buồn chán,... hãy đưa ra gợi ý thực tế, tích cực, an toàn (ví dụ: hít thở sâu, viết nhật ký, tập thể dục, nói chuyện với người tin tưởng,...).
    #     4. Nếu phát hiện người dùng có ý nghĩ tự làm hại bản thân (người dùng nói về tự tử, tự làm hại bản thân, hoặc nguy hiểm tới tính mạng), 
    #             KHÔNG đưa ra cách tự xử lý mà hãy khuyến khích họ tìm sự giúp đỡ từ chuyên gia tâm lý, 
    #             gọi ngay số điện thoại hỗ trợ khẩn cấp tại địa phương, hoặc liên hệ với bạn bè/người thân đáng tin cậy.
    #     5. Nếu là câu hỏi về lý thuyết chỉ cần trả lời câu hỏi, không đưa ra lời khuyên.
    #     6. Không bao giờ thay thế cho bác sĩ hoặc nhà trị liệu chuyên nghiệp.  

    #     Thông tin (context):  {context}

    #     Câu hỏi: {question}

    #     Trả lời:
    #     """

    # llm = load_llm()
    # prompt = create_prompt(TEMPLATE)
    # db = read_vectors_db()

    # qa_chain = create_qa_chain(prompt, llm, db)

    # while True:
    #     query = input("Nhập câu hỏi: ")
    #     if query.lower().strip() == "exit":
    #         print("Thoát chương trình.")
    #         break

    #     result = answer_query(query=query, llm=llm, template=TEMPLATE, qa_chain=qa_chain)
    #     print(result)
    #     print("\n=== Trả lời ===")
    #     print(result["result"])
    #     if "question" not in result or result["question"] == True:
    #         print("\n=== Nguồn tham chiếu ===")
    #         for doc in result["source_documents"]:
    #             print(f"- {doc.metadata.get('source', 'unknown')}")
    #         print("\n----------------------\n")