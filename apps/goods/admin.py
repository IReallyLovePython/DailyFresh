from django.contrib import admin
from django.core.cache import cache

from apps.goods.models import *
from celery_tasks.tasks import generate_static_index_html


class BaseAdmin(admin.ModelAdmin):
    """商品活动信息的管理类,运营人员在后台发布内容时，异步生成静态页面"""

    def save_model(self, request, obj, form, change):
        """后台保存对象数据时使用"""

        # obj表示要保存的对象，调用save(),将对象保存到数据库中
        obj.save()
        # 调用celery异步生成静态文件方法
        generate_static_index_html.delay()
        # 修改了数据库数据就需要删除缓存
        cache.delete('index_page_data')

    def delete_model(self, request, obj):
        """后台保存对象数据时使用"""
        obj.delete()
        generate_static_index_html.delay()
        cache.delete('index_page_data')


class IndexPromotionAdmin(BaseAdmin):
    """商品活动站点管理，如果有自己的新的逻辑也是写在这里"""
    # list_display = []
    pass


class GoodsCategoryAdmin(BaseAdmin):
    pass


class GoodsAdmin(BaseAdmin):
    pass


class GoodsSKUAdmin(BaseAdmin):
    pass


class IndexCategoryGoodsAdmin(BaseAdmin):
    pass


admin.site.register(GoodsCategory,GoodsCategoryAdmin)
admin.site.register(GoodsSPU,GoodsAdmin)
admin.site.register(GoodsSKU, GoodsSKUAdmin)
admin.site.register(GoodsImage)
admin.site.register(IndexSlideGoods)
admin.site.register(IndexCategoryGoods, IndexCategoryGoodsAdmin)
admin.site.register(IndexPromotion, IndexPromotionAdmin)


