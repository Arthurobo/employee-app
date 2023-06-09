from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from .models import Account, Profile
from rest_framework import serializers
from accounts.models import Account


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """
    class Meta:
        model = Account
        fields = ('pk', 'username', 'email', 'first_name', 'last_name',)
        read_only_fields = ('email', )


# My Own Custom registration
class RegistrationSerializer(serializers.ModelSerializer):

	password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

	class Meta:
		model = Account
		fields = ['email', 'username', 'password', 'password2', 'first_name', 'last_name']
		extra_kwargs = {
				'password': {'write_only': True},
		}	

	def	save(self):
		account = Account(
					email=self.validated_data['email'],
					username=self.validated_data['username'],
                    first_name = self.validated_data['first_name'],
                    last_name = self.validated_data['last_name'],
				)
		password = self.validated_data['password']
		password2 = self.validated_data['password2']
		if password != password2:
			raise serializers.ValidationError({'password': 'Passwords must match.'})
		account.set_password(password)
		account.save()
		return account