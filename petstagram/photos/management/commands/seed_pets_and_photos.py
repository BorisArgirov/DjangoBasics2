from datetime import date

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from pets.models import Pet
from photos.models import Photo


# Reuse the bundled images so the sample data works without downloads.
SAMPLES = [
    ("Buddy", "2021-04-12", "dog-on-road.jpg", "Borisova Garden, Sofia", "Buddy pauses on the path during his morning walk."),
    ("Luna", "2022-07-03", "dog-on-bed.jpg", "Lozenets, Sofia", "Luna claims the softest spot on the bed for an afternoon nap."),
    ("Max", "2020-11-18", "dog-on-road.jpg", "South Park, Sofia", "Max enjoys a quiet stroll after practicing his recall."),
    ("Daisy", "2023-02-14", "dog-on-bed.jpg", "Kapana, Plovdiv", "Daisy settles down at home after a busy day of play."),
    ("Charlie", "2021-09-25", "dog-on-road.jpg", "Sea Garden, Varna", "Charlie stops to investigate a new scent along the walking path."),
    ("Rosie", "2022-05-09", "dog-on-bed.jpg", "Lazur, Burgas", "Rosie takes a well-earned rest after her evening walk."),
    ("Cooper", "2019-08-30", "dog-on-road.jpg", "Rowing Canal, Plovdiv", "Cooper explores the path on a relaxed weekend outing."),
    ("Milo", "2023-06-21", "axolotl.jpeg", "Mladost, Sofia", "Milo the axolotl rests in his freshwater aquarium."),
    ("Pearl", "2022-12-05", "axolotl.jpeg", "Trakia, Plovdiv", "Pearl the axolotl poses for a close-up during the daily tank check."),
    ("Sunny", "2024-01-16", "axolotl.jpeg", "Centre, Ruse", "Sunny the axolotl enjoys a peaceful afternoon in the aquarium."),
]


class Command(BaseCommand):
    help = "Add 10 sample pets and tagged photos; safe to run repeatedly."

    @transaction.atomic
    def handle(self, *args, **options):
        pets_created = photos_created = 0
        for name, birthday, filename, location, description in SAMPLES:
            image_path = f"static/images/{filename}"
            if not (settings.BASE_DIR / image_path).is_file():
                raise CommandError(f"Missing sample image: {image_path}")

            pet, created = Pet.objects.get_or_create(
                name=name,
                date_of_birth=date.fromisoformat(birthday),
                defaults={"personal_photo": f"http://127.0.0.1:8000/{image_path}"},
            )
            if created:
                # Pet.save() needs the assigned primary key to form its slug.
                pet.save(update_fields=["slug"])
            pets_created += created

            photo, created = Photo.objects.get_or_create(
                description=description,
                location=location,
                defaults={"photo": image_path},
            )
            photo.tag_pets.add(pet)
            photos_created += created

        self.stdout.write(self.style.SUCCESS(
            f"Created {pets_created} pets and {photos_created} photos. "
            f"Totals: {Pet.objects.count()} pets, {Photo.objects.count()} photos."
        ))
