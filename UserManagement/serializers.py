from rest_framework import serializers
from .models import UserProfile, MembershipStatus
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = '__all__'

class MembershipStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipStatus
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    full_name = serializers.CharField()
    phone_number = serializers.CharField()
    address = serializers.CharField()
    date_of_birth = serializers.DateField()
    profile_picture = serializers.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'full_name', 
                 'phone_number', 'address', 'date_of_birth', 'profile_picture']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords must match")
        return data

    def create(self, validated_data):
        # Extract profile data
        profile_data = {
            'full_name': validated_data.pop('full_name'),
            'phone_number': validated_data.pop('phone_number'),
            'address': validated_data.pop('address'),
            'date_of_birth': validated_data.pop('date_of_birth')
        }
        
        if 'profile_picture' in validated_data:
            profile_data['profile_picture'] = validated_data.pop('profile_picture')
            
        # Remove password2 from validated_data
        validated_data.pop('password2')
        
        # Create user
        password = validated_data.pop('password')
        user = User.objects.create_user(
            **validated_data,
            password=password
        )
        
        # Create user profile
        UserProfile.objects.create(
            user=user,
            **profile_data
        )
        
        return user



class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()