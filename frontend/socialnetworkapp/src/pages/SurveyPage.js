import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import PostList from "../components/PostList/PostList";
import { fetchSurveyPosts } from "../features/posts/postSlice";
import LeftSidebar from "../components/layout/LeftSidebar";
import RightSidebar from "../components/layout/RightSidebar";
import SurveyCreateForm from "../components/survey/SurveyCreateForm";

const SurveyPage = () => {
  const dispatch = useDispatch();
  const { surveyPosts, error, surveyHasMore, surveyCurrentPage, surveyLoading } = useSelector(
    (state) => state.posts
  );
  const role = useSelector((state) => state.auth.role);

  useEffect(() => {
    dispatch(fetchSurveyPosts({ page: 1, size: 5, refresh: true }));
  }, [dispatch]);

  const fetchMoreData = () => {
    if (surveyHasMore) {
      dispatch(fetchSurveyPosts({ page: surveyCurrentPage + 1, size: 5 }));
    }
  };

  return (
    <div className="flex justify-center">
      {/* Left Sidebar */}
      <LeftSidebar />

      {/* Main Content */}
      <div className="w-full lg:w-3/5 space-y-6">
        <div className="bg-white rounded-xl shadow p-4">
          <h1 className="text-2xl font-bold text-gray-800 mb-4">Khảo sát</h1>
          <p className="text-gray-600 mb-6">
            Xem và tham gia các khảo sát Tâm lý học từ mọi người.
          </p>

          <SurveyCreateForm />
        </div>

        

        <PostList
          posts={surveyPosts}
          loading={surveyLoading}
          error={error}
          hasMore={surveyHasMore}
          fetchMoreData={fetchMoreData}
          customEmptyMessage={
            <div className="text-center py-8 text-gray-500">
              Hiện chưa có khảo sát nào
            </div>
          }
        />
      </div>

      {/* Right Sidebar */}
      <RightSidebar />
    </div>
  );
};

export default SurveyPage;
