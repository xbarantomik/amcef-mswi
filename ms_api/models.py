from django.db import models


class Post(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    original_post_id = models.IntegerField(null=True)
    user_id = models.IntegerField()
    title = models.CharField(max_length=255)
    body = models.CharField(max_length=255)
