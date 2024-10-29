from django.urls import path, include


auth = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]


urlpatterns = [
    path('v1/', include(auth)),
]
