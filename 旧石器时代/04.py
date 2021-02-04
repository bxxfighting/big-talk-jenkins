from jenkins_cli import jenkins_cli
from time import sleep


job_name = 'test'

# jenkins运行job是先把job放到队列中，然后再调度运行
# 因此调用运行job的方法返回的是队列号
# 之后需要拿队列号去获取运行会的构建号
# 其它操作都需要这个构建号当参数
# 在jenkins文档中说，这个队列号会在job运行完成后，保留5分钟
# 所以需要抓紧获取
# 我这里使用最蠢的while循环来获取
# 真正的程序中应该修改这个逻辑，这里只是展示基本功能而已
queue_number = jenkins_cli.run_job(job_name, {})

while True:
    build_info = jenkins_cli.queue_number_to_build_info(queue_number)
    if not build_info:
        sleep(3)
        continue
    print('构建记录：', build_info)
    build_number = build_info['build_number']
    output = jenkins_cli.get_job_build_output(job_name, build_number)
    print('日志输出: ', output)
    break
