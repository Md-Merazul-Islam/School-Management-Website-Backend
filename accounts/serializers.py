from rest_framework import serializers
from .models import Profile, User

class ProfileSerializer(serializers.ModelSerializer):
    is_staff = serializers.BooleanField(source='user.is_staff', read_only=True)
    account_no = serializers.IntegerField(read_only=True)
    profile_image = serializers.ImageField(max_length=None, use_url=True, required=False)  

    class Meta:
        model = Profile
        fields = ['phone_number', 'address', 'date_of_birth', 'department', 'account_no', 'is_staff', 'profile_image']



class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'profile']  

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        if profile_data:
            profile = instance.profile
            profile.phone_number = profile_data.get('phone_number', profile.phone_number)
            profile.address = profile_data.get('address', profile.address)
            profile.date_of_birth = profile_data.get('date_of_birth', profile.date_of_birth)
            profile.department = profile_data.get('department', profile.department)
            profile.save()

        return instance
    
    
class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"error": "Passwords don't match."})
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': "Email already exists!"})

        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username': "Username already exists!"})

        return data

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])  
        user.is_active = False
        user.save()
        Profile.objects.create(
            user=user,
            phone_number=None,
            address=None,
            date_of_birth=None,
            department=None,
            account_no=int(user.id)+1000,
            profile_image=None
        )
        return user
    
    

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    
    
    
    from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class UserDetailSerializer(serializers.ModelSerializer):
    # Fields from the related Profile model
    phone_number = serializers.CharField(source='profile.phone_number', allow_null=True, required=False)
    address = serializers.CharField(source='profile.address', allow_null=True, required=False)
    date_of_birth = serializers.DateField(source='profile.date_of_birth', allow_null=True, required=False)
    department = serializers.CharField(source='profile.department', allow_null=True, required=False)
    
    # Fields from the related Account model
    account_no = serializers.IntegerField(source='profile.account_no', read_only=True)
    profile_image = serializers.ImageField(source='profile.profile_image', allow_null=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'date_of_birth', 'department', 'account_no', 'profile_image']

    def update(self, instance, validated_data):
        # Extract nested profile data
        profile_data = validated_data.pop('profile', None)

        # Update User fields
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        # Update Profile fields if data exists
        if profile_data:
            profile = instance.profile
            
            # Only update profile fields that are provided
            profile.phone_number = profile_data.get('phone_number', profile.phone_number)
            profile.address = profile_data.get('address', profile.address)
            profile.date_of_birth = profile_data.get('date_of_birth', profile.date_of_birth)
            profile.department = profile_data.get('department', profile.department)
            
            # Handle the 'profile_image' separately, ensuring it doesn't reset to null
            profile_image = profile_data.get('profile_image', None)
            if profile_image is not None:
                profile.profile_image = profile_image
            
            profile.save()

        return instance
