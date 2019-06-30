from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from instar.images import models as image_models
from instar.users import models as user_models


class Notification(image_models.TimeStampedModel):

    TYPE_CHOICES = (
        ("like", "Like"),
        ("comment", "Comment"),
        ("follow", "Follow")
    )
    creator = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name="creator")
    to = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name="to")
    notification_type = models.CharField(max_length=120, choices=TYPE_CHOICES)
    image = models.ForeignKey(image_models.Image, on_delete=models.CASCADE, null=True, blank=True)
