from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="MenuCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveSmallIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
                ("name", models.CharField(max_length=50)),
                ("slug", models.SlugField(max_length=50, unique=True)),
            ],
            options={"verbose_name": "Menu category", "verbose_name_plural": "Menu categories", "db_table": "menu_categories", "ordering": ("order", "id")},
        ),
        migrations.CreateModel(
            name="PrivateEvent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveSmallIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
                ("title", models.CharField(max_length=120)),
                ("subtitle", models.CharField(blank=True, max_length=255)),
                ("text", models.TextField(blank=True)),
                ("image", models.CharField(max_length=255)),
                ("position", models.CharField(choices=[("left", "Left card"), ("right", "Right card")], max_length=10)),
            ],
            options={"verbose_name": "Private event", "verbose_name_plural": "Private events", "db_table": "private_events", "ordering": ("order", "id")},
        ),
        migrations.CreateModel(
            name="Speciality",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveSmallIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
                ("title", models.CharField(max_length=120)),
                ("subtitle", models.TextField()),
                ("text", models.TextField()),
                ("image", models.CharField(max_length=255)),
            ],
            options={"verbose_name": "Speciality", "verbose_name_plural": "Specialities", "db_table": "specialities", "ordering": ("order", "id")},
        ),
        migrations.CreateModel(
            name="StaticSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveSmallIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
                ("slug", models.SlugField(choices=[("about", "About Us"), ("team", "Our Team")], max_length=30, unique=True)),
                ("title", models.CharField(max_length=120)),
                ("subtitle", models.TextField()),
                ("text", models.TextField()),
                ("image", models.CharField(max_length=255)),
            ],
            options={"verbose_name": "Static section", "verbose_name_plural": "Static sections", "db_table": "static_sections", "ordering": ("order", "id")},
        ),
        migrations.CreateModel(
            name="Booking",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=30)),
                ("people", models.PositiveSmallIntegerField()),
                ("date", models.DateField()),
                ("time", models.TimeField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="bookings", to=settings.AUTH_USER_MODEL)),
            ],
            options={"db_table": "bookings", "ordering": ("-created_at",)},
        ),
        migrations.CreateModel(
            name="ContactMessage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(blank=True, max_length=30)),
                ("message", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="contact_messages", to=settings.AUTH_USER_MODEL)),
            ],
            options={"db_table": "contact_messages", "ordering": ("-created_at",)},
        ),
        migrations.CreateModel(
            name="MenuItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveSmallIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
                ("title", models.CharField(max_length=120)),
                ("subtitle", models.CharField(max_length=255)),
                ("price", models.DecimalField(decimal_places=2, max_digits=8)),
                ("on_main", models.BooleanField(default=True)),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="items", to="main.menucategory")),
            ],
            options={"verbose_name": "Menu item", "verbose_name_plural": "Menu items", "db_table": "menu_items", "ordering": ("order", "id")},
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=150)),
                ("phone", models.CharField(max_length=30)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="profile", to=settings.AUTH_USER_MODEL)),
            ],
            options={"db_table": "user_profiles"},
        ),
    ]
