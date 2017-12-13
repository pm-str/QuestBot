from django.contrib import admin
from django.db import models

from ckeditor.widgets import CKEditorWidget

from apps.web.models import *


class StepInline(admin.TabularInline):
    model = Step


class PhotoSizeInline(admin.TabularInline):
    model = PhotoSize
    readonly_fields = ('url',)
    fields = ('url', 'height', 'width', 'file_size',)

    def url(self, obj):
        return obj.message.updates.first().bot.get_file(
            obj.file_id)['file_path']

    def has_add_permission(self, request):
        return False


class HandlerInline(admin.TabularInline):
    model = Handler
    exclude = ('allowed',)
    readonly_fields = ('id', )
    fields = ('id', 'ids_expression', 'title', 'slug',)
    fk_name = 'step'


class ConditionInline(admin.TabularInline):
    model = Condition
    readonly_fields = ('id',)
    fields = ('id', 'value', 'rule',)


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ('name', 'enabled', 'token',)
    list_filter = ('enabled', 'owner',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'from_user', 'date',)
    list_filter = ('from_user', 'chat',)
    inlines = (PhotoSizeInline, )

@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_filter = ('bot',)
    list_display = ('update_id', 'message', 'handler', 'response',)


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'title',)


@admin.register(CallbackQuery)
class CallbackQueryAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user', 'data',)


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
        ('Handler', {
            'fields': (
                'handler',
            )
        }),
    )


@admin.register(Handler)
class HandlerAdmin(admin.ModelAdmin):
    inlines = (ConditionInline,)

    list_display = ('title', 'slug', 'step',)

    list_filter = ('step',)

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'slug',
                'step',
                'ids_expression',
            )
        }),
        ('Permissions', {
            'fields': (
                'allowed',
            )
        }),
        ('Actions', {
            'fields': (
                'step_on_success',
                'step_on_error',
            )
        })
    )


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    pass


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    inlines = (HandlerInline,)
    list_display = ('title', 'number', 'is_initial', )
    list_filter = ('quest', )


@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    exclude = ('groups',)
    readonly_fields = ('password', 'last_login')
    list_display = ('username', 'email', 'device_uid', 'is_staff', 'step')
    list_filter = (
        'step__number',
        ('is_staff', admin.BooleanFieldListFilter),
    )

    fieldsets = (
        (None, {
            'fields': (
                'username',
                'first_name',
                'last_name',
                'step',
                'email',
                'device_uid',
            )
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('password', 'user_permissions', 'last_login'),
        }),
    )
