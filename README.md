# 🧠 Psychological Social Network

Một **hệ thống mạng xã hội tâm lý học** giúp người dùng chia sẻ cảm xúc, tham gia cộng đồng hỗ trợ tinh thần và nhận tư vấn từ chatbot AI thông minh.  
Dự án sử dụng **Django (REST + Channels)** cho backend, **ReactJS** cho frontend, **Firebase** để lưu trữ tin nhắn thời gian thực, **WebSocket** cho thông báo tức thời và **RAG + LangChain** để xây dựng chatbot thông minh.

---

## 🚀 Tính năng chính

- 👥 **Mạng xã hội**: Đăng bài, bình luận, cảm xúc, theo dõi người dùng.
- 💬 **Chat Realtime**: Tin nhắn 1-1 và nhóm, lưu trên Firebase, cập nhật tức thời.
- 🤖 **Chatbot AI**:
  - Sử dụng mô hình **RAG (Retrieval-Augmented Generation)**.
  - Kết hợp **LangChain + FAISS** để tìm kiếm tài liệu liên quan.
  - Trả lời thông minh, ngắn gọn, thân thiện, có thể dẫn nguồn.
- 🔔 **Thông báo realtime**:
  - Like, comment, tin nhắn mới, phản hồi từ chatbot.
  - WebSocket (Django Channels + Redis).
- 🔍 **Tìm kiếm nâng cao**: Bài viết, người dùng, nhóm.
- 📊 **Quản trị**: Dashboard quản lý bài đăng, người dùng, báo cáo nội dung xấu.

---

## 🏗️ Kiến trúc hệ thống

```mermaid
graph TD
    A[React Frontend] -->|REST API| B[Django REST Framework]
    A -->|WebSocket| C[Django Channels + Redis]
    A -->|Realtime| D[Firebase Firestore]
    B -->|Vector Query| E[LangChain + FAISS Index]
    E -->|Call LLM| F[OpenAI/HuggingFace Model]
```
---
## 📂 Cấu trúc dự án
```
psychologicalSocialNetwork/
├── socialnetworkapp/
│   ├── esocialnetworkapi/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── rag.py      
│   ├── notification/
│   │   ├── consumers.py
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   └── package.json
└── README.md
```
---
## ⚙️ Cài đặt & Chạy
## 1️⃣ Backend (Django)

```
git clone https://github.com/<your-username>/psychologicalSocialNetwork.git
cd psychologicalSocialNetwork/backend

# Tạo virtualenv
python3 -m venv venv
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt

# Migrate database
python manage.py migrate

# Chạy server + websocket
daphne -b 0.0.0.0 -p 8000 backend.asgi:application
```
---
## 2️⃣ Frontend (React)

```
cd psychologicalSocialNetwork/frontend
npm install
npm start
```
---
## 3️⃣ Firebase

Tạo project trên Firebase Console

Bật Firestore + Realtime Database

Lấy config và đặt vào frontend/src/firebase/config.js
---
## 🧠 Chatbot (RAG + LangChain)
Thu thập dữ liệu: FAQ, bài viết cộng đồng, tài liệu tâm lý học.

Chunk dữ liệu -> Embedding -> FAISS index.

Truy vấn:

Nhúng câu hỏi người dùng.

Tìm top-k đoạn liên quan trong FAISS.

Kết hợp vào prompt → gửi tới LLM.

Trả về câu trả lời + tài liệu tham chiếu.
---
## 🛡️ Bảo mật & Quyền riêng tư

🔒 Token-based Authentication (JWT).

🛡️ Bảo vệ dữ liệu người dùng.

🧾 Log tất cả tương tác với chatbot (ẩn danh nếu cần).

⚠️ Hiển thị cảnh báo: “Chatbot chỉ mang tính hỗ trợ, không thay thế chuyên gia.”

