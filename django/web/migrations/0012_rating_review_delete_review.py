# Generated by Django 4.1.7 on 2023-05-02 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0011_alter_rating_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='review',
            field=models.CharField(max_length=512, null=True),
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]