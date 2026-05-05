from django.contrib.auth.models import AbstractUser
from django.db.models import Model, ForeignKey, CASCADE, ManyToManyField
from django.db.models.constraints import UniqueConstraint
from django.db.models.fields import CharField, TextField, DateTimeField, PositiveIntegerField, BooleanField, SlugField, \
    DecimalField, DateField
from django_ckeditor_5.fields import CKEditor5Field


class Category(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(Model):
    title = CharField(max_length=255)
    description = CKEditor5Field(blank=True)
    price = DecimalField(max_digits=10, decimal_places=2)
    category = ForeignKey('apps.Category', CASCADE, related_name='products')
    is_active = BooleanField(default=True)
    created_at = DateTimeField(auto_now=True)

class Favorite(Model):
    user = ForeignKey('apps.User', CASCADE, related_name='favorites')
    product = ForeignKey('apps.Product', CASCADE, related_name='favorites')

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'product'],
                name='unique_user_product'
            )
        ]


class Tag(Model):
    name = CharField(max_length=255)
    slug = SlugField(max_length=255,unique=True)
    posts = ManyToManyField('apps.Post', blank=True, related_name='tags')

class Like(Model):
    user = ForeignKey('apps.User', CASCADE, related_name='likes')
    post = ForeignKey('apps.Post', CASCADE, related_name='likes')

    class Meta:
        unique_together = (
            ('user', 'post'),
        )

class Post(Model):
    title = CharField(max_length=255)
    content = CKEditor5Field(blank=True)
    author = ForeignKey('apps.User', CASCADE, related_name='posts')
    category = ForeignKey('apps.Category', CASCADE, related_name='posts')
    is_published = BooleanField(db_default=True)
    views_count = PositiveIntegerField(db_default=0)
    created_at = DateTimeField(auto_now=True)





