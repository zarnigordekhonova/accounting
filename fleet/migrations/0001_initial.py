# Generated by Django 4.2 on 2024-11-02 16:24

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarrierType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Carrier Types',
                'db_table': 'carrier_types',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
                'db_table': 'companies',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': 'Departments',
                'db_table': 'departments',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=80)),
                ('SSN', models.CharField(blank=True, max_length=100, null=True)),
                ('driver_id', models.CharField(blank=True, max_length=30, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fleet.company')),
            ],
            options={
                'verbose_name_plural': 'Drivers',
                'db_table': 'drivers',
            },
        ),
        migrations.CreateModel(
            name='DriverStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Statuses',
                'db_table': 'driver_statuses',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='DriverType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
            ],
            options={
                'verbose_name_plural': 'Driver Types',
                'db_table': 'driver_types',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='LessorCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Lessor Companies',
                'db_table': 'lessor_companies',
            },
        ),
        migrations.CreateModel(
            name='Make',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Makes',
                'db_table': 'makes',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Models',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('make', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleet.make')),
            ],
            options={
                'verbose_name_plural': 'Models',
                'db_table': 'models',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Recruiter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
            ],
            options={
                'verbose_name_plural': 'Recruiters',
                'db_table': 'recruiters',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Truck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_number', models.CharField(max_length=40)),
                ('VIN', models.CharField(max_length=17)),
                ('carrier_company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='carrier_company', to='fleet.company')),
                ('carrier_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fleet.carriertype')),
                ('lessor_company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fleet.lessorcompany')),
                ('make', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleet.make')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleet.models')),
                ('owner_company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fleet.company')),
            ],
            options={
                'verbose_name_plural': 'Trucks',
                'db_table': 'trucks',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='TruckStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Statuses',
                'db_table': 'truck_statuses',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='UserStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Status',
                'verbose_name_plural': 'Statuses',
                'db_table': 'user_statuses',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='VehicleType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Vehicle Types',
                'db_table': 'vehicle_types',
            },
        ),
        migrations.CreateModel(
            name='TruckDriver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(blank=True, null=True)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleet.driver')),
                ('truck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='truck_drivers', to='fleet.truck')),
            ],
            options={
                'verbose_name_plural': 'Truck Drivers',
                'db_table': 'truck_drivers',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='truck',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleet.truckstatus'),
        ),
        migrations.AddField(
            model_name='truck',
            name='vehicle_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fleet.vehicletype'),
        ),
        migrations.AddField(
            model_name='driver',
            name='driver_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fleet.drivertype'),
        ),
        migrations.AddField(
            model_name='driver',
            name='recruiter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fleet.recruiter'),
        ),
        migrations.AddField(
            model_name='driver',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fleet.driverstatus'),
        ),
        migrations.AddField(
            model_name='company',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fleet.userstatus'),
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=False)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fleet.company')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fleet.department')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'CustomUser',
                'verbose_name_plural': 'CustomUsers',
                'db_table': 'users',
                'ordering': ['id'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
