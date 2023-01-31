from core.configs import settings
from core.database import engine


async def create_table():
    import models.__all_models
    print('Creating the tables in the database')

    async with engine.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)
        print('Successfully created tables.')


if __name__ == '__main__':
    import asyncio

    asyncio.run(create_table())
