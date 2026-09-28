from django.shortcuts import render

# Create your views here.

def photo_add_view(request):
    return render(request, 'photos/photo-add-page.html')

def photo_details_view(request, pk: int):
    return render(request, 'photos/photo-details-page.html')

def photo_edit_view(request, pk: int):
    return  render(request, 'photos/photo-edit-page.html')
