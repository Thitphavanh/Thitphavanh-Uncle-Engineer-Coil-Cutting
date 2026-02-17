# Complete department migration by mapping old data to new ForeignKey

from django.db import migrations


def map_old_to_new_department(apps, schema_editor):
    """Map old department_cutting_old values to new department_cutting ForeignKey"""
    CoilOut = apps.get_model('coil', 'CoilOut')
    Department = apps.get_model('coil', 'Department')

    for coilout in CoilOut.objects.all():
        if coilout.department_cutting_old:
            # Try to find matching department
            dept_name = str(coilout.department_cutting_old)
            try:
                dept = Department.objects.get(name=dept_name)
                coilout.department_cutting = dept
                coilout.save(update_fields=['department_cutting'])
            except Department.DoesNotExist:
                # If department doesn't exist, create it
                dept = Department.objects.create(
                    name=dept_name,
                    description=f'Auto-created during migration: {dept_name}'
                )
                coilout.department_cutting = dept
                coilout.save(update_fields=['department_cutting'])


def reverse_map(apps, schema_editor):
    """Reverse the mapping"""
    CoilOut = apps.get_model('coil', 'CoilOut')

    for coilout in CoilOut.objects.all():
        if coilout.department_cutting:
            coilout.department_cutting_old = coilout.department_cutting.name
            coilout.save(update_fields=['department_cutting_old'])


class Migration(migrations.Migration):

    dependencies = [
        ('coil', '0016_migrate_department_data'),
    ]

    operations = [
        # Map old data to new ForeignKey
        migrations.RunPython(map_old_to_new_department, reverse_map),

        # Remove old field
        migrations.RemoveField(
            model_name='coilout',
            name='department_cutting_old',
        ),
    ]
