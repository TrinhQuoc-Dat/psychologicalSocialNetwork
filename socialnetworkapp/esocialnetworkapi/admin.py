from import_export.admin import ExportMixin
from import_export import resources
from django.contrib import admin
from  esocialnetworkapi.models import (
    User, UGroup,
    Post, PostImage, Comment, Reaction,
    Notification,
    SurveyPost, SurveyQuestion, SurveyOption,
    SurveyDraft, SurveyDraftAnswer, UserSurveyOption, GroupPost,
    Contact, ThreadRoom, ThreadRoomParticipant
)
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.hashers import make_password


class SocialAdminSite(admin.AdminSite):
    site_header = "SOCIAL NETWOK PSYCHOLOGICAL"
    site_title = "SOCIAL NETWOK Admin"
    index_title = "Bảng điều khiển"


admin_site = SocialAdminSite(name="admin")

# ========== Inline ==============
class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get("password"):
            user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# ========== Người dùng ==============
@admin.register(User, site=admin_site)
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserCreationForm
    list_display = ("username", "email", "role", "is_active")
    search_fields = ("username", "email")
    list_filter = ("role",)
    list_editable = ("role", "is_active")
    ordering = ("-date_joined",)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Thông tin cá nhân', {'fields': ('first_name', 'last_name', 'email', 'avatar', 'cover')}),
        ('Quyền', {'fields': ('is_active', 'is_staff', 'is_superuser', 'role')}),
    )

@admin.register(Contact, site=admin_site)
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "from_user", "to_user", "status", "created_date", "updated_date")
    list_filter = ("status",)
    search_fields = ("from_user__username", "to_user__username")
    raw_id_fields = ("from_user", "to_user")


@admin.register(ThreadRoom, site=admin_site)
@admin.register(ThreadRoom)
class ThreadRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "thread_type", "name", "firebase_room_id", "created_at")
    list_filter = ("thread_type",)
    search_fields = ("name", "firebase_room_id")


@admin.register(ThreadRoomParticipant, site=admin_site)
@admin.register(ThreadRoomParticipant)
class ThreadRoomParticipantAdmin(admin.ModelAdmin):
    list_display = ("id", "thread", "user", "joined_at")
    list_filter = ("thread",)
    search_fields = ("thread__name", "user__username")
    raw_id_fields = ("thread", "user")


# ========== Nhóm & Thành viên ==============
@admin.register(UGroup, site=admin_site)
@admin.register(UGroup)
class UGroupAdmin(admin.ModelAdmin):
    list_display = ("group_name", "created_date", "active")
    search_fields = ("group_name",)
    list_filter = ("active",)
    ordering = ("-created_date",)

# ========== Bài đăng ==============
class PostResource(resources.ModelResource):
    class Meta:
        model = Post

@admin.register(Post, site=admin_site)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    resource_class = PostResource
    list_display = ("id", "user", "created_date", "lock_comment", "active")
    search_fields = ("content", "user__username")
    list_filter = ("active", "lock_comment")
    ordering = ("-created_date",)
    inlines = [PostImageInline, CommentInline]

@admin.register(PostImage, site=admin_site)
@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ("post", "image")


@admin.register(GroupPost, site=admin_site)
@admin.register(GroupPost)
class GroupPostAdmin(admin.ModelAdmin):
    pass
    # list_display = ("post", "image")

# ========== Bình luận & cảm xúc ==============
@admin.register(Comment, site=admin_site)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "content", "created_date", "label")
    search_fields = ("content", "user__username")
    list_filter = ("label", "created_date")

@admin.register(Reaction, site=admin_site)
@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "reaction", "created_date")
    list_filter = ("reaction",)
    search_fields = ("user__username",)

# ========== Thông báo ==============
@admin.register(Notification, site=admin_site)
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("recipient", "message", "is_read", "created_at", "notification_type")
    list_filter = ("is_read", "notification_type")
    search_fields = ("message", "recipient__username")
    ordering = ("-created_at",)

# ========== Khảo sát ==============
class SurveyOptionInline(admin.TabularInline):
    model = SurveyOption
    extra = 1

class SurveyQuestionInline(admin.TabularInline):
    model = SurveyQuestion
    extra = 1

@admin.register(SurveyPost, site=admin_site)
@admin.register(SurveyPost)
class SurveyPostAdmin(admin.ModelAdmin):
    list_display = ("post", "survey_type", "status", "end_time")
    list_filter = ("survey_type", "status")
    inlines = [SurveyQuestionInline]

@admin.register(SurveyQuestion, site=admin_site)
@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):
    list_display = ("survey_post", "question", "multi_choice")
    inlines = [SurveyOptionInline]

@admin.register(SurveyOption, site=admin_site)
@admin.register(SurveyOption)
class SurveyOptionAdmin(admin.ModelAdmin):
    list_display = ("survey_question", "option_text", "is_other_option")

@admin.register(SurveyDraft, site=admin_site)
@admin.register(SurveyDraft)
class SurveyDraftAdmin(admin.ModelAdmin):
    list_display = ("survey_post", "user", "drafted_at")

@admin.register(SurveyDraftAnswer, site=admin_site)
@admin.register(SurveyDraftAnswer)
class SurveyDraftAnswerAdmin(admin.ModelAdmin):
    list_display = ("draft", "question", "selected_option", "custom_text")

@admin.register(UserSurveyOption, site=admin_site)
@admin.register(UserSurveyOption)
class UserSurveyOptionAdmin(admin.ModelAdmin):
    list_display = ("user", "survey_option", "custom_text")
