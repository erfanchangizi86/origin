from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.
class test_mixin(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان(به فارسی)")
    url_name = models.CharField(max_length=300, verbose_name="عنوان در url(به انگلیسی)")
    is_active = models.BooleanField(default=True, verbose_name="فعال/غیرفعال")
    is_deleted = models.BooleanField(default=False, verbose_name="حذف شده/حذف نشده")

    def save(self, *args, **kwargs):
        self.url_name = self.url_name.title()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        abstract = True


class category(test_mixin):
    title_category = models.ForeignKey('category', on_delete=models.CASCADE, verbose_name="دسته بنده", null=True,
                                       blank=True, related_name='children')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "دسته بنده ها"
        verbose_name_plural = "دسته بندی"


class Brands(test_mixin):
    title_english = models.CharField(max_length=200, verbose_name="نام برند(به انگلیسی)")


class Product(models.Model):
    image = models.ImageField(upload_to="products/images")
    name = models.CharField(max_length=100, db_index=True, verbose_name='عنوان')
    price = models.IntegerField(verbose_name="قیمت")
    short_body = models.CharField(verbose_name="توضیحات کوتاه", max_length=300, db_index=True)
    body = models.TextField(db_index=True, verbose_name="توضیحات")
    is_active = models.BooleanField(default=True, verbose_name="فعال/غیرفعال")
    is_deleted = models.BooleanField(default=False, verbose_name="حذف شده/حذف نشده")

    is_sale = models.BooleanField(null=True, default=False, verbose_name="محصول تخفیف دارد./ندارد")
    sale_price = models.DecimalField(verbose_name="درصد تخفیف", default=0, max_digits=3, decimal_places=2)
    slug = models.SlugField(default='', null=False, blank=True, max_length=200, unique=True,
                            verbose_name='عنوان در url', allow_unicode=True)

    category_product = models.ManyToManyField(category, verbose_name="دسته بندی",
                                              db_index=True, null=True)
    # brand = models.ForeignKey(Brands, on_delete=models.CASCADE, verbose_name='برند', null=True, blank=True)
    # comments = GenericRelation('Comment')

    def __str__(self):
        return f"{self.name} ({self.price})"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.name = self.name.title()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("detail", args={'slug': self.slug, 'id': self.id})

    class Meta:
        verbose_name = 'محصول '
        verbose_name_plural = 'محصولات '


class Comment_product(models.Model):
    title = models.CharField(max_length=200)
