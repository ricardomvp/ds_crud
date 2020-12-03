from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, TeamMate

@admin.register(TeamMate)
class ProfileTeamMate(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user', 'is_user', 'is_admin')}),
    )
    readonly_fields=('is_owner',)

class ProfileInlineTeamMate(admin.StackedInline):
    model=TeamMate
    can_delete=False
    verbose_name_plural='Teammates'

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    inlines =(ProfileInlineTeamMate,)
    list_display = ('pk', 'name', 'email', 'is_active', 'created')
    list_filter = ('name', 'email', 'is_active',)
    fieldsets = (
        ('Profile', {'fields': ('name', 'email', 'password', 'created')}),
        ('Permissions', {'fields': ('is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'password1', 'password2', 'is_active')}
        ),
    )
    search_fields = ('name', )
    ordering = ('name', )
    readonly_fields=('created', )

admin.site.register(User, CustomUserAdmin)
# admin.site.register(TeamMate)
