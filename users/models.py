from django.db import models

from django.contrib.auth.models import User

from PIL import Image
# Create your models here.



class Profile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	image = models.ImageField(default = 'default.jpg', upload_to = 'profile_picture')


	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)					#save method is there in parent class Model 
														#but to resize large images we have to resize them, 
														#so we have created our own save function, ]
														#it uses the super to use the save of parent class then resize it using pillow
		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)

