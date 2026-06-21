from django.db import models
from django.urls import reverse
from django.utils.text import slugify


from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Наименование'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True,
        verbose_name='Slug'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category_products_view', kwargs={'category_slug': self.slug})


class Product(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Наименование'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Категория'
    )
    added_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )
    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name='Стоимость'
    )
    image = models.URLField(
        verbose_name='Изображение'
    )
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name='Остаток'
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['category__name', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_view', kwargs={'product_id': self.pk})

class CartItem(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='Товар',
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'

    @property
    def total(self):
        return self.product.price * self.quantity