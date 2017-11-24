from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from apps.web.models import *


class StepInline(admin.TabularInline):
    model = Step


class RequestInline(admin.TabularInline):
    model = Request
    exclude = ('allowed',)
    readonly_fields = ('id', )
    fields = ('id', 'ids_expression', 'title', 'slug',)


class ConditionInline(admin.TabularInline):
    model = Condition
    readonly_fields = ('id', )
    fields = ('id', 'value', 'rule',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }

    inlines = (StepInline,)


@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified')
    fieldsets = (
        (None, {
            'fields': (
                'rule',
                'value',
                'created',
                'modified',
            ),
        }),
        ('Request', {
            'fields': (
                'request',
            )
        }),
    )


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    inlines = (ConditionInline,)


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    pass


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    inlines = (RequestInline,)


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
