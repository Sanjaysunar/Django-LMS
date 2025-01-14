from rest_framework import serializers
from userauths.models import Profile, User

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'