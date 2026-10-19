from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
  MenuViewSet,
  UserViewSet,
  login_view,
  me_view,
  menu_access_check,
  user_menus_view,
)

router = DefaultRouter()

router.register("users", UserViewSet, basename="user")
router.register("menus", MenuViewSet, basename="menu")

urlpatterns = [
  # Autenticación y datos de la sesión actual.
  path("auth/login", login_view, name="api-login"),
  path("auth/me", me_view, name="api-me"),

  # Asignación de menús y comprobación de acceso.
  path("users/<int:pk>/menus", user_menus_view, name="user-menus"),
  path("users/<int:pk>/access", menu_access_check, name="menu-access-check"),

  # Rutas CRUD generadas por el router de DRF.
  path("", include(router.urls))
]
