# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name='chats')
    is_group_chat = models.BooleanField(default=False)
    group_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='deleted_messages')
    
    # Fields for attachments
    video = models.FileField(upload_to='message_attachments/videos/', blank=True, null=True)
    image = models.FileField(upload_to='message_attachments/images/', blank=True, null=True)
    voice_note = models.FileField(upload_to='message_attachments/voice_notes/', blank=True, null=True)
    document = models.FileField(upload_to='message_attachments/documents/', blank=True, null=True)
    gps_location = models.CharField(max_length=255, blank=True, null=True)
    url_link = models.URLField(max_length=255, blank=True, null=True)


class Event(models.Model):
    idevent = models.AutoField(primary_key=True)  # Field name made lowercase.
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=255)
    event_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    event_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    requires_tickets = models.BooleanField(default=False)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    event_date_time = models.DateTimeField()
    event_end_date_time = models.DateTimeField()
    posted_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event_name

class Flags(models.Model):
    flag_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location_name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DateTimeField()
    flag_type = models.CharField(max_length=10, choices=[('flag_1', 'Flag 1'), ('flag_2', 'Flag 2')])



class FlagRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flag = models.ForeignKey(Flags, on_delete=models.CASCADE, related_name='flag_requests')
    status = models.CharField(max_length=45, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')], default='pending')



class OrgStatus(models.Model):
    org_status_id = models.IntegerField(primary_key=True)
    org_stat_rq = models.ForeignKey('OrganizersRq', models.DO_NOTHING, blank=True, null=True)
    org_stat = models.CharField(max_length=45, blank=True, null=True)



class OrganizersRq(models.Model):
    orgrq_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('Userprofile', models.DO_NOTHING, blank=True, null=True)
    orgrq_time = models.CharField(max_length=45, blank=True, null=True)



class RelationRq(models.Model):
    rel_id = models.IntegerField(primary_key=True)
    follower = models.ForeignKey('Userprofile', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('Userprofile', models.DO_NOTHING, db_column='user', related_name='relationrq_user_set', blank=True, null=True)
    relatiion_stat = models.CharField(max_length=45, blank=True, null=True)



class Steeze(models.Model):
    steeze_id = models.IntegerField(primary_key=True)
    poster = models.ForeignKey('Userprofile', models.DO_NOTHING, blank=True, null=True)
    poster_gps_long = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    video = models.CharField(max_length=255, blank=True, null=True)
    caption = models.CharField(max_length=45, blank=True, null=True)
    steez_time = models.CharField(max_length=45, blank=True, null=True)
    poster_gps_lati = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)


class SteezeCom(models.Model):
    com_id = models.IntegerField(primary_key=True)
    commentor = models.ForeignKey('Userprofile', models.DO_NOTHING, db_column='commentor', blank=True, null=True)
    comment = models.CharField(max_length=45, blank=True, null=True)
    com_time = models.CharField(max_length=45, blank=True, null=True)
    stz = models.ForeignKey(Steeze, models.DO_NOTHING, blank=True, null=True)



class SteezeLikes(models.Model):
    like_id = models.IntegerField(primary_key=True)
    liker = models.ForeignKey('Userprofile', models.DO_NOTHING, db_column='liker', blank=True, null=True)
    post = models.ForeignKey(Steeze, models.DO_NOTHING, blank=True, null=True)
    like_time = models.CharField(max_length=45, blank=True, null=True)



class Userprofile(models.Model):
    following = models.ManyToManyField('self', related_name='followers', blank=True)
    phone = models.CharField(max_length=45, blank=True, null=True)
    username = models.CharField(max_length=45, blank=True, null=True)
    fname = models.CharField(max_length=45, blank=True, null=True)
    sname = models.CharField(max_length=45, blank=True, null=True)
    dob = models.CharField(max_length=45, blank=True, null=True)
    password_hash = models.CharField(max_length=145, blank=True, null=True)
    about = models.CharField(max_length=45, blank=True, null=True)
    profilepic = models.CharField(max_length=45, blank=True, null=True)
    org_stat = models.ForeignKey(OrgStatus, models.DO_NOTHING, db_column='org_stat', blank=True, null=True)
    verification = models.ForeignKey('VerificationStatus', models.DO_NOTHING, db_column='verification', blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class VerificationRq(models.Model):
    vrq_id = models.AutoField(primary_key=True)
    v_requester = models.ForeignKey(Userprofile, models.DO_NOTHING, db_column='v_requester', blank=True, null=True)
    scanned_doc = models.CharField(max_length=45, blank=True, null=True)
    vrq_time = models.CharField(max_length=45, blank=True, null=True)



class VerificationStatus(models.Model):
    idverification_status = models.AutoField(primary_key=True)
    vrequest = models.ForeignKey(VerificationRq, models.DO_NOTHING, blank=True, null=True)
    status = models.CharField(max_length=45, blank=True, null=True)

