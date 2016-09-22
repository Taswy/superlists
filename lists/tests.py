#coding=utf-8
from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item
# Create your tests here.
class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):

        request = HttpRequest()
        request.method = 'POST'

        request.POST["item_text"] = 'A new list item'
        respose = home_page(request)
        self.assertIn('A new list item', respose.content.decode())

        excepted_html = render_to_string('home.html',
                                         {'new_item_text': 'A new list item'}
                                         )
        self.assertEqual(excepted_html, respose.content.decode())

class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        saved_items = Item.objects.all()
        print saved_items.count()
        first_item = Item()
        first_item.text = 'The first list item.'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second.'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first list item.')
        self.assertEqual(second_saved_item.text, 'Item the second.')