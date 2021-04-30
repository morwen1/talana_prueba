from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls import include, path

from talana_prueba.users.api.views import UserViewSet
from talana_prueba.competition.views import CompetitionViewset

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("competition" , CompetitionViewset , basename="competition")


app_name = "api"
urlpatterns = router.urls




jwt = {
    path("auth-token" , TokenObtainPairView.as_view() , name="auth"), 
    path("refresh-token" ,TokenRefreshView.as_view() , name ="refresh_token" ),

}

urlpatterns += jwt