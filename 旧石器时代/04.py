from jenkins_cli import jenkins_cli
from time import sleep


job_name = 'test'

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
