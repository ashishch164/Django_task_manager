from rest_framework import serializers
from .models import Task, User, UserTask

class UserSerializer(serializers.ModelSerializer):
    role_name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = '__all__'

    def get_role_name(self, obj):
        return "admin" if obj.role == 0 else "normal_user"

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class UserTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTask
        fields = '__all__'

