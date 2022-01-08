from rest_framework import serializers
from .import models


class PollsSerializer(serializers.ModelSerializer):
    '''Serializer for poll'''
    class Meta:
        model = models.Poll
        fields = '__all__'


class PollSerializer(serializers.Serializer):
    '''Serializer of questions for specific serializer'''
    poll_id = serializers.SerializerMethodField('get_id')
    questions = serializers.DictField(source='get_questions')

    def get_id(self, obj):
        return obj.id


class TakePollSerializer(serializers.ModelSerializer):
    '''Serializer for taking poll'''
    class Meta:
        model = models.CustomPoll
        fields = ['poll', 'user_id']

    def create(self, validated_data):
        return models.CustomPoll.objects.create(**validated_data)


class AnswersSerializer(serializers.ModelSerializer):
    '''Serializer for respondents' answers'''
    class Meta:
        model = models.RespondentAnswer
        fields = ['custom_poll_id', 'question', 'text']

    def create(self, validated_data):
        return models.RespondentAnswer.objects.create(**validated_data)


class CustomPollsSerializer(serializers.Serializer):
    '''Serializer for all polls of user'''

    # poll = serializers.CharField()
    # answers = serializers.ListField()
    polls = serializers.ListField()
