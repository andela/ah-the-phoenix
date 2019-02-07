from rest_framework import serializers

from .models import Profile


class ProfilesSerializer(serializers.ModelSerializer):

    """Serialize user profile data"""

    username = serializers.CharField(source="user.username", read_only=True)
    bio = serializers.CharField(allow_blank=True, required=False)
    image = serializers.ImageField(default=None)

    class Meta:
        model = Profile
        fields = ['username', 'bio', 'image','created_at', 'updated_at']
        read_only_fields = ('username','created_at', 'updated_at',)