from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View

# Create your views here.
from django_redis import get_redis_connection

from apps.goods.models import GoodsSKU
from apps.users.models import Address


class PlaceOrdereView(View):
    def get(self,request):
        return HttpResponse('请不要乱来!')

    def post(self, request):
        if not request.user.is_authenticated():
            return redirect(reverse('users:login'))
        sku_ids = request.POST.getlist('sku_ids')

        if not sku_ids:
            # 如果sku_ids没有，就重定向购物车，重选
            return redirect(reverse('cart:cart'))

        # 定义临时容器
        skus = []
        total_count = 0
        total_sku_amount = 0
        trans_cost = 10
        total_amount = 0  # 实付款

        # 查询商品数据
        # 如果是从购物车页面过来，商品的数量从redis中获取
        redis_conn = get_redis_connection('default')
        user_id = request.user.id
        cart_dict = redis_conn.hgetall('cart_%s' % user_id)

        # 遍历商品sku_ids
        for sku_id in sku_ids:
            try:
                sku = GoodsSKU.objects.get(id=sku_id)
            except GoodsSKU.DoesNotExist:
                # 重定向到购物车
                return redirect(reverse('cart:cart'))

            # 取出每个sku_id对应的商品数量
            sku_count = cart_dict.get(sku_id.encode())
            sku_count = int(sku_count)

            # 计算商品总金额
            amount = sku.price * sku_count
            # 将商品数量和金额封装到sku对象
            sku.count = sku_count
            sku.amount = amount
            skus.append(sku)
            # 金额和数量求和
            total_count += sku_count
            total_sku_amount += amount

        # 实付款
        total_amount = total_sku_amount + trans_cost

        # 用户地址信息
        try:
            address = Address.objects.filter(user=request.user).latest('create_time')
        except Address.DoesNotExist:
            address = None  # 没有收货地址，用户需要点击新增地址

        # 构造上下文
        context = {
            'skus': skus,
            'total_count': total_count,
            'total_sku_amount': total_sku_amount,
            'trans_cost': trans_cost,
            'total_amount': total_amount,
            'address': address,
        }

        # 响应结果:html页面
        return render(request, 'place_order.html', context)


class CommitOrdereView(View):
    def post(self,request):
        # todo:订单确认
        pass