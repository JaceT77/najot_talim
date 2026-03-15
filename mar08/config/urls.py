from django.urls import include, path
from django.http import JsonResponse


def root_view(request):
    return JsonResponse({"message": "Hello to you."})


urlpatterns = [
    path("", root_view, name="root"),
    path("api/", include("catalog.urls")),
]
