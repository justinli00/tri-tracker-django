# Generated by Django 4.0.4 on 2022-06-21 01:21

import blog.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published', models.DateTimeField(default=django.utils.timezone.now)),
                ('content', models.TextField()),
            ],
            options={
                'ordering': ('-published',),
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('image', models.ImageField(default='rango.jpg', upload_to=blog.models.upload_to, verbose_name='Image')),
                ('content', models.TextField()),
                ('slug', models.SlugField(max_length=250, unique_for_date='published')),
                ('published', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='published', max_length=10)),
                ('activity_start', models.DateTimeField(default=django.utils.timezone.now)),
                ('activity_end', models.DateTimeField(default=django.utils.timezone.now)),
                ('activity_distance', models.FloatField(default=0.0)),
                ('distance_units', models.CharField(choices=[('km', 'Kilometers'), ('mi', 'Miles')], default='mi', max_length=10)),
                ('activity_type', models.CharField(choices=[('Running', 'Running'), ('Biking', 'Biking'), ('Swimming', 'Swimming')], default='running', max_length=8)),
            ],
            options={
                'ordering': ('-published',),
            },
        ),
    ]
