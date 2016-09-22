#coding=utf-8
from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest

from lists.views import home_page
from django.template.loader import render_to_string
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
