from django import forms
from django.core.exceptions import ValidationError


class PhotoCreateForm(forms.Form):
    link = forms.CharField(required=False)
    image = forms.ImageField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        link = cleaned_data.get('link')
        image = cleaned_data.get('image')
        if link and image:
            raise ValidationError('Заполните одно из полей!')
        if link:
            format_ = link.split('.')[-1]
            acceptable_formats = ('jpg', 'JPEG', 'PNG', 'png')
            if format_ not in acceptable_formats:
                raise ValidationError('Неправильный формат файла!')
        if not link and not image:
            raise ValidationError('Заполните хотя бы одно поле!')
        return cleaned_data


class PhotoUpdateForm(forms.Form):
    width = forms.IntegerField(required=False)
    height = forms.IntegerField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        width = cleaned_data['width']
        height = cleaned_data['height']
        if not width and not height:
            raise ValidationError('Заполните хотя бы одно поле!')
        return cleaned_data


