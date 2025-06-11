import time

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
    async with session.begin():
        query = update(Product).where(Product.id == product_id).values(
            article=f"TEMP-{int(time.time())}",
            **product_data
        )

        session.add(query)
        await session.flush()
        
        query.article = f"ART-{query.id:05d}"
        
        return query