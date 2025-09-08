import json
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score
from rouge import Rouge
from langchain_openai import OpenAIEmbeddings
from sentence_transformers import util
from pathlib import Path
from qchatbot_openai import load_llm, create_qa_chain, read_vectors_db, create_prompt, find_faq_answer, answer_query
import os
import torch
from libpy import libSupport
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Load dataset
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = os.path.join(BASE_DIR, "esocialnetworkapi", "resources", "data")

# load sẵn khi khởi động server để tránh load lại mỗi request
llm = load_llm()
TEMPLATE = """
    Bạn là một chuyên gia tâm lý. Hãy dựa vào context để trả lời ngắn gọn, rõ ràng (tối đa 3-5 câu), phù hợp với câu hỏi người dùng.  
    Yêu cầu:
    1. Đồng cảm với cảm xúc của người dùng, giọng văn nhẹ nhàng, không phán xét. 
    2. Nếu không có đủ thông tin, hãy thừa nhận và đưa ra lời khuyên tổng quát.
    3. Nếu phát hiện người dùng người dùng bị stress, căng thẳng, buồn chán,... hãy đưa ra gợi ý thực tế, tích cực và an toàn.
    4. Nếu phát hiện người dùng có ý nghĩ tự làm hại bản thân (người dùng nói về tự tử, tự làm hại bản thân, hoặc nguy hiểm tới tính mạng), 
            KHÔNG đưa ra cách tự xử lý mà hãy khuyến khích họ tìm sự giúp đỡ từ chuyên gia tâm lý, 
            gọi ngay số điện thoại hỗ trợ khẩn cấp tại địa phương, hoặc liên hệ với bạn bè/người thân đáng tin cậy.
    5. Nếu là câu hỏi về lý thuyết chỉ cần trả lời câu hỏi, không đưa ra lời khuyên.
    6. Nếu câu hỏi KHÔNG liên quan đến tâm lý học, hãy trả lời ngắn gọn, lịch sự rằng bạn chỉ hỗ trợ các chủ đề liên quan đến tâm lý, 
       và gợi ý người dùng đặt câu hỏi khác phù hợp.
    Thông tin (context):  {context}

    Câu hỏi: {question}

    Trả lời:
    """

prompt = create_prompt(TEMPLATE)
db = read_vectors_db()
qa_chain = create_qa_chain(prompt, llm, db)

FAQ_TEST = libSupport.getFile(os.path.join(DATA_PATH, 'tamlyhoc_data_test.json'))
if FAQ_TEST != None:
    FAQ_TEST = libSupport.json_load(FAQ_TEST)

FAQ_ASW = libSupport.getFile(os.path.join(DATA_PATH, 'tamlyhoc_data_answer.json'))
if FAQ_ASW != None:
    FAQ_ASW = libSupport.json_load(FAQ_ASW)
else:
    FAQ_ASW = []


def test_model():
    for item in FAQ_TEST:
        if "status" in item and item['status'] == True: 
            continue
        question = item["question"]
        # Gọi chatbot
        result = answer_query(query=question, llm=llm, template=TEMPLATE, qa_chain=qa_chain)
        answer = result["result"]

        data = {
            "question": question,
            "ground_truth": answer.strip().lower()
        }
        item['status'] = True
        libSupport.writeFile(DATA_PATH, "tamlyhoc_data_test.json", FAQ_TEST)

        FAQ_ASW.append(data)
        libSupport.writeFile(DATA_PATH, "tamlyhoc_data_answer.json", FAQ_ASW)

def longest_common_subsequence(a: str, b: str) -> int:
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(m):
            if a[i] == b[j]:
                dp[i+1][j+1] = dp[i][j] + 1
            else:
                dp[i+1][j+1] = max(dp[i][j+1], dp[i+1][j])
    return dp[n][m]


if __name__ == "__main__":
    # Bộ đo ROUGE
    rouge = Rouge()

    # Lưu kết quả
    y_true = []
    y_pred = []
    cosine_scores = []
    rouge_scores = []
    lcs_scores = []
    exact_matches = 0
    index = 0
    end = len(FAQ_ASW)

    while True:
        # Xử lý text
        test_answer = FAQ_TEST[index]["ground_truth"]
        chat_answer = FAQ_ASW[index]["ground_truth"]
        # Exact Match
        if test_answer == chat_answer:
            exact_matches += 1

        # ROUGE
        rouge_score = rouge.get_scores(chat_answer, test_answer)[0]["rouge-l"]["f"]
        rouge_scores.append(rouge_score)
        
        # Longest Common Subsequence
        lcs_len = longest_common_subsequence(chat_answer, test_answer)
        lcs_score = lcs_len / max(len(chat_answer), len(test_answer))
        lcs_scores.append(lcs_score)

        embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
        # Cosine Similarity
        emb1 = embedding_model.embed_query(chat_answer)
        emb2 = embedding_model.embed_query(test_answer)
        # conver sang tensor trước khi so sánh sos_sim
        emb1_tensor = torch.tensor(emb1).unsqueeze(0)
        emb2_tensor = torch.tensor(emb2).unsqueeze(0)

        cosine_sim = util.cos_sim(emb1_tensor, emb2_tensor).item()
        cosine_scores.append(cosine_sim)

        index += 1
        if index == end:
            break
        
    print("----------------------------")
    exact_match_score = exact_matches / len(FAQ_TEST)
    avg_rouge = np.mean(rouge_scores)
    avg_cosine = np.mean(cosine_scores)
    avg_lcs = np.mean(lcs_scores)

    print("Kết quả đánh giá Chatbot:")
    print(f"- Exact Match: {exact_match_score:.4f}")
    print(f"- ROUGE-L: {avg_rouge:.4f}")
    print(f"- Cosine Similarity: {avg_cosine:.4f}")
    print(f"- Longest Common Subsequence: {avg_lcs:.4f}")
