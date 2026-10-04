from django import forms

from exercise_templates.mixins import DisabledFormMixin
from reviews.models import Review


class ReviewBaseForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewCreateForm(ReviewBaseForm):
    ...

class ReviewEditForm(ReviewBaseForm):
    ...

class ReviewDeleteForm(DisabledFormMixin, ReviewBaseForm):
    ...