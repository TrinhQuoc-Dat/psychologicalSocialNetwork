from notifications.utils import create_and_send_notification

def add_reaction(user, post, reaction_type):
    # tạo reaction ...
    post_author = post.user
    if post_author != user:  # không tự thông báo cho chính mình
        create_and_send_notification(
            recipient=post_author,
            message=f"Đã {reaction_type} bài viết của bạn",
            notif_type="REACTION",
            link=f"/posts/{post.id}/",
            actor=user
        )

def delete_reaction(user, post, reaction_type):
    # tạo reaction ...
    post_author = post.user
    if post_author != user:  # không tự thông báo cho chính mình
        create_and_send_notification(
            recipient=post_author,
            message=f"Đã xoá {reaction_type} bài viết của bạn",
            notif_type="REACTION",
            link=f"/posts/{post.id}/",
            actor=user
        )


def add_comment(user, post, content):
    # tạo comment ...
    post_author = post.user
    if post_author != user:
        create_and_send_notification(
            recipient=post_author,
            message=f"Đã bình luận vào bài viết của bạn",
            notif_type="COMMENT",
            link=f"/posts/{post.id}/",
            actor=user
        )


def send_friend_request(from_user, to_user):
    # tạo Contact ...
    create_and_send_notification(
        recipient=to_user,
        message=f"Đã gửi cho bạn một lời mời kết nối",
        notif_type="CONTACT",
        link=f"/contacts/",
        actor=from_user
    )


def create_group_post(user, group, post):
    # tạo GroupPost ...
    members = group.followers.all()
    for member in members:
        if member != user:
            create_and_send_notification(
                recipient=member,
                message=f"Có bài viết mới trong nhóm {group.group_name}",
                notif_type="POSTGROUP",
                link=f"/groups/{group.id}/posts/{post.id}/",
                actor=user
            )
