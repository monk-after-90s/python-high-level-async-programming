'''
协程函数例子
'''

import asyncio


async def robot(name: str, sleep_seconds: int):
    '''
    正常运行的协程样例

    :param name:
    :param sleep_seconds:
    :return:
    '''
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
    try:
        writer.write('{}:starts...'.format(name).encode())
        await writer.drain()

        await asyncio.create_task(asyncio.sleep(sleep_seconds))

        writer.write('{}:ends.'.format(name).encode())
        await writer.drain()
        try:
            return "{}'s result.".format(name)
        finally:
            writer.close()
    except asyncio.CancelledError:
        writer.write('{} canceled'.format(name).encode())
        await writer.drain()
        raise
