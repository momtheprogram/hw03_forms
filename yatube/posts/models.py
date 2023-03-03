from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    text = models.TextField(
        help_text="Заполнение данного поля является обязательным",
        verbose_name="Текст поста",
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    group = models.ForeignKey(
        'Group',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        help_text="Выбрать группу (не обязательно)",
        verbose_name="Группа"
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-pub_date']


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, null=False, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title
