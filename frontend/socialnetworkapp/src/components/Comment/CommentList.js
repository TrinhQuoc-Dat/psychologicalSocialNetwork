import { useEffect, useState } from "react";
import axios from "axios";
import moment from "moment";
import "moment/locale/vi";
import CommentItem from "./CommentItem";
import CommentHasmore from "./CommentHasmore";
import CommentCreated from "./CommentCreated";
import Authorization from "../until/AuthorizationComponent"

moment.locale("vi");

const CommentList = ({ post, showComment, setCountComment }) => {
  const BASE_URL = "http://localhost:8000";
  const [comments, setComments] = useState([]);
  const [page, setPage] = useState(1);
  const [size] = useState(5);
  const [hasMore, setHasMore] = useState(true);

  useEffect(() => {
    setComments([]);
    setPage(0);
    setHasMore(true);
  }, [post.id]);

  useEffect(() => {
    if (hasMore) {
      fetchComments();
    }
  }, [page]);

  const fetchComments = async () => {
    try {
      const response = await axios.get(
        `${BASE_URL}/api/comments/parents?post=${post.id}&page=${1}&size=${size}`,
        {
          headers : Authorization(),
        }
      );
      console.log(response.data);
      const flag = response.data.next === null ? false : true;
      setComments((prev) => {
        const filtered = response.data.results
          .filter((newC) => !prev.some((c) => c.id === newC.id))
          .map((comment) => ({
            ...comment,
            children: [],
            hasMoreReplies: !flag,
          }));

        return [...prev, ...filtered];
      });

      setHasMore(flag);
    } catch (error) {
      console.error("Lỗi khi tải bình luận:", error);
    }
  };

  const updateCommentTree = (comments, parentId, newReplies, hasMore) => {
    return comments.map((comment) => {
      if (comment.id === parentId) {
        const existingIds = comment.children?.map((c) => c.id) || [];
        const uniqueReplies = newReplies.filter(
          (r) => !existingIds.includes(r.id)
        );
        if (hasMore === null)
          hasMore = false

        return {
          ...comment,
          children: [...(comment.children || []), ...uniqueReplies],
          hasMoreReplies: hasMore,
        };
      } else if (comment.children && comment.children.length > 0) {
        return {
          ...comment,
          children: updateCommentTree(
            comment.children,
            parentId,
            newReplies,
            hasMore
          ),
        };
      }
      return comment;
    });
  };

  const fetchReplies = async (parentId) => {
    try {
      const res = await axios.get(`${BASE_URL}/api/comments/children?parent_id=${parentId}`, {
        headers: Authorization(),
      });
      console.log("reaply===> ", res.data.results);
      const newReplies = res.data.results.map((reply) => ({
        ...reply,
        hasMoreReplies: true,
      }));

      setComments((prevComments) =>
        updateCommentTree(prevComments, parentId, newReplies, res.data.next)
      );
    } catch (err) {
      console.error("Lỗi khi tải replies:", err);
    }
  };

  const handleNewComment = (comment, parentId = null) => {
    if (parentId === null) {
      setComments((prev) => [comment, ...prev]);
    } else {
      const addReply = (comments) => {
        return comments.map((c) => {
          if (c.id === parentId) {
            return {
              ...c,
              children: [comment, ...(c.children || [])],
            };
          }
          if (c.children) {
            return {
              ...c,
              children: addReply(c.children),
            };
          }
          return c;
        });
      };
      setComments((prev) => addReply(prev));
    }
  };

  const handleDeleteComment = (commentId) => {
    const deleteRecursive = (comments) => {
      return comments
        .filter((c) => c.id !== commentId)
        .map((c) => ({
          ...c,
          children: c.children ? deleteRecursive(c.children) : [],
        }));
    };

    setComments((prev) => deleteRecursive(prev));
  };

  const handleCommentUpdated = (updatedComment) => {
    const updateRecursive = (comments) => {
      return comments.map((c) => {
        if (c.id === updatedComment.id) return updatedComment;
        if (c.children) {
          return {
            ...c,
            children: updateRecursive(c.children),
          };
        }
        return c;
      });
    };
    setComments((prev) => updateRecursive(prev));
  };

  const renderComments = (commentsList) => {
    return commentsList.map((comment) => (
      <div key={comment.id} className="ml-4 mt-4">
        <div className="flex gap-3">
          <CommentItem
            userId={post.user.id}
            comment={comment}
            post={post}
            onCommentAdded={(c) => handleNewComment(c, comment.id)}
            handleCommentUpdated={handleCommentUpdated}
            showComment={showComment}
            handleDeleteComment={handleDeleteComment}
            isComment={post.lockComment}
          />
        </div>

        {comment.children && comment.children.length > 0 && (
          <div className="ml-6 pl-6 border-l border-gray-200 space-y-4">
            {renderComments(comment.children)}
          </div>
        )}

        {comment.hasMoreReplies && (
          <div className="pl-6 mt-2">
            <button
              className="text-sm text-blue-600 font-medium hover:underline"
              onClick={() => fetchReplies(comment.id)}
            >
              Xem thêm trả lời
            </button>
          </div>
        )}
      </div>
    ));
  };


  return (
    <div className="space-y-2 gap-3">
      {renderComments(comments)}

      {hasMore && <CommentHasmore setPage={setPage} />}
      {post.lock_comment === false && (
        <CommentCreated post={post} onCommentAdded={handleNewComment} />
      )}
    </div>
  );
};

export default CommentList;
