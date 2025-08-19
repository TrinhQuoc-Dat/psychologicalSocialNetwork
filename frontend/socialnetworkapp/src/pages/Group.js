import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getUserProfile, getUserPosts } from "../services/userService";
import ProfileHeaderGroup from "../components/Group/ProfileHeaderGroup";
import ProfileTabsGroup from "../components/Group/ProfileTabsGroup";
import ProfileTimelineGroup from "../components/Group/ProfileTimelineGroup";
import ProfileAboutGroups from "../components/Group/ProfileAboutGroup";
import ProfilePhotosGroup from "../components/Group/ProfilePhotosGroup";
import { useSelector } from "react-redux";
import CreatePostBar from "../components/PostForm/CreatePostBar";
import { getGroup, getGroupPosts } from "../services/groupService";

const Group = () => {
  const { id } = useParams();
  const { token, user: currentUser } = useSelector((state) => state.auth);
  const [group, setGroup] = useState(null);
  const [posts, setPosts] = useState([]);
  const [page, setPage] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const [activeTab, setActiveTab] = useState("timeline");
  const [loading, setLoading] = useState(false);
  const [initialLoad, setInitialLoad] = useState(true);

  const loadPosts = async (pageNumber, reset = false) => {
    try {
      setLoading(true);
      const response = await getGroupPosts(id, pageNumber, 5);
      console.log("groupPost: ", response);
      setPosts((prev) =>
        reset ? response.results : [...prev, ...response.results]
      );
      setHasMore(response.next !== null);
      setInitialLoad(false);
    } catch (error) {
      console.error("Error loading posts:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (token) {
      const fetchGroup = async () => {
        try {
          const gData = await getGroup(id);
          console.log("group: ", gData);
          setGroup(gData);
        } catch (error) {
          console.error("Error fetching group:", error);
        }
      };

      fetchGroup();
      setPage(1);
      loadPosts(1, true);
    }
  }, [id, token]);


  const handleLoadMore = async () => {
    const nextPage = page + 1;
    setPage(nextPage);
    await loadPosts(nextPage);
  };

  if (!group && initialLoad) {
    return (
      <div className="max-w-4xl mx-auto mt-6 space-y-4">
        <div className="h-48 bg-gray-200 animate-pulse rounded-xl" />
        <div className="h-12 bg-gray-200 animate-pulse rounded-xl" />
      </div>
    );
  }


  const isCurrentUserProfile = currentUser?.id === group?.id;
  return (
    <div className="max-w-4xl mx-auto">
      {group && <ProfileHeaderGroup group={group} />}
      <ProfileTabsGroup activeTab={activeTab} setActiveTab={setActiveTab} />

      {activeTab === "timeline" && (
        <>
          {isCurrentUserProfile && (
            <div className="max-w-xl mx-auto mb-4">
              <CreatePostBar user={currentUser} />
            </div>
          )}
          {group && <ProfileTimelineGroup
            group={group}
            posts={posts}
            loadMore={handleLoadMore}
            hasMore={hasMore}
            loading={loading}
          />}

        </>
      )}

      {activeTab === "about" && (
        <div className="max-w-xl mx-auto">
          <ProfileAboutGroups group={group} />
        </div>
      )}

      {activeTab === "photos" && (
        <div className="max-w-xl mx-auto">
          <ProfilePhotosGroup posts={posts} />
        </div>
      )}
    </div>
  );
};

export default Group;