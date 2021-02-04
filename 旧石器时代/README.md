### 故事背景
在旧石器时代，人们刚刚接触jenkins，很新奇，于是研究了起来ing  

### 前期准备

* [Jenkins安装篇](https://my.oschina.net/bxxfighting/blog/3122435)  
> 安装完成后，可以使用admin用户，也可以接入ldap后，重新创建一个新用户  
> 以后所有操作都统一使用此用户，我是在ldap中创建了devops用户，所有都通过此用户来操作  
> 并且那个token也是在此用户下生成的，配置到jenkins_cli.py中  
```
jenkins_cli = JenkinsCli('http://jenkins.oldb.top', 'devops', '1166fff0ba663a66d34675e1d25f63ff48')
```

* [python jenkins开发包文档](https://python-jenkins.readthedocs.io/en/latest/examples.html)  
> 通过```pip install python-jenkins```安装  
> jenkins_cli.py中记录会用到的方法  
