from django.db import models


class Photo(models.Model):
    image = models.ImageField(verbose_name='Фото')

    def __str__(self):
        return self.image.url


class ResizedImage(models.Model):
    resized_image = models.ImageField(null=True, blank=True)
    original = models.OneToOneField('Photo', on_delete=models.CASCADE)

    def generate_filename(self, width, height):
        filename = self.original.image.path.split('/')[-1]
        file = filename.split('.')[0]
        format_ = filename.split('.')[-1]
        new_filename = f'{file}{width}x{height}.{format_}'
        return new_filename
