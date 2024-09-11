from django.db import models

from account.models import User
from products.models import Product


# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    is_paid = models.BooleanField(verbose_name='نهایی شده/نشده')
    payment_date = models.DateField(null=True, blank=True, verbose_name='تاریخ پرداخت')

    def __str__(self):
        return str(self.user)

    def sum_price(self):
        sum_price = 0
        for i in self.orderdetail_set.all():
            sum_price += i.product.price
        return sum_price

    def is_sale_prices(self):
        sum_price = 0
        for i in self.orderdetail_set.all():
            sum_price += (i.product.price - i.product.sale_price) * i.count
        return sum_price

    def calculate_total_price(self):
        total_amount = 0
        if self.is_paid:
            for order_detail in self.orderdetail_set.all():
                total_amount += order_detail.final_price * order_detail.count
        else:
            for order_detail in self.orderdetail_set.all():
                if order_detail.product.is_sale:
                    total_amount += order_detail.product.sale_price * order_detail.count
                else:
                    total_amount += order_detail.product.price * order_detail.count

        return total_amount

    def total_price(self):
        total_amount = 0
        if self.is_paid:
            for order_detail in self.orderdetail_set.all():
                total_amount += order_detail.final_price * order_detail.count
        else:
            for order_detail in self.orderdetail_set.all():
                    total_amount += order_detail.product.price * order_detail.count
        return total_amount
    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید کاربران'


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سبد خرید')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    final_price = models.IntegerField(null=True, blank=True, verbose_name='قیمت نهایی تکی محصول')
    count = models.IntegerField(verbose_name='تعداد')

    def __str__(self):
        return str(self.order)

    def price_is_sales(self):
        sum_price = 0
        sum_price += self.product.price * self.count
        return sum_price

    class Meta:
        verbose_name = 'جزییات سبد خرید'
        verbose_name_plural = 'لیست جزییات سبدهای خرید'
