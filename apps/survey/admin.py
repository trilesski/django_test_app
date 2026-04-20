from django.contrib import admin
import nested_admin

from .models import *


class AnswerInline(nested_admin.NestedTabularInline):
    model = AnswerOption
    extra = 1


class QuestionInline(nested_admin.NestedTabularInline):
    model = Question
    extra = 1
    inlines = [AnswerInline]


@admin.register(Survey)
class SurveyAdmin(nested_admin.NestedModelAdmin):
    fields = ('name', 'author', 'created_at', 'updated_at')
    list_display = ('name', 'author', 'created_at', 'updated_at')
    readonly_fields = ('name', 'author', 'created_at', 'updated_at')
    search_fields = ('name', 'author')
    search_help_text = 'Название опроса|Автор'
    inlines = (QuestionInline,)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = ('survey', 'number', 'text', 'created_at', 'updated_at')
    list_display = ('survey', 'number', 'created_at', 'updated_at')
    readonly_fields = ('survey', 'created_at', 'updated_at')
    search_fields = ('survey__id', )
    search_help_text = 'ID Опроса'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        pass


@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    fields = ('question', 'number', 'text', 'created_at', 'updated_at')
    list_display = ('question', 'number', 'created_at', 'updated_at')
    readonly_fields = ('question', 'created_at', 'updated_at')
    search_fields = ('question__id', )
    search_help_text = 'ID Вопроса'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        pass


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    fields = ('user', 'question', 'answer_option', 'user_option', 'created_at')
    list_display = ('user', 'question', 'created_at')
    readonly_fields = ('user', 'question', 'answer_option', 'user_option', 'created_at')
    search_fields = ('question__id', 'user__username')
    search_help_text = 'ID Вопроса|Имя пользователя'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        pass


@admin.register(PassSurvey)
class PassSurveyAdmin(admin.ModelAdmin):
    fields = ('user', 'survey', 'user_answer_ids', 'is_completed', 'started_at', 'finished_at')
    list_display = ('user', 'survey', 'is_completed', 'started_at', 'finished_at')
    readonly_fields = ('user', 'survey', 'user_answer_ids', 'is_completed', 'started_at', 'finished_at')
    search_fields = ('survey__name', 'user__username')
    search_help_text = 'Название опроса|Имя пользователя'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        pass