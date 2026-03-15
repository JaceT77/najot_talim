from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        db_table = "category"

    def __str__(self) -> str:
        return f"{self.pk}. {self.name}"


class Product(models.Model):
    name = models.CharField(max_length=30, unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
    )

    class Meta:
        db_table = "products"

    def __str__(self) -> str:
        return f"{self.pk}. {self.name}. {self.category.name}"
