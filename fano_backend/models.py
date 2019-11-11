from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.dispatch import receiver
import os
from django.utils.text import slugify
from .validators import FileValidator

# Create your models here.

validate_file = FileValidator(max_size=5242880, content_types=("audio/mpeg", "audio/mp4", "audio/ogg", 'audio/mp3'))


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    facebook = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    phone = models.CharField(max_length=20)
    track = models.FileField(upload_to='sign_up_track', validators=[validate_file])
    address = models.TextField(blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatar', blank=True, null=True)
    profession = models.CharField(max_length=200, blank=True, null=True)
    about_me = models.TextField(help_text='Describe yourself in 300 words or less', null=True, blank=True)

    def __str__(self):

        return self.user.username


@receiver(models.signals.post_delete, sender=Member)
def delete_avatar_on_object_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `avatar` object is deleted.
    """
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)


@receiver(models.signals.pre_save, sender=Member)
def auto_delete_avatar_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `music` object is updated
    with new file.
    """
    if not instance.id:
        return False
    try:
        old_file = Member.objects.get(id=instance.id).avatar
    except Member.DoesNotExist:
        return False

    new_file = instance.avatar
    if not old_file == new_file:
        try:
            os.path.isfile(old_file.path)
            os.remove(old_file.path)
        except ValueError:
            pass


@receiver(models.signals.post_delete, sender=Member)
def delete_track_on_object_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `avatar` object is deleted.
    """
    if instance.track:
        if os.path.isfile(instance.track.path):
            os.remove(instance.track.path)


class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=254, unique=True)
    context = RichTextField()
    image = models.ImageField(upload_to='blog_picture')
    music = models.FileField('blog_song', blank=True, null=True, validators=[validate_file])
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    edited_by = models.ForeignKey(User, related_name='edited_by', on_delete=models.CASCADE, blank=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.title)
        return super(Blog, self).save()


@receiver(models.signals.pre_save, sender=Blog)
def auto_blog_image_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `music` object is updated
    with new file.
    """
    if not instance.id:
        return False
    try:
        old_file = Blog.objects.get(id=instance.id).image
    except Blog.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        try:
            os.path.isfile(old_file.path)
            os.remove(old_file.path)
        except ValueError:
            pass


@receiver(models.signals.post_delete, sender=Blog)
def delete_blog_image_on_object_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `avatar` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


class Songs(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    cover_art = models.ImageField(upload_to='cover_art', blank=True, null=True)
    music = models.FileField(upload_to='member_track', validators=[validate_file])
    date = models.DateTimeField(auto_now_add=True)


@receiver(models.signals.post_delete, sender=Songs)
def delete_cover_art_on_object_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `avatar` object is deleted.
    """
    if instance.cover_art:
        if os.path.isfile(instance.cover_art.path):
            os.remove(instance.cover_art.path)

    if instance.music:
        if os.path.isfile(instance.music.path):
            os.remove(instance.music.path)


@receiver(models.signals.pre_save, sender=Songs)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `music` object is updated
    with new file.
    """
    if not instance.id:
        return False
    try:
        old_file = Songs.objects.get(id=instance.id).music
    except Songs.DoesNotExist:
        return False

    new_file = instance.music
    if not old_file == new_file:
        try:
            os.path.isfile(old_file.path)
            os.remove(old_file.path)
        except ValueError:
            pass

    try:
        old_file_art = Songs.objects.get(id=instance.id).cover_art
    except Songs.DoesNotExist:
        return False

    new_file_art = instance.cover_art
    if not old_file_art == new_file_art:
        try:
            os.path.isfile(old_file_art.path)
            os.remove(old_file_art.path)
        except ValueError:
            pass


class Events(models.Model):
    title = models.CharField(max_length=200)
    cover_image = models.ImageField(upload_to='event_image')
    content = RichTextField()
    date = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.title


class GalleryCategory(models.Model):
    cat_name = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.cat_name


class Gallery(models.Model):
    cat_name = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery')
    link = models.URLField(blank=True, null=True)
    title = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.title


class VideoGallery(models.Model):
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=20)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.title


class FanoArtist(models.Model):
    artist_name = models.CharField(max_length=200)
    designation = models.CharField(max_length=50)
    facebook = models.URLField()
    instagram = models.URLField()
    image = models.ImageField(upload_to='fano_artist')

    def __str__(self):

        return self.artist_name

