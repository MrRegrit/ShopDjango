import django.test
import django.urls

import feedback.forms


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
        form_data = {"mail": "exemple@mail.ru", "text": "Тест"}

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
        form_data = {"mail": "exemple.ru", "text": "Тест"}

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
        form_data = {"mail": "", "text": ""}

        response = django.test.Client().post(
            django.urls.reverse("feedback:feedback"),
            data=form_data,
        )

        self.assertFormError(response, "form", "mail", "Обязательное поле.")
        self.assertFormError(response, "form", "text", "Обязательное поле.")


__all__ = []
