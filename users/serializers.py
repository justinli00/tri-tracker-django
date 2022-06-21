from rest_framework import serializers
from users.models import NewUser

class RegisterUserSerializer(serializers.ModelSerializer):
    
    #variables
    email = serializers.EmailField(required=True)
    user_name = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)
    
    #defines required fields
    class Meta:
        model = NewUser
        fields = ('email', 'user_name', 'password')
        extra_kwargs = {'password': {'write_only':True}} #do not allow password to be read
    
    def create(self, validated_data):
        print(validated_data)
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ('id', 'email', 'user_name', 'first_name', 'start_date',
                  'about', 'is_staff', 'is_active',)