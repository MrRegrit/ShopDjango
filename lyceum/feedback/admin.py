import django.contrib.admin

import feedback.models as fb_models


class InlineFiles(django.contrib.admin.TabularInline):
    model = fb_models.FeedbackFiles
    readonly_fields = (fb_models.FeedbackFiles.file.field.name,)
    can_delete = False


@django.contrib.admin.register(fb_models.Feedback)
class FeedbackAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        fb_models.Feedback.__str__,
        fb_models.Feedback.created_on.field.name,
        fb_models.Feedback.extra.field.name,
    )

    readonly_fields = (
        fb_models.Feedback.text.field.name,
        fb_models.Feedback.created_on.field.name,
        fb_models.Feedback.extra.field.name,
    )
    inlines = [
        InlineFiles,
    ]

    def save_model(self, request, obj, form, change):
        if change and form.cleaned_data.get("status") != form.initial.get(
            "status",
        ):
            fb_models.StatusLog.objects.create(
                user=request.user,
                from_status=form.initial.get("status"),
                to=form.cleaned_data.get("status"),
            )
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request, obj=None):
        return False


@django.contrib.admin.register(fb_models.StatusLog)
class StatusLogAdmin(django.contrib.admin.ModelAdmin):
    readonly_fields = (
        fb_models.StatusLog.user.field.name,
        fb_models.StatusLog.timestamp.field.name,
        fb_models.StatusLog.from_status.field.name,
        fb_models.StatusLog.to.field.name,
    )

    def has_add_permission(self, request, obj=None):
        return False


@django.contrib.admin.register(fb_models.FeedbackExtra)
class FeedbackExtraAdmin(django.contrib.admin.ModelAdmin):
    readonly_fields = (
        fb_models.FeedbackExtra.mail.field.name,
        fb_models.FeedbackExtra.name.field.name,
    )

    def get_model_perms(self, request):
        return {}

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


__all__ = []
