from rest_framework import serializers
from .models import FlagRequest, Userprofile, Chat, Message, VerificationStatus, VerificationRq,  SteezeLikes, SteezeCom, Steeze, RelationRq,  OrganizersRq, OrgStatus, Flags, Event

class UserRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userprofile
        fields = ['phone']

    def create(self, validated_data):
        return Userprofile.objects.create(**validated_data)

class UserUpdateLogsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Userprofile
        fields = ['username', 'password']

    def update(self, instance, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')

        user = Userprofile(username=username)
        user.set_password(password)
        user.save()

        instance.user = user
        instance.save()
        return super().update(instance, validated_data)



class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class FlagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flags
        fields = '__all__'

class FlagRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlagRequest
        fields = '__all__'


class OrgStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgStatus
        fields = '__all__'

class OrganizersRqSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizersRq
        fields = '__all__'

class RelationRqSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelationRq
        fields = '__all__'

class SteezeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Steeze
        fields = '__all__'

class SteezeComSerializer(serializers.ModelSerializer):
    class Meta:
        model = SteezeCom
        fields = '__all__'

class SteezeLikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SteezeLikes
        fields = '__all__'

class VerificationRqSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationRq
        fields = '__all__'

class VerificationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationStatus
        fields = '__all__'