import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { ChatService } from "../../services/chatService";
import { getAllUsers } from "../../services/userService";

const INITIAL_PAGINATION = {
    page: 1,
    size: 10,
    totalPages: 1,
    totalItems: 0,
    hasMore: true,
};

// Lấy danh sách phiên chat của user
export const fetchUserChats = createAsyncThunk(
    "chat/fetchUserChats",
    async (userId, { rejectWithValue }) => {
        try {
            const chats = await new Promise((resolve) => {
                const unsubscribe = ChatService.subscribeToUserChats(
                    userId,
                    (chatsData) => {
                        resolve(chatsData);
                        unsubscribe();
                    }
                );
            });

            // Map lại dữ liệu để phù hợp với cây thư mục Firestore
            return chats.map((chat) => ({
                id: chat.id, // chat_<userId>_<sessionId>
                metadata: {
                    sessionId: chat.metadata.sessionId,
                    userId: chat.metadata.userId,
                    createdAt: chat.metadata.createdAt?.toMillis?.() ?? chat.metadata.createdAt,
                    updatedAt: chat.metadata.updatedAt?.toMillis?.() ?? chat.metadata.updatedAt,
                    title: chat.metadata.title || "Cuộc trò chuyện mới",
                },
                messages: chat.messages
                    ? chat.messages.map((msg) => ({
                        ...msg,
                        createdAt: msg.createdAt?.toMillis?.() ?? msg.createdAt,
                    }))
                    : [],
            }));
        } catch (error) {
            return rejectWithValue(error.message);
        }
    }
);

const chatAISlice = createSlice({
    name: "chat",
    initialState: {
        chats: [], // [{id, metadata, messages}]
        loading: false,
        loadingMore: false,
        error: null,
        lastFetch: null,
        pagination: INITIAL_PAGINATION,
        searchTerm: "",
    },
    reducers: {
        addMessageToChat: (state, action) => {
            const { chatId, message } = action.payload;
            const chat = state.chats.find((c) => c.id === chatId);
            if (chat) {
                chat.messages.push({
                    ...message,
                    createdAt: message.createdAt?.toMillis?.() ?? message.createdAt,
                });
                chat.metadata.updatedAt = Date.now();
            }
        },
        markChatAsRead: (state, action) => {
            const { chatId, userId } = action.payload;
            const chat = state.chats.find((c) => c.id === chatId);
            if (chat) {
                // tuỳ bạn lưu unread state ở metadata hoặc messages
                chat.metadata.hasUnread = false;
            }
        },
        setSearchTerm: (state, action) => {
            state.searchTerm = action.payload;
        },
        resetPagination: (state) => {
            state.pagination = INITIAL_PAGINATION;
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchUserChats.pending, (state) => {
                state.loading = true;
            })
            .addCase(fetchUserChats.fulfilled, (state, action) => {
                state.chats = action.payload;
                state.loading = false;
                state.lastFetch = Date.now();
            })
            .addCase(fetchUserChats.rejected, (state, action) => {
                state.error = action.payload;
                state.loading = false;
            })
    },
});

export const { addMessageToChat, markChatAsRead, setSearchTerm, resetPagination } = chatAISlice.actions;

export default chatAISlice.reducer;



// {
//   id: "chat_4_abc123",   // chat_<userId>_<sessionId>
//   metadata: {
//     sessionId: "abc123",
//     userId: "4",
//     createdAt: 1755418547384,
//     updatedAt: 1755419309266,
//     title: "Chat với AI"
//   },
//   messages: [
//     { senderId: "4", content: "hello", createdAt: 1755419309266, type: "text" }
//   ]
// }
