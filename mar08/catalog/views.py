from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Category, Product
from .serializers import (
    CategoryDetailSerializer,
    CategorySerializer,
    ProductCreateSerializer,
    ProductSerializer,
    ProductUpdateSerializer,
)


@api_view(["GET"])
def api_root(request):
    return Response({"message": "API root"})


@api_view(["GET"])
def category_list(request):
    categories = Category.objects.all()
    return Response(CategorySerializer(categories, many=True).data)


@api_view(["POST"])
def category_create(request):
    serializer = CategorySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        category = serializer.save()
    except IntegrityError:
        return Response(
            {"detail": f"this category {serializer.validated_data['name']} already exists in the database"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return Response(CategorySerializer(category).data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def category_item(request, id: int):
    if id <= 0:
        return Response(
            {"detail": "id cannot be equal or lower than 0"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    category = get_object_or_404(Category.objects.prefetch_related("products"), id=id)

    if request.method == "GET":
        return Response(CategoryDetailSerializer(category).data)

    if request.method in {"PUT", "PATCH"}:
        serializer = CategorySerializer(
            category,
            data=request.data,
            partial=request.method == "PATCH",
        )
        serializer.is_valid(raise_exception=True)
        try:
            category = serializer.save()
        except IntegrityError:
            return Response(
                {"detail": f"this category {serializer.validated_data['name']} already exists in the database"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(CategorySerializer(category).data)

    category.delete()
    return Response(True)


@api_view(["GET"])
def product_list(request):
    products = Product.objects.all()
    return Response(ProductSerializer(products, many=True).data)


@api_view(["POST"])
def product_create(request):
    serializer = ProductCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        product = serializer.save()
    except IntegrityError:
        return Response(
            {"detail": f"this product {serializer.validated_data['name']} already exists in the database"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def product_item(request, id: int):
    product = get_object_or_404(Product, id=id)

    if request.method == "GET":
        return Response(ProductSerializer(product).data)

    if request.method in {"PUT", "PATCH"}:
        serializer = ProductUpdateSerializer(
            product,
            data=request.data,
            partial=request.method == "PATCH",
        )
        serializer.is_valid(raise_exception=True)
        try:
            product = serializer.save()
        except IntegrityError:
            return Response(
                {"detail": "Unexpected Error: duplicate value violates a unique constraint"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(ProductSerializer(product).data)

    product.delete()
    return Response(True)
