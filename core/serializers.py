from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Menu

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(
    write_only=True,
    min_length=8
  )

  class Meta:
    model = User
    fields = [
      "id",
      "username",
      "email",
      "first_name",
      "last_name",
      "password",
      "is_active",
    ]
    read_only_fields = ["id", "is_active"]

  def create(self, validated_data):
    # create_user aplica el hash de contraseña 
    # no guarda la contraseña en texto plano.
    password = validated_data.pop("password")

    user = User(**validated_data)
    user.set_password(password)
    user.save()

    return user

class UserReadSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = [
      "id",
      "username",
      "email",
      "first_name",    
      "last_name",
      "is_active"
    ]

class MenuSerializer(serializers.ModelSerializer):
  class Meta:
    model = Menu
    fields = [
      "id",
      "name",
      "description",
      "route",
      "is_active",
      "created_at",
    ]
    read_only_fields = ["id", "created_at"]

class AssignMenuSerializer(serializers.Serializer):
  menu_ids = serializers.ListField(
    child=serializers.IntegerField(min_value=1),
    allow_empty=True,
  )

  def validate_menu_ids(self, value):
    # Evitamos recibir el mismo menú varias veces en una asignación.
    if len(value) != len(set(value)):
      raise serializers.ValidationError(
        "No se permiten identificadores duplicados."
      )

    # Solo se pueden asignar menús que existan y estén activos.
    existing_ids = set(
      Menu.objects.filter(
        id__in=value,
        is_active=True,
      ).values_list("id", flat=True)
    )

    missing_ids = set(value) - existing_ids

    if missing_ids:
      raise serializers.ValidationError(
        f"Menús inexistentes o inactivos: {sorted(missing_ids)}"
      )

    return value