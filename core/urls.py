from django.urls import path, include

from . import views
# from surveys import urls

urlpatterns = [
    path('', views.homepage, name="homepage"),
    # path("questionari", include('surveys.urls')),
]
