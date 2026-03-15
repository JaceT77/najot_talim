from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(min_length=3, max_length=30)

    class Meta:
        model = Category
        fields = ["id", "name"]

    def validate_name(self, value: str) -> str:
        name = value.strip()
        if not name:
            raise serializers.ValidationError("name cannot be empty")
        return name.title()


class ProductSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source="category.id", read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "category_id"]


class ProductCreateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=3, max_length=30)
    category_id = serializers.IntegerField(min_value=1)

    def validate_name(self, value: str) -> str:
        name = value.strip()
        if not name:
            raise serializers.ValidationError("Name cannot be empty")
        return name.title()

    def validate_category_id(self, value: int) -> int:
        if not Category.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Category does not exist. ID: {value}")
        return value

    def create(self, validated_data):
        category = Category.objects.get(id=validated_data["category_id"])
        return Product.objects.create(
            name=validated_data["name"],
            category=category,
        )


class ProductUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=3, max_length=30, required=False)
    category_id = serializers.IntegerField(min_value=1, required=False)

    def validate(self, attrs):
        if not attrs:
            raise serializers.ValidationError(
                "Provide at least one field to update: name or category_id"
            )
        return attrs

    def validate_name(self, value: str) -> str:
        name = value.strip()
        if not name:
            raise serializers.ValidationError("Name cannot be empty")
        return name.title()

    def validate_category_id(self, value: int) -> int:
        if not Category.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Category does not exist. ID: {value}")
        return value

    def update(self, instance, validated_data):
        if "category_id" in validated_data:
            instance.category = Category.objects.get(id=validated_data["category_id"])
        if "name" in validated_data:
            instance.name = validated_data["name"]
        instance.save()
        return instance


class CategoryDetailSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "products"]
