# Generated migration for Department model and data migration

from django.db import migrations, models
import django.db.models.deletion


def migrate_department_data(apps, schema_editor):
    """Migrate old CharField department_cutting to new ForeignKey"""
    CoilOut = apps.get_model('coil', 'CoilOut')
    Department = apps.get_model('coil', 'Department')

    # Get all unique department names from old data
    old_departments = set()
    for coilout in CoilOut.objects.all():
        if coilout.department_cutting:
            old_departments.add(str(coilout.department_cutting))

    # Create Department objects
    department_mapping = {}
    for dept_name in old_departments:
        if dept_name:
            dept, created = Department.objects.get_or_create(
                name=dept_name,
                defaults={'description': f'Migrated from old data: {dept_name}'}
            )
            department_mapping[dept_name] = dept


def reverse_migrate(apps, schema_editor):
    """Reverse migration - just delete all departments"""
    Department = apps.get_model('coil', 'Department')
    Department.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('coil', '0015_job_remove_coilout_job_name_short_and_more'),
    ]

    operations = [
        # Step 1: Create Department model
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='ชื่อแผนก')),
                ('description', models.TextField(blank=True, null=True, verbose_name='คำอธิบาย')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'แผนกที่ตัด',
                'verbose_name_plural': 'แผนกที่ตัด',
            },
        ),

        # Step 2: Rename old field to temporary name
        migrations.RenameField(
            model_name='coilout',
            old_name='department_cutting',
            new_name='department_cutting_old',
        ),

        # Step 3: Create new ForeignKey field
        migrations.AddField(
            model_name='coilout',
            name='department_cutting',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='coil.department',
                verbose_name='แผนกที่ตัด',
            ),
        ),

        # Step 4: Migrate data
        migrations.RunPython(migrate_department_data, reverse_migrate),
    ]
