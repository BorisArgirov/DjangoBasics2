from django import forms
from books.models import Book, Tags
from exercise_templates.mixins import DisabledFormMixin


# class BookFormBasic(forms.Form):
#     title = forms.CharField(
#         max_length=100,
#         widget=forms.Textarea(attrs={'placeholder':'e.g. Done'})
#     )
#     price = forms.DecimalField(max_digits=6, decimal_places=2)
#     isbn = forms.CharField(max_length=12)

class BookBaseForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tags.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    class Meta:
        model = Book
        exclude = ['slug']


class BookCreateForm(BookBaseForm):
    ...


class BookEditForm(BookBaseForm):
    ...

class BookDeleteForm(DisabledFormMixin, BookBaseForm):
    ...

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)
