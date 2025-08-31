from rest_framework import serializers
from .models import User, UGroup, Post,Tag, PostImage,Contact, ThreadRoom, ThreadRoomParticipant, Reaction, Comment, SurveyPost,SurveyOption,SurveyDraftAnswer,SurveyDraft,SurveyQuestion
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'username', 'email', 'avatar', 'role', 'cover']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    
    def get_avatar(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return None
    
    def get_cover(self, obj):
        if obj.cover:
            return obj.cover.url
        return None

class UserSearchSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'username','avatar']
        extra_kwargs = {'password': {'write_only': True}}

    def get_avatar(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return None
    

class ContactSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)

    class Meta:
        model = Contact
        fields = ["id", "from_user", "to_user", "status", "created_date", "updated_date"]
    
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UGroup
        fields = ['id', 'group_name', 'created_date', 'updated_date', 'creator']
        read_only_fields = ['creator']

class PostImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = PostImage
        fields = ['id', 'image']

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    images = serializers.SerializerMethodField()
    reaction_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    current_user_reacted = serializers.SerializerMethodField()
    survey_post = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'content', 'lock_comment', 'user',
                  'created_date', 'updated_date', 'deleted_date', 'images',
                  'reaction_count', 'comment_count', 'current_user_reacted', 'survey_post']
        
    def get_survey_post(self, obj):
        try:
            survey_post = SurveyPost.objects.get(post=obj)
            return SurveyPostSerializer(survey_post).data
        except SurveyPost.DoesNotExist:
            return None
        
    def get_images(self, obj):
        images = obj.postimage_set.filter(active=True)
        return PostImageSerializer(images, many=True).data

    def get_reaction_count(self, obj):
        return Reaction.objects.filter(post=obj, active=True).count()

    def get_comment_count(self, obj):
        return Comment.objects.filter(post=obj, active=True).count()

    def get_current_user_reacted(self, obj):
        user = self.context.get('request').user
        if not user or not user.is_authenticated:
            return False
        return Reaction.objects.filter(post=obj, user=user, deleted_date__isnull=True).exists()
    


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    replies_count = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'image', 'user', 'post', 'parent',
                  'created_date', 'replies_count']

    def get_replies_count(self, obj):
        return Comment.objects.filter(parent=obj, deleted_date__isnull=True).count()
    
    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None
    

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ['id', 'post', 'reaction', 'user']
        read_only_fields = ['id', 'user']


# ============== khảo sát =================

class SurveyPostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='post.id', read_only=True)
    class Meta:
        model = SurveyPost
        fields = ['id','end_time', 'survey_type', "status"]

class SurveyOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyOption
        fields = ['id', 'option_text', "is_other_option"]

# Dùng để đọc
class SurveyQuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = SurveyQuestion
        fields = ['id', 'question', 'multi_choice', 'options']

    def get_options(self, obj):
        options = SurveyOption.objects.filter(survey_question=obj)
        return SurveyOptionSerializer(options, many=True).data

# Dùng để tạo
class SurveyQuestionCreateSerializer(serializers.ModelSerializer):
    options = SurveyOptionSerializer(many=True, write_only=True)

    class Meta:
        model = SurveyQuestion
        fields = ['question', 'multi_choice', 'options']


class SurveyPostCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='post.id', read_only=True)
    created_date = serializers.DateTimeField(source='post.created_date', read_only=True)
    content = serializers.CharField(source='post.content', write_only=True)
    questions = SurveyQuestionCreateSerializer(many=True, write_only=True)
    questions_read = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SurveyPost
        fields = ['id', 'content', 'end_time','created_date', 'survey_type', "status", 'questions', 'questions_read']

    def get_questions_read(self, obj):
        questions = SurveyQuestion.objects.filter(survey_post=obj)
        return SurveyQuestionSerializer(questions, many=True).data

    def create(self, validated_data):
        post_data = validated_data.pop('post')
        questions_data = validated_data.pop('questions')
        user = self.context['request'].user

        post = Post.objects.create(content=post_data['content'], user=user)
        survey_post = SurveyPost.objects.create(post=post, **validated_data)

        for question_data in questions_data:
            options_data = question_data.pop('options')
            question = SurveyQuestion.objects.create(survey_post=survey_post, **question_data)
            for option_data in options_data:
                SurveyOption.objects.create(survey_question=question, **option_data)

        return survey_post



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class GroupDetailSerializer(serializers.ModelSerializer):
    creator = UserSerializer()
    tags = TagSerializer(many=True)
    member_count = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField()

    class Meta:
        model = UGroup
        fields = [
            'id', 'group_name', 'creator', 'avatar', 'cover',
            'introduce', 'rule', 'private', 'type', 'location',
            'tags', 'report_count', 'created_date', 'updated_date',
            'deleted_date', 'active', 'member_count'
        ]

    def get_avatar(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return None
    
    def get_cover(self, obj):
        if obj.cover:
            return obj.cover.url
        return None

    def get_member_count(self, obj):
        return obj.followers.count()

class SimpleGroupSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    class Meta:
        model = UGroup
        fields = ['id', 'group_name', 'avatar']


    def get_avatar(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return None