import { configureStore } from '@reduxjs/toolkit';
import postReducer from '../features/posts/postSlice';
import authReducer from '../features/auth/authSlice';
import userReducer  from '../features/users/userSlice';
import chatReducer  from '../features/chat/chatSlice';
import chatAIReducer  from '../features/chat/chatAISlice';
import notificationReducer  from '../features/notifications/notificationSlice';



const store = configureStore({
  reducer: {
    auth: authReducer,
    posts: postReducer,
    users: userReducer,
    chat: chatReducer,
    chatAI: chatAIReducer,
    notifications: notificationReducer,
  },
});

export default store;
