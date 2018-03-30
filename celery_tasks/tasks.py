# 添加到celery服务器所在电脑的项目中,
# 让celery执行发送邮件前初始化django环境
# import os
# import django
# # 设置环境变量
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DailyFresh.settings")
# # 初始化django环境
# django.setup()
import time
from celery import Celery
from django.core.mail import send_mail
from django.template import loader

from DailyFresh import settings

# 创建celery应用对象
from apps.goods.models import GoodsCategory, IndexSlideGoods, IndexPromotion, IndexCategoryGoods


app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/1')


# 生成未登录的用户访问的静态首页
@app.task
def generate_static_index_html():
    """显示首页"""
    # 防止因celery执行太快，比后台保存还快，导致版本落后
    time.sleep(0.5)

    # 查询商品类别数据
    categories = GoodsCategory.objects.all()

    # 查询商品轮播轮数据
    slide_skus = IndexSlideGoods.objects.all().order_by('index')

    # 查询商品促销活动数据
    promotions = IndexPromotion.objects.all().order_by('index')

    # 查询类别商品数据
    for category in categories:
        # 查询某一类别下的文字类别商品
        text_skus = IndexCategoryGoods.objects.filter(
            category=category, display_type=0).order_by('index')
        # 查询某一类别下的图片类别商品
        img_skus = IndexCategoryGoods.objects.filter(
            category=category, display_type=1).order_by('index')
        # 动态地给类别新增实例属性
        category.text_skus = text_skus
        # 动态地给类别新增实例属性
        category.img_skus = img_skus

    # 定义模板数据
    context = {
        'categories': categories,
        'slide_skus': slide_skus,
        'promotions': promotions,
    }

    # 获取模板文件
    template = loader.get_template('index.html')
    # 渲染生成标准备的html内容
    html_str = template.render(context)

    # 生成一个叫index.html的文件: 放在桌面的static目录下
    file_path = '/home/python/Desktop/static/index.html'
    with open(file_path, 'w') as file:
        # 写入html内容
        file.write(html_str)

app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/1')
@app.task
def send_active_email(username, receiver, token):
    """封装发送邮件方法"""

    subject = "天天生鲜用户激活"  # 标题
    message = ""  # 邮件正文(纯文本)
    sender = settings.EMAIL_FROM  # 发件人
    receivers = [receiver]  # 接收人, 需要是列表
    # 邮件正文(带html样式)
    html_message = '<h2>尊敬的 %s, 感谢注册天天生鲜</h2>' \
                   '<p>请点击此链接激活您的帐号: ' \
                   '<a href="http://127.0.0.1:8000/users/active/%s">' \
                   'http://127.0.0.1:8000/users/active/%s</a>' \
                   % (username, token, token)
    send_mail(subject, message, sender, receivers, html_message=html_message)
