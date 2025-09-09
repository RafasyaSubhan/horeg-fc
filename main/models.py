from django.db import models

class News(models.Model):
    CATEGORY_CHOICES = [
        ('jersey', 'Jersey'),
        ('shoes', 'Footbal Shoes'),
        ('ball', 'Ball'),
        ('photocard', 'Photocard'),
        ('accessories', 'Accessories')
    ]

    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='update')
    is_featured = models.BooleanField(default=False)
    rating = models.FloatField(default=0)
    visitor = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name
    
    @property
    def is_viral(self):
        return self.rating > 3
        
    def total_visitor(self):
        self.visitor += 1
        self.save()