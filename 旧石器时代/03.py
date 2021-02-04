from jenkins_cli import jenkins_cli

# 如果我们使用jenkins的方式是一个服务对应一个job
# 那么如果服务很多就会有很多job，都在一个页面上不好查看
# 这时候可以通过view来管理，通过view来把job分组
# 这个view的划分需要根据实际情况，比如同一部门的job放在一起？或者同一种语言的job放在一起？等等

# 创建一个view叫做dev
# 传None就是使用默认配置
view_name = 'dev'
if not jenkins_cli.view_exists(view_name):
    jenkins_cli.create_view(view_name, None)

# 将job加入到view下，方便分类管理
jobs = ['test', 'new-test']
jenkins_cli.add_jobs_to_view(jobs, view_name)
