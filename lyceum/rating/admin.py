import django.contrib

import rating.models

django.contrib.admin.site.register(rating.models.Rating)
