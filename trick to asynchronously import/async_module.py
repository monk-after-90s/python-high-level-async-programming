import asyncio


async def c():
    return 'Hello world'


c_task = asyncio.get_running_loop().create_task(c())
