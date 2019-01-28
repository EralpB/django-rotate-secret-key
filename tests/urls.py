from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import include, path
from django.contrib.auth import views as auth_views

from django.contrib import admin

urlpatterns = [
    path('', lambda request: HttpResponse("Hello World", content_type="text/plain")),
    path('login', auth_views.LoginView.as_view(template_name='admin/login.html')),
    path('admin/', admin.site.urls),

    path('profile', login_required(lambda request: HttpResponse(request.user.username, content_type="text/plain"))),
]