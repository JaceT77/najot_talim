from django.test import TestCase
from rest_framework.test import APIClient

from .models import Category


class CatalogAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hello to you."})

    def test_category_crud(self):
        response = self.client.post("/api/category/create/", {"name": "books"}, format="json")
        self.assertEqual(response.status_code, 201)
        category_id = response.json()["id"]

        response = self.client.get("/api/category/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(item["id"] == category_id for item in response.json()))

        response = self.client.patch(f"/api/category/{category_id}", {"name": "Stationery"}, format="json")
        self.assertEqual(response.status_code, 200)

        response = self.client.delete(f"/api/category/{category_id}")
        self.assertEqual(response.status_code, 200)

    def test_product_crud(self):
        category = Category.objects.create(name="Electronics")
        response = self.client.post(
            "/api/product/create/",
            {"name": "Laptop", "category_id": category.id},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        product_id = response.json()["id"]

        response = self.client.patch(f"/api/product/{product_id}", {"name": "Ultrabook"}, format="json")
        self.assertEqual(response.status_code, 200)

        response = self.client.delete(f"/api/product/{product_id}")
        self.assertEqual(response.status_code, 200)
