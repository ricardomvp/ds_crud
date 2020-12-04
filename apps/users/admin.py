from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, Profile
from apps.teams.admin import MemberInline

@admin.register(Profile)
class ProfileProfile(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user', 'is_user', 'is_admin')}),
    )

class ProfileInlineProfile(admin.StackedInline):
    model=Profile
    inlines = (MemberInline,)
    can_delete=False
    verbose_name_plural='Teammates'

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    inlines =(
              ProfileInlineProfile,
              # MemberInline,
              )
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
# admin.site.register(Profile)
