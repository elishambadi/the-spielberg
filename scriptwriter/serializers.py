"""
Serializers for the scriptwriter app.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Character, Script, ScriptVersion, Scene, Job


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']


class CharacterSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Character
        fields = ['id', 'user', 'name', 'personality', 'goals', 'voice', 'backstory', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class SceneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scene
        fields = ['id', 'script_version', 'scene_number', 'setting', 'goal', 'tension', 'tone', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ScriptVersionSerializer(serializers.ModelSerializer):
    scenes = SceneSerializer(many=True, read_only=True)
    
    class Meta:
        model = ScriptVersion
        fields = ['id', 'script', 'version_number', 'content', 'notes', 'scenes', 'created_at']
        read_only_fields = ['id', 'created_at']


class ScriptSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    characters = CharacterSerializer(many=True, read_only=True)
    character_ids = serializers.PrimaryKeyRelatedField(
        many=True, 
        write_only=True, 
        queryset=Character.objects.all(),
        source='characters',
        required=False
    )
    versions = ScriptVersionSerializer(many=True, read_only=True)
    latest_version = serializers.SerializerMethodField()
    
    class Meta:
        model = Script
        fields = ['id', 'user', 'title', 'genre', 'tone', 'logline', 'characters', 'character_ids', 
                  'versions', 'latest_version', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_latest_version(self, obj):
        latest = obj.get_latest_version()
        if latest:
            return ScriptVersionSerializer(latest).data
        return None
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        characters = validated_data.pop('characters', [])
        script = Script.objects.create(**validated_data)
        script.characters.set(characters)
        return script
    
    def update(self, instance, validated_data):
        characters = validated_data.pop('characters', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if characters is not None:
            instance.characters.set(characters)
        
        return instance


class JobSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Job
        fields = ['id', 'user', 'job_id', 'job_type', 'status', 'prompt', 'script', 'scene', 
                  'result', 'error_message', 'is_continuation', 'parent_job', 'continuation_count',
                  'created_at', 'started_at', 'completed_at']
        read_only_fields = ['id', 'user', 'job_id', 'status', 'result', 'error_message', 
                            'is_continuation', 'parent_job', 'continuation_count',
                            'created_at', 'started_at', 'completed_at']


class JobCreateSerializer(serializers.Serializer):
    """Serializer for creating a new job"""
    prompt = serializers.CharField()
    job_type = serializers.ChoiceField(choices=Job.JOB_TYPE_CHOICES)
    script_id = serializers.IntegerField(required=False, allow_null=True)
    scene_id = serializers.IntegerField(required=False, allow_null=True)
    script_type = serializers.CharField(required=False, default='screenplay')


class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
