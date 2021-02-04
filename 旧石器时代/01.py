from jenkins_cli import jenkins_cli

# 获取所有job列表
jobs = jenkins_cli.get_jobs()
print(jobs)

# 获取job为test的配置信息，返回的是xml结构
config = jenkins_cli.get_job_config('test')
print(config)

# 通过test的配置再创建一个新job
jenkins_cli.create_job('test-test', config)
