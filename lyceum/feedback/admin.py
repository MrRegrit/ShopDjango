import django.contrib.admin

import feedback.models as fb_models


@django.contrib.admin.register(fb_models.Feedback)
class FeedbackAdmin(django.contrib.admin.ModelAdmin):
    readonly_fields = (
        fb_models.Feedback.mail.field.name,
        fb_models.Feedback.text.field.name,
        fb_models.Feedback.created_on.field.name,
        fb_models.Feedback.name.field.name,
    )

    def save_model(self, request, obj, form, change):
        if change and form.cleaned_data.get("status") != form.initial.get(
            "status",
        ):
            fb_models.StatusLog.objects.create(
                user=request.user,
                from_status=form.initial.get("status"),
                to_status=form.cleaned_data.get("status"),
            )
        super().save_model(request, obj, form, change)


@django.contrib.admin.register(fb_models.StatusLog)
class StatusLogAdmin(django.contrib.admin.ModelAdmin):
    readonly_fields = (
        fb_models.StatusLog.user.field.name,
        fb_models.StatusLog.timestamp.field.name,
        fb_models.StatusLog.from_status.field.name,
        fb_models.StatusLog.to_status.field.name,
    )

    def has_add_permission(self, request, obj=None):
        return False


__all__ = []
