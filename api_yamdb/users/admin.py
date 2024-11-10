from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import MyUser


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    """Настройка отображения и редактирования модели MyUser в админке."""

    list_display = ('username', 'email', 'role', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email')

    fieldsets = (
        ('Пользователь', {'fields': ('username',)}),
        ('Информация', {'fields': (
            'first_name',
            'last_name',
            'email',
            'bio'
        )}),
        ('Права', {'fields': ('role', 'is_superuser', 'is_staff')}),
        ('Дата добавления', {'fields': ('date_joined',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'is_staff', 'is_superuser')
        }),
    )
