from django.conf import settings
from django.db import models

# Create your models here.
class Menu(models.Model):
  name = models.CharField(max_length=100, unique=True)
  description = models.TextField(blank=True)
  route = models.CharField(max_length=200, unique=True)
  is_active = models.BooleanField(default=True)

  # Un menú puede estar disponible para varios usuarios y un usuario
  # puede tener acceso a diferentes menús.
  users = models.ManyToManyField(
    settings.AUTH_USER_MODEL,
    related_name="menus",
    blank=True,
  )

  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ["name"]

  def __str__(self):
    return self.name

