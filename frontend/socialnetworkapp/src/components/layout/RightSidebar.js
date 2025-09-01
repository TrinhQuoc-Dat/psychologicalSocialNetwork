import { useState, useEffect } from "react";
import axios from "axios";
import BASE_URL from "../../services/baseUrl";
import Authorization from "../until/AuthorizationComponent";
import { useSelector } from "react-redux";

const RightSidebar = () => {
  const [contacts, setContacts] = useState([]);
  const [page, setPage] = useState(1);
  const [hasNext, setHasNext] = useState(false);
  const { user } = useSelector((state) => state.auth);
  useEffect(() => {
    const fetchContacts = async () => {
      try {
        if (user) {
          const res = await axios.get(
            `${BASE_URL}/api/contact/friends/?page=${page}&size=10`,
            { headers: Authorization() }
          );
          // Nếu có results thì append vào danh sách
          const newContacts = res.data.results || res.data;
          setContacts((prev) => [...prev, ...newContacts]);

          // Kiểm tra còn trang tiếp theo không
          if (res.data.next) {
            setHasNext(true);
          } else {
            setHasNext(false);
          }
        }

      } catch (error) {
        console.error("Lỗi khi lấy danh sách liên hệ:", error);
      }
    };

    fetchContacts();
  }, [page]);

  const handleOpenChat = (user) => {
    alert(`Mở chat với ${user.username}`);
    // TODO: mở hộp thoại chat thực sự tại đây
  };

  const getDisplayName = (user) => {
    if (user.first_name || user.last_name) {
      return `${user.first_name ?? ""} ${user.last_name ?? ""}`.trim();
    }
    return user.username;
  };
  return (
    <aside className="w-1/5 hidden lg:block pl-4">
      <div className="bg-white rounded-xl shadow p-4 mb-6 sticky top-14">
        <h2 className="font-semibold text-gray-700 mb-2">🆕 Gợi ý</h2>
        <p className="text-sm text-gray-600">Tính năng mới sắp ra mắt...</p>
      </div>

      <div className="bg-white rounded-xl shadow p-4 sticky top-14">
        <h2 className="font-semibold text-gray-700 mb-3">Người liên hệ</h2>
        <ul className="space-y-3 text-sm text-gray-800 max-h-96 overflow-y-auto pr-2">
          {contacts.map((user) => (
            <li
              key={user.id}
              className="flex items-center gap-3 cursor-pointer hover:bg-gray-100 p-2 rounded-md transition"
              onClick={() => handleOpenChat(user)}
            >
              <img
                src={
                  user.avatar
                    ? user.avatar
                    : "https://png.pngtree.com/png-vector/20190710/ourmid/pngtree-user-vector-avatar-png-image_1541962.jpg"
                }
                alt={user.username}
                className="w-8 h-8 rounded-full object-cover"
              />
              <span className="font-medium truncate">
                {getDisplayName(user)}
              </span>
            </li>
          ))}

          {hasNext && (
            <li>
              <button
                onClick={() => setPage((prev) => prev + 1)}
                className="w-full text-center font-semibold text-gray-500 py-2 hover:text-blue-600 transition"
              >
                Xem thêm
              </button>
            </li>
          )}
        </ul>
      </div>
    </aside>
  );
};

export default RightSidebar;
