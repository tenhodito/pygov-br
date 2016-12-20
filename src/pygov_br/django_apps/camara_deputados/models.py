from django.db import models


class LegislativeBodyType(models.Model):

    class Meta:
        verbose_name = "Legislative Body Type"
        verbose_name_plural = "Legislative Body Types"

    def __str__(self):
        return self.description

    description = models.CharField(max_length=100)


class LegislativeBody(models.Model):

    class Meta:
        verbose_name = "Legislative Body"
        verbose_name_plural = "Legislative Bodies"

    def __str__(self):
        return self.initials

    legislative_body_type = models.ForeignKey('LegislativeBodyType')
    initials = models.CharField(max_length=10)
    description = models.TextField()
    members = models.ManyToManyField('Deputy', through='LegislativeBodyMember')


class LegislativeBodyMember(models.Model):

    class Meta:
        verbose_name = "Legislative Body Member"
        verbose_name_plural = "Legislative Body Members"

    def __str__(self):
        return self.legislative_body.initials + ' - ' + self.deputy.name

    legislative_body = models.ForeignKey('LegislativeBody')
    deputy = models.ForeignKey('Deputy', related_name='comissions')
    role = models.ForeignKey('LegislativeBodyRole', null=True)


class LegislativeBodyRole(models.Model):

    class Meta:
        verbose_name = "Legislative Body Role"
        verbose_name_plural = "Legislative Body Roles"

    def __str__(self):
        return self.description

    description = models.CharField(max_length=100)


class Party(models.Model):

    class Meta:
        verbose_name = "Party"
        verbose_name_plural = "Parties"

    def __str__(self):
        return self.name

    creation_date = models.DateField(null=True)
    extinction_date = models.DateField(null=True)
    name = models.CharField(max_length=100)
    initials = models.CharField(max_length=20, primary_key=True)


class PartyBloc(models.Model):

    class Meta:
        verbose_name = "Party Bloc"
        verbose_name_plural = "Party Blocs"

    def __str__(self):
        return self.name

    creation_date = models.DateField(null=True)
    extinction_date = models.DateField(null=True)
    name = models.CharField(max_length=100)
    initials = models.CharField(max_length=50)
    members = models.ManyToManyField('Party', through='PartyBlocMember')


class PartyBlocMember(models.Model):

    class Meta:
        verbose_name = "Party Bloc Member"
        verbose_name_plural = "Party Bloc Members"

    def __str__(self):
        return self.party_bloc.name + ' - ' + self.party.initials

    party_bloc = models.ForeignKey('PartyBloc')
    party = models.ForeignKey('Party', related_name='party_blocs')
    adhesion_date = models.DateField(null=True)
    shutdown_date = models.DateField(null=True)


class ParliamentarySeat(models.Model):

    class Meta:
        verbose_name = "Parliamentary Seat"
        verbose_name_plural = "Parliamentary Seats"

    def __str__(self):
        return self.name

    name = models.CharField(max_length=150)
    initials = models.CharField(max_length=20, primary_key=True)


class Deputy(models.Model):

    class Meta:
        verbose_name = "Deputy"
        verbose_name_plural = "Deputies"

    def __str__(self):
        return self.parliamentary_name

    outbuilding = models.IntegerField()
    budget_id = models.IntegerField(null=True)
    condition = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    cabinet = models.IntegerField()
    parliamentary_id = models.IntegerField()
    enrollment_id = models.IntegerField()
    name = models.CharField(max_length=150)
    parliamentary_name = models.CharField(max_length=100)
    party = models.ForeignKey('Party', related_name='members')
    gender = models.CharField(max_length=50)
    region = models.CharField(max_length=2)
    photo_url = models.URLField()
    parliamentary_seat = models.ForeignKey('ParliamentarySeat', null=True,
                                           related_name='members')
    parliamentary_seat_leader = models.BooleanField(default=False)


class SessionType(models.Model):

    class Meta:
        verbose_name = "SessionType"
        verbose_name_plural = "Session Types"

    def __str__(self):
        return self.description

    description = models.CharField(max_length=255)


class Session(models.Model):

    class Meta:
        verbose_name = "Session"
        verbose_name_plural = "Sessions"

    def __str__(self):
        return self.code + ' - ' + self.session_type.description

    code = models.CharField(primary_key=True, max_length=255)
    date = models.DateField()
    session_type = models.ForeignKey('SessionType')
    number = models.IntegerField()


class SessionPhase(models.Model):

    class Meta:
        verbose_name = "Session Phase"
        verbose_name_plural = "Session Phases"

    def __str__(self):
        return self.description

    code = models.CharField(primary_key=True, max_length=50)
    description = models.CharField(max_length=50)


class Speech(models.Model):

    class Meta:
        verbose_name = "Speech"
        verbose_name_plural = "Speeches"

    def __str__(self):
        return str(self.author) + ' - ' + str(self.initial_time)

    initial_time = models.DateTimeField()
    insertion_number = models.IntegerField()
    quarter_number = models.IntegerField()
    order = models.IntegerField()
    full_text = models.TextField()
    summary = models.TextField(null=True)
    indexes = models.TextField(null=True)
    author = models.ForeignKey('Deputy', related_name='speeches', null=True)
    session = models.ForeignKey('Session', related_name='speeches')
    session_phase = models.ForeignKey('SessionPhase', related_name='speeches')

    def save(self, *args, **kwargs):
        if self.author is not None:
            super(Speech, self).save(*args, **kwargs)
