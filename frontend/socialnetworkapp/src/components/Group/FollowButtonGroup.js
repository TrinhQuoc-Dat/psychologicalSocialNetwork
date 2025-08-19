import { useEffect, useState } from "react";
import { checkFollowingGroup, followGroup, unfollowGroup } from "../../services/groupService";

const FollowButtonGroup = ({ groupId }) => {
  const [isFollowing, setIsFollowing] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const checkFollow = async () => {
      try {
        const res = await checkFollowingGroup(groupId);
        setIsFollowing(res.data.is_following);
      } catch (err) {
        console.error("Lỗi kiểm tra theo dõi:", err);
      }
    };
    checkFollow();
  }, [groupId]);

  const handleFollow = async () => {
    setLoading(true);
    try {
      await followGroup(groupId);
      setIsFollowing(true);
    } catch (err) {
      console.error("Lỗi theo dõi nhóm:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleUnfollow = async () => {
    setLoading(true);
    try {
      await unfollowGroup(groupId);
      setIsFollowing(false);
    } catch (err) {
      console.error("Lỗi hủy theo dõi nhóm:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      disabled={loading}
      onClick={isFollowing ? handleUnfollow : handleFollow}
      className={`${
        isFollowing
          ? "bg-gray-200 hover:bg-gray-300 text-gray-800"
          : "bg-blue-600 hover:bg-blue-700 text-white"
      } text-sm font-medium px-4 py-2 rounded-md shadow`}
    >
      {isFollowing ? "✔ Đã theo dõi" : "+ Theo dõi"}
    </button>
  );
};

export default FollowButtonGroup;
