import React, { useEffect } from 'react';
import { useInView } from 'react-intersection-observer';
import PostList from '../PostList/PostList';
import ProfileAbout from './ProfileAbout';

const ProfileTimeline = ({ posts, loadMore, hasMore, loading, user }) => {
  const { ref, inView } = useInView();

  useEffect(() => {
    if (inView && hasMore && !loading) {
      loadMore();
    }
  }, [inView, hasMore, loadMore, loading]);

  return (
    <div className="max-w-6xl mx-auto mb-5 grid grid-cols-1 lg:grid-cols-3 gap-6">
  {/* Cột trái: giới thiệu, cố định khi scroll */}
  <div className="lg:col-span-1">
    <div className="sticky top-4">
      <ProfileAbout user={user} />
    </div>
  </div>

  {/* Cột phải: danh sách bài post */}
  <div className="lg:col-span-2">
    <PostList 
      posts={posts}
      loading={loading}
      error={null}
      hasMore={hasMore}
      fetchMoreData={loadMore}
      customEmptyMessage={
        <div className="text-center py-8 text-gray-500">
          No posts yet
        </div>
      }
    />
  </div>
</div>

  );
};

export default ProfileTimeline;