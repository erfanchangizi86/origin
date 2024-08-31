from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.

#

class Media(models.Model):
    # id - به صورت خودکار توسط Django اضافه می‌شود، نیازی به تعریف آن نیست

    title = models.CharField(max_length=255)  # string معادل
    description = models.TextField()  # text معادل
    url = models.URLField(max_length=255)  # string معادل (URL)
    thumbnail = models.URLField(max_length=255)  # string معادل (URL برای تصویر کوچک)

    # type - enum معادل
    TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('file', 'File'),
        ('pdf', 'PDF'),
        ('link', 'Link'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    # mediable_id و mediable_type - برای پیاده‌سازی morph در Django
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    mediable = GenericForeignKey()

    def __str__(self):
        return self.title