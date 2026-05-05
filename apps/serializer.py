from django.template.context_processors import request
from jsonschema import ValidationError
from rest_framework.fields import IntegerField, SerializerMethodField, ReadOnlyField, HiddenField, CurrentUserDefault, \
    CharField, empty
from rest_framework.serializers import ModelSerializer, ListSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.models import Post, Tag, Category, User
from apps.models.posts import Like, Product


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'slug')


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

# ------------------------------------------------------------------------------------------------


class UserModelSerializer(ModelSerializer ):
    confirm_password = CharField()
    username = CharField(default='Ziyobek')
    first_name = CharField(default='Valijon')
    email = CharField(default='vali@gmail.com')
    phone = CharField(default='+998976543210')
    password = CharField()


    class Meta:
        model = User
        fields = ('id', 'username','first_name', 'email','phone','password','confirm_password')


    def validate(self, data):
        if data.pop('password') != data.pop('confirm_password'):
            raise ValidationError("Passwords don't match")

    def validate_phone(self, phone):
        if phone.count('+') != 1:
            raise ValidationError("Phone numbers don't match")



# ------------------------------------------------------------------------------------------------


class PostModelSerializer(ModelSerializer):
    likes_count = SerializerMethodField()
    is_liked = SerializerMethodField()
    author = HiddenField(default=CurrentUserDefault())
    tags = ListSerializer(child=CharField(max_length=25),write_only=True)


    class Meta:
        model = Post
        fields = 'id', 'title', 'content', 'category', 'is_published', 'views_count', 'likes_count'
        read_only_fields = ('author',)

    def __init__(self,instance=None,data = empty,**kwargs):
        fields = self.context['request'].query_params.get('fields')
        super().__init__(instance,data,**kwargs)

        if fields:
            allowed = set(fields.split(','))
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)




    def get_likes_count(self, obj: Post):
        # return Like.objects.filter(post=obj).count()
        return obj.likes.count()

    def get_is_liked(self, obj: Post):
        # request = self.context.get('request')
        # user = request.user
        # if user.is_authenticated:
        #     return Like.objects.filter(user=user, post=obj).exists()
        # return False
        return obj.is_liked

    def _chek_tag(self,validated_data):
        tags = validated_data.pop('tags', [] )
        tag_list = []
        for tag in tags:
            obj, created = Tag.objects.get_or_create(name=tag)
            tag_list.append(obj)

        return tag_list


    def create(self, validated_data):
        tag_list = self._chek_tag(validated_data)
        instance: Post = super().create(validated_data)
        instance.tags.set(tag_list)
        return instance

    def update(self, instance, validated_data):
        tag_list = self._chek_tag(validated_data)
        instance.tags.set(tag_list)
        return super().update(instance,validated_data)






class PostSerializer(ModelSerializer):
    likes_count = SerializerMethodField()
    is_liked = SerializerMethodField()

    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'content',
            'category',
            'tags',
            'views_count',
            'is_published',
            'likes_count',
            'is_liked'
        )
        read_only_fields = ('views_count',)




class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        data = cls.token_class.for_user(user)
        data.payload['role'] = user.role
        return data

class ProductSerializer(ModelSerializer):
    favorites_count =SerializerMethodField()
    is_favorited = SerializerMethodField()
    category_name = CharField(
        source='category.name',
        read_only=True
    )

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'description',
            'price',
            'category',
            'category_name',
            'is_active',
            'created_at',
            'favorites_count',
            'is_favorited',
        ]

    def get_favorites_count(self, obj):
        return getattr(obj, 'favorites_count', 0)

    def get_is_favorited(self, obj):
        request = self.context.get('request')

        if not request or request.user.is_anonymous:
            return False

        return getattr(obj, 'is_favorited', False)


