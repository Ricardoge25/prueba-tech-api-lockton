
from django.contrib.auth import authenticate, get_user_model
from django.db import transaction

from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Menu
from .permissions import IsStaffUser
from .serializers import (
  AssignMenuSerializer,
  MenuSerializer,
  UserReadSerializer,
  UserSerializer,
)

User = get_user_model()


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
  # El inicio de sesión es público: el token se obtiene después
  # de validar las credenciales, no antes.
  identifier = str(request.data.get("identifier", "")).strip()
  password = request.data.get("password", "")

  if not identifier or not password:
    return Response(
      {"detail": "Debes indicar usuario y contraseña."},
      status=status.HTTP_400_BAD_REQUEST,
    )

  username = identifier

  # Permitimos iniciar sesión con el nombre de usuario o el correo.
  if "@" in identifier:
    matching_user = User.objects.filter(
      email__iexact=identifier
    ).first()

    if matching_user:
      username = matching_user.get_username()

  user = authenticate(
    request,
    username=username,
    password=password,
  )

  if user is None or not user.is_active:
    return Response(
      {"detail": "Credenciales inválidas."},
      status=status.HTTP_401_UNAUTHORIZED,
    )

  token, _ = Token.objects.get_or_create(user=user)

  # El usuario solo recibe los menús que tiene asignados y que siguen activos.
  menus = Menu.objects.filter(is_active=True)

  if not user.is_staff:
    menus = menus.filter(users=user)

  return Response({
    "token": token.key,
    "user": UserReadSerializer(user).data,
    "menus": MenuSerializer(menus, many=True).data,
  })


class UserViewSet(viewsets.ModelViewSet):
  # La administración de cuentas está reservada a usuarios con is_staff=True.
  queryset = User.objects.all().order_by("username")
  permission_classes = [IsAuthenticated, IsStaffUser]
  http_method_names = ["get", "post", "head", "options"]

  def get_serializer_class(self):
    if self.action == "create":
      return UserSerializer

    return UserReadSerializer

  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    return Response(
      UserReadSerializer(user).data,
      status=status.HTTP_201_CREATED,
    )


class MenuViewSet(viewsets.ModelViewSet):
  queryset = Menu.objects.all()
  serializer_class = MenuSerializer
  permission_classes = [IsAuthenticated]
  http_method_names = ["get", "post", "head", "options"]

  def get_queryset(self):
    if getattr(self, "swagger_fake_view", False):
      return Menu.objects.none()

    queryset = Menu.objects.filter(is_active=True)

    if not self.request.user.is_authenticated:
      return Menu.objects.none()

    if self.request.user.is_staff:
      return queryset

    return queryset.filter(users=self.request.user)

  def get_permissions(self):
    if self.action == "create":
      return [
        IsAuthenticated(),
        IsStaffUser(),
      ]

    return [
      permission()
      for permission in self.permission_classes
    ]


@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated, IsStaffUser])
def user_menus_view(request, pk):
  try:
    target_user = User.objects.get(pk=pk)
  except User.DoesNotExist:
    return Response(
      {"detail": "Usuario no encontrado."},
      status=status.HTTP_404_NOT_FOUND,
    )

  if request.method == "GET":
    menus = target_user.menus.filter(is_active=True)
    return Response(MenuSerializer(menus, many=True).data)

  serializer = AssignMenuSerializer(data=request.data)
  serializer.is_valid(raise_exception=True)
  menu_ids = serializer.validated_data["menu_ids"]

  with transaction.atomic():
    target_user.menus.set(
      Menu.objects.filter(
        id__in=menu_ids,
        is_active=True,
      )
    )

  assigned_menus = target_user.menus.filter(is_active=True)

  return Response({
    "detail": "Asignaciones actualizadas correctamente.",
    "user_id": target_user.id,
    "menus": MenuSerializer(assigned_menus, many=True).data,
  })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def menu_access_check(request, pk):
  try:
    menu = Menu.objects.get(pk=pk, is_active=True)
  except Menu.DoesNotExist:
    return Response(
      {"detail": "Menú no encontrado."},
      status=status.HTTP_404_NOT_FOUND,
    )

  if (
    not request.user.is_staff
    and not menu.users.filter(pk=request.user.pk).exists()
  ):
    return Response(
      {"detail": "No tienes autorización para acceder a este recurso."},
      status=status.HTTP_403_FORBIDDEN,
    )

  return Response({
    "detail": "Acceso autorizado.",
    "menu": MenuSerializer(menu).data,
  })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_view(request):
  # El token identifica al usuario; no confiamos en un ID enviado
  # desde el frontend para determinar qué información devolver.
  if request.user.is_staff:
    menus = Menu.objects.filter(is_active=True)
  else:
    menus = Menu.objects.filter(
      is_active=True,
      users=request.user,
    )

  return Response({
    "user": UserReadSerializer(request.user).data,
    "menus": MenuSerializer(menus, many=True).data,
  })
