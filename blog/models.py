from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from django_resized import ResizedImageField
from jdatetime import datetime
from django.template.defaultfilters import slugify


# Managers
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        REJECTED = 'RJ', 'Rejected'

    CATEGORY_CHOICES = (
        ('هوش مصنوعی', 'هوش مصنوعی'),
        ('برنامه نویسی', 'برنامه نویسی'),
        ('بلاکچین', 'بلاکچین'),
        ('امنیت', 'امنیت'),
        ('سایر', 'سایر'),
    )

    # relations
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts", verbose_name="نویسنده")
    # data fields
    title = models.CharField(max_length=200, verbose_name="عنوان")
    description = models.TextField(verbose_name="توضیحات")
    slug = models.SlugField(max_length=200, verbose_name="اسلاگ")
    # date fields
    publish = jmodels.jDateTimeField(default=timezone.now, verbose_name="تاریخ انتشار")
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")
    # choice fields
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT, verbose_name="وضعیت")
    reading_time = models.PositiveIntegerField(verbose_name="زمان مطالعه")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="سایر", verbose_name='دسته بندی')

    objects = jmodels.jManager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(viewname='blog:post_detail', kwargs={'post_id': self.id})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        for img in self.images.all():
            storage, path = img.image_file.storage, img.image_file.path
            storage.delete(path)
        super().delete(*args, **kwargs)


class Ticket(models.Model):
    message = models.TextField(verbose_name='پیام')
    name = models.CharField(max_length=200, verbose_name='نام')
    email = models.EmailField(verbose_name='ایمیل')
    phone = models.CharField(max_length=11, verbose_name='شماره تماس')
    subject = models.CharField(max_length=200, verbose_name='موضوع')

    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت ها'

    def __str__(self):
        return self.subject


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='پست')
    name = models.CharField(max_length=200, verbose_name="نام")
    body = models.TextField(verbose_name="متن کامنت")
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")
    active = models.BooleanField(default=False, verbose_name="وضعیت")

    objects = jmodels.jManager()

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'

    def __str__(self):
        return f"{self.name}: {self.post}"


def get_image(instance, filename):
    return f"post_images/{datetime.now().strftime('%Y/%m/%d')}/{filename}"


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', verbose_name='پست')
    image_file = ResizedImageField(upload_to=get_image, crop=['middle', 'center'], size=[500, 500], quality=100,
                                   verbose_name='فایل تصویر')
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name='عنوان')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')

    objects = jmodels.jManager()

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصویر ها'

    def __str__(self):
        return self.title if self.title else self.image_file.name

    def delete(self, *args, **kwargs):
        storage, path = self.image_file.storage, self.image_file.path
        storage.delete(path)
        super().delete(*args, **kwargs)


def get_image_account(instance, filename):
    return f"account_images/{datetime.now().strftime('%Y/%m/%d')}/{filename}"


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account', verbose_name='کاربر')
    date_of_birth = jmodels.jDateField(blank=True, null=True, verbose_name='تاریخ تولد')
    bio = models.TextField(blank=True, null=True, verbose_name='بایو')
    job = models.CharField(max_length=200, blank=True, null=True, verbose_name='شغل')
    photo = ResizedImageField(upload_to=get_image_account, size=[500, 500], quality=100, crop=['middle', 'center'],
                              blank=True, null=True, verbose_name='تصویر')

    objects = jmodels.jManager()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'اکانت'
        verbose_name_plural = 'اکانت ها'
