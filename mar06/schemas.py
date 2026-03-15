from pydantic import BaseModel, field_validator, ConfigDict, Field, model_validator
from typing import Optional, List

class APIModel(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        from_attributes=True,
    )


class CategoryCreateSchema(APIModel):
    name: str = Field(min_length=3, max_length=30)

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, name: str):
        if not name:
            raise ValueError("name cannot be empty")
        return name.title()


class CategoryOutSchema(APIModel):
    id: int
    name: str


class CategoryDetailSchema(APIModel):
    id: int

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, id: int):
        if id <= 0:
            raise ValueError("id cannot be equal or lower than 0")
        return id


class ProductCreateSchema(APIModel):
    name: str = Field(min_length=3, max_length=30)
    category_id: int = Field(gt=0)

    @model_validator(mode="after")
    def validate_fields(self):
        if not self.name.strip():
            raise ValueError("Name cannot be empty")
        return self


class ProductUpdateSchema(APIModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=30)
    category_id: Optional[int] = Field(default=None, gt=0)

    @model_validator(mode="after")
    def at_least_one_field(self):
        if self.name is None and self.category_id is None:
            raise ValueError("Provide at least one field to update: name or category_id")
        if self.name is not None and not self.name.strip():
            raise ValueError("Name cannot be empty")
        return self


class ProductOutSchema(APIModel):
    id: int
    name: str
    category_id: int


class CategoryWithProductsSchema(CategoryOutSchema):
    products: List[ProductOutSchema] = Field(default_factory=list)
