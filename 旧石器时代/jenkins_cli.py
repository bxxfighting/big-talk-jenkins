import jenkins
from xml.etree.ElementTree import Element
from xml_utils import XMLUtil


class JenkinsCli:
    '''
    Jenkins操作类
    '''

    def __init__(self, host, username, token):
        self.host = host
        self.username = username
        self.token = token
        self.server = jenkins.Jenkins(self.host, username=self.username, password=self.token)

    def get_views(self):
        '''
        获取所有view
        '''
        views = self.server.get_views()
        return views

    def get_jobs(self, view_name=None):
        '''
        获取所有job，指定了view名称，就是获取指定view下的job
        '''
        jobs = self.server.get_jobs(view_name=view_name)
        return jobs

    def get_job_config(self, job_name):
        '''
        获取job配置
        '''
        config_xml = self.server.get_job_config(job_name)
        return config_xml

    def create_job(self, job_name, config_xml):
        self.server.create_job(job_name, config_xml)

    def get_view_config(self, view_name):
        '''
        获取视图配置
        '''
        config_xml = self.server.get_view_config(view_name)
        return config_xml

    def create_view(self, view_name, config_xml):
        '''
        创建view
        '''
        if config_xml is None:
            config_xml = jenkins.EMPTY_VIEW_CONFIG_XML
        self.server.create_view(view_name, config_xml)

    def reconfig_view(self, view_name, config_xml):
        '''
        重新配置view
        '''
        self.server.reconfig_view(view_name, config_xml)

    def view_exists(self, view_name):
        '''
        判断view是否存在
        '''
        return self.server.view_exists(view_name)

    def add_jobs_to_view(self, jobs_name, view_name):
        '''
        增加job到view
        '''
        view_config_xml = jenkins.EMPTY_VIEW_CONFIG_XML
        apply_config_func = self.create_view
        if self.view_exists(view_name):
            view_config_xml = self.get_view_config(view_name)
            apply_config_func = self.reconfig_view

        tr = XMLUtil.str2xml_tree(view_config_xml)

        # jenkins中views下所有job必须按字符序正确排序，要不然会显示不正常
        jns = tr.find('jobNames')
        for job in list(jns.iter()):
            if job.tag == 'string':
                jobs_name.append(job.text)
                # 先把原来的删除了
                jns.remove(job)

        # 重新把所有job排好序后，再加入到view中
        jobs_name.sort()
        for job_name in jobs_name:
            ele = Element('string')
            ele.text = job_name
            jns.append(ele)
        view_config_xml = XMLUtil.xml_tree2str(tr)
        apply_config_func(view_name, view_config_xml)

    def run_job(self, job_name, d_param):
        '''
        运行job，指定job名称及参数
        d_param: 参数dict
        '''
        return self.server.build_job(job_name, d_param)

    def get_job_info(self, job_name):
        '''
        获取job信息
        '''
        data = self.server.get_job_info(job_name)
        return data

    def get_job_build_info(self, job_name, build_number):
        '''
        获取job构建信息
        '''
        try:
            data = self.server.get_build_info(job_name, build_number)
        except jenkins.JenkinsException as e:
            data = None
        return data

    def get_next_build_number(self, job_name):
        '''
        获取job下次构建号
        '''
        return self.server.get_job_info(job_name)['nextBuildNumber']

    def job_exists(self, job_name):
        '''
        判断job是否存在
        '''
        return self.server.job_exists(job_name)

    def _get_queue_info(self, queue_number):
        '''
        使用队列号，获取队列信息
        '''
        return self.server.get_queue_item(queue_number)

    def queue_number_to_build_info(self, queue_number):
        '''
        队列号获取构建信息
        '''
        data = self._get_queue_info(queue_number)
        build_info = {}
        # 当开始执行或在队列时被取消，会存在executable字段和cancelled字段
        if 'executable' in data.keys():
            executable = data.get('executable')
            cancelled = data.get('cancelled')
            build_info['cancelled'] = cancelled
            if not cancelled:
                build_info['build_number'] = executable.get('number')
                build_info['build_url'] = executable.get('url')
        return build_info

    def get_job_build_output(self, job_name, build_number):
        '''
        获取job构建输出
        这里根据pipeline的输出格式进行了一些处理
        其实我是觉得一大坨直接显示就不错，跟jenkins本身output一样
        '''
        output = self.server.get_build_console_output(job_name, build_number)
        output = output.replace('\\n', '\n')
        stages = output.split('[Pipeline] stage')
        stage_list = []
        for stage in stages:
            lines = stage.split('\n')
            lines = [line.strip() for line in lines if line.strip() != '']
            title = re.match(r'\[Pipeline\] { \((.*?)\)', lines[0])
            if not title:
                continue
            title = title.group(1)
            lines = [line for line in lines if line.find('[Pipeline]') == -1]
            stage_list.append({
                'title': title,
                'output': lines
            })
        return stage_list


jenkins_cli = JenkinsCli('http://jenkins.oldb.top', 'devops', '1166fff0ba663a66d34675e1d25f63ff48')
