from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'
    
    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Task name cannot be empty or whitespace.")
        return value
    
    def validate_status(self, value):
        valid_statuses = ['running', 'completed', 'failed']
        if value not in valid_statuses:
            raise serializers.ValidationError(f"status must be one of {valid_statuses}")
        return value

    def validate(self, data):
        name = data.get('name')
        status = data.get('status', 'running')  #default status if not passed

        # check for tasks with same name that are not 'completed'
        existing_conflict = Task.objects.filter(name=name).exclude(status='completed')
        if self.instance:
            # If it is an update, exclude the current instance from conflict check
            existing_conflict = existing_conflict.exclude(id=self.instance.id)
        
        if existing_conflict.exists():
            raise serializers.ValidationError({'name' : 'A task with this name already exists and is not completed'})
        
        return data