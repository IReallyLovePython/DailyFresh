from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django_redis import get_redis_connection

from apps.goods.models import GoodsCategory, IndexSlideGoods, IndexPromotion, IndexCategoryGoods, GoodsSKU


# Create your views here.


class IndexView(View):
    def get(self, request):
        """进入首页"""

        # 读取缓存:  键=值
        # index_page_data=context字典数据
        context = cache.get('index_page_data')

        if context is None:
            print('首页缓存为空,读取数据库数据')
            # 获取商品类别
            categories = GoodsCategory.objects.all()
            # 获取首页轮播商品
            slide_skus = IndexSlideGoods.objects.all().order_by('index')
            # 获取首页促销活动 (最多获取两条数据)
            promotions = IndexPromotion.objects.all()[0:2]
            # 获取首页类别商品
            # category_skus = IndexCategoryGoods.objects.all() # 界面不好显示
            # [注意]: 针对每一种类别, 查询出属于该类别的 文字商品text_skus
            # 和 图片商品img_skus, 并保存到该类别的对象下
            for c in categories:
                # 查询当前类别的文字商品
                text_skus = IndexCategoryGoods.objects.filter(
                    category=c, display_type=0).order_by('index')
                # 查询当前类别的图片商品
                img_skus = IndexCategoryGoods.objects.filter(
                    category=c, display_type=1).order_by('index')
                # 动态地给类别对象新增两个实例属性
                c.text_skus = text_skus
                c.img_skus = img_skus

            context = {
                'categories': categories,
                'slide_skus': slide_skus,
                'promotions': promotions,
            }

            # 缓存数据:
            # 参数1: 键名
            # 参数2: 缓存的字典数据
            # 参数3: 缓存失效时间1小时
            cache.set('index_page_data', context, 3600)
        else:
            print('缓存不为空, 使用缓存')

        # 获取首页类别购物车中商品总数量
        cart_count = 0
        # 新增一个键值(如果键存在,则为修改)
        context.update({'cart_count': cart_count})

        # 响应请求, 返回html界面
        return render(request, 'index.html', context)


class DetailView(View):
    """商品类别"""

    def get(self, request, sku_id):
        # 查询商品详情信息
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            # 查询不到商品则跳转到首页
            # return HttpResponse('商品不存在')
            return redirect(reverse('goods:index'))

        # 获取所有的类别数据
        categories = GoodsCategory.objects.all()

        # 获取最新推荐
        new_skus = GoodsSKU.objects.filter(
            category=sku.category).order_by('-create_time')[0:2]

        # 查询其它规格的商品
        other_skus = sku.spu.goodssku_set.exclude(id=sku.id)

        # 获取购物车中的商品数量
        cart_count = 0
        # 如果是登录的用户
        if request.user.is_authenticated():
            # 获取用户id
            user_id = request.user.id
            # 从redis中获取购物车信息
            redis_conn = get_redis_connection("default")
            # 如果redis中不存在，会返回None
            cart_dict = redis_conn.hgetall("cart_%s" % user_id)
            for val in cart_dict.values():
                cart_count += int(val)  # 转成int再作累加

            # 保存用户的历史浏览记录
            # history_用户id: [3, 1, 2]
            # 移除现有的商品浏览记录
            key = 'history_%s' % request.user.id
            redis_conn.lrem(key, 0, sku.id)
            # 从左侧添加新的商品浏览记录
            redis_conn.lpush(key, sku.id)
            # 控制历史浏览记录最多只保存3项(包含头尾)
            redis_conn.ltrim(key, 0, 2)

        # 定义模板数据
        context = {
            'categories': categories,
            'sku': sku,
            'new_skus': new_skus,
            'cart_count': cart_count,
            'other_skus': other_skus,
        }

        # 响应请求,返回html界面
        return render(request, 'detail.html', context)


class ListView(View):
    """商品列表"""
    def get(self,request,category_id, page_num):
        # 获取sort参数:如果用户不传，就是默认的排序规则
        sort = request.GET.get('sort', 'default')

        # 校验参数
        # 判断category_id是否正确，通过异常来判断
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return redirect(reverse('goods:index'))

        # 查询商品所有类别
        categories = GoodsCategory.objects.all()

        # 查询该类别商品新品推荐
        new_skus = GoodsSKU.objects.filter(category=category).order_by('-create_time')[0:2]

        # 查询该类别所有商品SKU信息：按照排序规则来查询
        if sort == 'price':
            # 按照价格由低到高
            skus = GoodsSKU.objects.filter(category=category).order_by('price')
        elif sort == 'hot':
            # 按照销量由高到低
            skus = GoodsSKU.objects.filter(category=category).order_by('-sales')
        else:
            skus = GoodsSKU.objects.filter(category=category)
            # 无论用户是否传入或者传入其他的排序规则，我在这里都重置成'default'
            sort = 'default'

        # 分页：需要知道从第几页展示
        page_num = int(page_num)

        # 创建分页器：每页两条记录
        paginator = Paginator(skus, 5)

        # 校验page_num：只有知道分页对对象，才能知道page_num是否正确
        try:
            page = paginator.page(page_num)
        except EmptyPage:
            # 如果page_num不正确，默认给用户显示第一页数据
            page = paginator.page(1)

        # 获取页数列表
        page_list = paginator.page_range

        # 购物车
        cart_count = 0
        # 如果是登录的用户
        if request.user.is_authenticated():
            # 获取用户id
            user_id = request.user.id
            # 从redis中获取购物车信息
            redis_conn = get_redis_connection("default")
            # 如果redis中不存在，会返回None
            cart_dict = redis_conn.hgetall("cart_%s" % user_id)
            for val in cart_dict.values():
                cart_count += int(val)

        # 构造上下文
        context = {
            'category': category,
            'categories': categories,
            'page': page,
            'new_skus': new_skus,
            'page_list': page_list,
            'cart_count': cart_count,
            'sort': sort,
        }

        # 渲染模板
        return render(request, 'list.html', context)