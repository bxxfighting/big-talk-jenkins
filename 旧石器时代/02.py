from jenkins_cli import jenkins_cli
from xml_utils import XMLUtil


# 获取job为test的配置信息，返回的是xml结构
config = jenkins_cli.get_job_config('test')
print(config)

xml_tree = XMLUtil.str2xml_tree(config)
print(xml_tree)
path = 'builders/hudson.tasks.Shell/command'

node = xml_tree.find(path)
print(node.text)
node.text = 'echo "我是new-test"'
config = XMLUtil.xml_tree2str(xml_tree)

# # 通过test的配置再创建一个新job
jenkins_cli.create_job("new-test", config)
