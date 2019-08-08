from django.db import migrations, models
import django.db.models.deletion


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
        migrations.RemoveField(
            model_name='planlist',
            name='plans',
        ),
        migrations.AlterField(
            model_name='planlistdetail',
            name='plan',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='plan_list_details',
                to='subscriptions.SubscriptionPlan'
            ),
        ),
        migrations.AlterField(
            model_name='planlistdetail',
            name='plan_list',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='plan_list_details',
                to='subscriptions.PlanList'
            ),
        ),
    ]
