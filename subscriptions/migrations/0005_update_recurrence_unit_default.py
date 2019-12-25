"""Migration to fix incorrect default for recurrence unit."""
from django.db import migrations, models

class Migration(migrations.Migration):
    """Updates plancost recurrentunit to '6' instead of 'm'."""
    dependencies = [
        ('subscriptions', '0004_change_recurrence_unit_type_2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plancost',
            name='recurrence_unit',
            field=models.CharField(
                choices=[
                    ('0', 'once'),
                    ('1', 'second'),
                    ('2', 'minute'),
                    ('3', 'hour'),
                    ('4', 'day'),
                    ('5', 'week'),
                    ('6', 'month'),
                    ('7', 'year'),
                ],
                default='6',
                max_length=1
            ),
        ),
    ]
