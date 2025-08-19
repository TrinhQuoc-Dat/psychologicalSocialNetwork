import { useNavigate } from "react-router-dom";
import {
  Newspaper,
  Users,
  ClipboardList,
  CalendarDays,
  Trash2,
  AlarmClock,
} from "lucide-react";
import { useEffect, useState } from "react";
import { getFollowerGroup } from "../../services/groupService";

const LeftSidebar = () => {
  const [page, setPage] = useState(1);
  const [userGroups, setUserGroups] = useState(null)
  const [hasMore, setHasMore] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getFollowerGroup(page, 5);
        if (page === 1) {
          setUserGroups(data.results);
        } else {
          setUserGroups((prev) => [...prev, ...data.results]);
        }
        if (data.next === null) {
          setHasMore(false);
        }
      } catch (error) {
        console.error("Failed to fetch followed groups", error);
      }
    };

    fetchData();
  }, [page]);
  const navigate = useNavigate();

  const handleDeletedPostsClick = () => {
    navigate("/deleted-posts");
  };

  const handleNewPost = () => {
    window.location.reload();
  }
  const handleSurveyPost = () => {
    navigate("/survey");
  }

  const handleEvent = () => {
    navigate("/event");
  }

  const handleExpiredSurveyClick = () => {
    navigate("/expired-survey-posts");
  };

  return (
    <aside className="w-1/5 hidden lg:block pr-4 ">
      <div className="bg-white rounded-2xl shadow-md p-4 sticky top-14">
        <h2 className="text-lg font-bold text-gray-800 mb-4">📚 Danh mục</h2>
        <ul className="space-y-3 text-gray-700 text-sm">
          <li
            onClick={handleNewPost}
            className="flex items-center gap-2 cursor-pointer hover:text-blue-500">
            <Newspaper size={18} />
            Tin mới
          </li>
          <li
            onClick={handleSurveyPost}
            className="flex items-center gap-2 cursor-pointer hover:text-blue-500">
            <ClipboardList size={18} />
            Khảo sát
          </li>
          <li
            onClick={handleEvent}
            className="flex items-center gap-2 cursor-pointer hover:text-blue-500">
            <CalendarDays size={18} />
            Sự kiện
          </li>
          <li
            onClick={handleDeletedPostsClick}
            className="flex items-center gap-2 cursor-pointer hover:text-red-500"
          >
            <Trash2 size={18} />
            Bài viết đã xóa
          </li>
          <li
            onClick={handleExpiredSurveyClick}
            className="flex items-center gap-2 cursor-pointer hover:text-yellow-600"
          >
            <AlarmClock size={18} />
            Khảo sát hết hạn
          </li>
        </ul>

        {userGroups?.length > 0 && (
          <div className="mt-6">
            <h3 className="text-md font-semibold text-gray-800 mb-2 flex items-center gap-x-2">
              <Users size={18} />
              <span>Nhóm bạn tham gia</span>
            </h3>
            <ul className="space-y-3 text-gray-700 text-sm">
              {userGroups.map((group, index) => (
                <li key={index}>
                  <button
                    onClick={() => navigate(`/group/${group.id}`)}
                    className="flex items-center gap-3 w-full text-left hover:text-blue-600 cursor-pointer"
                  >
                    <img
                      src={group.avatar || "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRVs1Lq3x9vC32Bs_M77R8FJj1nMlgyhSKkCg&s"}
                      alt={group.group_name}
                      className="w-8 h-8 rounded-md object-cover"
                    />
                    <span className="font-medium truncate">{group.group_name}</span>
                  </button>
                </li>
              ))}
              <li>
                {hasMore && (
                  <button
                    onClick={() => setPage((prev) => prev + 1)}
                    className="w-full text-center font-semibold text-gray-500 py-2 hover:text-blue-600 transition"
                  >
                    Xem thêm
                  </button>)}

              </li>
            </ul>
          </div>
        )}
      </div>
    </aside>
  );
};

export default LeftSidebar;
