# pylint: disable=missing-docstring, line-too-long, invalid-name

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('subscriptions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlanList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, help_text='Title to display on the subscription plan list page', null=True)),
                ('subtitle', models.TextField(blank=True, help_text='Subtitle to display on the subscription plan list page', null=True)),
                ('header', models.TextField(blank=True, help_text='Header text to display on the subscription plan list page', null=True)),
                ('footer', models.TextField(blank=True, help_text='Header text to display on the subscription plan list page', null=True)),
                ('active', models.BooleanField(default=True, help_text='Whether this plan list is active or not.')),
            ],
        ),
        migrations.CreateModel(
            name='PlanListDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, help_text='Title to display for this subscription plan', null=True)),
                ('subtitle', models.TextField(blank=True, help_text='Subitle to display for this subscription plan', null=True)),
                ('header', models.TextField(blank=True, help_text='Header text to display for this subscription plan', null=True)),
                ('footer', models.TextField(blank=True, help_text='Footer text to display for this subscription plan', null=True)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscriptions.SubscriptionPlan')),
                ('plan_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscriptions.PlanList')),
            ],
        ),
        migrations.AddField(
            model_name='planlist',
            name='plans',
            field=models.ManyToManyField(blank=True, related_name='plan_lists', through='subscriptions.PlanListDetail', to='subscriptions.SubscriptionPlan'),
        ),
    ]
