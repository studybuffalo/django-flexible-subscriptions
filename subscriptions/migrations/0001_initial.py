# pylint: disable=missing-docstring, line-too-long, invalid-name

import uuid

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlanCost',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('recurrence_period', models.PositiveSmallIntegerField(default=1, help_text='how often the plan is billed (per recurrence unit)', validators=[django.core.validators.MinValueValidator(1)])),
                ('recurrence_unit', models.PositiveIntegerField(default=6, help_text='the unit of measurement for the recurrence period', validators=[django.core.validators.MaxValueValidator(7)])),
                ('cost', models.DecimalField(blank=True, decimal_places=4, help_text='the cost per recurrence of the plan', max_digits=19, null=True)),
            ],
            options={
                'ordering': ('recurrence_unit', 'recurrence_period', 'cost',),
            }
        ),
        migrations.CreateModel(
            name='PlanTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(help_text='the tag name', max_length=64, unique=True)),
            ],
            options={
                'ordering': ('tag',),
            },
        ),
        migrations.CreateModel(
            name='SubscriptionPlan',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_name', models.CharField(help_text='the name of the subscription plan', max_length=128)),
                ('plan_description', models.CharField(blank=True, help_text='a description of the subscription plan', max_length=512, null=True)),
                ('grace_period', models.PositiveIntegerField(default=0, help_text='how many days after the subscription ends before the subscription expires')),
                ('group', models.ForeignKey(blank=True, help_text='the Django auth group for this plan', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='plans', to='auth.Group')),
                ('tags', models.ManyToManyField(blank=True, help_text='any tags associated with this plan', related_name='plans', to='subscriptions.PlanTag')),

            ],
            options={
                'ordering': ('plan_name',),
                'permissions': (('subscriptions', 'Can interact with subscription details'),),
            },
        ),
        migrations.CreateModel(
            name='SubscriptionTransaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_transaction', models.DateTimeField(help_text='the datetime the transaction was billed', verbose_name='transaction date')),
                ('amount', models.DecimalField(blank=True, decimal_places=4, help_text='how much was billed for the user', max_digits=19, null=True)),
                ('subscription', models.ForeignKey(help_text='the plan costs that were billed', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions', to='subscriptions.PlanCost')),
                ('user', models.ForeignKey(help_text='the user that this subscription was billed for', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subscription_transactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('date_transaction', 'user',),
            },
        ),
        migrations.CreateModel(
            name='UserSubscription',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_billing_start', models.DateTimeField(blank=True, help_text='the date to start billing this subscription', null=True, verbose_name='billing start date')),
                ('date_billing_end', models.DateTimeField(blank=True, help_text='the date to finish billing this subscription', null=True, verbose_name='billing start end')),
                ('date_billing_last', models.DateTimeField(blank=True, help_text='the last date this plan was billed', null=True, verbose_name='last billing date')),
                ('date_billing_next', models.DateTimeField(blank=True, help_text='the next date billing is due', null=True, verbose_name='next start date')),
                ('active', models.BooleanField(default=True, help_text='whether this subscription is active or not')),
                ('cancelled', models.BooleanField(default=False, help_text='whether this subscription is cancelled or not')),
                ('subscription', models.ForeignKey(help_text='the plan costs and billing frequency for this user', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='subscriptions.PlanCost')),
                ('user', models.ForeignKey(help_text='the user this subscription applies to', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('user', 'date_billing_start',),
            },
        ),
        migrations.AddField(
            model_name='plancost',
            name='plan',
            field=models.ForeignKey(help_text='the subscription plan for these cost details', on_delete=django.db.models.deletion.CASCADE, related_name='costs', to='subscriptions.SubscriptionPlan'),
        ),
    ]
