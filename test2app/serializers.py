from rest_framework import serializers
from .models import *
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


# Serializers for Thoughts

class ThCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ThComment
        fields = ['id', 'user', 'text', 'created_at']

class ThoughtsSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    comments = ThCommentSerializer(many=True, read_only=True)
    shares_count = serializers.IntegerField(source='shares.count', read_only=True)
    reposts_count = serializers.IntegerField(source='reposts.count', read_only=True)

    class Meta:
        model = Thoughts
        fields = ['id', 'user', 'content', 'video_url', 'created_at', 'likes_count', 'comments', 'shares_count', 'reposts_count']

class ThLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThLike
        fields = ['id', 'user', 'post', 'created_at']

class ThCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThComment
        fields = ['id', 'text']

class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThShare
        fields = ['id', 'user', 'post', 'created_at']

class RepostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThRepost
        fields = ['id', 'user', 'original_post', 'reposted_at']