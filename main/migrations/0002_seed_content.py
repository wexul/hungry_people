from django.db import migrations


SECTIONS = [
    {
        "slug": "about",
        "title": "About Us",
        "subtitle": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis at velit maximus, molestie est a, tempor magna.",
        "text": "Integer ullamcorper neque eu purus euismod, ac faucibus mauris posuere. Morbi non ultrices ligula. Sed dictum, enim sed ullamcorper feugiat, dui odio vehicula eros, a sollicitudin lorem quam nec sem. Mauris tincidunt feugiat diam convallis pharetra. Nulla facilisis semper laoreet.",
        "image": "about-fire.png",
        "order": 1,
    },
    {
        "slug": "team",
        "title": "Master Chef",
        "subtitle": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis at velit maximus, molestie est a, tempor magna.",
        "text": "Integer ullamcorper neque eu purus euismod, ac faucibus mauris posuere. Morbi non ultrices ligula. Sed dictum, enim sed ullamcorper feugiat, dui odio vehicula eros, a sollicitudin lorem quam nec sem. Mauris tincidunt feugiat diam convallis pharetra. Nulla facilisis semper laoreet.",
        "image": "team-chef.png",
        "order": 2,
    },
]

SPECIALITIES = [
    {
        "title": "Chocolate Pancakes",
        "subtitle": "Chocolate pancakes with berry cream, crispy flakes and fresh seasonal fruit.",
        "text": "A bright dessert with rich chocolate notes and a soft, delicate texture. Fresh berries add a light sour accent, while crispy decoration gives the dish contrast and an elegant restaurant-style finish.",
        "image": "specialty-pancakes.png",
        "order": 1,
    },
    {
        "title": "Chocolate Cake",
        "subtitle": "Rich chocolate cake with smooth cream, deep cocoa flavour and elegant plating.",
        "text": "A classic dessert made for slow evenings and warm conversations. Deep cocoa flavour, soft layers and gentle cream create a balanced taste that feels rich, refined and not too sweet.",
        "image": "specialty-chocolate.png",
        "order": 2,
    },
    {
        "title": "Grilled Salmon Fillet",
        "subtitle": "Tender grilled salmon with fresh herbs, light garnish and creamy sauce.",
        "text": "A refined main course with clean flavour and careful presentation. The salmon is cooked until tender, served with herbs, vegetables and a light sauce that keeps the dish fresh, elegant and balanced.",
        "image": "specialty-salmon.png",
        "order": 3,
    },
]

CATEGORIES = [
    ("Soupe", "soup"),
    ("Pizza", "pizza"),
    ("Pasta", "pasta"),
    ("Desert", "dessert"),
    ("Wine", "wine"),
    ("Beer", "beer"),
    ("Drinks", "drink"),
]

MENU_ITEMS = [
    ("soup", "Roasted Tomato Soup", "Slow-roasted tomatoes, basil oil and sourdough toast.", "18.40"),
    ("soup", "Wild Mushroom Cream", "Forest mushrooms, thyme cream and toasted seeds.", "21.90"),
    ("soup", "Seafood Bisque", "Shellfish stock, cream, herbs and garlic croutons.", "27.60"),
    ("pizza", "Pizza Quattro Stagioni", "Tomato, mozzarella, mushrooms, olives and artichokes.", "42.50"),
    ("pizza", "Prosciutto & Burrata", "Prosciutto, burrata, rocket and cherry tomatoes.", "46.80"),
    ("pizza", "Four Cheese Pizza", "Mozzarella, gorgonzola, parmesan and taleggio.", "39.90"),
    ("pasta", "Classic Carbonara", "Guanciale, egg yolk, pecorino and black pepper.", "31.40"),
    ("pasta", "Seafood Linguine", "Prawns, mussels, garlic, tomato and white wine.", "44.70"),
    ("pasta", "Truffle Tagliatelle", "Fresh pasta, truffle cream, parmesan and herbs.", "38.90"),
    ("dessert", "Chocolate Pancakes", "Berry cream, crisp flakes and seasonal fruit.", "19.80"),
    ("dessert", "Vanilla Berry Souffle", "Vanilla cream, berries and caramelised almonds.", "23.60"),
    ("dessert", "Classic Tiramisu", "Mascarpone, espresso, cocoa and savoiardi biscuits.", "20.40"),
    ("wine", "Chianti Classico", "Dry red wine with cherry, herbs and gentle spice.", "36.00"),
    ("wine", "Pinot Grigio", "Fresh white wine with citrus and green apple notes.", "32.50"),
    ("wine", "Prosecco Brut", "Crisp sparkling wine with pear and floral aromas.", "34.80"),
    ("beer", "Craft Pale Ale", "Citrus hops, light caramel malt and a clean finish.", "9.50"),
    ("beer", "Belgian Wheat Beer", "Soft wheat beer with orange peel and coriander.", "10.20"),
    ("beer", "Dark Lager", "Roasted malt, cocoa notes and balanced bitterness.", "9.80"),
    ("drink", "Berry Lemonade", "Fresh berries, lemon, mint and sparkling water.", "8.90"),
    ("drink", "Citrus Garden", "Orange, grapefruit, rosemary and sparkling water.", "9.40"),
    ("drink", "Cold Brew Tonic", "Cold brew coffee, tonic water and orange zest.", "7.80"),
]

EVENTS = [
    {
        "title": "Weddings",
        "subtitle": "Private wedding celebrations",
        "text": "For private events please call or use the contact form.",
        "image": "event-wedding.png",
        "position": "left",
        "order": 1,
    },
    {
        "title": "Corporate Parties",
        "subtitle": "Corporate and business events",
        "text": "For private events please call or use the contact form.",
        "image": "event-corporate.png",
        "position": "right",
        "order": 2,
    },
]


def seed_content(apps, schema_editor):
    StaticSection = apps.get_model("main", "StaticSection")
    Speciality = apps.get_model("main", "Speciality")
    MenuCategory = apps.get_model("main", "MenuCategory")
    MenuItem = apps.get_model("main", "MenuItem")
    PrivateEvent = apps.get_model("main", "PrivateEvent")

    for section in SECTIONS:
        slug = section["slug"]
        defaults = {key: value for key, value in section.items() if key != "slug"}
        StaticSection.objects.update_or_create(slug=slug, defaults=defaults)

    for speciality in SPECIALITIES:
        title = speciality["title"]
        defaults = {key: value for key, value in speciality.items() if key != "title"}
        Speciality.objects.update_or_create(title=title, defaults=defaults)

    categories = {}
    for order, (name, slug) in enumerate(CATEGORIES, start=1):
        category, _ = MenuCategory.objects.update_or_create(
            slug=slug,
            defaults={"name": name, "order": order, "is_active": True},
        )
        categories[slug] = category

    for order, (category_slug, title, subtitle, price) in enumerate(MENU_ITEMS, start=1):
        MenuItem.objects.update_or_create(
            title=title,
            defaults={
                "category": categories[category_slug],
                "subtitle": subtitle,
                "price": price,
                "on_main": True,
                "is_active": True,
                "order": order,
            },
        )

    for event in EVENTS:
        title = event["title"]
        defaults = {key: value for key, value in event.items() if key != "title"}
        PrivateEvent.objects.update_or_create(title=title, defaults=defaults)


class Migration(migrations.Migration):
    dependencies = [("main", "0001_initial")]

    operations = [migrations.RunPython(seed_content, migrations.RunPython.noop)]
