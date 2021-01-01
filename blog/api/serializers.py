from rest_framework import serializers
from blog.models import Blog
from django.contrib.auth.models import User

class BlogSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField('get_username_from_author')


    class Meta:
        model = Blog
        fields = ['title','category','created_date','published_date','header_image','text','username']

    def get_username_from_author(self,blog):
        username = blog.author.username
        return username

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password','password2']
        extra_kwargs = {
                    'password':{'write_only':True}

        }

    def save(self):
        user = User(
                 email = self.validated_data['email'],
                 username = self.validated_data['username']

        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password':'Passwords must match'})
        user.set_password(password)
        user.save()
        return user
