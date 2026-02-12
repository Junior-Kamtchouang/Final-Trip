from django.db import models
from django.utils import timezone

class Association(models.Model):
    # Status-Optionen
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]
    # Beitrag-Optionen
    FEE_TYPE_CHOICES = [
        ('once', 'Einmalig'),
        ('monthly', 'Monatlich'),
        ('yearly', 'Jährlich'),
    ]
    name = models.CharField(max_length=200)
    entry_date = models.DateField(verbose_name="Eintrittsdatum", null=True, blank=True)

    head_of_association = models.CharField(max_length=200, verbose_name="Leiter/in der Assocation", null=True)
    head_phone = models.CharField(max_length=50, verbose_name="Telefon (Head)", null=True, blank=True)

    member_count = models.PositiveIntegerField(default=0, verbose_name="Anzahl Mitglieder",  null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="Mitgliedstatus")

    # Beitrag
    fee_amount = models.FloatField(default=0.0, verbose_name="Beitrag (€)")
    fee_type = models.CharField(max_length=20, choices=FEE_TYPE_CHOICES, default='once', verbose_name="Beitragstyp")
    def __str__(self):
        return self.name

    @property
    def years_active(self):
        if self.entry_date:
            delta = timezone.now().date() - self.entry_date
            return int(delta.days / 365)
        return 0

    # Berechnet die Summe aller Teilnahmen dieser Assoziation

class ManualStats(models.Model):
    # Wir verknüpfen es mit der Association, damit du pro Partner steuern kannst
    association_count = models.PositiveIntegerField(default=0, verbose_name="Association Anzahl/Partner (Manuell)")
    manual_member_count = models.PositiveIntegerField(default=0, verbose_name="Mitglieder/Members (Manuell)")
    manual_participation_fee = models.FloatField(default=0.0, verbose_name="Beitrag/Participation (Manuell)")

    is_active_override = models.BooleanField(default=True, verbose_name="Diese Daten nutzen?")

    def __str__(self):
        return f"Manuelle Daten "

    @property
    def participation_per_member(self):
        if self.manual_member_count > 0:
            return self.manual_participation_fee / self.manual_member_count
        return 0


    @property
    def total_participation_value(self):
        return self.participations.aggregate(models.Sum('value'))['value__sum'] or 0

    # Berechnet den Anteil pro Kopf (Participation / Aktive Member)
    @property
    def participation_per_member(self):
        count = self.members.filter(is_active=True).count()
        if count > 0:
            return self.total_participation_value / count
        return 0

class Member(models.Model):
    association = models.ForeignKey(
        Association,
        related_name='members',
        on_delete=models.CASCADE,
        verbose_name="Association"
    )
    name = models.CharField(max_length=200, verbose_name="Name des Mitglieds")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")

    def __str__(self):
        return f"{self.name} ({self.association.name})"

    class Meta:
        verbose_name = "Member"
        verbose_name_plural = "Members"
        ordering = ['name']

class Participation(models.Model):
    association = models.ForeignKey(
        Association,
        related_name='participations',
        on_delete=models.CASCADE
    )
    value = models.FloatField(help_text="Wert der Teilnahme / Beitrag")
    date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True, help_text="Wofür war diese Teilnahme?")

    def __str__(self):
        return f"{self.association.name}: {self.value} ({self.date})"