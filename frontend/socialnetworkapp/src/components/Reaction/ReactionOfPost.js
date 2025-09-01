import axios from "axios";
import BASE_URL from "../../services/baseUrl";

const ReactionOfPost = async (postId) => {
    try {
        const res = await axios.get(`${BASE_URL}/api/reactions/post-reactions/?post_id=${postId}`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token') || ''}`
            }
        });
        return res.data;
    } catch (err) {
        console.error("Lỗi khi thêm phản ứng:", err);
    }
}

export default ReactionOfPost;