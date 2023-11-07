import django.conf
import django.contrib.messages
import django.core.mail
import django.shortcuts

import feedback.forms as fb_forms
import feedback.models as fb_models


def feedback(request):
    template = "feedback/feedback.html"

    feedback_extra_form = fb_forms.FeedbackExtraForm(request.POST or None)
    feedback_form = fb_forms.FeedbackForm(request.POST or None)
    feedback_files_form = fb_forms.FeedbackFilesForm(
        request.POST or None,
        request.FILES or None,
    )

    if request.method == "POST":
        if feedback_form.is_valid() and feedback_extra_form.is_valid():
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

    context = {
        "feedback_form": feedback_form,
        "feedback_extra_form": feedback_extra_form,
        "feedback_files_form": feedback_files_form,
    }
    return django.shortcuts.render(request, template, context)


__all__ = []
