import pytest
from fastapi import status
from sqlalchemy import select

from src.models import books
from src.models import sellers


# Тест на ручку создания продавца
@pytest.mark.asyncio
async def test_create_seller(db_session, async_client):
    data = {"first_name": "1", "last_name": "1", "e_mail": "123@mail.com", "password": "123123123123"}
    response = await async_client.post("/api/v1/sellers/", json=data)
    assert response.status_code == status.HTTP_201_CREATED

    result_data = response.json()

    assert result_data == {
        "id": result_data["id"],
        "first_name": "1",
        "last_name": "1",
        "e_mail": "123@mail.com"
    }


# Тест на ручку получения списка всех продавцов
@pytest.mark.asyncio
async def test_get_sellers(db_session, async_client):
    seller1 = sellers.Seller(first_name="name", last_name="familia", e_mail="asdfasdf", password="qwertyuiop")
    seller2 = sellers.Seller(first_name="name_2", last_name="familia_2", e_mail="asdfasdf_123", password="qwertyuiop")
    db_session.add_all([seller1, seller2])
    await db_session.flush()

    response = await async_client.get("/api/v1/sellers/")

    assert response.status_code == status.HTTP_200_OK

    assert response.json() == {
        "sellers": [{"id": seller1.id, "first_name": "name", "last_name": "familia", "e_mail": "asdfasdf"},
                    {"id": seller2.id, "first_name": "name_2", "last_name": "familia_2", "e_mail": "asdfasdf_123"},
                    ]
    }


# Тест на ручку получения продавца со списком его книг
@pytest.mark.asyncio
async def test_get_seller_with_books(db_session, async_client):
    seller = sellers.Seller(first_name="name", last_name="familia", e_mail="asdfasdf", password="qwertyuiop")
    db_session.add(seller)
    await db_session.flush()
    
    data = { "title": "Wrong Code", "author": "Robert Martin", "pages": 104, "year": 2007,
            "seller_id": seller.id}
    response = await async_client.post("/api/v1/books/", json=data)

    result_data = response.json()
    response = await async_client.request(method="GET", url=f"/api/v1/sellers/{seller.id}")

    assert response.status_code == status.HTTP_200_OK
    
    assert response.json() == {"id": seller.id,
                               "first_name": "name",
                               "last_name": "familia",
                               "e_mail": "asdfasdf",
                               "books": [result_data]
                               }


# Тест на ручку удаления продавца
@pytest.mark.asyncio
async def test_delete_seller(db_session, async_client):
    seller = sellers.Seller(first_name="name", last_name="familia", e_mail="asdfasdf", password="qwertyuiop")
    db_session.add(seller)
    await db_session.flush()
    
    book = books.Book(author="Pushkin", title="Eugeny Onegin", year=2001, count_pages=104, seller_id=seller.id)
    db_session.add(book)
    await db_session.flush()

    response = await async_client.delete(f"/api/v1/sellers/{seller.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    await db_session.flush()

    all_sellers = await db_session.execute(select(sellers.Seller))
    res = all_sellers.scalars().all()
    assert len(res) == 0

    all_seller_books = await db_session.execute(select(books.Book).where(books.Book.seller_id == seller.id))
    res = all_seller_books.scalars().all()
    assert len(res) == 0


# Тест на ручку обновления продавца
@pytest.mark.asyncio
async def test_update_seller(db_session, async_client):
    seller = sellers.Seller(first_name="name", last_name="familia", e_mail="asdfasdf", password="qwertyuiop")
    db_session.add(seller)
    await db_session.flush()

    response = await async_client.put(
        f"/api/v1/sellers/{seller.id}",
        json={"first_name": "shop", "last_name": "SPb", "e_mail": "spb_books", "id": seller.id},
    )

    assert response.status_code == status.HTTP_200_OK
    await db_session.flush()

    res = await db_session.get(sellers.Seller, seller.id)
    assert res.first_name == "shop"
    assert res.last_name == "SPb"
    assert res.e_mail == "spb_books"
    assert res.id == seller.id