from controllers.core.database import create_table

if __name__ == '__main__':
    import asyncio

    asyncio.run(create_table())