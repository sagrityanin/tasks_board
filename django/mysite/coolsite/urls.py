from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from coolsite import settings

from tasks.views import pageNotFound
from tasks.views import view_handler403

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls'))
]
if settings.DEBUG:
    import debug_toolbar
    print("ddt added to url")
    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
print(urlpatterns)
handler404 = pageNotFound
handler403 = view_handler403
