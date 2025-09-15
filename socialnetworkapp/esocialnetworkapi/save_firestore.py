from google.cloud import firestore
import datetime
import firebase_admin
from google.cloud import firestore
from google.oauth2 import service_account

key_path = "/Users/trinhquocdat/Documents/DAN/psychologicalsocialnetwork-firebase-adminsdk-fbsvc-4cdb94cd45.json"
credentials = service_account.Credentials.from_service_account_file(key_path)
db_firestore = firestore.Client(credentials=credentials, project="psychologicalsocialnetwork")

def save_chat_message(user_id, message, role="user"):
    doc_ref = db_firestore.collection("chatAI").document('chat_'+str(user_id)).collection("messages").document()
    doc_ref.set({
        "senderId": "chat",
        "status": 'sent',
        "text": message,
        "timestamp": datetime.datetime.utcnow()
    })

def get_chat_history(user_id, limit=10):
    docs = (
        db_firestore.collection("chatAI")
        .document('chat_'+str(user_id))
        .collection("messages")
        .order_by("timestamp", direction=firestore.Query.DESCENDING)
        .limit(limit)
        .stream()
    )
    history = [{"role": doc.to_dict()["senderId"], "message": doc.to_dict()["text"]} for doc in docs]
    return list(reversed(history))  # đảo lại cho đúng thứ tự thời gian


if __name__ == "__main__":
    print(get_chat_history(15))