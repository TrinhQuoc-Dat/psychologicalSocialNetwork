import React, { useEffect, useState } from "react";
import { fetchExpiredSurveyPosts } from "../services/surveyPostService";
import PostList from "../components/PostList/PostList";
import { useSelector } from "react-redux";
import InfiniteScroll from "react-infinite-scroll-component";
import PostSkeleton from "../components/PostList/PostSkeleton";
import PostItem from "../components/PostList/PostItem";

const ExpiredSurveyPostsPage = () => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [size] = useState(3);
  const [total, setTotal] = useState(0);
  const [hasMore, setHasMore] = useState(true);

  const fetchPosts = async (pageNum) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetchExpiredSurveyPosts(
        { page: pageNum, size },
      );
      console.log(response.results)

      setPosts(prev => pageNum === 1 ? response.results : [...prev, ...response.results]);
      setTotal(response.count);
      setHasMore(response.next !== null);
    } catch (err) {
      setError(err.message || "Lỗi khi tải dữ liệu khảo sát hết hạn");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Load initial data
  useEffect(() => {
    fetchPosts(1);
  }, []);

  // Handle infinite scroll
  const fetchMoreData = () => {
    if (!loading && hasMore) {
      const nextPage = page + 1;
      setPage(nextPage);
      fetchPosts(nextPage);
    }
  };

  // Handle manual pagination (optional)
  const handlePageChange = (newPage) => {
    if (newPage !== page) {
      setPage(newPage);
      fetchPosts(newPage);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-semibold mb-4">Danh sách khảo sát đã hết hạn</h1>
      <InfiniteScroll
        dataLength={posts?.length || 0}
        next={fetchMoreData}
        hasMore={hasMore}
        loader={
          <div className="space-y-4">
            {[...Array(2)].map((_, i) => (
              <PostSkeleton key={i} />
            ))}
          </div>
        }
        endMessage={
          <p className="text-center text-gray-500 py-4">
            You've seen all posts
          </p>
        }
        scrollThreshold={0.8}
      >
        <div className="space-y-4">
          {posts && posts.map((survey) => (
            <div key={survey.id} className="mb-4">
              <p className="text-sm text-red-500">
                Hết hạn: {new Date(survey.end_time).toLocaleString()}
              </p>
              <PostItem key={survey.post.id} post={survey.post} survey_id={survey.id}/>
            </div>
          ))}
        </div>
      </InfiniteScroll>

      {/* Optional: Traditional pagination */}
      {total > size && (
        <div className="flex justify-center space-x-2 mt-4">
          <button
            disabled={page === 1 || loading}
            onClick={() => handlePageChange(page - 1)}
            className="px-3 py-1 bg-gray-200 rounded disabled:opacity-50"
          >
            Trước
          </button>
          <span className="px-3 py-1">
            {page} / {Math.ceil(total / size)}
          </span>
          <button
            disabled={page === Math.ceil(total / size) || loading}
            onClick={() => handlePageChange(page + 1)}
            className="px-3 py-1 bg-gray-200 rounded disabled:opacity-50"
          >
            Tiếp
          </button>
        </div>
      )}
    </div>
  );
};

export default ExpiredSurveyPostsPage;