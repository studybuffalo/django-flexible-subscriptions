"""Part 1 of migration to switch recurrence_unit to CharField."""
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('subscriptions', '0003_update_plan_list_detail'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plancost',
            old_name='recurrence_unit',
            new_name='old_recurrence_unit',
        ),
        migrations.AddField(
            model_name='plancost',
            name='recurrence_unit',
            field=models.CharField(
                choices=[
                    ('o', 'once'),
                    ('s', 'second'),
                    ('n', 'minute'),
                    ('h', 'hour'),
                    ('d', 'day'),
                    ('w', 'week'),
                    ('m', 'month'),
                    ('y', 'year')
                ],
                default='m',
                max_length=1
            ),
        ),
    ]
