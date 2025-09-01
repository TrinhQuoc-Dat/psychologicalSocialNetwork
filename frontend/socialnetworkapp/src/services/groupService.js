import axios from "axios";
import Authorization, { AuthorizationFromData } from "../components/until/AuthorizationComponent";
import BASE_URL from "./baseUrl";


export const getGroup = async (Groupid) => {
  try {
    console.log("Groupid", Groupid);
    const response = await axios.get(`${BASE_URL}/api/group/${Groupid}/`, {
      headers: Authorization(),
    });
    console.log("group: ", response.data);
    return response.data;
  } catch (error) {
    console.error("Error fetching user profile:", error);
    throw error;
  }
};

export const getGroupPosts = async (groupId, page = 0, size = 5) => {
  try {
    const response = await axios.get(`${BASE_URL}/api/posts/group/${groupId}/`, {
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

export const followGroup = (groupId) => {
  const res = axios.post(`${BASE_URL}/api/group/${groupId}/follow/`,{}, {
    headers: Authorization()
  });
  return res
};

export const unfollowGroup = (groupId) => {

  return axios.post(`${BASE_URL}/api/group/${groupId}/unfollow/`,{}, {
    headers: Authorization()
  })
};

export const checkFollowingGroup = (groupId) => {
  return axios.get(`${BASE_URL}/api/group/${groupId}/is-following/`, 
    {
      headers: Authorization()
    }
  );
};


export const followingGroupCount = (groupId) => {
  return axios.get(`${BASE_URL}/api/group/${groupId}/followers-count/`, 
    {
      headers: Authorization()
    }
  );
};


export const updateGroupAvatarOrCover = async (formData, groupId) => {
  try {
    const res = await axios.patch(`${BASE_URL}/api/group/${groupId}/update-media/`, formData, {
      headers:AuthorizationFromData(),
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


export const getFollowerGroup = async (page, size=8) => {
  try {
    const res = await axios.get(`${BASE_URL}/api/group/followed/?page=${page}&size=${size}`, {
      headers: Authorization()
    });
    return res.data;
  } catch (error) {
    console.error("Lỗi khi fetch nhóm follower", {
      message: error.message,
      response: error.response?.data,
    });
    throw error;
  }
};