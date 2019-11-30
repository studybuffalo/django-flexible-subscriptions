"""Part 2 of migration to switch recurrence_unit to CharField."""
from django.db import migrations, models


def convert_recurrence_unit_forward(apps, schema_editor):
    """Copy integer-based unit to char-based."""
    PlanCost = apps.get_model('subscriptions', 'PlanCost')

    # Conversions from integer to char
    UNITS = ['o', 's', 'n', 'h', 'd', 'w', 'm', 'y']

    # Update recurrence unit for all PlanCost instances
    for cost in PlanCost.objects.all():
        old_unit = cost.old_recurrence_unit
        new_unit = UNITS[old_unit]
        cost.recurrence_unit = new_unit
        cost.save()

def convert_recurrence_unit_reverse(apps, schema_editor):
    """Copy char-based unit to integer-based."""
    PlanCost = apps.get_model('subscriptions', 'PlanCost')

    # Conversions from integer to char
    UNITS = {'o': 0, 's': 1, 'n': 2, 'h':3, 'd': 4, 'w': 5, 'm': 6, 'y': 7}

    # Update recurrence unit for all PlanCost instances
    for cost in PlanCost.objects.all():
        new_unit = cost.recurrence_unit
        old_unit = UNITS[new_unit]
        cost.old_recurrence_unit = old_unit
        cost.save()

class Migration(migrations.Migration):
    dependencies = [
        ('subscriptions', '0004_change_recurrence_unit_type_1'),
    ]

    operations = [
        migrations.RunPython(convert_recurrence_unit_forward, convert_recurrence_unit_reverse),
        migrations.RemoveField('plancost', 'old_recurrence_unit'),
    ]
