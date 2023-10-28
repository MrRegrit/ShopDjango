import django.test
import parameterized

import lyceum.middleware as lyc_mw


class MiddlewaresTests(django.test.TestCase):
    @django.test.override_settings(ALLOW_REVERSE=True)
    def test_reverse_russion_words_middleware(self):
        contents = [
            django.test.Client().get("/coffee/").content.decode()
            for _ in range(10)
        ]
        self.assertTrue(contents.count("Я кинйач") == 1)

    @django.test.override_settings(ALLOW_REVERSE=False)
    def test_negative_russion_words_middleware(self):
        contents = [
            django.test.Client().get("/coffee/").content.decode()
            for _ in range(10)
        ]
        self.assertTrue("Я кинйач" not in contents)

    def test_russion_words_middleware(self):
        content = django.test.Client().get("/coffee/").content.decode()
        self.assertTrue(content in ("Я кинйач", "Я чайник"))


class ReverseRussianWordsFunctionTest(django.test.TestCase):
    @parameterized.parameterized.expand(
        [
            ("Привет тевирП", "тевирП Привет"),
            ("HQDшка", "HQDшка"),
            ("Привет_Привет, Иван!", "Привет_Привет, навИ!"),
        ],
    )
    def test_reverse_russianr_words_function(self, inp, out):
        self.assertEqual(
            lyc_mw.ReversRussionWordsMiddleware.reverse_russian_words(
                inp,
            ),
            out,
        )


__all__ = ["MiddlewaresTests", "ReverseRussianWordsFunctionTest"]
