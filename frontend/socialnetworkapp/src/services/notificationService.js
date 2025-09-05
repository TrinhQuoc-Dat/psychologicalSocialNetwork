import axios from "axios";
import BASE_URL from "./baseUrl";
import Authorization from "../components/until/AuthorizationComponent";

const NotificationService = {
    getUserNotifications: async () => {
        try {
            const response = await axios.get(
                `${BASE_URL}/api/notifications/`,
                { headers: Authorization() }
            );
            console.log("/api/notifications/", response.data)
            return response.data;
        } catch (error) {
            console.error("Error fetching notifications:", error);
            throw error;
        }
    },

    getUnreadNotifications: async () => {
        try {
            const response = await axios.get(
                `${BASE_URL}/api/notifications/unread/`,
                { headers: Authorization() }
            );
            return response.data;
        } catch (error) {
            console.error("Error fetching unread notifications:", error);
            throw error;
        }
    },

    markAsRead: async (id) => {
        try {
            const response = await axios.post(
                `${BASE_URL}/api/notifications/${id}/read/`,
                null,
                { headers: Authorization() }
            );
            return response.data;
        } catch (error) {
            console.error(`Error marking notification ${id} as read:`, error);
            throw error;
        }
    },

    markAllAsRead: async () => {
        try {
            const response = await axios.post(
                `${BASE_URL}/api/notifications/read-all/`,
                null,
                { headers: Authorization() }
            );
            return response.data;
        } catch (error) {
            console.error("Error marking all notifications as read:", error);
            throw error;
        }
    },
};

export default NotificationService;
