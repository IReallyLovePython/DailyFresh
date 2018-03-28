from django.core.files.storage import FileSystemStorage
from fdfs_client.client import Fdfs_client


class FdfsStorage(FileSystemStorage):
    """自定义文件存储系统"""

    def _save(self, name, content):
        """
        当用户通过管理后台上传文件时,
        django会调用此方法来保存用户上传到django网站的文件,
        我们可以在此方法中保存用户上传的文件到FastDFS服务器中
        """
        # 把用户上传的图片, 通过FastDFS的api, 上传到FastDFS服务器
        client = Fdfs_client('/etc/fdfs/client.conf')
        # client = Fdfs_client('./utils/client.conf')

        # 返回文件在fastdfs服务器中的路径
        try:
            data = content.read()
            # {
            #   'Status': 'Upload successed.',
            #   'Remote file_id':'group1/M00/00/00/wKjSolqihW2ATqs4AAAmv27pX4k506.jpg'
            #    ...
            # }
            json = client.upload_by_buffer(data)
        except Exception as e:
            print(e)
            raise e  # 不要直接捕获异常, 抛出去由调用者进行处理

        if 'Upload successed.' != json.get('Status'):
            # 上传文件失败了
            raise Exception('FastDFS上传文件失败, Status不正确.')

        # 获取文件id
        path = json.get('Remote file_id')
        # 返回文件id, django会自动保存此路径到数据库中
        return path

    def url(self, name):
        """返回图片显示时的url地址"""

        # 此url的值为: 数据库中保存的url路径的值
        url = super().url(name)
        # print(url)
        return 'http://127.0.0.1:8888/' + url