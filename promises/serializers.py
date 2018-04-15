from rest_framework import serializers
from promises.models import Promise
from django.contrib.auth.models import User
from django.db.models import Q

class PromiseSerializer(serializers.ModelSerializer):
  def validate(self, data):
    if data.get('sinceWhen') > data.get('tilWhen'):
      raise serializers.ValidationError('tilWhen should be later than sinceWhen')
    elif self.context.get('request').method == 'POST' and self.context.get('request').user == data.get('user2'):
      raise serializers.ValidationError('One should not promise to oneself')
    return data
        
  class Meta:
    model = Promise
    fields = ('id', 'created', 'sinceWhen', 'tilWhen', 'user1', 'user2')
    read_only_fields = ('user1',)

class PromiseUpdateSerializer(PromiseSerializer):
  class Meta(PromiseSerializer.Meta):
    read_only_fields = ('user1', 'user2')

class UserSerializer(serializers.ModelSerializer):
  promises_as_inviter = serializers.PrimaryKeyRelatedField(many=True, queryset=Promise.objects.all())
  promises_as_invitee = serializers.PrimaryKeyRelatedField(many=True, queryset=Promise.objects.all())

  class Meta:
    model = User
    fields = ('id', 'username', 'promises_as_inviter', 'promises_as_invitee')

class UserAllSerializer(serializers.ModelSerializer):
  whole_promises = serializers.SerializerMethodField()
  def get_whole_promises(self, obj):
    return Promise.objects.filter(Q(user1=obj.id) | Q(user2=obj.id)).values_list('id', flat=True).distinct()

  class Meta:
    model = User
    fields = ('id', 'username', 'whole_promises')