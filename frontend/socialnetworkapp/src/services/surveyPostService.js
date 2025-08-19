import axios from "axios";
import BASE_URL from './baseUrl';
import Authorization from "../components/until/AuthorizationComponent";

export const createSurvey = async (payload, token) => {
  try {
    console.log(payload);
    const response = await axios.post(`${BASE_URL}/survey-posts`, payload, {
      headers: Authorization(),
    });
    return response.data;
  } catch (error) {
    console.error("Error creating survey:", error);
    if (error.response)
      throw error.response?.data;
    throw error
  }
};

export const fetchExpiredSurveyPosts = async (params = {}) => {
  try {
    const response = await axios.get(`${BASE_URL}/api/survey/endtime/`, {
      params,
      headers: Authorization(),
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching expired survey posts:", error);
    if (error.response) throw error.response.data;
    throw error;
  }
};

export const getSurveyStatistics = async (surveyPostId) => {
  try {
    const response = await axios.get(
      `${BASE_URL}/api/survey/${surveyPostId}/statistics/`,
      {
        headers: Authorization(),
      }
    );
    console.log("getSurveyStatistics", response.data)
    return response.data;
  } catch (error) {
    console.error("Error fetching survey statistics:", error);
    throw error;
  }
};

export const checkUserHasAnsweredSurvey = async (surveyPostId) => {
  try {
    const res = await axios.get(`${BASE_URL}/api/survey/${surveyPostId}/answered/`, {
      method: "GET",
      headers: Authorization(),
    });

    console.log(res.data)

    if (res.status !== 200) {
      throw new Error("Không thể kiểm tra trạng thái khảo sát");
    }

    return res.data //  true hoặc false
  } catch (error) {
    console.error("Error checking survey answer status:", error);
    throw error;
  }
};

export const selectMultipleSurveyOptions = async (answers, surveyPostId) => {
  try {
    const res = await axios.post(`${BASE_URL}/api/survey/${surveyPostId}/submit/`, answers, {
      headers: Authorization()
    });

    if (res.status !== 200) {
      throw new Error(res.message || "Lỗi khi gửi khảo sát");
    }

    return res.data;
  } catch (error) {
    console.error(
      "Error selecting multiple survey options:",
      error.response ? error.response.data : error.message
    );
    throw new Error("Có lỗi xảy ra khi gửi lựa chọn khảo sát.");
  }
};
