# Generated by Django 4.2.4 on 2023-08-16 12:12

from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_file', models.ImageField(upload_to='post_images/', verbose_name='فایل تصویر')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='عنوان')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('created', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_images', to='blog.post', verbose_name='تصویر')),
            ],
            options={
                'verbose_name': 'تصویر',
                'verbose_name_plural': 'تصویر ها',
                'ordering': ['-created'],
                'indexes': [models.Index(fields=['-created'], name='blog_image_created_a116df_idx')],
            },
        ),
    ]
