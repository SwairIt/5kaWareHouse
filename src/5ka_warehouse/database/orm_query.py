import time

# import uuid

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Category, Product


# async def orm_get_categories(session: AsyncSession):
#     ...

# async def orm_create_categories(session: AsyncSession, categories: list):
#     query = select(Category)
#     result = await session.execute(query)
#     if result.first():
#         return
#     session.add_all([Category(name=name) for name in categories])
#     await session.commit()


async def orm_add_product(session: AsyncSession, product_data: dict):
    async with session.begin():
        product = Product(
            article=f"TEMP-{int(time.time())}",
            **product_data
        )
        session.add(product)
        await session.flush()
        
        product.article = f"ART-{product.id:05d}"
        
        return product
    



async def orm_update_product(session: AsyncSession, product_id: int, product_data: dict):
    query = update(Product).where(Product.id == product_id).values(
        name=product_data["name"],
        price=product_data["price"],
        quantity=product_data["quantity"],
        category_id=product_data["category_id"])
    await session.execute(query)
    await session.commit()


async def orm_get_products(session: AsyncSession):
    query = select(Product)
    result = await session.scalars(query)
    return result
    

async def orm_get_product(session: AsyncSession, product_id: int):
    query = select(Product).where(Product.id == product_id)
    result = await session.scalar(query)
    return result


async def orm_delete_product(session: AsyncSession, product_id: int) -> None:
    query = delete(Product).where(Product.id == product_id)
    await session.execute(query)
    await session.commit()


# async def orm_update_product(session: AsyncSession, product_id: int, product_data: dict):
#     query = update(Product).where(Product.id == product_id).values(**product_data)
#     session.add(query)
#     await session.commit()