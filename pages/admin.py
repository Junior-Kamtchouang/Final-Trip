from django.contrib import admin
from .models import Association, Participation, Member, ManualStats

class ManualStatsInline(admin.StackedInline):
    model = ManualStats
    can_delete = False
    verbose_name_plural = 'Manuelle Anzeige-Steuerung (JETZT)'
class ParticipationInline(admin.TabularInline):
    model = Participation
    extra = 1  # Zeigt standardmäßig ein leeres Feld für neue Eingaben

@admin.register(Association)
class AssociationAdmin(admin.ModelAdmin):
    ('name', 'head_of_association', 'get_manual_members', 'get_manual_fee')

    inlines = [ParticipationInline]

    # Hilfsmethode für die Mitgliederanzahl aus dem ManualStats-Model
    def get_manual_members(self, obj):
        if hasattr(obj, 'manual_data'):
            return obj.manual_data.manual_member_count
        return 0

    get_manual_members.short_description = "Mitglieder (Manuell)"

    # Hilfsmethode für die Gebühr aus dem ManualStats-Model
    def get_manual_fee(self, obj):
        if hasattr(obj, 'manual_data'):
            return obj.manual_data.manual_participation_fee
        return 0

    get_manual_fee.short_description = "Beitrag (Manuell)"

@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('association', 'value', 'date')
    list_filter = ('association', 'date')

    @admin.register(ManualStats)
    class ManualStatsAdmin(admin.ModelAdmin):
        list_display = ('association_count', 'manual_member_count', 'manual_participation_fee')
