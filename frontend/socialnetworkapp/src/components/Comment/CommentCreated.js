import axios from "axios";
import { useReducer, useState } from "react";
import { FaImage, FaPaperPlane, FaSpinner } from "react-icons/fa";
import { useSelector } from "react-redux";
import { toast } from "react-toastify";
import defaultAvatar from "../../assets/image/default-user.png";
import Authorization from "../until/AuthorizationComponent";

const CommentCreated = ({
  post,
  parentComment = null,
  onCommentAdded,
  handleReplies,
  setReplyTo,
}) => {
  const BASE_URL = "http://127.0.0.1:8000";
  const [content, setContent] = useState("");
  const [parentId, setParentId] = useState(parentComment);
  const [file, setFile] = useState(null);
  const { user } = useSelector((state) => state.auth);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmitAddComment = async (e) => {
    e.preventDefault();

    if (!content.trim() && !file) {
      return toast.error("Nhập nội dung bình luận");
    }

    setIsSubmitting(true);
    const formData = new FormData();
    formData.append("content", content);
    formData.append("post", post.id);
    if (parentId) formData.append("parent", parentId);
    if (file) formData.append("image", file);

    try {
      const response = await axios.post(`${BASE_URL}/api/comments/`, formData, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}` || null,
          "Content-Type": "multipart/form-data",
        },
      });

      if (response.status === 201) {
        const result = response.data;
        toast.success("Bình luận thành công");
        if (parentId !== null) {
          setReplyTo(null);
          handleReplies(result, parentId);
        } else {
          onCommentAdded(result);
        }
        setFile(null);
        setContent("");
      } else {
        alert("Lỗi khi gửi bình luận");
      }
    } catch (error) {
      console.error("Lỗi:", error.response?.data || error.message);
      toast.success("Lỗi:", error.response?.data || error.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmitAddComment}
      className="flex items-start gap-4 p-4 border rounded-lg"
    >
      {/* Avatar */}
      <img
        src={user?.avatar || defaultAvatar}
        alt="Avatar"
        className="w-10 h-10 rounded-full object-cover"
      />

      {/* Input & actions */}
      <div className="flex-1 flex flex-col gap-2">
        {/* Row: input + send */}
        <div className="flex items-center gap-2">
          <input
            type="text"
            className="flex-1 border border-gray-300 rounded-full px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
            placeholder="Viết bình luận..."
            value={content}
            onChange={(e) => setContent(e.target.value)}
            disabled={isSubmitting}
          />
          <button
            type="submit"
            className={`p-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 transition
                            ${isSubmitting
                ? "bg-gray-300 cursor-not-allowed"
                : "bg-blue-500 hover:bg-blue-600 text-white"
              }`}
          >
            {isSubmitting ? (
              <FaSpinner className="w-4 h-4 animate-spin text-gray-600" />
            ) : (
              <FaPaperPlane className="w-4 h-4 text-white" />
            )}
          </button>
        </div>

        {/* Row: image picker */}
        <label className="flex items-center text-gray-500 hover:text-gray-700 cursor-pointer">
          <FaImage className="w-5 h-5 mr-1 text-blue" />
          <span className="text-sm">Chọn hình</span>
          <input
            type="file"
            accept="image/*"
            className="hidden"
            onChange={(e) => setFile(e.target.files[0])}
            disabled={isSubmitting}
          />
        </label>

        {/* Preview file name (nếu có) */}
        {file && (
          <div className="text-xs text-gray-600">Đã chọn: {file.name}</div>
        )}
      </div>
    </form>
  );
};

export default CommentCreated;
