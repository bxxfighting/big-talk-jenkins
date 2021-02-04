from jenkins_cli import jenkins_cli


# 创建一个view叫做dev
# 传None就是使用默认配置
view_name = 'dev'
if not jenkins_cli.view_exists(view_name):
    jenkins_cli.create_view(view_name, None)

# 将job加入到view下，方便分类管理
jobs = ['test', 'new-test']
jenkins_cli.add_jobs_to_view(jobs, view_name)
