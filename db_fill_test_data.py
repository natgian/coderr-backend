from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token

from offers_app.models import Offer, OfferDetail
from profiles_app.models import Profile

User = get_user_model()

print("Cleaning up old test data...")
Offer.objects.all().delete()
Profile.objects.all().delete()
User.objects.filter(username__in=["customerUser", "businessUser", "businessUser2", "emptyProfileUser"]).delete()

print("Creating users, tokens and profiles...")
# Create users
customer_user = User.objects.create_user(username="customerUser", email="customer@mail.com", password="customerPassword", type="customer")
business_user = User.objects.create_user(username="businessUser", email="business@mail.com", password="businessPassword", type="business")
business_user2 = User.objects.create_user(username="businessUser2", email="business2@mail.com", password="business2Password", type="business")
empty_user = User.objects.create_user(username="emptyProfileUser", email="emptyProfle@mail.com", password="emptyProfilePassword", type="customer")

# Create tokens
token_customer = Token.objects.create(user=customer_user)
token_business = Token.objects.create(user=business_user)
token_business2 = Token.objects.create(user=business_user2)
token_empty = Token.objects.create(user=empty_user)

# Create profiles
Profile.objects.create(user=customer_user, first_name="Max", last_name="Muster", location="Zürich", tel="123456789")
Profile.objects.create(user=business_user, first_name="John", last_name="Carter", location="New York", tel="987654321")
Profile.objects.create(user=business_user2, first_name="Jane", last_name="Butler", location="San Francisco", tel="111154321")
Profile.objects.create(user=empty_user, first_name="", last_name="")

print("Creating offers and details...")

# Create offer & details
offer_web = Offer.objects.create(
    user=business_user,
    title="Webdesign & Entwicklung-Paket",
    description="Erstellung einer modernen, responsiven Website für Ihren digitalen Auftritt.",
)
OfferDetail.objects.create(
    offer=offer_web,
    title="Basic Web",
    revisions=2,
    delivery_time_in_days=10,
    price=450,
    features=["One-Page Website", "Responsives Design", "Kontaktformular"],
    offer_type="basic",
)
OfferDetail.objects.create(
    offer=offer_web,
    title="Standard Web",
    revisions=4,
    delivery_time_in_days=20,
    price=950,
    features=["Website mit bis zu 5 Unterseiten", "Responsives Design", "Kontaktformular", "Basis-SEO-Optimierung", "CMS-Einrichtung (WordPress)"],
    offer_type="standard",
)
OfferDetail.objects.create(
    offer=offer_web,
    title="Premium Web",
    revisions=8,
    delivery_time_in_days=30,
    price=2200,
    features=[
        "Website mit unbegrenzten Unterseiten",
        "Responsives Design",
        "Kontaktformular",
        "Erweiterte SEO-Optimierung",
        "CMS-Einrichtung (WordPress)",
        "Onlineshop-Integration",
        "1 Monat technischer Support",
    ],
    offer_type="premium",
)

offer_graphic = Offer.objects.create(
    user=business_user,
    title="Grafikdesign-Paket",
    description="Ein umfassendes Grafikdesign-Paket für Unternehmen.",
)
OfferDetail.objects.create(
    offer=offer_graphic,
    title="Basic Design",
    revisions=2,
    delivery_time_in_days=5,
    price=100,
    features=["Logo Design", "Visitenkarte"],
    offer_type="basic",
)
OfferDetail.objects.create(
    offer=offer_graphic,
    title="Standard Design",
    revisions=5,
    delivery_time_in_days=7,
    price=200,
    features=["Logo Design", "Visitenkarte", "Briefpapier"],
    offer_type="standard",
)
OfferDetail.objects.create(
    offer=offer_graphic,
    title="Premium Design",
    revisions=10,
    delivery_time_in_days=10,
    price=500,
    features=["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"],
    offer_type="premium",
)

offer_social = Offer.objects.create(
    user=business_user2,
    title="Social Media Marketing-Paket",
    description="Professionelle Betreuung und Content-Erstellung für Ihre Social-Media-Kanäle.",
)
OfferDetail.objects.create(
    offer=offer_social,
    title="Basic Social",
    revisions=1,
    delivery_time_in_days=7,
    price=150,
    features=["3 Post-Vorlagen", "Kanal-Optimierung"],
    offer_type="basic",
)
OfferDetail.objects.create(
    offer=offer_social,
    title="Standard Social",
    revisions=3,
    delivery_time_in_days=10,
    price=350,
    features=["6 Post-Vorlagen", "Kanal-Optimierung", "1 Video/Reel", "Hashtag-Analyse"],
    offer_type="standard",
)
OfferDetail.objects.create(
    offer=offer_social,
    title="Premium Social",
    revisions=5,
    delivery_time_in_days=14,
    price=750,
    features=["12 Post-Vorlagen", "Kanal-Optimierung", "3 Videos/Reels", "Hashtag-Analyse", "Redaktionsplan", "Monatliches Reporting"],
    offer_type="premium",
)

print("Database successfully populated with all test data.")
