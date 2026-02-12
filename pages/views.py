from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from .models import Association, ManualStats
from django.db.models.functions import Coalesce
from django.db.models import DecimalField, Value

def index(request):

    stats = ManualStats.objects.first()

    context = {
        'stats': stats
    }

    return render(request, 'pages/index.html', context)


# Deine anderen Views bleiben gleich
def about(request):
    return render(request, 'pages/about.html')


def finalTrip(request):
    return render(request, 'pages/finalTrip.html')


# Neue View für die Association-Liste


def association_list(request):
    associations = Association.objects.all()

    total_members = associations.aggregate(
        total=Coalesce(Sum('member_count'), Value(0))
    )['total']

    # Wenn fee_amount Decimal ist:
    total_monthly_volume = associations.aggregate(
        total=Coalesce(
            Sum('fee_amount'),
            Value(0),
            output_field=DecimalField(max_digits=12, decimal_places=2)
        )
    )['total']

    context = {
        'associations': associations,
        'associations_count': associations.count(),
        'total_members': total_members,
        'total_monthly_volume': total_monthly_volume,
    }
    return render(request, 'pages/association_list.html', context)
# Neue View für die Association-Detailseite
def association_detail(request, pk):
    association = get_object_or_404(Association, pk=pk)

    context = {
        'association': association,
    }
    return render(request, 'pages/association_detail.html', context)