from rest_framework.decorators import action
from rest_framework.response import Response
from esocialnetworkapi.models import User, Comment, UGroup, Contact, ThreadRoom, ThreadRoomParticipant, Post, GroupPost, PostImage, Reaction, SurveyPost, UserSurveyOption, SurveyQuestion,SurveyOption,SurveyDraft,SurveyDraftAnswer
from esocialnetworkapi import serializers, perms, paginators
from rest_framework import viewsets, generics, parsers, permissions, status
from django.db.models import Count, Q
from django.utils import timezone
from django.db.models import Exists, OuterRef
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from esocialnetworkapi.qchatbot_openai import load_llm, create_qa_chain, read_vectors_db, create_prompt, find_faq_answer, answer_query, is_psychology_post

# load sẵn khi khởi động server để tránh load lại mỗi request
llm = load_llm()
TEMPLATE = """
    Bạn là một chuyên gia tâm lý. Hãy dựa vào context để trả lời ngắn gọn, rõ ràng (tối đa 3-5 câu), phù hợp với câu hỏi người dùng.  
    Yêu cầu:
    1. Đồng cảm với cảm xúc của người dùng, giọng văn nhẹ nhàng, không phán xét. 
    2. Nếu không có đủ thông tin, hãy thừa nhận và đưa ra lời khuyên tổng quát.
    3. Nếu phát hiện người dùng người dùng bị stress, căng thẳng, buồn chán,... hãy đưa ra gợi ý thực tế, tích cực và an toàn.
    4. Nếu phát hiện người dùng có ý nghĩ tự làm hại bản thân (người dùng nói về tự tử, tự làm hại bản thân, hoặc nguy hiểm tới tính mạng), 
            KHÔNG đưa ra cách tự xử lý mà hãy khuyến khích họ tìm sự giúp đỡ từ chuyên gia tâm lý, 
            gọi ngay số điện thoại hỗ trợ khẩn cấp tại địa phương, hoặc liên hệ với bạn bè/người thân đáng tin cậy.
    5. Nếu là câu hỏi về lý thuyết chỉ cần trả lời câu hỏi, không đưa ra lời khuyên.
    6. Không bao giờ thay thế cho bác sĩ hoặc nhà trị liệu chuyên nghiệp.  

    Thông tin (context):  {context}

    Câu hỏi: {question}

    Trả lời:
    """


prompt = create_prompt(TEMPLATE)
db = read_vectors_db()
qa_chain = create_qa_chain(prompt, llm, db)

class UserViewSet(viewsets.ViewSet, generics.UpdateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser, parsers.JSONParser, parsers.FormParser]

    @action(methods=['get'], url_path='current-user', detail=False, permission_classes=[permissions.IsAuthenticated])
    def get_current_user(self, request):
        return Response(serializers.UserSerializer(request.user).data)
    
    @action(methods=['post'], detail=False, url_path="register", permission_classes=[permissions.AllowAny])
    def register(self, request):
        ser = serializers.RegisterSerializer(data=request.data)
        if ser.is_valid():
            user = ser.save()
            return Response(serializers.UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['PATCH'], detail=False, url_path="change-password", permission_classes=[perms.OwnerPerms])
    def change_password(self, request):
        ser = serializers.ChangePasswordSerializer(data=request.data)
        if ser.is_valid():
            user = request.user
            old_password = ser.validated_data["old_password"]

            if not user.check_password(old_password):
                return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

            user.password = make_password(ser.validated_data["new_password"])
            user.save()
            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)

        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['get'], detail=False, url_path='search')
    def search(self, request):
        query = request.GET.get("q", "").strip()
        if not query:
            return Response({"error": "Vui lòng nhập từ khóa"}, status=400)

        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
        # Phân trang
        paginator = PageNumberPagination()
        paginator.page_size = 5  # số bản ghi trên 1 trang, có thể chỉnh
        result_page = paginator.paginate_queryset(users, request)

        data = serializers.UserSearchSerializer(result_page, many=True).data
        return paginator.get_paginated_response(data)
    

# Tạo group
class GroupCreateView(generics.CreateAPIView):
    queryset = UGroup.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

