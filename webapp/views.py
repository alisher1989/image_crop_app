import urllib.request
from io import BytesIO
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from uuid import uuid4
from webapp.forms import PhotoCreateForm, PhotoUpdateForm
from webapp.models import Photo, ResizedImage
from PIL import Image
from django.core.files.base import ContentFile


class IndexView(ListView):
    model = Photo
    template_name = 'list.html'
    context_object_name = 'photos'
    queryset = Photo.objects.all()


class PhotoDetailView(DetailView):
    model = Photo

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'] = PhotoUpdateForm
        return context

    def post(self, request, *args, **kwargs):
        width = request.POST.get('width')
        height = request.POST.get('height')
        form = PhotoUpdateForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            image = Image.open(self.get_object().image.path)
            if width and not height:
                height = float(width) * self.get_object().image.height / self.get_object().image.width
            elif height and not width:
                width = float(height) * self.get_object().image.width / self.get_object().image.height
            new_image = image.resize((int(width), int(height)))
            thumb_io = BytesIO()
            new_image.save(thumb_io, image.format)
            resized_image, _ = ResizedImage.objects.get_or_create(original=self.get_object())
            new_filename = resized_image.generate_filename(width, height)
            resized_image.resized_image.save(new_filename, ContentFile(thumb_io.getvalue()), save=False)
            resized_image.save()
            context['resized_image'] = resized_image
        return render(request, 'webapp/photo_detail.html', context=context)


class PhotoCreateView(View):
    def get(self, request, *args, **kwargs):
        form = PhotoCreateForm
        return render(request, 'create.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        link = request.POST['link']
        image = request.FILES.get('image')
        form = PhotoCreateForm(request.POST, request.FILES)
        if form.is_valid():
            if link:
                file_name = f'{uuid4()}.jpg'
                urllib.request.urlretrieve(link, f'media/{file_name}')
                photo = Photo.objects.create(image=file_name)
            else:
                photo = Photo.objects.create(image=image)
            return redirect('detail', photo.pk)
        return render(request, 'create.html', context={'form': form})


