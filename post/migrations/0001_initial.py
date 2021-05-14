# Generated by Django 3.1 on 2021-05-11 13:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('title', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=100, primary_key=True, serialize=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='categories/')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('title', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='posts/')),
                ('posted', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='post.category')),
                ('tags', models.ManyToManyField(to='post.Tag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-posted'],
            },
        ),
    ]
