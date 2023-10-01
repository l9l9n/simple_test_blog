from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
    """Новый менеджер для работы с QuerySet запросами"""
    def get_queryset(self):
        """
        Конкретно-прикладной набор запросов QuerySet, фильтрующий посты по их
        статусу и возвращающий поочередный набор запросов QuerySet,
        содержащий посты только со статусом PUBLISHED.
        Позволяет извлекать посты, используя обозначение Post.published.all()
        """
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    objects = models.Manager() # менеджер, применяемый по умолчанию
    published = models.Manager() # конкретно-прикладной менеджер

    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish']),]

    def __str__(self):
        return self.title


