import axios from "axios";
import BASE_URL from './baseUrl'; 
import Authorization from "../components/until/AuthorizationComponent";

export const changePassword = async (formData) => {
  try {
    console.log(Authorization())
    const response = await axios.patch(
      `${BASE_URL}/api/users/change-password/`,
      formData,
      {
        headers: Authorization()
      }
    );
    return response.data;
  } catch (error) {
    console.log(error)
    if (error.response && error.response.data) {
      throw new Error(error.response.data.message);
    } else {
      throw new Error("Đã xảy ra lỗi khi đổi mật khẩu");
    }
  }
};

export const getUserProfile = async (userId) => {
  try {
    const response = await axios.get(`${BASE_URL}/api/users/${userId}`, {
      headers: Authorization(),
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching user profile:", error);
    throw error;
  }
};

export const getUserPosts = async (userId, token, page = 0, size = 5) => {
  try {
    const response = await axios.get(`${BASE_URL}/api/users/${userId}/posts`, {
      headers:Authorization(),
      params: {
        page,
        size,
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching user posts:", error);
    throw error;
  }
};

export const getAllUsers = async (
  { page = 1, size = 10, keyword = "" },
  token
) => {
  try {
    const params = { page, size };
    if (keyword.trim() !== "") {
      params.keyword = keyword;
    }

    const response = await axios.get(`${BASE_URL}/api/contact/friends/`, {
      params,
      headers: Authorization(),
    });

    return response.data;
  } catch (error) {
    console.error("Lỗi API getAllUsers:", {
      message: error.message,
      response: error.response?.data,
      config: error.config,
    });
    throw error;
  }
};

export const updateUserAvatarOrCover = async (formData, token) => {
  try {
    const res = await axios.put(`${BASE_URL}/user/update`, formData, {
      headers: {
        Authorization: token,
        "Content-Type": "multipart/form-data",
      },
    });
    return res.data;
  } catch (error) {
    console.error("Lỗi cập nhật avatar/cover:", {
      message: error.message,
      response: error.response?.data,
    });
    throw error;
  }
};


export const sendFriendRequest = async (toUserId) => {
  try {
    const response = await axios.post(
      `${BASE_URL}/api/contact/user/`,
      { to_user: toUserId },
      { headers: Authorization() }
    );
    return response.data;
  } catch (error) {
    console.error("Lỗi gửi lời mời kết bạn:", error);
    throw error.response?.data || { message: "Đã xảy ra lỗi" };
  }
};