from django.contrib import admin
from .models import Team, Member
from .forms import CustomTeamCreationForm, CustomTeamChangeForm


@admin.register(Member)
class ProfileMember(admin.ModelAdmin):
    list_display = ('team', 'user', 'join_date')
    fieldsets = (
        (None, {'fields': ('team', 'user', 'join_date')}),
    )
    readonly_fields=('join_date',)
class MemberInline(admin.StackedInline):
    model=Member
    can_delete=False
    verbose_name_plural='Members'

class CustomTeam(admin.ModelAdmin):
    add_form = CustomTeamCreationForm
    form = CustomTeamChangeForm
    model=Team
    inlines =(MemberInline,)
    list_display = ('name', 'active','created')
    fieldsets = (
        (None, {'fields': ('image', 'name', 'created_by', 'created', 'modified_by', 'modified', 'active')}),
    )
    readonly_fields=('created_by', 'created', 'modified_by', 'modified', )

# Register your models here.
admin.site.register(Team, CustomTeam)
# admin.site.register(Member)
