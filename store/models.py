from django.db import models


class Product(models.Model):
    PRODUCT_TYPE = [
        ("Jersey", "Jersey"),
        ("Hoodie", "Hoodies"),
        ("Tshirt", "T-shirt"),
        ("Sweater", "Sweat-gear"),
        ("Watterbottle", "Water-bottle"),
    ]
    product_name = models.CharField(
        choices=PRODUCT_TYPE, max_length=150, blank=True, null=True
    )
    image = models.ImageField(null=True, blank=True,
                              default='/placeholder.png')
    price = models.PositiveIntegerField()
    description = models.TextField(max_length=500)
    color = models.CharField(max_length=100, blank=True, null=True)
    count_in_stock = models.PositiveIntegerField(
        default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    class Meta:
        ordering = ('-product_name',)
