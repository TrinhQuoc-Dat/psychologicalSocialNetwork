import axios from "axios";
import BASE_URL from './baseUrl';
import Authorization, { AuthorizationFromData } from "../components/until/AuthorizationComponent";

export const fetchPosts = async (params = {}) => {
  try {
    const response = await axios.get(`${BASE_URL}/api/posts/`, {
      params,
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching posts:", error);
    throw error;
  }
};

export const createPost = async (formData) => {
  try {
    const response = await axios.post(`${BASE_URL}/api/posts/`, formData, {
      headers: AuthorizationFromData(),
    });
    return response.data;
  } catch (error) {
    console.error("Error creating post:", error);
    throw error;
  }
};

export const updatePost = async (postId, formData) => {
  try {
    const response = await axios.put(`${BASE_URL}/api/posts/${postId}/`, formData, {
      headers: AuthorizationFromData(),
    });
    return response.data;
  } catch (error) {
    console.error("Error updating post:", error);
    throw error;
  }
};

export const getPostById = async (postId) => {
  try {
    const response = await axios.get(`${BASE_URL}/api/posts/${postId}/`);
    return response.data;
  } catch (error) {
    console.error("Error fetching post by ID:", error);
    throw error;
  }
};

export const getSurveyById = async (SurveyById) => {
  try {
    const response = await axios.get(`${BASE_URL}/api/survey/${SurveyById}/`, {
      headers: Authorization()
    }
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching post by ID:", error);
    throw error;
  }
};


// Xóa mềm bài viết
export const softDeletePost = async (postId, token) => {
  try {
    const response = await axios.put(
      `${BASE_URL}/api/posts/${postId}/delete/`,
      {},
      {
        headers: Authorization(),
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error soft deleting post:", error);
    throw error;
  }
};

// Khôi phục bài viết
export const restorePost = async (postId, token) => {
  try {
    const response = await axios.put(
      `${BASE_URL}/api/posts/${postId}/restore/`,
      {},
      {
        headers: Authorization(),
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error restoring post:", error);
    throw error;
  }
};

// Xóa cứng bài viết
export const forceDeletePost = async (postId, token) => {
  console.log("token: ", token)
  try {
    const response = await axios.delete(
      `${BASE_URL}/api/posts/${postId}/force/`,
      {
        headers: Authorization(),
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error force deleting post:", error);
    throw error;
  }
};

// Lấy danh sách các bài viết đã bị xóa mềm
export const getDeletedPosts = async (token) => {
  try {
    const response = await axios.get(
      `${BASE_URL}/api/posts/deleted/`,
      {
        headers: Authorization(),
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching deleted posts:", error);
    throw error;
  }
};
