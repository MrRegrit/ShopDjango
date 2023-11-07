import django.core.files.uploadedfile
import django.test
import django.urls

import feedback.forms
import feedback.models


class FormTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.feedback_form = feedback.forms.FeedbackForm()
        cls.feedback_extra_form = feedback.forms.FeedbackExtraForm()
        cls.feedback_fiels_form = feedback.forms.FeedbackFilesForm()

    def test_labels(self):
        mail_label = FormTests.feedback_extra_form.fields["mail"].label
        self.assertEqual(mail_label, "Почта")
        text_label = FormTests.feedback_form.fields["text"].label
        self.assertEqual(text_label, "Текст обращения")
        name_label = FormTests.feedback_extra_form.fields["name"].label
        self.assertEqual(name_label, "Имя")

    def test_help_texts(self):
        mail_help_text = FormTests.feedback_extra_form.fields["mail"].help_text
        self.assertEqual(mail_help_text, "Введите вашу почту")
        text_help_text = FormTests.feedback_form.fields["text"].help_text
        self.assertEqual(text_help_text, "Введите текст обращение")
        name_help_text = FormTests.feedback_extra_form.fields["name"].help_text
        self.assertEqual(name_help_text, "Введите ваше имя")

    def test_create_valid_form(self):
        form_data = {
            "mail": "exemple@mail.ru",
            "text": "Тест",
            "name": "banana",
        }

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
            "feedback_extra_form",
            "mail",
            "Введите правильный адрес электронной почты.",
        )

    def test_create_feedback_with_empty_fields(self):
        form_data = {"mail": "", "text": "", "name": ""}

        response = django.test.Client().post(
            django.urls.reverse("feedback:feedback"),
            data=form_data,
        )

        self.assertFormError(
            response,
            "feedback_extra_form",
            "mail",
            "Обязательное поле.",
        )
        self.assertFormError(
            response,
            "feedback_form",
            "text",
            "Обязательное поле.",
        )

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

        self.assertIsNotNone(
            feedback.models.Feedback.objects.get(text=form_data["text"]),
        )

    def test_upload_file(self):
        feedback_count = feedback.models.FeedbackFiles.objects.count()

        test_file = django.core.files.uploadedfile.SimpleUploadedFile(
            "test.png",
            b"file_content",
            content_type="image/png",
        )
        form_data = {
            "mail": "test@test.com",
            "text": "test",
            "name": "name",
            "file": test_file,
        }

        django.test.Client().post(
            django.urls.reverse("feedback:feedback"),
            data=form_data,
        )

        self.assertEqual(
            feedback_count + 1,
            feedback.models.FeedbackFiles.objects.count(),
        )


__all__ = []
