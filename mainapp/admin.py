from django.contrib import admin

from mainapp.models import UserEntity, CateTypeEntity, FruitEntity, StoreEntity

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    # 列表中显示的字段
    list_display = ('id', 'name', 'phone')
    list_per_page = 2  # 每一页显示记录数
    list_filter = ('id', 'phone')  # 过滤器（一般配置分类字段）
    search_fields = ('id', 'phone')  # 搜索字段

class CateTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'order_num')

class FruitAdmin(admin.ModelAdmin):
    list_display = ('name', 'source', 'price', 'category')

class StoreAdmin(admin.ModelAdmin):
    list_display = ('id_', 'name', 'city', 'address', 'store_type', 'logo')
    # 指定表单修改的字段
    fields = ('name', 'city', 'address', 'store_type', 'logo', 'summary')

# 将模型增加到站点中
admin.site.register(UserEntity, UserAdmin)
admin.site.register(CateTypeEntity, CateTypeAdmin)
admin.site.register(FruitEntity, FruitAdmin)
admin.site.register(StoreEntity, StoreAdmin)