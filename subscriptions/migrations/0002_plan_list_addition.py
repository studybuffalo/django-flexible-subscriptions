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
                ('title', models.TextField(blank=True, help_text='title to display on the subscription plan list page', null=True)),
                ('subtitle', models.TextField(blank=True, help_text='subtitle to display on the subscription plan list page', null=True)),
                ('header', models.TextField(blank=True, help_text='header text to display on the subscription plan list page', null=True)),
                ('footer', models.TextField(blank=True, help_text='header text to display on the subscription plan list page', null=True)),
                ('active', models.BooleanField(default=True, help_text='whether this plan list is active or not.')),
            ],
        ),
        migrations.CreateModel(
            name='PlanListDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('html_content', models.TextField(blank=True, help_text='HTML content to display for plan', null=True)),
                ('subscribe_button_text', models.CharField(blank=True, default='Subscribe', max_length=128, null=True)),
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
