# hedge 2.1相对2.0的变化
### 1、待机与启动之间的安全转换，既防止数据的丢失，也防止脏数据的产生，确保待机重启前后状态的延续，网页待机、启动开关
    hedge2_launcher.py line:28
    hedge_style.py line:79
    hedging_pool.py line:91
### 对程序执行kill(不带参数)命令时，程序内部处理了该异常，确保先待机，再关闭进程
    hedge2_launcher.py line:196
### 货币配置的网页展示和修改
    hedge2_launcher.py line:75
### 网页展示当时的单量池，并可以通过网页手动往单量池倒入正负单量
    hedge2_launcher.py line:35
### 加入强制对冲功能，适配在定时对冲
    core_packages/hedging_pool.py line:400 
    core_packages/hedge_style.py line:272,42
### 对冲单量在不同账户间按参数比例分配
    core_packages/hedging_pool.py line:383
    core_packages/hedging_pool.py line:263
    core_packages/json_arguments.json line:49
### 货币配置的对冲账户可以在下单时选择买卖1档价格中较便宜的、快的、平均价，并可以对此价格配置修正比例
    core_packages/hedging_pool.py line:237
### 余额不足报警的格式化
    core_packages/hedging_pool.py:303
### 统计成交量的循环中对未变化货币单量倒入0单量来触发单量检查
    core_packages/once_check.py:180
### 记录订单的手续费、手续费结算货币、成交均价
    core_packages/exchanges.py:723
### 除了主程序外添加一些实用脚本
    count_as_quote_as_base.py
    generate_amount_pool_json.py
    initialize_program.py
    mysql_cleaner.py
    order_history.py
    order_newest_info_check.py
    不同交易所返回值示例.py
### 钉钉报警给货币配置了无法生成货币对的参数
    core_packages/hedging_pool.py:284
### 使用账户原生订单历史进行订单检查
    core_packages/exchanges.py:747