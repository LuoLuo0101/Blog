from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from blogger.viewsets import TagViewSet, CategoryViewSet, ArticleViewSet
from operation.viewsets import UserFavViewSet, UserFocusViewSet, UserLeavingMessageViewSet, UserCommentViewSet
from users.viewsets import UserRegisterViewSet, UserViewSet
from django.views.static import serve  # 媒体文件
from Blog.settings import MEDIA_ROOT

router = DefaultRouter()
router.register(prefix="register", viewset=UserRegisterViewSet, base_name="register")
router.register(prefix="userdetail", viewset=UserViewSet, base_name="userdetail")
router.register(prefix="tag", viewset=TagViewSet, base_name="tag")
router.register(prefix="category", viewset=CategoryViewSet, base_name="category")
router.register(prefix="article", viewset=ArticleViewSet, base_name="article")
router.register(prefix="userfav", viewset=UserFavViewSet, base_name="userfav")
router.register(prefix="userfocus", viewset=UserFocusViewSet, base_name="userfocus")
router.register(prefix="userleamsg", viewset=UserLeavingMessageViewSet, base_name="userleamsg")
router.register(prefix="usercomment", viewset=UserCommentViewSet, base_name="usercomment")

urlpatterns = [
    # router 解释根路由
    url(r'^', include(router.urls)),

    # admin 后台
    url(r'^admin/', admin.site.urls),

    # docs 下的文档路由
    url(r'^docs/', include_docs_urls(title='博客系统')),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # 登录
    url(r'^login/', obtain_jwt_token),

    # 主页
    url(r"^index/$", TemplateView.as_view(template_name="index.html"), name="index"),

    # 上传的文件问题
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
]
