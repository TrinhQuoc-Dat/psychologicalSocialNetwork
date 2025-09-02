import { useState } from "react";
import { ChatService } from "../services/chatService";

const useChat = (currentUser) => {
  const [activeChats, setActiveChats] = useState([]);
  const [chatMessages, setChatMessages] = useState({});

  const handleOpenChat = async (chatInfo) => {
    if (!activeChats.some((c) => c.chatId === chatInfo.chatId)) {
      const newChats = [...activeChats, chatInfo].slice(-2);
      setActiveChats(newChats);

      const unsubscribe = ChatService.subscribeToMessages(
        chatInfo.chatId,
        (messages) => {
          setChatMessages((prev) => ({
            ...prev,
            [chatInfo.chatId]: messages,
          }));
        }
      );

      await ChatService.markMessagesAsRead(
        chatInfo.chatId,
        currentUser.id.toString()
      );

      return unsubscribe;
    }
  };

  const handleCloseChat = (chatId) => {
    setActiveChats((prev) => prev.filter((c) => c.chatId !== chatId));
    setChatMessages((prev) => {
      const newMessages = { ...prev };
      delete newMessages[chatId];
      return newMessages;
    });
  };

  const handleSendMessage = async (chatId, message) => {
    return await ChatService.sendMessage(chatId, {
      ...message,
      senderId: currentUser.id.toString(),
    });
  };

  return {
    activeChats,
    chatMessages,
    handleOpenChat,
    handleCloseChat,
    handleSendMessage,
  };
};

export default useChat;
