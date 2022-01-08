from re import S
from django.http import request
from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.fields import set_value
from rest_framework.permissions import AllowAny
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from .import serializers
from .models import Poll, Question, CustomPoll, RespondentAnswer
import datetime
from rest_framework.status import(
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR
)


class PollsList(generics.ListAPIView):
    '''List of polls'''
    permission_classes = ([AllowAny])
    queryset = Poll.objects.all().filter(finish_date__gt=datetime.date.today()).order_by('start_date')
    serializer_class = serializers.PollsSerializer


class QuestionsList(generics.RetrieveAPIView):
    '''List of questions of poll'''
    
    queryset = Poll.objects.all()
    serializer_class = serializers.PollSerializer


class TakePoll(generics.ListAPIView):
    '''Gets data form user and takes poll'''

    def post(self, request):
        custom_poll = request.data.get('custom_poll')
        poll_pk = custom_poll['poll']
        polls = Poll.objects.filter(pk=poll_pk) 
        if len(polls) == 0:
            return Response({'status': 'error',
                            'response': 'You choose non-existent poll'},
                            status=HTTP_404_NOT_FOUND)
        user_id = custom_poll['user_id']
        if len(CustomPoll.objects.filter(poll=poll_pk, user_id=user_id)) != 0:
            return Response({'status': 'error',
                            'response': 'You\'ve alredy taken this poll'},
                            status=HTTP_400_BAD_REQUEST) 
        serializer = serializers.TakePollSerializer(data=custom_poll)
        if serializer.is_valid():
            serializer.save()
            custom_poll_id = CustomPoll.objects.get(poll=poll_pk, user_id=user_id).pk
            answers = custom_poll.get('answers', None)
            if answers is None:
                return Response({'status': 'error',
                                'response': 'Where are your answers, man?'},
                                status=HTTP_400_BAD_REQUEST)
            for answer in answers:
                answer_dic = {}
                answer_dic['custom_poll_id'] = custom_poll_id
                answer_dic['question'] = answer
                answer_dic['text'] = answers[answer]
                ans_serializer = serializers.AnswersSerializer(data=answer_dic)
                if ans_serializer.is_valid():
                    ans_serializer.save()
                else:
                    return Response({'status': 'error',
                                    'response': 'Something goes wrong while parcing your answers :('},
                                    status=HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'error',
                            'response': 'Something goes wrong while pircing your poll :('},
                            status=HTTP_400_BAD_REQUEST)
            
        poll_name = polls[0].name
        return Response({'status': f'You\'ve taken the pole \'{poll_name}\'.'},
                        status=HTTP_200_OK)

            
class GetPolls(generics.ListAPIView):
    '''All polls of chosen user'''
       
    def get(self, request, user_id):
        polls = CustomPoll.objects.filter(user_id=user_id)
        if len(polls) == 0:
            return Response({'status': 'no polls',
                            'response': 'You haven\'t takend any polls.'},
                            status=HTTP_200_OK)
        
        polls_dic = {}
        polls_dic['polls'] = []
        for poll in polls:
            one_more_poll = {}
            one_more_poll['poll_name'] = poll.poll.name
            polls_dic['polls'].append(one_more_poll)
            one_more_poll['answers'] = []
            answers = RespondentAnswer.objects.filter(custom_poll_id=poll.pk)
            for answer in answers:
                answer_dic = {answer.question.text: answer.text}
                one_more_poll['answers'].append(answer_dic)
            
        serializer = serializers.CustomPollsSerializer(data=polls_dic)
        if serializer.is_valid():
            print(serializer.data)
            return Response({'status': 'success',
                            'data': serializer.data},
                            status=HTTP_200_OK)
        else:
            return Response({'status': 'error',
                            'response': 'Something goes wrong while seeking your polls data in db :('},
                            status=HTTP_500_INTERNAL_SERVER_ERROR)