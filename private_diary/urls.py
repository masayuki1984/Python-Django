from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.urls import path, include
from . import settings_common, settings_dev

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('diary.urls')),
    path('accounts/', include('allauth.urls')),
]

# 開発サーバーでメディアを配信できるようにする設定
urlpatterns += static(settings_common.MEDIA_URL, document_root=settings_dev.MEDIA_ROOT)