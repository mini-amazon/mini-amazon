from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Product, Category


class ProductForm(forms.ModelForm):
    """
    Form for creating and updating products.
    """
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (limit to 5MB)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError(_('Image file too large. Maximum size is 5MB.'))
            
            # Check file type
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            import os
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError(
                    _('Unsupported file extension. Use JPG, JPEG, PNG or GIF.')
                )
        return image


class ProductSearchForm(forms.Form):
    """
    Form for searching products with various filters.
    """
    query = forms.CharField(
        label=_('Search'),
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('Search products...')})
    )
    category = forms.ModelChoiceField(
        label=_('Category'),
        queryset=Category.objects.all(),
        required=False,
        empty_label=_('All Categories')
    )
    min_price = forms.DecimalField(
        label=_('Min Price'),
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': _('Min')})
    )
    max_price = forms.DecimalField(
        label=_('Max Price'),
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': _('Max')})
    )
    SORT_CHOICES = [
        ('name', _('Name (A-Z)')),
        ('-name', _('Name (Z-A)')),
        ('price_asc', _('Price (Low to High)')),
        ('price_desc', _('Price (High to Low)')),
        ('-created_at', _('Newest First')),
        ('created_at', _('Oldest First')),
    ]
    sort_by = forms.ChoiceField(
        label=_('Sort By'),
        choices=SORT_CHOICES,
        required=False,
        initial='-created_at'
    )
