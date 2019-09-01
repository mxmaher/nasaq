from rest_framework import serializers

from todo.models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Simple Task model serializer, that implements 
    """
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'children',
            'state',
            'created_at',
        ]


class ChildTaskSerializer(serializers.Serializer):
    """
    Serializer used with the link action on StateFullTaskViewSet
    it takes an id and validates that it exists, returning a task instance
    in the validated_data.
    """
    
    child = serializers.IntegerField(required=True)

    def validate_child(self, value):
        """
        Make sure that the givin child's id has a crossponding object in
        the database and return it's instance in the validated_data.
        """
        try:
            task = Task.objects.get(pk=value)
        except Task.DoesNotExist:
            raise serializers.ValidationError("The task you're trying to link is not found.")
        return task