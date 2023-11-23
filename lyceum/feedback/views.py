import django.conf
import django.contrib.messages
import django.core.mail
import django.shortcuts
import django.views.generic

import feedback.forms as fb_forms
import feedback.models as fb_models


class FeedbackView(django.views.generic.TemplateView):
    template_name = "feedback/feedback.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if (
            "feedback_form" not in context
            and "feedback_extra_form" not in context
            and "feedback_files_form" not in context
        ):
            feedback_extra_form = fb_forms.FeedbackExtraForm(
                self.request.POST or None,
            )
            feedback_form = fb_forms.FeedbackForm(self.request.POST or None)
            feedback_files_form = fb_forms.FeedbackFilesForm(
                self.request.POST or None,
                self.request.FILES or None,
            )
            return context | {
                "feedback_form": feedback_form,
                "feedback_extra_form": feedback_extra_form,
                "feedback_files_form": feedback_files_form,
            }
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        feedback_form = context["feedback_form"]
        feedback_extra_form = context["feedback_extra_form"]
        feedback_files_form = context["feedback_files_form"]
        if (
            feedback_form.is_valid()
            and feedback_extra_form.is_valid()
            and feedback_files_form.is_valid()
        ):
            mail = feedback_extra_form.cleaned_data.get("mail")
            text = feedback_form.cleaned_data.get("text")

            django.core.mail.send_mail(
                "Обращение",
                text,
                django.conf.settings.MAIL,
                [
                    mail,
                ],
                fail_silently=False,
            )

            feedback_extra_form.save()
            fb = feedback_form.save(commit=False)
            fb.extra = feedback_extra_form.instance
            fb.save()

            files = request.FILES.getlist("file")

            for file in files:
                feedback_files_model = fb_models.FeedbackFiles(
                    file=file,
                    feedback=feedback_form.instance,
                )
                feedback_files_model.save()

            django.contrib.messages.success(request, "Обращение отправлено!")
            return django.shortcuts.redirect("feedback:feedback")
        return django.shortcuts.render(request, self.template_name, context)


__all__ = []
