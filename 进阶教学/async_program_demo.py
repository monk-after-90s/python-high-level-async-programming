'''
异步程序的DEMO
'''
import asyncio
from aiohttp import web


class Work():
    '''
    以下演示全是类方法，业务被封装在一个类里面。具体类实例的实现在业务下层，这里不说。
    '''
    # 网络服务端
    app = None
    # 待机时确保完成的Task
    ensured_tasks = []
    # 业务删除锁
    work_lock = asyncio.Lock()
    # 不可等待只可删除的业务
    endless_work_task: asyncio.Task = None

    @classmethod
    async def setup_server(cls, host='0.0.0.0', port=8088):
        '''
        建立网络服务端

        :return:
        '''
        # 路由
        routes = web.RouteTableDef()

        # 操控待机/恢复的路径
        @routes.view('/switch')
        class SwitchView(web.View):
            async def get(self):
                return web.json_response(data=bool(cls.endless_work_task and not cls.endless_work_task.done()))

            async def post(self):
                # 获得开关切换命令
                # 如果有必要，前端可以post过来一些附加消息，比如操作人账号
                alternate_msg = await self.request.post()
                # 关
                if cls.endless_work_task and not cls.endless_work_task.done():
                    asyncio.create_task(cls.rest())
                # 开
                else:
                    asyncio.create_task(cls.work())
                return web.json_response(data=True)

        cls.app = web.Application()
        cls.app.add_routes(routes)
        # 启动网络服务
        asyncio.create_task(web._run_app(app=cls.app,
                                         host=host,
                                         port=port))

    @classmethod
    async def clear_server(cls):
        '''
        退出并清理服务端

        :return:
        '''
        await cls.app.shutdown()
        await cls.app.cleanup()

    @classmethod
    async def turn_on(cls):
        '''
        开机达到待机状态

        :return:
        '''
        # 建立网络服务端
        asyncio.create_task(cls.setup_server())
        # 待机状态中需要的其他载入
        pass

    @classmethod
    async def work(cls):
        '''
        从待机进入业务运行

        :return:
        '''

        # 举例：业务中1、一般的不确定是否完成的asyncio.Task；2、死循环不可等待的肯定没完成的asyncio.Task
        # 1、===============================================================================
        async def type1coroutine_function():
            print('normal_coroutine starts')
            await asyncio.sleep(2)
            print('normal_coroutine ends')

        # 运行协程而不等待
        type1coroutine_function_task = asyncio.create_task(type1coroutine_function())

        # 自清理回调函数，防止ensured_tasks过大
        def clear_self(task: asyncio.Task):
            cls.ensured_tasks.remove(task)

        # 添加自清理回调函数
        type1coroutine_function_task.add_done_callback(clear_self)

        # 保存Task以备待机之需
        cls.ensured_tasks.append(type1coroutine_function_task)

        # 2、===============================================================================
        async def type2coroutine_function():
            '''
            返回2型协程，该协程一次迭代运行一次1型协程

            :return:
            '''
            while True:
                # 举例一次迭代有一个业务协程的执行和一个休眠
                # 竞争删除锁，确保业务业务关键期间无锁去删除
                async with cls.work_lock:
                    # 业务协程，用一个sleep模拟一下;也可以使用上面的1型示例
                    work_task = asyncio.create_task(asyncio.sleep(3, 'Once work accomplished'))
                    await work_task
                # 休眠
                await asyncio.sleep(60)

        # 启动死循环业务协程，不可等待
        cls.endless_work_task = asyncio.create_task(type2coroutine_function())

    @classmethod
    async def rest(cls):
        '''
        从业务运行到待机

        :return:
        '''
        ensured_tasks_task = None
        # 确保被保护的协程运行完毕
        if cls.ensured_tasks:
            ensured_tasks_task = asyncio.create_task(asyncio.wait(cls.ensured_tasks))
        # 其他待机处理。这一步跟下面await ensured_tasks_task的前后顺序要看具体业务
        pass
        # 等待删除锁
        async with cls.work_lock:
            cls.endless_work_task.cancel()

        if ensured_tasks_task: await ensured_tasks_task

    @classmethod
    async def turn_off(cls):
        '''
        从待机进入关机

        :return:
        '''
        # 清理网络服务端
        clear_server_task = asyncio.create_task(cls.clear_server())
        # 其他关机处理
        pass

        await clear_server_task


loop = asyncio.get_event_loop()


async def turn_on_then_work():
    '''
    关机——>待机——>工作

    :return:
    '''
    await Work.turn_on()
    await Work.work()


loop.create_task(turn_on_then_work())
loop.run_forever()
try:
    loop.run_forever()
except:
    print('Loop detects an exception')


    async def rest_then_off():
        '''
        工作——>待机——>关机

        :return:
        '''
        await Work.rest()
        await Work.turn_off()


    loop.run_until_complete(rest_then_off())
