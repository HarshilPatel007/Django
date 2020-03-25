from django.db import models

# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=100, null=False)
    email = models.CharField(max_length=100, null=False)
    phone = models.CharField(max_length=100, null=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor')
    )
    name = models.CharField(max_length=100, null=False)
    price = models.FloatField(max_length=100, null=False)
    category = models.CharField(max_length=100, null=False, choices=CATEGORY)
    description = models.TextField(max_length=500, null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    )

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=100, null=False, choices=STATUS)
    date_created = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        template = '{0.customer} {0.product} {0.status}'
        return template.format(self)


