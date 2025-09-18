import os
from django.core.management.base import BaseCommand
from django.core.files import File
from movie.models import Movie

class Command(BaseCommand):
    help = "Update movie images from media/movie/images folder by matching filenames with movie titles (m_TITLE.png format)"

    def handle(self, *args, **kwargs):
        # 📂 Carpeta donde ya están las imágenes generadas
        images_folder = "media/movie/images"

        if not os.path.exists(images_folder):
            self.stderr.write(f"Folder '{images_folder}' not found.")
            return

        updated_count = 0

        for filename in os.listdir(images_folder):
            if not filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                continue

            # 🔄 Quitar prefijo `m_` y extensión
            name, _ = os.path.splitext(filename)   # -> "m_Inception"
            if name.startswith("m_"):
                movie_title = name[2:]  # quita "m_" → "Inception"
            else:
                movie_title = name

            try:
                # buscar ignorando mayúsculas/minúsculas
                movie = Movie.objects.get(title__iexact=movie_title)

                image_path = os.path.join(images_folder, filename)
                with open(image_path, "rb") as img_file:
                    movie.image.save(filename, File(img_file), save=True)

                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f"Updated image for: {movie_title}"))

            except Movie.DoesNotExist:
                self.stderr.write(f"Movie not found: {movie_title}")
            except Exception as e:
                self.stderr.write(f"Failed to update {movie_title}: {str(e)}")

        self.stdout.write(self.style.SUCCESS(f"Finished updating {updated_count} movies with images."))