import React, { useEffect } from 'react';
import { useInView } from 'react-intersection-observer';
import PostList from '../PostList/PostList';
import CreatePostBar from '../PostForm/CreatePostBar';
import { useSelector } from 'react-redux';

const ProfileTimelineGroup = ({ posts, loadMore, hasMore, loading, group }) => {
  const { ref, inView } = useInView();
  const { user } = useSelector((state) => state.auth);
  useEffect(() => {
    if (inView && hasMore && !loading) {
      loadMore();
    }
  }, [inView, hasMore, loadMore, loading]);

  return (
    <div className="max-w-6xl mx-auto px-4 grid grid-cols-1 lg:grid-cols-10 gap-6 mt-6">
      {/* Cột Giới thiệu - chiếm 4 phần */}
      <div className="lg:col-span-4">
        <div className="sticky top-10">
          <div className="bg-white rounded-xl shadow p-4 w-full text-sm">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Giới thiệu</h2>
            <p className="text-gray-700 mb-4">
              {group?.introduce}
            </p>
            <ul className="space-y-3 text-gray-700">
              <li className="flex items-start gap-2">
                <span className="text-gray-500">📄</span>
                <span><strong>Trang</strong> · {group?.type}</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-gray-500">📍</span>
                <span>{group?.location}</span>
              </li>
              {group.creator.phone && (
                <li className="flex items-start gap-2">
                  <span className="text-gray-500">📞</span>
                  <span>{group?.creator.phone}</span>
                </li>)}

              {group.creator.email && (
                <li className="flex items-start gap-2">
                  <span className="text-gray-500">✉️</span>
                  <span>{group?.creator.email}</span>
                </li>)}

              <li className="flex items-start gap-2">
                <span className="text-gray-500">🔗</span>
                <a
                  href="https://ou.edu.vn/"
                  className="text-blue-600 hover:underline"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  ou.edu.vn
                </a>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-green-600">🟢</span>
                <span>Luôn mở cửa</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-yellow-500">⭐</span>
                <span>96% đề xuất</span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* Cột PostList - chiếm 6 phần */}
      <div className="lg:col-span-6">
        <CreatePostBar user={user} groupId={group.id} />
        <div className='mt-3'>
          {posts.count === 0 ? <div className="text-center py-8 text-gray-500">
            Không tìm thấy bài viết nào trong group!!!
          </div> : <PostList
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
          />}
        </div>


      </div>
    </div>

  );
};

export default ProfileTimelineGroup;