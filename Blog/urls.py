from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from blogger.viewsets import TagViewSet, CategoryViewSet, ArticleViewSet
from operation.viewsets import UserFavViewSet, UserFocusViewSet, UserLeavingMessageViewSet, UserCommentViewSet
from users.viewsets import UserRegisterViewSet

router = DefaultRouter()
router.register(prefix="register", viewset=UserRegisterViewSet, base_name="register")
router.register(prefix="tag", viewset=TagViewSet, base_name="tag")
router.register(prefix="category", viewset=CategoryViewSet, base_name="category")
router.register(prefix="article", viewset=ArticleViewSet, base_name="article")
router.register(prefix="userfav", viewset=UserFavViewSet, base_name="userfav")
router.register(prefix="userfocus", viewset=UserFocusViewSet, base_name="userfocus")
router.register(prefix="userleamsg", viewset=UserLeavingMessageViewSet, base_name="userleamsg")
router.register(prefix="usercomment", viewset=UserCommentViewSet, base_name="usercomment")

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^docs/', include_docs_urls(title='博客系统')),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # 登录
    url(r'^login/', obtain_jwt_token),
]
