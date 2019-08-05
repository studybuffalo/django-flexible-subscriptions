from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('subscriptions', '0002_plan_list_addition'),
    ]

    operations = [
        migrations.AddField(
            model_name='planlistdetail',
            name='order',
            field=models.PositiveIntegerField(
                default=1,
                help_text='Order to display plan in (lower numbers displayed first)'
            ),
        ),
    ]
