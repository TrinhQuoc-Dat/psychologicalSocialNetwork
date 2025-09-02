import { addNotification } from "../features/notifications/notificationSlice";

let socket = null;
const token = localStorage.getItem("token");

export const connectNotificationSocket = (dispatch) => {
  socket = new WebSocket(`ws://127.0.0.1:8000/ws/notifications/?token=${token}`);

  socket.onopen = () => {
    console.log("✅ WebSocket connected!");
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);

    if (data.notification) {
      console.log("📩 Notification received:", data.notification);

      const notificationSound = new Audio("/sounds/notification.wav");
      notificationSound
        .play()
        .catch((err) => console.error("⚠️ Không thể phát âm thanh:", err));

      dispatch(addNotification(data.notification));
    } else if (data.message) {
      console.log("📨 Server echo:", data.message);
    }
  };

  socket.onerror = (error) => {
    console.error("WebSocket error:", error);
  };

  socket.onclose = (event) => {
    console.log("WebSocket closed:", event);
    // có thể auto reconnect nếu muốn
    setTimeout(() => connectNotificationSocket(dispatch), 5000);
  };
};

export const disconnectNotificationSocket = () => {
  if (socket) {
    socket.close();
  }
};
