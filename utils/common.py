from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from DailyFresh import settings


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


class LoginRequiredMixin(object):
    """检测用户是否已经登录"""

    @classmethod
    def as_view(cls, **initkwargs):
        # 调用父类view的as_view方法, 并返回视图函数
        view_fun = super().as_view(**initkwargs)
        # 对视图函数进行装饰
        view_fun = login_required(view_fun)
        # 返回装饰后的视图函数
        return view_fun
