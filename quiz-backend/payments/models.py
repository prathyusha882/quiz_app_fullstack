from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]

    PAYMENT_TYPE_CHOICES = [
        ('course_purchase', 'Course Purchase'),
        ('subscription', 'Subscription'),
        ('certificate', 'Certificate'),
        ('donation', 'Donation'),
    ]

    # Payment details
    payment_id = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    
    # Amount and currency
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Payment information
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # External payment provider
    provider = models.CharField(max_length=50, default='stripe')  # stripe, paypal, etc.
    provider_payment_id = models.CharField(max_length=255, blank=True)
    provider_refund_id = models.CharField(max_length=255, blank=True)
    
    # Related objects
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, null=True, blank=True, related_name='payments')
    
    # Metadata
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    # Timing
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    refunded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment {self.payment_id} - {self.user.username} - {self.amount} {self.currency}"

    def save(self, *args, **kwargs):
        if not self.total_amount:
            self.total_amount = self.amount + self.tax_amount
        super().save(*args, **kwargs)

    def process_payment(self):
        """Mark payment as processed"""
        self.status = 'completed'
        self.processed_at = timezone.now()
        self.save()

    def refund_payment(self):
        """Mark payment as refunded"""
        self.status = 'refunded'
        self.refunded_at = timezone.now()
        self.save() 