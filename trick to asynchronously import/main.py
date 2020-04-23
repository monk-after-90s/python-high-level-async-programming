'''
Hwo to import something in a module which must be generated after waited?
'''
import asyncio


async def main():
    # As we said, you'd better treat here as a aio-python programming environment. So the module needed here would
    # better be imported here. Thus the default import style is synchronous, I would like to introduce an asynchronous version.
    # Let see the default import style first:
    ## common import(synchronous import)
    # To get the result of this coroutine here, we'd have to make use of the coroutine function.
    import module
    await module.c()
    # or
    from module import c
    await c()


async def main2():
    # Then asynchronous version:
    ## asynchronous import
    # Now that the module helps us to register the coroutine and get the task(c_task)(see the module async_module),
    # however the task can not be
    # awaited in that module, even the module is in the event loop already when be using. So we import the task(c_task)
    # and await the task here, aiming at wrapping the coroutine result in that module as 'much' as possible.
    import async_module
    await async_module.c_task
    # or
    from async_module import c_task
    await c_task


asyncio.run(main2())
