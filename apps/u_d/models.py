from __future__ import unicode_literals
from django.db import models

import re
import bcrypt
import datetime

pass_regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,}')
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
admin_code = '1234'

class UserManager(models.Manager):
    def registration_validator(self, post_data):
        errors = []
        if len(post_data['first_name']) < 1 or len(post_data['last_name']) < 1:
            errors.append("First and Last Name fields cannot be empty")
        if not post_data['first_name'].isalpha or not post_data['last_name'].isalpha:
            errors.append("First and Last Name must only include letters")
        if len(User.objects.filter(email = post_data['email'])) > 0:
            errors.append("Already registered as an Admin. Please login.")
        if not email_regex.match(post_data['email']):
            errors.append("Email address format is not valid")
        if not pass_regex.match(post_data['pw']):
            errors.append("Password format is not valid")
        if not post_data['pw'] == post_data['pw_confirm']:
            errors.append("Passwords do not match")
        if 'admin_code' in post_data:
            if len(post_data['admin_code']) < 1 or not post_data['admin_code'] == admin_code:
                errors.append("Admin code is not valid")

        if not errors:
            hashed = bcrypt.hashpw(post_data['pw'].encode(), bcrypt.gensalt(5))
            user = User(
                first_name = post_data['first_name'],
                last_name = post_data['last_name'],
                email = post_data['email'],
                password = hashed
                )
            user1.save()

            if 'admin_code' in post_data:
                if post_data['admin_code'] == admin_code:
                    level = User_Level(
                        user = user,
                        level = 'admin'
                    )
                    level.save()
                else:
                    level = User_Level(
                        user = user,
                        level = 'normal'
                    )
                    level.save()
            
            if 'user_level' in post_data:
                if post_data['user_level'] == 'admin':
                    level = User_Level(
                        user = user,
                        level = 'admin'
                    )
                    level.save()
                else:
                    level = User_Level(
                        user = user,
                        level = 'normal'
                    )
                    level.save()
        else:
            return errors 
    
    def login_validator(self, post_data):
        errors = []
        print post_data
        print self.filter(email = post_data['email'])
        if len(self.filter(email = post_data['email'])) > 0:
            user = self.filter(email = post_data['email'])[0]
            if not bcrypt.checkpw(post_data['pw'].encode(), user.password.encode()):
                errors.append("Password is not valid")
        else:
            errors.append("Email address is not valid")

        if errors:
            return errors
        else:
            return user
    
    def edit_user(self, post_data):
        errors = []
        user = User.objects.get(id=post_data['user_id'])
        user_level = User_Level.objects.get(user_id=post_data['user_id'])
        if 'user_level' in post_data:
            user_level.level = post_data['user_level']   
        if 'first_name' in post_data:
            user.first_name = post_data['first_name']   
        if 'first_name' in post_data:
            user.last_name = post_data['last_name']
        if 'first_name' in post_data:
            user.email = post_data['email']
        user.save()

        if 'pw' in post_data:
            if not pass_regex.match(post_data['pw']):
                errors.append("Password format is not valid")
            if not post_data['pw'] == post_data['pw_confirm']:
                errors.append("Passwords do not match")
            if not errors:
                hashed = bcrypt.hashpw(post_data['pw'].encode(), bcrypt.gensalt(5))
                user.password = hashed
                user.save()
            else:
                return errors

        if 'desc' in post_data:
            if len(post_data['desc']) < 1:
                errors.append("Description field cannot be blank...")
                return errors
            else:
                desc = User_Description(
                    user = user,
                    desc = post_data['desc']
                )
                desc.save()

class MessageManager(models.Manager):
    def message_validator(self, post_data):
        errors = []
        if len(post_data['message']) < 1:
            errors.append("Message field cannot be empty")
            return errors
        message = Message(
            message = post_data['message'],
            sender = User.objects.get(id=post_data['sender_id']),
            receiver = User.objects.get(id=post_data['receiver_id'])
        )
        message.save()
        return message

    def comment_validator(self, post_data):
        errors = []
        if len(post_data['comment']) < 1:
            errors.append("Comment field cannot be empty")
            return errors
        comment = Comment(
            comment = post_data['comment'],
            commenter = User.objects.get(id=post_data['commenter_id']),
            message = Message.objects.get(id=post_data['message_id'])
        )
        comment.save()
        return comment

class User(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)
    password = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    objects = UserManager()

    def __repr__(self):
        return "<User object: {} {}>".format(self.first_name, self.last_name)

class User_Level(models.Model):
    user = models.OneToOneField(User, related_name="user_level")
    level = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    objects = UserManager()

    def __repr__(self):
         return "<User_Level object: {} {}>".format(self.user_id, self.level)

class User_Description(models.Model):
    user = models.OneToOneField(User, related_name="user_desc")
    desc = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __repr__(self):
         return "<User_Description object: {} {}>".format(self.user_id, self.desc)

class Message(models.Model):
    message = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sender = models.ForeignKey(User, related_name="sent_messages")
    receiver = models.ForeignKey(User, related_name="received_messages")
    objects = MessageManager()

    def __repr__(self):
         return "<Message object: {} {}>".format(self.sender, self.message)

class Comment(models.Model):
    comment = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    commenter = models.ForeignKey(User, related_name="user_comments")
    message = models.ForeignKey(Message, related_name="message_comments")
    objects = MessageManager()

    def __str__(self):     
        return "%s %s" % (self.commenter.first_name, self.comment)

    # def __repr__(self):
    #      return "<Comment object: {}>".format(self.comment)