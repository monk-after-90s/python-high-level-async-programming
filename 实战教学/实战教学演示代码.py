import asyncio


async def main():
    # 异步代码放置处
    async def total_task():
        '''
        测试百度、新浪、淘宝主页的平均加载速度

        :return:
        '''
        import aiohttp

        async def baidu_avg():
            '''
            测试百度主页的平均加载时间

            :return:
            '''
            async with aiohttp.ClientSession() as session:
                async def baidu_v(session=session):
                    '''
                    测试一次百度主页的加载时间

                    :return:
                    '''
                    start_time = asyncio.get_running_loop().time()

                    async with session.get("http://www.baidu.com") as r:
                        res = await asyncio.create_task(r.text())
                    end_time = asyncio.get_running_loop().time()
                    return end_time - start_time

                tasks = []
                tasks.append(asyncio.create_task(baidu_v()))
                tasks.append(asyncio.create_task(baidu_v()))
                tasks.append(asyncio.create_task(baidu_v()))
                return sum([(await task) for task in tasks]) / len(tasks)

        async def sina_avg():
            '''
            测试新浪主页的平均加载时间

            :return:
            '''
            async with aiohttp.ClientSession() as session:
                async def sina_v(session=session):
                    '''
                    测试一次新浪主页的加载时间

                    :return:
                    '''
                    start_time = asyncio.get_running_loop().time()
                    async with session.get('https://www.sina.com.cn')as r:
                        await asyncio.create_task(r.text())
                    end_time = asyncio.get_running_loop().time()
                    return end_time - start_time

                task1 = asyncio.create_task(sina_v())
                task2 = asyncio.create_task(sina_v())
                return (await task1 + await task2) / 2

        async def taobao_avg():
            '''
            测试淘宝主页的平均加载时间

            :return:
            '''
            async with aiohttp.ClientSession() as session:
                async def taobao_v(session=session):
                    '''
                    测试一次淘宝主页的加载速度

                    :return:
                    '''
                    start_time = asyncio.get_running_loop().time()
                    async with session.get('https://www.taobao.com')as r:
                        await asyncio.create_task(r.text())
                    end_time = asyncio.get_running_loop().time()
                    return end_time - start_time

                tasks = [asyncio.create_task(taobao_v()) for i in range(4)]
                return sum([await task for task in tasks]) / len(tasks)

        baidu_avg_task = asyncio.create_task(baidu_avg())
        sina_avg_task = asyncio.create_task(sina_avg())
        taobao_avg_task = asyncio.create_task(taobao_avg())
        return f'百度均速:{await baidu_avg_task},新浪均速:{await sina_avg_task},淘宝均速:{await taobao_avg_task}'

    # 测试百度、新浪、淘宝主页的平均加载速度
    task = asyncio.create_task(total_task())
    print(await task)


asyncio.get_event_loop().run_until_complete(main())
