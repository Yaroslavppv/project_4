from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    forbidden_words = [
        'казино', 'криптовалюта', 'крипта', 'биржа',
        'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
    ]

    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'category', 'price')

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('name')
        for word in self.forbidden_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError(f'Название не может содержать слово "{word}"')
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data.get('description')
        for word in self.forbidden_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError(f'Описание не может содержать слово "{word}"')
        return cleaned_data

    def clean_price(self):
        cleaned_data = self.cleaned_data.get('price')
        if cleaned_data < 0:
            raise forms.ValidationError('Цена продукта не может быть отрицательной')
        return cleaned_data

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
            max_size = 5 * 1024 * 1024
            if image.size > max_size:
                raise forms.ValidationError("Файл слишком большой. Максимальный размер — 5 МБ.")

            valid_extensions = ['jpg', 'jpeg', 'png']
            extension = image.name.split('.')[-1].lower()
            if extension not in valid_extensions:
                raise forms.ValidationError("Допустимые форматы: JPEG, PNG.")

        return image

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-check-input'