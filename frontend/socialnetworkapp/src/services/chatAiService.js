import axios from "axios";
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
import BASE_URL from "./baseUrl";
import Authorization from "../components/until/AuthorizationComponent";

export const ChatAIService = {
  /**
   * Lấy phiên chat AI của người dùng
   */
  subscribeToUserChatAI: (userId, callback) => {
    const chatId = `chat_${userId}`;
    const chatRef = doc(db, "chatAI", chatId);

    return onSnapshot(chatRef, (snapshot) => {
      if (!snapshot.exists()) {
        callback(null);
        return;
      }

      const data = snapshot.data();
      callback({
        id: snapshot.id,
        ...data,
        lastMessageTime: data.lastMessageTime?.toDate()?.getTime() || 0,
        createdAt: data.createdAt?.toDate()?.getTime() || 0,
      });
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
      console.log("message", message)
      // Cập nhật document phiên chat 
      await updateDoc(chatRef, {
        lastMessage: message.text || "[Media]",
        lastMessageTime: serverTimestamp(),
        lastSenderId: message.senderId,
      });

      // 2. Gọi API backend để lấy câu trả lời
      const res = await axios.post(`${BASE_URL}/api/chat/`,
        { query: message.text },
        { headers: Authorization() },
      ); 
      // 3. Lưu response AI vào Firestore
      const aiMessage = {
        senderId: "chat",
        text: res.data.result || "Xin lỗi, tôi chưa có câu trả lời.",
        timestamp: serverTimestamp(),
        status: "sent",
      };

      return { success: true, messageId: docRef.id };
    } catch (error) {
      console.error("Error sending AI message:", error);
      return { success: false, error: error.message };
    }
  },

  /**
   * Tạo hoặc lấy 1 phiên chat AI
   */
  getOrCreateChat: async (userId) => {
    try {
      const chatId = `chat_${userId}`;
      const chatRef = doc(db, "chatAI", chatId);

      const chatDoc = await getDoc(chatRef);
      if (!chatDoc.exists()) {
        await setDoc(chatRef, {
          userId,
          createdAt: serverTimestamp(),
          lastMessage: null,
          lastMessageTime: null,
          lastSenderId: null,
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
   * Đánh dấu toàn bộ tin nhắn đã đọc (optional)
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
//  └── chat_<userId> (document)     // mỗi user có thể có 1 session chatbot
//      ├── createdAt: Timestamp                 // thời điểm tạo
//      ├── lastMessage: "..."                   // tin nhắn cuối cùng
//      ├── lastMessageTime: Timestamp           // thời gian tin cuối cùng
//      ├── lastSenderId: "<userId>" || "chat"   // ai gửi tin cuối
//      └── messages (subcollection)
//          └── <messageId> (document)
//              ├── senderId: "<userId>" || "chat"
//              ├── content: "..."
//              ├── timestamp: Timestamp
//              ├── status: "sent" || "seen"
//              ├── seenAt: time,

