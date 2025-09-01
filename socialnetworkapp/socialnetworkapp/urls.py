from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
import debug_toolbar


schema_view = get_schema_view(
    openapi.Info(
        title="Psychological API",
        default_version='v2.9',
        description="APIs for PsychologicalApp",
        contact=openapi.Contact(email="trinhquocdat041004@gmail.com"),
        license=openapi.License(name="Trinh Quoc Dat"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('oauth/', include('social_django.urls', namespace='social')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('__debug__/', include(debug_toolbar.urls)),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
    re_path(r'^redoc/$',
            schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'),
    path('', include('esocialnetworkapi.urls')),
]
