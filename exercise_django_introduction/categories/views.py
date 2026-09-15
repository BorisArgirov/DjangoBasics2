from django.shortcuts import render

from categories.models import Category


# Create your views here.

def list_categories(request):
    categories = Category.objects.all()

    context = {
        'categories': categories
    }

    return render(request, 'categories/list_categories.html', context)

