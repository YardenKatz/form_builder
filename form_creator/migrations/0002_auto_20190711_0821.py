# Generated by Django 2.2.3 on 2019-07-11 08:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('form_creator', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userform',
            name='form_id',
        ),
        migrations.AddField(
            model_name='userform',
            name='name',
            field=models.CharField(default='yarden', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userform',
            name='submissions',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='formfield',
            name='data',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='formfield',
            name='form_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='has_fields', to='form_creator.UserForm'),
        ),
        migrations.DeleteModel(
            name='FormList',
        ),
    ]
