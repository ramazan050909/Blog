from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class AbstractModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey('article.Article', on_delete=models.CASCADE)
    
    
    
    class Meta:
        abstract = True


class Comment(AbstractModel):
    text = models.TextField()
    created_at = models.DateField(auto_now_add=True)


    def __str__(self) -> str:
        return f'Comment {self.id} from {self.user.username}'
    
    class Meta:
        default_related_name = 'comments'
    
class RatingChoices(models.IntegerChoices):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class Rating(AbstractModel):
    rate = models.PositiveIntegerField(choices=RatingChoices.choices)


    def __str__(self) -> str:
        return str(self.rate)
    
    class Meta:
        default_related_name = 'ratings'
        unique_together = ('user', 'article')
    

class Favorite(AbstractModel):
    pass

    class Meta:
        default_related_name = 'favorites'
        unique_together = ('user', 'article')

