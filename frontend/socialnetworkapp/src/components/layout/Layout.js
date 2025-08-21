import { Outlet } from "react-router-dom";
import Navbar from "../../components/layout/Navbar";
import ChatContainer from "../../components/Message/ChatContainer";
import { useState } from "react";
import { useSelector } from "react-redux";
import { ChatService } from "../../services/chatService";
import { ChatAIService } from "../../services/chatAiService";

const Layout = () => {
  const [activeChats, setActiveChats] = useState([]);
  const [chatMessages, setChatMessages] = useState({});
  const { user } = useSelector((state) => state.auth);

  const handleOpenChat = async (chatInfo) => {
    if (!activeChats.some((c) => c.chatId === chatInfo.chatId)) {
      const newChats = [...activeChats, chatInfo].slice(-2);
      setActiveChats(newChats);

      if (chatInfo.chatId.includes("chat")) {
        //========== nhắn trao đổi với chatAI ==========
        //lắng nghe tin nhắn realtime
        console.log("unsubscribeAI AI=========")
        const unsubscribeAI = ChatAIService.subscribeToMessages(
          chatInfo.chatId,
          (messages) => {
            setChatMessages((prev) => ({
              ...prev,
              [chatInfo.chatId]: messages,
            }));
          }
        );

        //Đánh dấu tin nhắn là đã đọc
        await ChatAIService.markMessagesAsRead(chatInfo.chatId, user.id.toString());

        return unsubscribeAI;
      }
      //============ các api của user nhắn với người dùng ==========
      //lắng nghe tin nhắn realtime
      console.log("unsubscribe ------------")
      const unsubscribe = ChatService.subscribeToMessages(
        chatInfo.chatId,
        (messages) => {
          setChatMessages((prev) => ({
            ...prev,
            [chatInfo.chatId]: messages,
          }));
        }
      );

      //Đánh dấu tin nhắn là đã đọc
      await ChatService.markMessagesAsRead(chatInfo.chatId, user.id.toString());

      return unsubscribe;
    }
  };

  const sendMess = async (chatId, message) => {
    if (chatId.includes("chat")) {
      return await ChatAIService.sendMessage(chatId, {
      ...message,
      senderId: user.id.toString(),
    });
    }
    return await ChatService.sendMessage(chatId, {
      ...message,
      senderId: user.id.toString(),
    });
  }

  const handleCloseChat = (chatId) => {
    setActiveChats(activeChats.filter((c) => c.chatId !== chatId));
    setChatMessages((prev) => {
      const newMessages = { ...prev };
      delete newMessages[chatId];
      return newMessages;
    });
  };

  return (
    <div className="bg-gray-100 min-h-screen pt-20">
      <Navbar onOpenChat={handleOpenChat} />

      {/* Phần main content không có sidebar */}
      <main className="max-w-7xl m-auto ">
        <Outlet />
      </main>

      <ChatContainer
        activeChats={activeChats}
        chatMessages={chatMessages}
        currentUser={user}
        onCloseChat={handleCloseChat}
        onSendMessage={sendMess}
      />
    </div>
  );
};

export default Layout;
