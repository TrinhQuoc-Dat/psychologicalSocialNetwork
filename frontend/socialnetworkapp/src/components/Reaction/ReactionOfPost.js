import axios from "axios";

const ReactionOfPost = async (postId) => {
    const BASE_URL = 'http://localhost:8000';

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