# Cập nhật tên group – chỉ người tạo được sửa
class GroupUpdateView(generics.RetrieveUpdateAPIView):
    queryset = UGroup.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = [permissions.IsAuthenticated,  perms.IsCreatorOrReadOnly]


class UserPostListView(generics.ListAPIView):
    serializer_class = serializers.PostSerializer
    pagination_class = paginators.PostPaginator
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Post.objects.filter(user__id=user_id, active=True).order_by('-created_date')
    

class UserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserProfileSerializer
    permission_classes = [permissions.AllowAny] 
    lookup_field = 'id'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request 
        return context


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(active=True)
    serializer_class = serializers.PostSerializer
    parser_classes = [parsers.MultiPartParser]
    pagination_class = paginators.PostPaginator

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'delete', 'restore', 'force']:
            return [permissions.IsAuthenticated(), perms.IsOwnerOrReadOnly()]
        return [permissions.IsAuthenticatedOrReadOnly()]

    def perform_destroy(self, instance):
        # Xóa mềm mặc định
        instance.active = False
        instance.deleted_date = timezone.now()
        instance.save()

    def perform_create(self, serializer):
        content = self.request.data.get("content")
        # AI kiểm tra nội dung
        if not is_psychology_post(llm, content):
            raise ValidationError("Bài viết không thuộc lĩnh vực tâm lý học, không thể chia sẻ.")

        post = serializer.save(user=self.request.user)
        # Lấy groupId từ URL
        group_id = self.request.data.get("group_id")
        if group_id:
            group = get_object_or_404(UGroup, pk=group_id)
            GroupPost.objects.create(post=post, group=group)
        # Lưu ảnh
        images = self.request.FILES.getlist('images[]')
        for img in images:
            PostImage.objects.create(post=post, image=img)


    def perform_update(self, serializer):
        post = serializer.save()

        # Lấy danh sách ID ảnh cũ cần giữ lại
        keep_image_ids = self.request.data.getlist("existingImages[]")

        # XÓA MỀM các ảnh không nằm trong danh sách giữ lại
        PostImage.objects.filter(post=post, active=True).exclude(id__in=keep_image_ids).update(
            active=False,
            deleted_date=timezone.now()
        )

        # Lưu các ảnh mới
        new_images = self.request.FILES.getlist("images[]")
        for img in new_images:
            PostImage.objects.create(post=post, image=img)

    def get_queryset(self):
        queryset = Post.objects.filter(active=True)
        has_survey = self.request.query_params.get('hasSurvey')
        if has_survey == 'true':
            queryset = queryset.annotate(
                is_survey=Exists(SurveyPost.objects.filter(post=OuterRef('pk')))
            ).filter(is_survey=True)

        if self.action in ['force', 'restore']:
            return Post.objects.all()
        return queryset


    @action(methods=['post'], detail=True, url_path='react')
    def react(self, request, pk):
        post = self.get_object()
        reaction_type = request.data.get("reaction", "LIKE")
        obj, created = Reaction.objects.update_or_create(
            user=request.user, post=post,
            defaults={'reaction': reaction_type}
        )
        return Response({"status": "reacted", "type": obj.reaction})
    

    @action(detail=False, methods=['get'], url_path='group/(?P<group_id>[^/.]+)')
    def get_posts_by_group(self, request, group_id=None):
        posts = Post.objects.filter(
            active=True,
            grouppost__group__id=group_id
        ).order_by('-created_date')

        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, url_path='comment-count')
    def comment_count(self, request, pk):
        post = self.get_object()
        count = post.comment_set.filter(active=True).count()
        return Response({'post_id': pk, 'comment_count': count}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='deleted')
    def get_deleted_posts(self, request):
        posts = Post.objects.filter(active=False)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(methods=['put'], detail=True, url_path='delete')
    def soft_delete(self, request, pk):
        post = self.get_object()
        post.active = False
        post.deleted_date = timezone.now()
        post.save()
        return Response({'status': 'soft-deleted'}, status=status.HTTP_200_OK)

    @action(methods=['put'], detail=True, url_path='restore')
    def restore(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        post.active = True
        post.deleted_date = None
        post.save()
        return Response({'status': 'restored'}, status=status.HTTP_200_OK)

    @action(methods=['delete'], detail=True, url_path='force')
    def force_delete(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        post.delete()
        return Response({'status': 'force-deleted'}, status=status.HTTP_204_NO_CONTENT)
    
    
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(active=True)
    serializer_class = serializers.CommentSerializer
    pagination_class = paginators.CommentPaginator

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), perms.IsOwnerOrPostOwner()]
        elif self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        def soft_delete(comment):
            comment.active = False
            comment.deleted_date = timezone.now()
            comment.save()

            # Lấy tất cả các bình luận con
            children = Comment.objects.filter(parent=comment, active=True)
            for child in children:
                soft_delete(child)

        soft_delete(instance)

    def get_queryset(self):
        post_id = self.request.query_params.get('post_id')
        qs = self.queryset.select_related('user')
        if post_id:
            qs = qs.filter(post_id=post_id)
        return qs
    
    @action(methods=['get'], detail=False, url_path='count')
    def count_comments(self, request):
        post_id = request.query_params.get('post')
        if not post_id:
            return Response({"detail": "post is required"}, status=400)
        
        count = self.queryset.filter(post_id=post_id).count()
        return Response({"post_id": post_id, "comment_count": count})

    @action(methods=['get'], url_path='parents', detail=False)
    def parent_comments(self, request):
        post_id = request.query_params.get('post')
        if not post_id:
            return Response({'detail': 'post is required'}, status=status.HTTP_400_BAD_REQUEST)

        qs = self.queryset.filter(post_id=post_id, parent__isnull=True)
        print(qs)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(methods=['get'], url_path='children', detail=False)
    def child_comments(self, request):
        parent_id = request.query_params.get('parent_id')
        if not parent_id:
            return Response({'detail': 'parent_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        qs = self.queryset.filter(parent_id=parent_id)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.select_related('user', 'post')
    serializer_class = serializers.ReactionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(methods=['get'], detail=False, url_path='post-reactions')
    def post_reactions(self, request):
        post_id = request.query_params.get('post_id')
        if not post_id:
            return Response({"detail": "post_id is required"}, status=400)

        reactions = self.queryset.filter(post_id=post_id)
        total_counts = reactions.values('reaction').annotate(count=Count('id'))

        data = {
            "counts": {r['reaction']: r['count'] for r in total_counts},
            "user_reacted": False,
            "user_reaction": None
        }

        if request.user.is_authenticated:
            user_reaction = reactions.filter(user=request.user).first()
            if user_reaction:
                data["user_reacted"] = True
                data["user_reaction"] = user_reaction.reaction

        return Response(data)

    def perform_create(self, serializer):
        user = self.request.user
        post = serializer.validated_data.get("post")
        new_reaction = serializer.validated_data.get("reaction")

        existing = Reaction.objects.filter(user=user, post=post).first()
        if existing:
            if existing.reaction == new_reaction:
                # Nếu reaction trùng → xóa
                existing.delete()
            else:
                # Nếu khác → cập nhật
                existing.reaction = new_reaction
                existing.save()
        else:
            serializer.save(user=user)


class SurveyPostViewSet(viewsets.ModelViewSet):
    queryset = SurveyPost.objects.all()
    serializer_class = serializers.SurveyPostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = paginators.SurveyPostPaginator
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    @action(detail=True, methods=['get'], url_path='answered', permission_classes=[permissions.IsAuthenticated])
    def has_answered(self, request, pk=None):
        user = request.user
        try:
            survey_post = self.get_object()
            has_answered = UserSurveyOption.objects.filter(
                user=user,
                survey_option__survey_question__survey_post=survey_post
            ).exists()

            return Response(has_answered)
        except SurveyPost.DoesNotExist:
            return Response(False)
        
        
    @action(detail=True, methods=['post'], url_path='submit', permission_classes=[permissions.IsAuthenticated])
    @transaction.atomic
    def submit(self, request, pk=None):
        user = request.user
        data = request.data  # list of {"questionId": x, "optionIds": [...]}

        # VD data = [{"questionId": 1,"optionIds": [4, 5]},{"questionId": 2, "optionIds": [7]}]

        try:
            survey_post = self.get_object()

            if survey_post.status == "EXPIRED":
                return Response(
                    {"message": "Khảo sát đã hết hạn"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Kiểm tra đã gửi chưa
            has_answered = UserSurveyOption.objects.filter(
                user=user,
                survey_option__survey_question__survey_post=survey_post
            ).exists()
            if has_answered:
                return Response(
                    {"message": "Bạn đã gửi khảo sát này rồi"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            for answer in data:
                question_id = answer.get("questionId")
                option_ids = answer.get("optionIds", [])

                if not question_id or not option_ids:
                    continue  # bỏ qua câu không hợp lệ

                question = SurveyQuestion.objects.get(id=question_id, survey_post=survey_post)

                for opt_id in option_ids:
                    option = SurveyOption.objects.get(id=opt_id, survey_question=question)
                    UserSurveyOption.objects.create(
                        user=user,
                        survey_option=option
                    )

            return Response({"message": "Gửi khảo sát thành công"}, status=status.HTTP_200_OK)

        except SurveyPost.DoesNotExist:
            return Response({"message": "Không tìm thấy khảo sát"}, status=status.HTTP_404_NOT_FOUND)
        except SurveyQuestion.DoesNotExist:
            return Response({"message": "Câu hỏi không hợp lệ"}, status=status.HTTP_400_BAD_REQUEST)
        except SurveyOption.DoesNotExist:
            return Response({"message": "Lựa chọn không hợp lệ"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    @action(detail=True, methods=['get'], url_path='statistics', permission_classes=[permissions.IsAuthenticated])
    def get_survey_statistics(self, request, pk=None):
        try:
            survey_post = SurveyPost.objects.get(pk=pk)
        except SurveyPost.DoesNotExist:
            return Response({"message": "Khảo sát không tồn tại."}, status=status.HTTP_404_NOT_FOUND)

        # Số người tham gia khảo sát (dựa vào bảng trung gian UserSurveyOption)
        participant_ids = UserSurveyOption.objects.filter(
            survey_option__survey_question__survey_post=survey_post
        ).values('user').distinct()
        participant_count = participant_ids.count()

        # Lấy tất cả các câu hỏi và options liên quan
        questions = SurveyQuestion.objects.filter(survey_post=survey_post).prefetch_related('surveyoption_set')

        statistics = []

        for question in questions:
            for option in question.surveyoption_set.all():
                total_selected = UserSurveyOption.objects.filter(survey_option=option).count()

                statistics.append({
                    "questionId": question.id,
                    "question": question.question,
                    "optionId": option.id,
                    "optionText": option.option_text,
                    "totalSelected": total_selected
                })

        return Response({
            "participantCount": participant_count,
            "statistics": statistics
        })
    
    @action(methods=['get'], detail=False, url_path='expired')
    def get_expired_surveys(self, request):
        now = timezone.now()
        expired_surveys = SurveyPost.objects.filter(end_time__lt=now, status='EXPIRED')
        paginator = PageNumberPagination()
        paginator.page_size = 5
        result_page = paginator.paginate_queryset(expired_surveys, request)

        serializer = serializers.SurveyPostExpiredSerializer(result_page, many=True, context={'request': request} )
        return paginator.get_paginated_response(serializer.data)
    

class GroupViewSet(viewsets.ViewSet, generics.RetrieveAPIView, generics.CreateAPIView, generics.DestroyAPIView  ):
    queryset = UGroup.objects.filter(active=True)
    serializer_class = serializers.GroupDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='follow')
    def follow(self, request, pk=None):
        try:
            group = self.get_object()
            user = request.user
            group.followers.add(user)
            return Response({'message': 'Đã theo dõi nhóm'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='unfollow')
    def unfollow(self, request, pk=None):
        try:
            group = self.get_object()
            user = request.user
            group.followers.remove(user)
            return Response({'message': 'Đã hủy theo dõi nhóm'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

    @action(detail=True, methods=['get'], url_path='is-following')
    def is_following(self, request, pk=None):
        group = self.get_object()
        user = request.user
        is_following = group.followers.filter(id=user.id).exists()
        return Response({'is_following': is_following}, status=status.HTTP_200_OK)
    
    
    @action(detail=True, methods=['get'], url_path='followers-count')
    def followers_count(self, request, pk=None):
        group = self.get_object()
        count = group.followers.count()
        return Response({'followers_count': count}, status=status.HTTP_200_OK)
    

    @action(detail=True, methods=['patch'], url_path='update-media')
    def update_media(self, request, pk=None):
        group = self.get_object()
        user = request.user

        if group.creator != user:
            return Response({'error': 'Bạn không có quyền chỉnh sửa nhóm này.'}, status=status.HTTP_403_FORBIDDEN)

        avatar = request.FILES.get('avatar')
        cover = request.FILES.get('cover')

        if avatar:
            group.avatar = avatar
        if cover:
            group.cover = cover

        group.save()
        return Response({'message': 'Cập nhật ảnh thành công.'}, status=status.HTTP_200_OK)
    

    @action(detail=False, methods=['get'], url_path='followed')
    def followed_groups(self, request):
        user = request.user
        groups = user.followed_groups.filter(active=True)

        page = self.paginate_queryset(groups)
        if page is not None:
            serializer = serializers.SimpleGroupSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.SimpleGroupSerializer(groups, many=True)
        return Response(serializer.data)


class ContactViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = paginators.ContactPaginator
    

    # Gửi lời mời kết bạn
    @action(methods=["post"], detail=False, url_path='user')
    def send_request(self, request):
        to_user_id = request.data.get("to_user")
        if not to_user_id:
            return Response({"error": "Thiếu user nhận lời mời"}, status=400)

        to_user = get_object_or_404(User, id=to_user_id)

        contact, created = Contact.objects.get_or_create(
            from_user=request.user, to_user=to_user, status="ACCEPTED"
        )

        if not created:
            return Response({"message": "Đã gửi lời mời hoặc đã có quan hệ"}, status=400)

        return Response({"message": "Đã gửi lời mời kết bạn"}, status=201)


    # Chấp nhận lời mời(đang phát triển)
    @action(methods=["post"], detail=True)
    def accept_request(self, request, pk=None):
        contact = get_object_or_404(Contact, id=pk, to_user=request.user)

        if contact.status != "PENDING":
            return Response({"error": "Lời mời này đã được xử lý"}, status=400)

        contact.status = "ACCEPTED"
        contact.save()

        return Response({"message": "Đã chấp nhận lời mời"})

    # Danh sách bạn bè
    @action(methods=["get"], detail=False)
    def friends(self, request):
        contacts = Contact.objects.filter(
            (Q(from_user=request.user) | Q(to_user=request.user)),
            status="ACCEPTED"
        ).order_by("-updated_date")

        # Lấy list user đã contact
        friends = []
        for c in contacts:
            if c.from_user == request.user:
                friends.append(c.to_user)
            else:
                friends.append(c.from_user)
        paginator = paginators.ContactPaginator()
        paginated_contacts = paginator.paginate_queryset(friends, request)
        serializer = serializers.UserSerializer(paginated_contacts, many=True)
        return paginator.get_paginated_response(serializer.data)

    # Lấy thông tin phòng chat
    @action(methods=["post"], detail=False, url_path="thread-room")
    def thread_room(self, request):
        thread_id = request.data.get("thread_id")

        try:
            thread = ThreadRoom.objects.get(id=thread_id, participants__user=request.user)
        except ThreadRoom.DoesNotExist:
            return Response({"error": "Not allowed"}, status=403)

        # Trả về firebase_room_id để client push message
        return Response({
            "firebase_room_id": thread.firebase_room_id,
            "user": request.user.username
        })

class ChatAPIView(APIView):
    def post(self, request):
        query = request.data.get("query", "")
        if not query:
            return Response({"error": "Thiếu query"}, status=status.HTTP_400_BAD_REQUEST)

        if "tự tử" in query or "muốn chết" in query:
            return Response({"result": "Tôi rất tiếc khi nghe điều này. Hãy tìm ngay sự giúp đỡ từ chuyên gia tâm lý hoặc gọi số khẩn cấp tại địa phương. Bạn không đơn độc."})
        # Tiền sử lý câu hỏi
        
        faq_answer = find_faq_answer(query)
        if faq_answer:
            return Response({"result": faq_answer})

        result = answer_query(query=query, llm=llm, template=TEMPLATE, qa_chain=qa_chain)
        response = {
            "result": result["result"],
        }

        return Response(response)

