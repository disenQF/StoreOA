import uuid

from django.db import models


# Create your models here.
# 客户的用户表
class UserEntity(models.Model):
    name = models.CharField(max_length=20,
                            verbose_name='账号')
    age = models.IntegerField(default=0,
                              verbose_name='年龄')
    phone = models.CharField(max_length=11,
                             verbose_name='手机号',
                             blank=True,  # 站点的表单字段值可以为空
                             null=True)  # 数据表的字段可以是null值

    def __str__(self):
        return self.name

    class Meta:
        # 设置表名
        db_table = 'app_user'
        verbose_name = '客户管理'
        # 设置复数的表示方式
        verbose_name_plural = verbose_name


class RealProfile(models.Model):
    # 声明一对一的关联关系
    user = models.OneToOneField(UserEntity,
                                verbose_name='账号',
                                on_delete=models.CASCADE)

    real_name = models.CharField(max_length=20,
                                 verbose_name='真实姓名')
    number = models.CharField(max_length=30,
                              verbose_name='证件号')

    real_type = models.IntegerField(verbose_name='证件类型',
                                    choices=((0, '身份证'),
                                             (1, '护照'),
                                             (2, '驾驶证')))

    image1 = models.ImageField(verbose_name='正面照',
                               upload_to='user/real')
    image2 = models.ImageField(verbose_name='反面照',
                               upload_to='user/real')

    def __str__(self):
        return self.real_name

    class Meta:
        db_table = 't_user_profile'
        verbose_name = verbose_name_plural = '实名认证表'


class CartEntity(models.Model):
    class Meta:
        db_table = 't_cart'
        verbose_name = verbose_name_plural = '购物车表'

    user = models.OneToOneField(UserEntity,
                                on_delete=models.CASCADE,
                                verbose_name='账号')

    no = models.CharField(primary_key=True,
                          max_length=10,
                          verbose_name='购物车编号')

    def __str__(self):
        return self.no


# 水果分类模型
class CateTypeEntity(models.Model):
    name = models.CharField(max_length=20,
                            verbose_name='分类名')
    order_num = models.IntegerField(verbose_name='排序')

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'mainapp'  # 指定应用的名称
        db_table = 't_category'
        ordering = ['-order_num']  # 指定排序字段， - 表示降序
        verbose_name = '水果分类'
        verbose_name_plural = verbose_name


class FruitEntity(models.Model):
    name = models.CharField(max_length=20,
                            verbose_name='水果名')
    price = models.FloatField(verbose_name='价格')
    source = models.CharField(max_length=30,
                              verbose_name='源产地')

    # 建议多对一的关联关系
    category = models.ForeignKey(CateTypeEntity,
                                 related_name='fruits',
                                 to_field='id',
                                 on_delete=models.CASCADE)

    # 默认情况下，反向引用的名称是当前类的名称(小写)_set
    # 可以通过related_name 来指定
    # db_table='t_collect' 使用第三张表建立fruit和user的多对多关系
    users = models.ManyToManyField(UserEntity,
                                   db_table='t_collect',
                                   related_name='fruits',
                                   verbose_name='收藏用户列表')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 't_fruit'
        verbose_name = '水果表'
        verbose_name_plural = verbose_name


# 声明水果商品与购物车的关系表
class FruitCartEntity(models.Model):
    cart = models.ForeignKey(CartEntity,
                             on_delete=models.CASCADE,
                             verbose_name='购物车')

    fruit = models.ForeignKey(FruitEntity,
                              on_delete=models.CASCADE,
                              verbose_name='水果名')
    cnt = models.IntegerField(verbose_name='数量',
                              default=1)

    def __str__(self):
        return self.fruit.name + ':' + self.cart.no

    @property
    def price1(self):
        # 属性方法在后台显示时没有verbose_name, 如何解决？
        return self.fruit.price  # 从获取主的对象属性

    @property
    def price(self):
        # 属性方法在后台显示时没有verbose_name, 如何解决？
        return round(self.cnt * self.fruit.price, 2)

    class Meta:
        db_table = 't_fruit_cart'
        verbose_name_plural = verbose_name = '购物车详情表'


class StoreEntity(models.Model):
    # 默认情况下，模型自动创建主键id字段--隐式
    # 但是也可以显示的方式声明主键（primary key）
    id = models.UUIDField(primary_key=True,
                          verbose_name='店号')

    name = models.CharField(max_length=50,
                            verbose_name='店名')

    # 表中对应的字段是 type_
    store_type = models.IntegerField(choices=((0, '自营'), (1, '第三方')),
                                     verbose_name='类型',
                                     db_column='type_')

    address = models.CharField(max_length=100,
                               verbose_name='地址')

    # 支持城市搜索， 所以创建city索引
    city = models.CharField(max_length=50,
                            verbose_name='城市',
                            db_index=True)

    logo = models.ImageField(verbose_name='LOGO',
                             upload_to='store',
                             width_field='logo_width',
                             height_field='logo_height',
                             null=True,
                             blank=True)

    logo_width = models.IntegerField(verbose_name='LOGO宽',
                                     null=True)
    logo_height = models.IntegerField(verbose_name='LOGO高',
                                      null=True)

    summary = models.TextField(verbose_name='介绍',
                               blank=True,
                               null=True)

    opened = models.BooleanField(verbose_name='是否开业',
                                 default=False)

    create_time = models.DateTimeField(verbose_name='成立时间',
                                       auto_now_add=True,
                                       null=True)

    last_time = models.DateTimeField(verbose_name='最后变更时间',
                                     auto_now=True,
                                     null=True)

    @property
    def open_time(self):
        print(self.create_time)
        return self.create_time

    # 站点显示对象的字符串信息
    def __str__(self):
        return self.name + "-" + self.city

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # 调用模型保存方法时被调用
        if not self.id:  # 判断是否为新增
            self.id = uuid.uuid4().hex

        super().save()

    @property
    def id_(self):
        # return str(self.id).replace('-', '')
        return self.id.hex

    class Meta:  # 元数据
        db_table = 't_store'
        unique_together = (('name', 'city'),)
        verbose_name = '水果店'
        verbose_name_plural = verbose_name
