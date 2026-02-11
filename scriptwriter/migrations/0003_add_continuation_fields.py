# Generated manually for continuation feature

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scriptwriter', '0002_scene_character_script_job_scriptversion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='is_continuation',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='job',
            name='parent_job',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='continuations',
                to='scriptwriter.job'
            ),
        ),
        migrations.AddField(
            model_name='job',
            name='continuation_count',
            field=models.IntegerField(default=0),
        ),
    ]
