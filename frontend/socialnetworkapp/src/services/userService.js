import axios from "axios";
import BASE_URL from './baseUrl'; 
import Authorization from "../components/until/AuthorizationComponent";

export const changePassword = async (token, oldPassword, newPassword) => {
  try {
    const response = await axios.put(
      `${BASE_URL}/users/password`,
      {
        oldPassword,
        newPassword,
      },
      {
        headers: {
          Authorization: token,
        },
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

export const getUserProfile = async (userId, token) => {
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
