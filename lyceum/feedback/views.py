import django.conf
import django.contrib.messages
import django.core.mail
import django.shortcuts

import feedback.forms as fb_forms


def feedback(request):
    template = "feedback/feedback.html"

    form = fb_forms.FeedbackForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            mail = form.cleaned_data.get("mail")
            text = form.cleaned_data.get("text")

            django.core.mail.send_mail(
                "Обращение",
                text,
                django.conf.settings.MAIL,
                [
                    mail,
                ],
                fail_silently=False,
            )

            form.save()

            django.contrib.messages.success(request, "Обращение отправлено!")
            return django.shortcuts.redirect("feedback:feedback")
    context = {
        "form": form,
    }
    return django.shortcuts.render(request, template, context)


__all__ = []
