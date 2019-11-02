# python-high-level-async-programming
官方简化的方向，借鉴多线程编程的模板

by 90后老和尚
##从函数说起（Python3.7及以上）:
####在Python里，一切皆是对象，不存在称作过程的东西。函数例如:
    def f(*args,**kwargs):
        print("FUnction f")
####可以看作一种隐式写法。显示写法应该类似如：
    class F():
        def __call__(self):
            print("FUnction f")

    f=F()
####函数的调用
    f(*args,**kwargs)
####定义一个函数，是声明了一个Python内置函数类实例，并且将函数体内的代码封装进该实例的__call__()方法里，使得其能够被调用（后面跟()就是调用，可以有参数）。
####基本上定义函数就是为了调用函数。但函数的定义和调用是两个步骤，两者是独立的。
##协程函数:
####形如
    async def g(*args,**kwargs):
        print("Coroutine function g")
####的函数即是协程函数。可以简单粗暴理解协程函数即是被调用即返回协程的函数，是制作协程最普遍的方法。协程：
    coroutine=g(*args,**kwargs)
##代码包
####为方便讲述，引入一个代码包的概念，简单指封装了一包代码的对象。
####上面的函数f是一个代码包，通过调用函数运行其内包含的代码。而协程函数g不是代码包，调用g(g(*args,**kwargs))并不会运行其定义体中的代码。通过type()函数可以查看f、g都是函数类。可以相信协程函数类是继承于函数类，其__call__()方法被重写了，不包含定义体中的代码，return一个协程对象:
    coroutine=g(*args,**kwargs)
####这个协程对象是代码包！包含了返回他的协程函数的定义体中的代码！
####就好像定义函数就是为了调用它基本没有其他用途，定义协程函数就是为了调用它得到协程基本没有其他用途，定义和调用是两步。
####调用之后，函数的生命就结束了；但是协程函数还远远没有。
##协程的使用，即协程内代码的运行
####异步编程环境的搭建
#####脚本
    import asyncio
    async def main():
        #异步代码放置处
        pass
    asycio.get_event_loop().run_until_complete(main())
#####程序
    import asyncio
    async def main():
        #异步代码放置处
        pass
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
####至此，同步编程环境变成了同步兼异步编程环境。注意，在这里别把main协程函数的定义体当作一个协程函数内部，应该理解为异步版的Python语言（aiopython?），忘掉main外面的东西。下面之说main里面发生的事情。
####在新环境里运行同步代码，只要你不求速度完全没毛病：
    async def main():
        print("Hello world")
        import requests
        requests.get("http://www.baidu.com")
        requests.get("http://www.baidu.com")
        requests.get("http://www.baidu.com")
        requests.get("http://www.baidu.com")
        requests.get("http://www.baidu.com")
        requests.get("http://www.baidu.com")
        requests.get("http://www.baidu.com")
        requests.get("http://www.baidu.com")
        requests.get("http://www.baidu.com")
        requests.get("http://www.baidu.com")
####要是求速度，那么就通过注册协程达到并发。
##同步兼异步环境的协程注册（重点！！！）
####所谓注册协程全称注册协程到事件循环，就是运行协程代码包内的代码。
    async def main():
        async def coro():#协程函数的定义
            print('Hello world')
            return 123
            
        coroutine=coro()#协程的生成
        
        asyncio.create_task(coroutine)#协程的注册(遇到不兼容试试asyncio.ensure_future)
####上面演示了一个协程函数的定义、协程的生成和协程的注册全过程。这是最基础的用法，协程的注册这一步是注册协程之后三不管的：
#####不管何时运行完毕
#####不管返回值（上面那个123）
#####不管报错

    async def main():
        async def coro():#协程函数的定义
            print('Hello world')
            return 123
            
        coroutine=coro()#协程的生成
        
        task=asyncio.create_task(coroutine)#协程的注册
        res=await task
####上面演示了三管的情形。注册协程之后得到一个task(asyncio.Task)。这个task用于管理协程。最普遍的使用是:
    await task#等待运行完
    res=await task#等待协程完成，并且获取协程返回值
####当然，协程内的报错也会传导过来报错。
####并发当然要多个协程一起运行，其宗旨是：尽早注册协程，尽晚等待任务：
    
    async def main():
        async def coro():#协程函数的定义
            print('Hello world')
            return 123
            
        coroutine=coro()#协程的生成
        task=asyncio.create_task(coroutine)#协程的注册
        coroutine2=coro()#协程的生成
        task2=asyncio.create_task(coroutine2)#协程的注册
        coroutine3=coro()#协程的生成
        task3=asyncio.create_task(coroutine3)#协程的注册
        res1=await task1
        res2=await task2
        res3=await task3
####要是多了就得用for循环了（接下来用异步sleep协程函数示范）：
    async def main():
        tasks=[]#搜集task的列表
        for i in range(30):
            tasks.append(asycnio.create_task(asyncio.sleep(i)))
        #获取结果用于打印
        for task in tasks:
            print(await task)
####上面演示了大批量协程的集中注册与等待，做到了协程的尽早提交与尽晚等待。
###for的陷阱
####使用for提交协程有一个陷阱。运行:
    
    async def main():
        tasks = []  # 搜集task的列表
        for i in range(3):
            async def coro():
                return i
    
            tasks.append(asyncio.create_task(coro()))
        #获取结果用于打印
        for task in tasks:
            print(await task)

####结果：
    2
    2
    2
####并不是理想中的
    0
    1
    2
####对于for里面的易变的变量不能直接在协程内跨作用域使用它，而应该通过协程函数的参数传递它的值来锚定它(除非你就是想达到上面的效果)：

    async def main():
        tasks = []  # 搜集task的列表
        for i in range(3):
            async def coro(i=i):
                return i
    
            tasks.append(asyncio.create_task(coro()))
        #获取结果用于打印
        for task in tasks:
            print(await task)

##高并发思路
####通过上面的讲解，不知道你有没有发现一个递归嵌套的现象：在协程内注册协程。高并发的思路就是基于此。结合程序的具体逻辑，能打包的就打包，能并发的就并发。
##很重要的库
####协程应用在耗时的io场景中，最广泛的场景就是网络请求。同步有同步的方法（requests.get），异步也有异步的方法，使用最广泛的是aiohttp库：
        async def aio_get():
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get("http://www.baidu.com") as r:
                    res = await r.text()
####更多内容上网找。