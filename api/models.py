from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg

User = get_user_model()

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=360)

    def no_of_ratings(self):
        ratings = Rating.objects.filter(movie=self)
        if ratings:
            return len(ratings)
        else:
            return 0

    def avg_rating(self):
        if self.no_of_ratings() > 0:
            result = Rating.objects.filter(movie=self).aggregate(rating_medio=Avg('stars'))
            return result['rating_medio']
        else:
            return 0


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