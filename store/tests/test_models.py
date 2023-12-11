from django.contrib.auth.models import User
from django.test import TestCase

from store.models import Category, Product


class TestCategoryModel(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="django", slug="django")

    def test_category_model_entry(self):
        """
        Test Category model data insertion/types/field attributes
        """
        data = self.category
        self.assertTrue(isinstance(data, Category))
        self.assertEqual(str(data), "django")


class TestProductsModel(TestCase):

    def setUp(self):
        c = Category.objects.create(name='django', slug='django')
        c.save()
        u = User.objects.create(username='admin')
        u.save()
        self.p1 = Product.objects.create(category_id=c.id, title='django beginners', created_by_id=u.id,
                                         slug='django-beginners', price='20.00', image='django')
        self.p2 = Product.objects.create(category_id=c.id, title='django advanced', created_by_id=u.id,
                                         slug='django-advanced', price='20.00', image='django', is_active=False)

    def test_products_model_entry(self):
        """
        Test product model data insertion/types/field attributes
        """
        data = self.p1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), 'django beginners')
