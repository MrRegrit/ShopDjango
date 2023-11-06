import django.test
import django.urls

import feedback.forms
import feedback.models


class FormTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = feedback.forms.FeedbackForm()

    def test_labels(self):
        mail_label = FormTests.form.fields["mail"].label
        self.assertEqual(mail_label, "Почта")
        text_label = FormTests.form.fields["text"].label
        self.assertEqual(text_label, "Текст обращения")

    def test_help_texts(self):
        mail_label = FormTests.form.fields["mail"].help_text
        self.assertEqual(mail_label, "Введите вашу почту")
        text_label = FormTests.form.fields["text"].help_text
        self.assertEqual(text_label, "Введите текст обращение")

    def test_create_valid_form(self):
        form_data = {"mail": "exemple@mail.ru", "text": "Тест", "name": "banana"}

        response = django.test.Client().post(
            django.urls.reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )

        self.assertIn("form", response.context)

        self.assertRedirects(
            response,
            django.urls.reverse("feedback:feedback"),
        )

    def test_create_form__with_invalid_mail(self):
        form_data = {"mail": "exemple.ru", "text": "Тест", "name": "banana"}

        response = django.test.Client().post(
            django.urls.reverse("feedback:feedback"),
            data=form_data,
        )

        self.assertFormError(
            response,
            "form",
            "mail",
            "Введите правильный адрес электронной почты.",
        )

    def test_create_feedback_with_empty_fields(self):
        form_data = {"mail": "", "text": "", "name": ""}

        response = django.test.Client().post(
            django.urls.reverse("feedback:feedback"),
            data=form_data,
        )

        self.assertFormError(response, "form", "mail", "Обязательное поле.")
        self.assertFormError(response, "form", "text", "Обязательное поле.")

    def test_created_feedback_and_model(self):
        feedback_count = feedback.models.Feedback.objects.count()

        form_data = {"mail": "test@test.com", "text": "test", "name": "name"}

        django.test.Client().post(
            django.urls.reverse("feedback:feedback"),
            data=form_data,
        )

        self.assertEqual(
            feedback_count + 1,
            feedback.models.Feedback.objects.count(),
        )


__all__ = []
