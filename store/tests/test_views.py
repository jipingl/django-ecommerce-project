from unittest import skip

from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from store.models import Product, Category
from store.views import all_products


@skip("demo skipping")
class TestSkip(TestCase):
    def test_skip(self):
        pass


class TestViewResponses(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        u = User.objects.create(username='admin')
        u.save()
        c = Category.objects.create(name='django', slug='django')
        c.save()
        p = Product.objects.create(category_id=c.id, title='django beginners', created_by_id=u.id,
                                   slug='django-beginners', price='20.00', image='django')
        p.save()

    def test_url_allowed_hosts(self):
        """
        Test allowed hosts
        """
        response = self.client.get('/', HTTP_HOST='localhost')
        self.assertEqual(response.status_code, 400)
        response = self.client.get('/', HTTP_HOST='127.0.0.1')
        self.assertEqual(response.status_code, 200)

    def test_homepage_url(self):
        """
        Test homepage response status
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_product_list_url(self):
        """
        Test category response status
        """
        response = self.client.get(reverse('store:category_detail', args=['django']))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        """
        Test items response status
        """
        response = self.client.get(
            reverse('store:product_detail', args=['django-beginners']))
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        """
        Example: code validation, search HTML for text
        """
        request = HttpRequest()
        response = all_products(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Home</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)

    def test_view_function(self):
        """
        Example: Using request factory
        """
        request = self.factory.get('/item/django-beginners')
        response = all_products(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Home</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)
