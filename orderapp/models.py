from django.db import models


class BaseModel(models.Model):
    create_time = models.DateTimeField(verbose_name='创建时间',
                                       auto_now_add=True)
    last_time = models.DateTimeField(verbose_name='更新时间',
                                     auto_now=True)

    class Meta:
        abstract = True  # 抽象的模型类，即不会创建表


# Create your models here.
class OrderModel(BaseModel):
    num = models.CharField(max_length=20,
                           primary_key=True,
                           verbose_name='订单号')
    title = models.CharField(max_length=100,
                             verbose_name='订单名称')

    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name='订单金额')
    pay_type = models.IntegerField(choices=((0, '余额'),
                                            (1, '银行卡'),
                                            (2, '微信支付'),
                                            (3, '支付宝')),
                                   verbose_name='支付方式',
                                   default=0)
    pay_status = models.IntegerField(choices=((0, '待支付'),
                                              (1, '已支付'),
                                              (2, '待收货'),
                                              (3, '已收货'),
                                              (4, '完成'),
                                              (5, '取消')),
                                     verbose_name='订单状态',
                                     default=0)

    receiver = models.CharField(verbose_name='收货人',
                                max_length=20)
    receiver_phone = models.CharField(max_length=11,
                                      verbose_name='收货人的手机')
    receive_address = models.TextField(verbose_name='收货地址')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 't_order'
        verbose_name = verbose_name_plural = '订单表'
