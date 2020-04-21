from django.db import models

from members.models import User


class Room(models.Model):

    title = models.CharField(max_length=100, unique=True)

    staff_only = models.BooleanField(default=False)
    chat = models.ManyToManyField('self', symmetrical=False, through='Chat' )

    def __str__(self):
        return f'{self.title}'

    @property
    def group_name(self):
        """
        Returns the Channels Group name that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return "room-%s" % self.id


class Chat(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='chat_by_room')
    # from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_by_from_user')
    to_user   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_by_to_user')
    log = models.CharField(max_length=300)
    created_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
