from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio.session import AsyncSession
from models import Category, Product
from crud_errors import (
    CategoryError,
    PayloadMissingRequiredData,
    CategoryNotFoundError,
    InvalidCategoryDeleteError,
    ProductError,
    ProductNotFoundError,
    InvalidProductDeleteError,
)


async def create_category(payload, db: AsyncSession) -> Category:
    name = payload.name
    if not name:
        raise PayloadMissingRequiredData("Expected name, instead got None")

    if (await db.execute(select(Category).where(Category.name == name))).scalars().first():
        raise ValueError(f"this category {name} already exists in the database")

    try:
        category = Category(name=name)
        db.add(category)
        await db.commit()
        await db.refresh(category)
        return category
    except Exception as e:
        await db.rollback()
        raise CategoryError(f"Unexpected event occured while creating category. Error: {e}")
    
async def category_detail(payload, db: AsyncSession) -> Category:
    id: int = payload.id
    q = (
        select(Category)
        .where(Category.id == id)
        .options(selectinload(Category.products))
    )
    c: Category | None = (await db.execute(q)).scalar_one_or_none()
    if not c:
        raise CategoryNotFoundError("The category is not found")
    return c

async def category_update(id: int, payload, db: AsyncSession) -> Category:
    try:
        c = await db.get(Category, id)
        if c is None:
            raise CategoryNotFoundError("Category does not exist")

        c.name = payload.name
        await db.commit()
        await db.refresh(c)
        return c

    except (CategoryError, CategoryNotFoundError):
        raise

    except Exception as e:
        await db.rollback()
        raise CategoryError(f"Unexpected error: {e}")

async def delete_category(payload, db: AsyncSession) -> bool:    
    id = payload.id
    r = await db.execute(select(Category).where(Category.id == id))

    c = r.scalar_one_or_none()

    if c is None:
        raise CategoryNotFoundError("Category Not Found")
    try:
        await db.delete(c)
        await db.commit()
        return True
    except Exception as e:
        await db.rollback()
        raise InvalidCategoryDeleteError(f"Unexpected error while deleting category: {e}")

async def create_product(payload, db: AsyncSession) -> Product:
    name = payload.name
    category_id = payload.category_id
    if not name:
        raise PayloadMissingRequiredData("Expected name, instead got None")
    if not category_id:
        raise PayloadMissingRequiredData("Expected category_id, instead got None")

    category = await db.get(Category, category_id)
    if category is None:
        raise CategoryNotFoundError(f"Category does not exist. ID: {category_id}")

    if (await db.execute(select(Product).where(Product.name == name))).scalars().first():
        raise ValueError(f"this product {name} already exists in the database")

    try:
        product = Product(name=name, category_id=category_id)
        db.add(product)
        await db.commit()
        await db.refresh(product)
        return product
    except Exception as e:
        await db.rollback()
        raise ProductError(f"Unexpected event occured while creating product. Error: {e}")

async def product_detail(id: int, db: AsyncSession) -> Product:
    product = await db.get(Product, id)
    if not product:
        raise ProductNotFoundError(f"Product does not exist. ID: {id}")
    return product

async def product_update(id: int, payload, db: AsyncSession):
    product = await db.get(Product, id)
    if not product:
        raise ProductNotFoundError(f"Product does not exist. ID: {id}")
    try:
        if payload.category_id is not None:
            category = await db.get(Category, payload.category_id)
            if category is None:
                raise CategoryNotFoundError(f"Category does not exist. ID: {payload.category_id}")
            product.category_id = payload.category_id

        if payload.name is not None:
            product.name = payload.name

        await db.commit()
    except Exception as e:
        await db.rollback()
        raise ProductError(f"Unexpected Error: {e}")
    else:
        await db.refresh(product)
        return product

async def delete_product(id: int, db: AsyncSession) -> bool:
    p = await db.get(Product, id)
    if p is None:
        raise ProductNotFoundError("Product Not Found")
    try:
        await db.delete(p)
    except Exception as e:
        await db.rollback()
        raise InvalidProductDeleteError(f"Unexpected error while deleting product: {e}")
    else:
        await db.commit()
        return True
