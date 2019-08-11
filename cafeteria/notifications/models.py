from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from cafeteria.images import models as image_models
from cafeteria.users import models as user_models


class Notification(image_models.TimeStampedModel):

    TYPE_CHOICES = (
        ("like", "Like"),
        ("comment", "Comment"),
        ("follow", "Follow")
        # 실제 값  ,  보여지는 값
    )
    creator = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name="creator")
    to = models.ForeignKey(user_models.User, on_delete=models.CASCADE, related_name="to")
    notification_type = models.CharField(max_length=120, choices=TYPE_CHOICES)
    image = models.ForeignKey(image_models.Image, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return "from: {} - to: {}".format(self.creator, self.to)
