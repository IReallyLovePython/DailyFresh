from django.shortcuts import render
from django.views.generic import View

from apps.goods.models import GoodsCategory, IndexSlideGoods, IndexPromotion, IndexCategoryGoods
# Create your views here.


class IndexView(View):

    def get(self, request):
        """显示首页"""

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

        # 查询购物车中的商品数量
        cart_count = 0

        # 定义模板数据
        context = {
            'categories': categories,
            'slide_skus': slide_skus,
            'promotions': promotions,
            'cart_count': cart_count,
        }

        # 响应请求,返回html界面
        return render(request, 'index.html', context)