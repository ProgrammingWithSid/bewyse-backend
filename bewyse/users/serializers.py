from rest_framework import serializers
from .models import CustomUser

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff')


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True, error_messages={
        'required': 'Username is required.',
        'max_length': 'Username must be at most 100 characters.',
    })
    email = serializers.EmailField(required=True, error_messages={
        'required': 'Email is required.',
        'invalid': 'Enter a valid email address.',
    })
    password = serializers.CharField(min_length=8, required=True, error_messages={
        'required': 'Password is required.',
        'min_length': 'Password must be at least 8 characters long.',
    })
    first_name = serializers.CharField(max_length=100, required=True, error_messages={
        'max_length': 'First name must be at most 100 characters.',
    })
    last_name = serializers.CharField(max_length=100, required=True, error_messages={
        'max_length': 'Last name must be at most 100 characters.',
    })



class EditProfileSerializer(serializers.ModelSerializer):
    # Fields for editing the user profile
    username = serializers.CharField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name']

    def update(self, instance, validated_data):
        # Update user profile fields if they are provided in the request
        if 'username' in validated_data:
            instance.username = validated_data['username']
        if 'first_name' in validated_data:
            instance.first_name = validated_data['first_name']
        if 'last_name' in validated_data:
            instance.last_name = validated_data['last_name']

        # Save the changes to the user profile
        instance.save()
        return instance
    

class ViewProfile(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class UserProfileEditSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        # Update the user instance with validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance