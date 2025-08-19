import axios from "axios";
import Authorization from "../until/AuthorizationComponent";

const BASE_URL = 'http://localhost:8000/api';

const addReaction = async (postId, typeReaction) => {
    try {
        const formData = new FormData();
        formData.append("post", postId);
        formData.append("reaction", typeReaction);
        console.log(typeReaction);

        const res = await axios.post(`${BASE_URL}/reactions/`, formData, {
            headers: Authorization()
        });
        console.log(res);
        console.log(res.status);
    } catch (err) {
        console.error("Lỗi khi thêm phản ứng:", err);
    }
};

export default addReaction;