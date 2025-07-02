from django.db import models
from django.contrib.auth.models import User

class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    following = models.ManyToManyField('self', related_name='followers', symmetrical=False, blank=True)
    is_organization = models.BooleanField(default=False)
    phone = models.CharField(max_length=45, blank=True, null=True)
    username = models.CharField(max_length=45, blank=True, null=True)
    fname = models.CharField(max_length=45, blank=True, null=True)
    sname = models.CharField(max_length=45, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    password_hash = models.CharField(max_length=145, blank=True, null=True)
    about = models.CharField(max_length=45, blank=True, null=True)
    profilepic = models.CharField(max_length=45, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    is_organizer = models.ForeignKey('OrgStatus', on_delete=models.SET_NULL, null=True, blank=True)
    is_verified = models.ForeignKey('VerificationStatus', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username or self.user.username

class Chat(models.Model):
    participants = models.ManyToManyField(Userprofile, related_name='chats')
    is_group_chat = models.BooleanField(default=False)
    group_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.group_name or f"Chat {self.id}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(Userprofile, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(Userprofile, on_delete=models.SET_NULL, null=True, blank=True, related_name='deleted_messages')
    video = models.FileField(upload_to='message_attachments/videos/', blank=True, null=True)
    image = models.FileField(upload_to='message_attachments/images/', blank=True, null=True)
    voice_note = models.FileField(upload_to='message_attachments/voice_notes/', blank=True, null=True)
    document = models.FileField(upload_to='message_attachments/documents/', blank=True, null=True)
    gps_location = models.CharField(max_length=255, blank=True, null=True)
    url_link = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Message by {self.sender.username} at {self.timestamp}"

class Event(models.Model):
    idevent = models.AutoField(primary_key=True)
    organizer = models.ForeignKey(Userprofile, on_delete=models.CASCADE, related_name='organized_events')
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
    user = models.ForeignKey(Userprofile, on_delete=models.CASCADE, related_name='flags')
    location_name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DateTimeField()
    flag_type = models.CharField(max_length=10, choices=[('flag_1', 'Flag 1'), ('flag_2', 'Flag 2')])

    def __str__(self):
        return f"{self.location_name} ({self.flag_type})"

class FlagRequest(models.Model):
    user = models.ForeignKey(Userprofile, on_delete=models.CASCADE, related_name='flag_requests_made')
    flag = models.ForeignKey(Flags, on_delete=models.CASCADE, related_name='flag_requests')
    status = models.CharField(max_length=45, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')], default='pending')

    def __str__(self):
        return f"{self.user.username} -> {self.flag.location_name} ({self.status})"

class OrganizersRq(models.Model):
    orgrq_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Userprofile, on_delete=models.CASCADE, related_name='organizer_requests')
    orgrq_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Organizer request by {self.user.username}"

class OrgStatus(models.Model):
    org_status_id = models.AutoField(primary_key=True)
    org_stat_rq = models.ForeignKey(OrganizersRq, on_delete=models.CASCADE, related_name='status')
    org_stat = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return f"Status {self.org_stat} for request {self.org_stat_rq.id}"

class RelationRq(models.Model):
    rel_id = models.AutoField(primary_key=True)
    follower = models.ForeignKey(Userprofile, on_delete=models.CASCADE, related_name='following_requests')
    user = models.ForeignKey(Userprofile, on_delete=models.CASCADE, related_name='follower_requests')
    relatiion_stat = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return f"{self.follower.username} -> {self.user.username} ({self.relatiion_stat})"

class Steeze(models.Model):
    steeze_id = models.AutoField(primary_key=True)
    poster = models.ForeignKey(Userprofile, on_delete=models.CASCADE, related_name='steeze_posts')
    poster_gps_long = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    poster_gps_lati = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    video = models.CharField(max_length=255, blank=True, null=True)
    caption = models.CharField(max_length=45, blank=True, null=True)
    steez_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Steeze by {self.poster.username}"

class SteezeCom(models.Model):
    com_id = models.AutoField(primary_key=True)
    commentor = models.ForeignKey(Userprofile, on_delete=models.CASCADE, related_name='steeze_comments')
    stz = models.ForeignKey(Steeze, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=45, blank=True, null=True)
    comment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.commentor.username} on Steeze {self.stz.id}"

class SteezeLikes(models.Model):
    like_id = models.AutoField(primary_key=True)
    liker = models.ForeignKey(Userprofile, on_delete=models.CASCADE, related_name='steeze_likes')
    post = models.ForeignKey(Steeze, on_delete=models.CASCADE, related_name='likes')
    like_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like by {self.liker.username} on Steeze {self.post.id}"

class VerificationRq(models.Model):
    vrq_id = models.AutoField(primary_key=True)
    v_requester = models.ForeignKey(Userprofile, on_delete=models.CASCADE, related_name='verification_requests')
    scanned_doc = models.CharField(max_length=45, blank=True, null=True)
    vrq_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Verification request by {self.v_requester.username}"

class VerificationStatus(models.Model):
    idverification_status = models.AutoField(primary_key=True)
    vrequest = models.ForeignKey(VerificationRq, on_delete=models.CASCADE, related_name='status')
    status = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return f"Verification status {self.status} for request {self.vrequest.id}"

class Thoughts(models.Model):
    user = models.ForeignKey(Userprofile, on_delete=models.CASCADE, related_name='thoughts')
    content = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Thought by {self.user.username}"

class ThLike(models.Model):
    user = models.ForeignKey(Userprofile, on_delete=models.CASCADE, related_name='thought_likes')
    thought = models.ForeignKey(Thoughts, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like by {self.user.username} on Thought {self.thought.id}"

class ThComment(models.Model):
    user = models.ForeignKey(Userprofile, on_delete=models.CASCADE, related_name='thought_comments')
    thought = models.ForeignKey(Thoughts, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on Thought {self.thought.id}"

class ThShare(models.Model):
    user = models.ForeignKey(Userprofile, on_delete=models.CASCADE, related_name='thought_shares')
    thought = models.ForeignKey(Thoughts, on_delete=models.CASCADE, related_name='shares')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Share by {self.user.username} on Thought {self.thought.id}"

class ThRepost(models.Model):
    user = models.ForeignKey(Userprofile, on_delete=models.CASCADE, related_name='thought_reposts')
    original_thought = models.ForeignKey(Thoughts, on_delete=models.CASCADE, related_name='reposts')
    reposted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Repost by {self.user.username} of Thought {self.original_thought.id}"