import PostItem from "./PostItem";
import InfiniteScroll from "react-infinite-scroll-component";
import PostSkeleton from "./PostSkeleton";
import { useEffect, useState } from "react";

const PostList = ({
  posts,
  loading,
  error,
  hasMore,
  fetchMoreData,
  customEmptyMessage,
}) => {
  const [page, setPage] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      if (
        window.innerHeight + window.scrollY >=
        document.body.offsetHeight - 100 &&
        hasMore
      ) {
        setPage((prev) => prev + 1);
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, [hasMore]);

  if (loading && Array.isArray(posts) && posts.length === 0) {
    return (
      <div className="max-w-xl mx-auto space-y-4">
        {[...Array(3)].map((_, i) => (
          <PostSkeleton key={i} />
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center text-red-500 p-4">
        Error loading posts: {error}
      </div>
    );
  }

  return (
    <div className="mx-auto">
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
        scrollThreshold={0.8}>
        <div className="space-y-4">
          {posts && posts.map((post) => (
            <PostItem key={post.id} post={post} />
          ))}
        </div>
      </InfiniteScroll>
      {!loading &&
        Array.isArray(posts) &&
        posts.length === 0 &&
        (customEmptyMessage || (
          <div className="text-center py-8 text-gray-500">No posts yet</div>
        ))}
    </div>
  );
};

export default PostList;
