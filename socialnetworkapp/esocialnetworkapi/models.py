from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField
from django.utils import timezone


# ========== NGười Dùng ===============

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    deleted_date = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class User(AbstractUser):
    ROLE_CHOICES = [('ADMIN', 'admin'), ('USER', 'user'), ("USERPREMIUM", "userpremium")]
    avatar = CloudinaryField('avatar', default='v1753776324/gmrkdeularqtqhqidc4g.jpg')
    cover = CloudinaryField('cover', null=True, blank=True)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='USER')

class Contact(BaseModel):
    # Người gửi lời mời
    from_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='contacts_sent')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts_received')

    STATUS_CHOICES = [
        ('PENDING', 'pending'),   # Đang chờ chấp nhận
        ('ACCEPTED', 'accepted'), # Đã là bạn bè
        ('BLOCKED', 'blocked'),   # Đã chặn
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user} → {self.to_user} ({self.status})"


class ThreadRoom(models.Model):
    THREAD_TYPE_CHOICES = [
        ("DIRECT", "direct"),  # Chat 1-1
        ("GROUP", "group"),    # Chat nhóm
    ]

    thread_type = models.CharField(max_length=10, choices=THREAD_TYPE_CHOICES, default="DIRECT")
    name = models.CharField(max_length=255, blank=True, null=True)  # Tên nhóm (nếu group)
    avatar = models.URLField(blank=True, null=True)  # Ảnh nhóm (nếu cần)
    firebase_room_id = models.CharField(max_length=255)  # ID phòng trên Firebase

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Thread {self.name}"
    

class ThreadRoomParticipant(models.Model):
    thread = models.ForeignKey(ThreadRoom, on_delete=models.CASCADE, related_name="participants")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("thread", "user")
        indexes = [
            models.Index(fields=["thread", "user"]),
        ]

    def __str__(self):
        return f"{self.user.username} in Thread {self.thread}"
    

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

class UGroup(models.Model):
    GROUP_TYPE_CHOICES = [
        ('support', 'Hỗ trợ tâm lý'),
        ('research', 'Nghiên cứu khoa học'),
        ('sharing', 'Chia sẻ - Tâm sự'),
        ('therapy', 'Trị liệu'),
    ]

    group_name = models.CharField(max_length=255, unique=True)
    creator = models.ForeignKey('User', on_delete=models.CASCADE, null=True,  related_name='created_groups')
    avatar = CloudinaryField('avatar', default='v1753776324/gmrkdeularqtqhqidc4g.jpg')
    cover = CloudinaryField("cover", default='v1753776324/gmrkdeularqtqhqidc4g.jpg')
    introduce = models.CharField(max_length=255, null=True)
    rule = models.TextField(null=True)
    private = models.BooleanField(default=True)
    type = models.CharField(max_length=50, choices=GROUP_TYPE_CHOICES, default='support')
    location = models.CharField(max_length=255, null=True, blank=True)
    followers = models.ManyToManyField(User,related_name='followed_groups',blank=True)
    tags = models.ManyToManyField(Tag, related_name='groups', blank=True)
    report_count = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    deleted_date = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_date']

# ================ Bài Đăng, like, comment===============
class Post(BaseModel):
    content = models.TextField()
    lock_comment = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        ordering = ['-created_date']

class PostImage(BaseModel):
    image = CloudinaryField('post_image', null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Comment(BaseModel):
    content = models.TextField()
    image = CloudinaryField('comment_image', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    label = models.CharField(max_length=20, null=True, blank=True)

class Reaction(BaseModel):
    REACTION_CHOICES = [('LIKE', 'like'), ('HAHA', 'haha'), ('LOVE', 'love')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=10, choices=REACTION_CHOICES, default='LIKE')

    class Meta:
        unique_together = ('user', 'post')


class GroupPost(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, primary_key=True)
    group = models.ForeignKey(UGroup, on_delete=models.CASCADE, related_name="group_post")

# ============= THông Báo ======================
class Notification(models.Model):
    NOTIF_TYPE = [('POSTGROUP', 'postgroup'), ('SYSTEM', 'system'), ("REACTION", "reaction"), ("COMMENT", "comment"), ("CONTACT", "contact")]
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_received')
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_sent', null=True, blank=True)
    message = models.CharField(max_length=500)
    link = models.CharField(max_length=255, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    notification_type = models.CharField(max_length=20, choices=NOTIF_TYPE, null=True, blank=True)

# ============ Khảo sát =====================
class SurveyPost(models.Model):
    TYPE = [
        ('MENTAL_HEALTH', 'Mental Health'),
        ('TRAINING_PROGRAM', 'Training Program'),
        ('RECRUITMENT_INFORMATION', 'Recruitment Info'),
        ('INCOME', 'Income'),
        ('EMPLOYMENT_SITUATION', 'Employment Situation'),
    ]
    STATUS = [('ACTIVE', 'active'), ('EXPIRED', 'expired')]
    post = models.OneToOneField(Post, on_delete=models.CASCADE, primary_key=True)
    end_time = models.DateTimeField()
    survey_type = models.CharField(max_length=30, choices=TYPE)
    status = models.CharField(max_length=10, choices=STATUS, default='ACTIVE')


class SurveyQuestion(models.Model):
    question = models.TextField()
    multi_choice = models.BooleanField(default=False)
    survey_post = models.ForeignKey(SurveyPost, on_delete=models.CASCADE)


class SurveyOption(models.Model):
    option_text = models.TextField()
    survey_question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    is_other_option = models.BooleanField(default=False)


class SurveyDraft(models.Model):
    survey_post = models.ForeignKey(SurveyPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    drafted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('survey_post', 'user')


class SurveyDraftAnswer(models.Model):
    draft = models.ForeignKey(SurveyDraft, on_delete=models.CASCADE)
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(SurveyOption, on_delete=models.CASCADE)
    custom_text = models.TextField(null=True, blank=True)


class UserSurveyOption(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    survey_option = models.ForeignKey(SurveyOption, on_delete=models.CASCADE)
    custom_text = models.TextField(null=True, blank=True)  

    class Meta:
        unique_together = ('user', 'survey_option')

