import httpx
import pytest
import pytest_asyncio

from main import app


@pytest_asyncio.fixture
async def async_client():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture
async def db_client():
    from core import settings

    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

    from db import Base, get_db

    test_engine = create_async_engine(settings.database_url)
    TestSessionLocal = async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async def override_get_db():
        async with TestSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest.mark.asyncio
async def test_read_main(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello to you."}


@pytest.mark.asyncio
async def test_read_api_main(async_client):
    response = await async_client.get("/api/")
    assert response.status_code == 200
    assert response.json() == {"message": "API root"}


@pytest.mark.asyncio
async def test_category_crud(db_client):
    # Create
    r = await db_client.post("/api/category/create/", json={"name": "books"})
    assert r.status_code == 201
    created = r.json()
    assert created["name"] == "Books"
    category_id = created["id"]

    # List
    r = await db_client.get("/api/category/")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert any(item["id"] == category_id for item in data)

    # Detail (includes products)
    r = await db_client.get(f"/api/category/{category_id}")
    assert r.status_code == 200
    detail = r.json()
    assert detail["id"] == category_id
    assert detail["products"] == []

    # Update
    r = await db_client.patch(f"/api/category/{category_id}", json={"name": "Stationery"})
    assert r.status_code == 200
    assert r.json()["name"] == "Stationery"

    # Delete
    r = await db_client.delete(f"/api/category/{category_id}")
    assert r.status_code == 200
    assert r.json() is True


@pytest.mark.asyncio
async def test_product_crud(db_client):
    r = await db_client.post("/api/category/create/", json={"name": "Electronics"})
    assert r.status_code == 201
    category_id = r.json()["id"]

    # Create product
    r = await db_client.post("/api/product/create/", json={"name": "Laptop", "category_id": category_id})
    assert r.status_code == 201
    product_id = r.json()["id"]

    # Detail
    r = await db_client.get(f"/api/product/{product_id}")
    assert r.status_code == 200
    assert r.json()["name"] == "Laptop"

    # Update
    r = await db_client.patch(f"/api/product/{product_id}", json={"name": "Ultrabook"})
    assert r.status_code == 200
    assert r.json()["name"] == "Ultrabook"

    # List
    r = await db_client.get("/api/product/")
    assert r.status_code == 200
    assert any(p["id"] == product_id for p in r.json())

    # Delete
    r = await db_client.delete(f"/api/product/{product_id}")
    assert r.status_code == 200
    assert r.json() is True
