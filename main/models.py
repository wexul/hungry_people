from django.conf import settings
from django.db import models


class OrderedActiveModel(models.Model):
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ("order", "id")


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30)

    class Meta:
        db_table = "user_profiles"

    def __str__(self):
        return self.full_name or self.user.email


class StaticSection(OrderedActiveModel):
    ABOUT = "about"
    TEAM = "team"
    SECTION_CHOICES = (
        (ABOUT, "About Us"),
        (TEAM, "Our Team"),
    )

    slug = models.SlugField(max_length=30, choices=SECTION_CHOICES, unique=True)
    title = models.CharField(max_length=120)
    subtitle = models.TextField()
    text = models.TextField()
    image = models.CharField(max_length=255)

    class Meta(OrderedActiveModel.Meta):
        db_table = "static_sections"
        verbose_name = "Static section"
        verbose_name_plural = "Static sections"

    def __str__(self):
        return self.title


class Speciality(OrderedActiveModel):
    title = models.CharField(max_length=120)
    subtitle = models.TextField()
    text = models.TextField()
    image = models.CharField(max_length=255)

    class Meta(OrderedActiveModel.Meta):
        db_table = "specialities"
        verbose_name = "Speciality"
        verbose_name_plural = "Specialities"

    def __str__(self):
        return self.title


class MenuCategory(OrderedActiveModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta(OrderedActiveModel.Meta):
        db_table = "menu_categories"
        verbose_name = "Menu category"
        verbose_name_plural = "Menu categories"

    def __str__(self):
        return self.name


class MenuItem(OrderedActiveModel):
    category = models.ForeignKey(
        MenuCategory,
        on_delete=models.PROTECT,
        related_name="items",
    )
    title = models.CharField(max_length=120)
    subtitle = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    on_main = models.BooleanField(default=True)

    class Meta(OrderedActiveModel.Meta):
        db_table = "menu_items"
        verbose_name = "Menu item"
        verbose_name_plural = "Menu items"

    @property
    def price_display(self):
        return f"{self.price:.2f}".replace(".", ",")

    def __str__(self):
        return self.title


class PrivateEvent(OrderedActiveModel):
    LEFT = "left"
    RIGHT = "right"
    POSITION_CHOICES = (
        (LEFT, "Left card"),
        (RIGHT, "Right card"),
    )

    title = models.CharField(max_length=120)
    subtitle = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=True)
    image = models.CharField(max_length=255)
    position = models.CharField(max_length=10, choices=POSITION_CHOICES)

    class Meta(OrderedActiveModel.Meta):
        db_table = "private_events"
        verbose_name = "Private event"
        verbose_name_plural = "Private events"

    def __str__(self):
        return self.title


class Booking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings",
    )
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    people = models.PositiveSmallIntegerField()
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "bookings"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.name}: {self.date} {self.time:%H:%M}"


class ContactMessage(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contact_messages",
    )
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "contact_messages"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.name}: {self.created_at:%Y-%m-%d %H:%M}"
