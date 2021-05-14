from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CheckConstraint
from django.utils import timezone
from pytils.translit import slugify

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, primary_key=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(primary_key=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=100, )
    slug = models.SlugField(max_length=100, primary_key=True)
    description = models.TextField()

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    tags = models.ManyToManyField(Tag)
    image = models.ImageField(upload_to='posts/')
    posted = models.DateTimeField(auto_now_add=True)

    price = models.IntegerField(default=0)
    phone_number = models.IntegerField()
    CITIES = (
        ('Ак-Джол', 'Ак-Джол'),
        ('Ананьево', 'Ананьево'),
        ('Ат-Башы', 'Ат-Башы'),
        ('Балыкчы', 'Балыкчы'),
        ('Бишкек', 'Бишкек'),
        ('Каракол', 'Каракол'),
        ('Чолпон-Ата', 'Чолпон-Ата'),
        ('Кара-Балта', 'Кара-Балта'),
        ('Токмок', 'Токмок'),
        ('Нарын', 'Нарын'),
        ('Талас', 'Талас'),
        ('Ош', 'Ош'),
        ('Джалал-Абад', 'Джалал-Абад'),
    )
    city = models.CharField(verbose_name='City', choices=CITIES, max_length=50)


    class Meta:
        ordering = ['-posted']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            current = timezone.now().strftime('%s')
            self.slug = slugify(self.title) + current
        super().save()


class Comment(models.Model):
    text = models.TextField()
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='comments')
    rating = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            CheckConstraint(
                check=models.Q(rating__gte=1) & models.Q(rating__lte=5),
                name='rating_range'
            )
        ]


class Like(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='likes')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='likes')
    is_liked = models.BooleanField(default=False)
