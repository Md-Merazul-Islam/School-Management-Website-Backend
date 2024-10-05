from rest_framework import serializers
from .models import Student, Teacher, Class, Subject,Notice, Review
from activites.models import Mark
from activites.serializers import  MarkSerializer
from rest_framework.exceptions import ValidationError

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    # class_name = serializers.StringRelatedField()
    marksheet = serializers.SerializerMethodField()
    class Meta:
        model = Student
        fields = [
           'id' ,'roll_no', 'username', 'first_name', 'last_name', 'email',
            'phone_number', 'address', 'photo', 'class_name', 'marksheet'
        ]

    def get_marksheet(self, obj):
        marks = Mark.objects.filter(student=obj)
        return MarkSerializer(marks, many=True).data
    def update(self, instance, validated_data):
        
        photo = validated_data.get('photo', None)
        if photo is None:
            validated_data.pop('photo', None)

        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()
        return instance
    
    
class StudentSerializerForList(serializers.ModelSerializer):
    class_name = serializers.StringRelatedField()
    marksheet = serializers.SerializerMethodField()
    class Meta:
        model = Student
        fields = [
           'id' ,'roll_no', 'username', 'first_name', 'last_name', 'email',
            'phone_number', 'address', 'photo', 'class_name', 'marksheet'
        ]

    def get_marksheet(self, obj):
        marks = Mark.objects.filter(student=obj)
        return MarkSerializer(marks, many=True).data
    def update(self, instance, validated_data):

        photo = validated_data.get('photo', None)
        if photo is None:
            validated_data.pop('photo', None)

        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()
        return instance

class TeacherSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)  
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), write_only=True)

    class Meta:
        model = Teacher
        fields = ['id', 'employee_id', 'first_name', 'last_name', 'email', 'subject_name', 'subject', 'photo']

    def update(self, instance, validated_data):
        photo = validated_data.get('photo', None)
        if photo is None:
            validated_data.pop('photo', None)
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance


        
class SubjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Subject
        fields = ['id','name','slug','code','description','photo']




class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['id', 'title', 'description', 'file', 'created_at']

    def validate_file(self, value):
        """Ensure only PDF and image files are allowed."""
        if value and not value.name.endswith(('.pdf', '.png', '.jpg', '.jpeg')):
            raise serializers.ValidationError("Only PDF and image files are allowed.")
        return value

    def update(self, instance, validated_data):
        """Update only provided fields and ensure file is not reset to null."""
        file = validated_data.pop('file', None)

        # Update other fields
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)

        # Only update the file if a new file is provided
        if file is not None:
            instance.file = file
        
        # Save the updated instance
        instance.save()
        return instance




from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['author']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author'] = request.user
        return super().create(validated_data)