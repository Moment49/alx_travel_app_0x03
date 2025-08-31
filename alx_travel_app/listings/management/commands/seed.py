from django.core.management.base import BaseCommand, CommandError
from listings.models import Listing
from django.contrib.auth.models import User
import random, string


class Command(BaseCommand):
    help = "Seeds the database with initial data"

    # Add positional arguments if needed to create the data
    def add_arguments(self, parser):
        parser.add_argument(
            "count", 
            nargs="+", 
            type=int,
            help="Number of sample listings, booking and users to create")
    
    def handle(self, *args, **options):
        # First create the users randomly
        # convert the count to a pure interger from list
        count = options['count']
       
        counter = int(''.join(map(str, count)))
        print(counter)
    
        created = 0
        users = {
            "username" : ["dev_moment", "kevin_dev", 'matt_gibbs'],
            "email" : ["dev@gmail.com", "kev@ymail.com", 'matt@yhaoo.com'],
            "first_name" :["Elvis", "Kelvin", 'Matthew'],
            "last_name" : ["Ibenacho", 'James', 'Tim'],
            "password" : ["dev@moment", "dev@kevin", 'dev@matt']
        }
            # Create the Listings
        listing_names = [
                    "Sunny 2-Bedroom Apartment",
                    "Cozy Downtown Studio",
                    "Luxury Beachside Villa"]
        descriptions = [
            "A bright and spacious apartment with modern decor and natural lighting. Perfect for small families.",
            "A compact yet stylish studio in the heart of downtown. Ideal for solo travelers or remote workers.",
            "A premium villa with ocean views, private pool, and 5-star amenities. Great for vacations and events."
        ]

        addresses = [
            "14 Maple Avenue, Lagos, Nigeria",
            "221B Herbert Macaulay Way, Abuja, Nigeria",
            "5 Paradise Island Road, Lekki, Lagos"
        ]

        prices = [
            450.00,   # in Dollars per night
            300.00,
            1500.00
        ]
        while created < counter:
            username = f"{random.choice(users['username'])}{random.randint(1, 10000)}"
            email = random.choice(users['email'])
            # split the email to make it unique as well
            email_parts = email.split("@")
            user_email_part = email_parts[0]
            user_domain_part = email_parts[1]
            email = f"{user_email_part}{random.randint(1, 10000)}@{user_domain_part}"
            first_name = f"{random.choice(users['first_name'])}"
            last_name = f"{random.choice(users['last_name'])}{random.randint(1, 10000)}"
            password = f"{random.choice(users['password'])}{random.randint(1, 10000)}"

            # Create the user
            
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                self.stdout.write(self.style.WARNING(f"Duplicate found: {username} or {email}. Retrying..."))
                continue

            # Create the user data
            user = User.objects.create(username=username, 
                                first_name=first_name, 
                                last_name=last_name,
                                email=email)
            # This is to set and ensure that password is hashed before saving to db
            user.set_password(password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created the following users: {username}')
            )

            # Make the listing names unique to aviod duplication
            listing_name =f"{random.choice(listing_names)}_{random.randint(1,1000)}"
            
            listing_desctiptiom = random.choice(descriptions)
            listing_address = random.choice(addresses)
            listing_pricepernight = random.choice(prices)
            
            # Check lisiting exisit if so to aviod duplication   
            if Listing.objects.filter(name=listing_name).exists():
                self.stdout(
                    self.style.WARNING(f"The listing with name already exists:{listing_name}")
                )
                continue

            # Create the listing if it does not exists
            Listing.objects.create(host=user, 
                                name=listing_name,
                                description=listing_desctiptiom,
                                address=listing_address,
                                pricepernight=listing_pricepernight)
            self.stdout.write(
                self.style.SUCCESS(f"Successfully created the following Listings: {listing_name}")
            )
            
            # Increment the counter
            created += 1
    