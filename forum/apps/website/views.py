# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from django.http.response import HttpResponseRedirect
from rest_framework import serializers
from rest_framework.decorators import detail_route
from rest_framework.permissions import AllowAny
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from forum.apps.website.models import Topic, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class TopicSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = '__all__'


class TopicViewSet(ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = (AllowAny,)

    renderer_classes = (TemplateHTMLRenderer, JSONRenderer)

    def list(self, request, errors=None, **kwargs):
        queryset = Topic.objects.all()
        serializer = self.get_serializer(queryset, many=True)

        if request.accepted_renderer.format == 'html':
            context = {
                'topics': serializer.data,
                'validation_errors': errors,
                'serializer': self.serializer_class,
            }
            return Response(context, template_name='website/list.html')
        else:
            return Response(serializer.data)

    def retrieve(self, request, pk=None, errors=None, **kwargs):
        queryset = Topic.objects.all()
        topic = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(topic)

        if request.accepted_renderer.format == 'html':
            context = {
                'topic': serializer.data,
                'validation_errors': errors,
            }
            return Response(context, template_name='website/detail.html')
        else:
            return Response(serializer.data)

    def create(self, request, **kwargs):
        serializer = TopicSerializer(data=request.data)

        if serializer.is_valid():
            topic = serializer.save()
            return HttpResponseRedirect('/{}'.format(topic.pk))
        else:
            return self.list(request, errors=serializer.errors)

    @detail_route(methods=['post'])
    def post_comment(self, request, pk=None):
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return HttpResponseRedirect('/{}'.format(pk))
        else:
            return self.retrieve(request, pk, errors=serializer.errors)
