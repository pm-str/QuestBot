from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from apps.web.models import *


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


class StepInline(admin.TabularInline):
    model = Step


@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }

    inlines = [StepInline]


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    pass


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    pass


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    pass


@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    exclude = ('groups',)
    readonly_fields = ('password', 'last_login')
    list_display = ('username', 'email', 'device_uid', 'is_staff')
    list_filter = (
        'steps__number',
        ('is_staff', admin.BooleanFieldListFilter),
    )

    fieldsets = (
        (None, {
            'fields': (
                'username',
                'first_name',
                'last_name',
                'steps',
                'email',
                'device_uid',
            )
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('password', 'user_permissions', 'last_login'),
        }),
    )
