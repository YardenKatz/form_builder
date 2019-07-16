# Generated by Django 2.2.3 on 2019-07-16 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('form_creator', '0006_auto_20190716_0719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldsubmission',
            name='submission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='field_set', to='form_creator.Submissions'),
        ),
        migrations.AlterField(
            model_name='submissions',
            name='submission_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='submissions',
            name='user_form',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='has_submission', to='form_creator.UserForm'),
        ),
    ]
