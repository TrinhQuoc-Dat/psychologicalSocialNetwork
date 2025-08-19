import { db } from "../filebase/config";
import {
  collection,
  doc,
  setDoc,
  getDoc,
  addDoc,
  query,
  orderBy,
  onSnapshot,
  serverTimestamp,
  where,
  writeBatch,
  updateDoc,
  getDocs,
} from "firebase/firestore";

export const ChatAIService = {
  /**
   * Lấy danh sách các phiên chat AI của người dùng
   */
  subscribeToUserChatAI: (userId, callback) => {
    const chatsRef = collection(db, "chatAI");
    const q = query(
      chatsRef,
      where("userId", "==", userId),
      orderBy("lastMessageTime", "desc")
    );

    return onSnapshot(q, (snapshot) => {
      const chats = snapshot.docs.map((doc) => ({
        id: doc.id,
        ...doc.data(),
        lastMessageTime: doc.data().lastMessageTime?.toDate()?.getTime() || 0,
      }));
      callback(chats);
    });
  },

  /**
   * Lắng nghe tin nhắn trong 1 phiên chat AI
   */
  subscribeToMessages: (chatId, callback) => {
    const messagesRef = collection(db, "chatAI", chatId, "messages");
    const q = query(messagesRef, orderBy("timestamp", "asc"));

    return onSnapshot(q, (snapshot) => {
      const messages = snapshot.docs.map((doc) => ({
        id: doc.id,
        ...doc.data(),
        timestamp: doc.data().timestamp?.toDate()?.getTime() || Date.now(),
      }));
      callback(messages);
    });
  },

  /**
   * Gửi tin nhắn mới trong phiên chat AI
   */
  sendMessage: async (chatId, message) => {
    try {
      const messagesRef = collection(db, "chatAI", chatId, "messages");
      const chatRef = doc(db, "chatAI", chatId);

      const newMessage = {
        ...message,
        timestamp: serverTimestamp(),
        status: "sent",
      };

      // Thêm tin nhắn
      const docRef = await addDoc(messagesRef, newMessage);

      // Cập nhật document phiên chat
      await updateDoc(chatRef, {
        lastMessage: message.content || "[Media]",
        lastMessageTime: serverTimestamp(),
        lastSenderId: message.senderId,
      });

      return { success: true, messageId: docRef.id };
    } catch (error) {
      console.error("Error sending AI message:", error);
      return { success: false, error: error.message };
    }
  },

  /**
   * Tạo hoặc lấy 1 phiên chat AI
   */
  getOrCreateChat: async (userId, sessionId, topic = "General") => {
    try {
      const chatId = `chat_${userId}_${sessionId}`;
      const chatRef = doc(db, "chatAI", chatId);

      const chatDoc = await getDoc(chatRef);
      if (!chatDoc.exists()) {
        await setDoc(chatRef, {
          userId,
          sessionId,
          createdAt: serverTimestamp(),
          lastMessage: null,
          lastMessageTime: null,
          lastSenderId: null,
          topic,
          status: "active",
        });
      }

      return { success: true, chatId };
    } catch (error) {
      console.error("Error creating/getting AI chat:", error);
      return { success: false, error: error.message };
    }
  },

  /**
   * Đánh dấu toàn bộ tin nhắn AI đã đọc (optional)
   */
  markMessagesAsRead: async (chatId, userId) => {
    try {
      const messagesRef = collection(db, "chatAI", chatId, "messages");
      const q = query(messagesRef, where("senderId", "!=", userId));

      const snapshot = await getDocs(q);
      const batch = writeBatch(db);

      snapshot.forEach((doc) => {
        batch.update(doc.ref, {
          status: "seen",
          seenAt: serverTimestamp(),
        });
      });

      await batch.commit();
      return { success: true };
    } catch (error) {
      console.error("Error marking AI messages as read:", error);
      return { success: false };
    }
  },
};


// cấu trúc thư mục của chatAI

// chatAI (collection)
//  └── chat_<userId>_<sessionId> (document)     // mỗi user có thể có nhiều session chatbot
//      ├── createdAt: Timestamp                 // thời điểm tạo session
//      ├── lastMessage: "..."                   // tin nhắn cuối cùng
//      ├── lastMessageTime: Timestamp           // thời gian tin cuối cùng
//      ├── lastSenderId: "<userId>" || "chat"   // ai gửi tin cuối
//      ├── topic: "Tâm lý học"                  // chủ đề phiên chat
//      ├── status: "active" || "closed"         // trạng thái session
//      └── messages (subcollection)
//          └── <messageId> (document)
//              ├── senderId: "<userId>" || "chat"
//              ├── text: "..."
//              ├── timestamp: Timestamp
//              ├── status: "sent" || "seen"

