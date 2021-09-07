from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=360)


class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.PositiveIntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(5)] #1-5 stars
    )

    class Meta:
        unique_together = (('user','movie'),)
        index_together = (('user', 'movie'),) # OGNI RATING HA UN SOLO USER PER OGNI FILM.
        # ( per ogni film, uno user può solo creare un voto)