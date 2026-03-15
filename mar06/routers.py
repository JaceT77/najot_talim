from sqlalchemy import select
from models import Category, Product
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import Depends, APIRouter, HTTPException, status
from db import get_db
import schemas
import crud
import crud_errors as ce
from crud_errors import PayloadMissingRequiredData


router = APIRouter()

@router.get("/")
async def api_root():
    return {"message": "API root"}

@router.get("/category/", response_model=list[schemas.CategoryOutSchema])
async def get_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category))
    categories = result.scalars().all()
    return categories

@router.post('/category/create/', response_model=schemas.CategoryOutSchema, status_code=status.HTTP_201_CREATED)
async def create_category(category: schemas.CategoryCreateSchema, db: AsyncSession = Depends(get_db)):
    try:
        result = await crud.create_category(category, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PayloadMissingRequiredData as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ce.CategoryError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        return result
    
@router.get('/category/{id}', response_model=schemas.CategoryWithProductsSchema)
async def category_detail(id: int, db: AsyncSession = Depends(get_db)):
    try:
        data = schemas.CategoryDetailSchema(id=id)
        result = await crud.category_detail(payload=data, db=db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ce.CategoryNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ce.CategoryError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    else:
        return result

@router.delete('/category/{id}', status_code=status.HTTP_200_OK)
async def category_delete(id: int, db: AsyncSession = Depends(get_db)):
    try:
        data = schemas.CategoryDetailSchema(id=id)
        result = await crud.delete_category(payload=data, db=db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ce.CategoryNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ce.CategoryError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    else:
        return result
    
@router.put('/category/{id}', response_model=schemas.CategoryOutSchema)
@router.patch('/category/{id}', response_model=schemas.CategoryOutSchema)
async def category_update(id: int, category: schemas.CategoryCreateSchema, db: AsyncSession = Depends(get_db)):
    try:
        result = await crud.category_update(id=id, payload=category, db=db)
    except ce.CategoryNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ce.CategoryError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    else:
        return result


@router.get("/product/", response_model=list[schemas.ProductOutSchema])
async def get_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    return result.scalars().all()


@router.post("/product/create/", response_model=schemas.ProductOutSchema, status_code=status.HTTP_201_CREATED)
async def create_product(product: schemas.ProductCreateSchema, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.create_product(product, db)
    except (PayloadMissingRequiredData, ValueError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ce.CategoryNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ce.ProductError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/product/{id}", response_model=schemas.ProductOutSchema)
async def product_detail(id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.product_detail(id=id, db=db)
    except ce.ProductNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/product/{id}", response_model=schemas.ProductOutSchema)
@router.patch("/product/{id}", response_model=schemas.ProductOutSchema)
async def product_update(id: int, payload: schemas.ProductUpdateSchema, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.product_update(id=id, payload=payload, db=db)
    except (ce.ProductNotFoundError, ce.CategoryNotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ce.ProductError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/product/{id}", status_code=status.HTTP_200_OK)
async def product_delete(id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.delete_product(id=id, db=db)
    except ce.ProductNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ce.ProductError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
