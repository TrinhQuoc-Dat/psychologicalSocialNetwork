import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { ChatAIService } from "../../services/chatAiService";


// Lấy phiên chat của user
export const fetchUserChatAI = createAsyncThunk(
    "chat/fetchUserChatAI",
    async (userId, { rejectWithValue }) => {
        try {
            const chat = await new Promise((resolve) => {
                const unsubscribe = ChatAIService.subscribeToUserChatAI(
                    userId,
                    (chatData) => {
                        resolve(chatData);
                        unsubscribe();
                    }
                );
            });

            if (!chat) return null;

            return {
                id: chat.id, // chat_<userId>
                metadata: {
                    ...chat,
                    createdAt: chat.createdAt?.toMillis?.() ?? chat.createdAt,
                    updatedAt:chat.updatedAt?.toMillis?.() ?? chat.updatedAt,
                    title: chat.title || "Cuộc trò chuyện mới",
                },
                messages: chat.messages
                    ? chat.messages.map((msg) => ({
                        ...msg,
                        createdAt: msg.createdAt?.toMillis?.() ?? msg.createdAt,
                    }))
                    : [],
            };
        } catch (error) {
            return rejectWithValue(error.message);
        }
    }
);


const chatAISlice = createSlice({
    name: "chatAI",
    initialState: {
        chat: {
            id: null,
            metadata: {},
            messages: []
        },
        loadingAI: false,
        error: null,
        lastFetch: null,
    },
    reducers: {
        addMessage: (state, action) => {
            if (state.chat) {
                state.chat.messages.push({
                    ...action.payload,
                    createdAt:
                        action.payload.createdAt?.toMillis?.() ?? action.payload.createdAt,
                });
                state.chat.metadata.updatedAt = Date.now();
            }
        },
        markAsRead: (state) => {
            if (state.chat) {
                state.chat.metadata.hasUnread = false;
            }
        },
        resetChat: (state) => {
            state.chat = null;
            state.lastFetch = null;
        }
    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchUserChatAI.pending, (state) => {
                state.loadingAI = true;
            })
            .addCase(fetchUserChatAI.fulfilled, (state, action) => {
                state.chat = action.payload;
                state.loadingAI = false;
                state.lastFetch = Date.now();
            })
            .addCase(fetchUserChatAI.rejected, (state, action) => {
                state.error = action.payload;
                state.loadingAI = false;
            })
    },
});

export const { addMessage, markAsRead, resetChat } = chatAISlice.actions;

export default chatAISlice.reducer;



// {
//   id: "chat_4",   // chat_<userId>
//   metadata: {
//     userId: "4",
//     createdAt: 1755418547384,
//     updatedAt: 1755419309266,
//     title: "Chat với AI"
//      lastMessage:"Thương em thật nhiều"
//      lastMessageTime:1755679275613
//      lastSenderId: "4"
//   },
//   messages: [
//     { senderId: "4", content: "hello", createdAt: 1755419309266, type: "text" }
//   ]
// }
