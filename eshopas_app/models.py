import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
import logging
from django.shortcuts import get_object_or_404
from imagekit.models import ImageSpecField
from django.db.models.signals import post_save
from django.dispatch import receiver
from .image_processors import ResizeImageProcessor, ResizeToFill, resize_image


class Category(models.Model):
    name = models.CharField(max_length=100)
    type = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_id = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    thumbnail = ImageSpecField(source='image', processors=[ResizeToFill(150, 200)], format='JPEG', options={'quality': 90})
    is_featured = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    favorites = models.ManyToManyField(User, related_name='favorites', blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        logger = logging.getLogger(__name__)

        try:
            img = Image.open(self.image.path)

            if img.height > 200 or img.width > 150:
                output_size = (150, 200)
                img.thumbnail(output_size)
                img.save(self.image.path)

                logger.info(f"Resized image for product {self.id} to {img.width}x{img.height}")

        except Exception as e:
            logger.exception(f"Failed to resize image for product {self.id}")

    def avg_rating(self):
        if self.reviews.exists():
            return self.reviews.aggregate(models.Avg('rating'))['rating__avg']
        return None

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart for {self.user.username}"

    def update_quantity(self, product_id, new_quantity):
        cart_item = self.cartitem_set.get(product_id=product_id)
        cart_item.quantity = new_quantity
        cart_item.save()


@receiver(post_save, sender=User)
def create_or_update_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)
    else:
        instance.cart.save()


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, default=None)

    def total_price(self):
        return self.product.price * self.quantity



class ProductComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()

    def __str__(self):
        return self.user.username


class ProductOrder(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    string = models.TextField()

    def __str__(self):
        return f"Order ID: {self.order_id}, Customer: {self.customer}"


class Review(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='reviews', default=None)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    reviewed_product = models.ForeignKey(
        Product,
        related_name='reviews',
        on_delete=models.CASCADE,
        default=5  # Default value for reviewed_product
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=5  # Default value for user
    )
    rating = models.PositiveIntegerField(
        choices=((1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')),
        default=5
    )
    comment = models.TextField(default="Default Comment")
    date_posted = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.order:  # Check if the order instance is not provided
            # Set the default ProductOrder instance for reviews, assuming you have one with id=1
            self.order = Order.objects.get(pk=1)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Review by {self.user.username} for {self.reviewed_product.name}"


class Status(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    STATUS_CHOICES = (
        ('Paid-Waiting', 'Paid-Waiting'),
        ('Approved', 'Approved'),
        ('OnDelivery', 'On Delivery'),
    )

    status_type = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Paid-Waiting')

    def __str__(self):
        return self.status_type


class Order(models.Model):
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None)
    products = models.ManyToManyField(Product)  # This line associates products with the order
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Order ID: {self.id} - Customer: {self.customer.user.username}"


class User_login(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    product_id = models.IntegerField()

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city_town = models.CharField(max_length=100, blank=True)
    home_address = models.CharField(max_length=255, blank=True)
    img = models.ImageField(upload_to='profile_pics', default='default.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.product.name}"


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=50)

    def __str__(self):
        return f"Billing Address for {self.user.username}"
