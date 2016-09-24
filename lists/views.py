from django.shortcuts import render, redirect
from django.http import HttpResponse

from lists.models import Item, List

# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def new_lists(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/the-only-list-in-the-world/')

def view_lists(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the-only-list-in-the-world/')
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})