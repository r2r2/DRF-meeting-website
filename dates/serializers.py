from rest_framework import serializers

from dates.models import User, Follower


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class ClientCreateSerializer(serializers.ModelSerializer):
    """Client registration"""
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'gender', 'image', 'adress', 'location')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('location',)

    def create(self, validated_data):
        user = super().create(validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            user.save()
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)


class UserFollowerSerializer(serializers.ModelSerializer):
    """Serialization for matching users"""
    distance = serializers.DecimalField(source='distance.km',
                                        max_digits=10,
                                        decimal_places=2,
                                        required=False,
                                        read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'gender', 'image', 'adress', 'distance', 'location')
        read_only_fields = ('location',)


class ListFollowerSerializer(serializers.ModelSerializer):
    """List of my followers"""
    user_2 = UserFollowerSerializer()

    class Meta:
        model = Follower
        fields = ('user_2',)

