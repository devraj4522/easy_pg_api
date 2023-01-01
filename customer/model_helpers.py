from django.db import models


class HostelTypeChoice(models.TextChoices):
    TRIPLE_SHARING = "TRIPLE_SHARING", "TRIPLE_SHARING"
    DOUBLE_SHARING = "DOUBLE_SHARING", "DOUBLE_SHARING"
    SINGLE = "SINGLE", "SINGLE"
