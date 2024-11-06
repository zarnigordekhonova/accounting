from rest_framework import serializers
from .models import (Facility, FacilityHistory, Broker, BrokerHistory, LoadProcess,
                     Status, Load, LoadHistory, LoadFile, LoadStop)


class BrokersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Broker
        fields = '__all__'


class BrokerHistoryViewSerializer(serializers.ModelSerializer):
    broker = serializers.SerializerMethodField(method_name='get_broker')
    changed_by = serializers.SerializerMethodField(method_name='get_changed_by')
    last_updated = serializers.SerializerMethodField()

    class Meta:
        model = BrokerHistory
        fields = '__all__'

    def get_broker(self, obj):
        if obj.broker:
            return {
                "id": obj.broker.id,
                "name": obj.broker.name,
                "mc": obj.broker.mc
            }
        return None

    def get_changed_by(self, obj):
        if obj.changed_by:
            return {
                "id": obj.changed_by.id,
                "username": obj.changed_by.username,
                "department": obj.changed_by.department.name
            }
        return None

    def get_last_updated(self, obj):
        return obj.broker.last_updated if obj.broker else None


class BrokerHistoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrokerHistory
        fields = '__all__'


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = '__all__'


class FacilityHistoryViewSerializer(serializers.ModelSerializer):
    facility = serializers.SerializerMethodField(method_name='get_facility')
    changed_by = serializers.SerializerMethodField(method_name='get_changed_by')
    last_updated = serializers.SerializerMethodField()

    class Meta:
        model = FacilityHistory
        fields = '__all__'

    def get_facility(self, obj):
        if obj.facility:
            return {
                "id": obj.facility.id,
                "name": obj.facility.name,
                "address": obj.facility.address
            }
        return None

    def get_changed_by(self, obj):
        if obj.changed_by:
            return {
                "id": obj.changed_by.id,
                "username": obj.changed_by.username,
                "department": obj.changed_by.department.name
            }
        return None

    def get_last_updated(self, obj):
        return obj.facility.last_updated if obj.facility else None


class FacilityHistoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityHistory
        fields = '__all__'


class LoadProcessesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoadProcess
        fields = '__all__'


class StatusesViewSerializer(serializers.ModelSerializer):
    process = LoadProcessesSerializer()

    class Meta:
        model = Status
        fields = '__all__'


class StatusesWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class LoadsViewSerializer(serializers.ModelSerializer):
    booked_by = serializers.SerializerMethodField(method_name='get_booked_by')
    created_by = serializers.SerializerMethodField(method_name='get_created_by')
    from_facility = serializers.SerializerMethodField(method_name='get_from_facility')
    broker = serializers.SerializerMethodField(method_name='get_broker')
    driver = serializers.SerializerMethodField(method_name='get_driver')
    process = LoadProcessesSerializer()

    class Meta:
        model = Load
        fields = '__all__'

    def get_booked_by(self, obj):
        if obj.booked_by:
            return {
                "id": obj.booked_by.id,
                "username": obj.booked_by.username,
                "department": obj.booked_by.department.name
            }
        return None

    def get_created_by(self, obj):
        if obj.created_by:
            return {
                "id": obj.created_by.id,
                "username": obj.created_by.username,
                "department": obj.created_by.department.name
            }
        return None

    def get_from_facility(self, obj):
        if obj.from_facility:
            return {
                "id": obj.from_facility.id,
                "name": obj.from_facility.name,
                "address": obj.from_facility.address
            }
        return None

    def get_broker(self, obj):
        if obj.broker:
            return {
                "id": obj.broker.id,
                "name": obj.broker.name,
                "mc": obj.broker.mc,
                "address": obj.broker.address,
                "city": obj.broker.city,
                "state": obj.broker.state
            }
        return None

    def get_driver(self, obj):
        if obj.driver:
            return {
                "id": obj.driver.id,
                "full_name": obj.driver.full_name,
                "company": obj.driver.company.name,
                "driver_id": obj.driver.driver_id if obj.driver.driver_id else None
            }
        return None


class LoadsWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Load
        fields = '__all__'

    def create(self, validated_data):
        if 'process' not in validated_data:
            pending_process = LoadProcess.objects.get(name='Pending')
            validated_data['process'] = pending_process
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class LoadHistoryViewSerializer(serializers.ModelSerializer):
    load = serializers.SerializerMethodField(method_name='get_load')
    changed_by = serializers.SerializerMethodField(method_name='get_changed_by')

    class Meta:
        model = LoadHistory
        fields = '__all__'

    def get_load(self, obj):
        if obj.load:
            return {
                "id": obj.load.id,
                "carrier": obj.load.carrier,
                "driver": obj.load.driver.full_name
            }
        return None

    def get_changed_by(self, obj):
        if obj.changed_by:
            return {
                "id": obj.changed_by.id,
                "username": obj.changed_by.username,
                "department": obj.changed_by.department.name
            }
        return None


class LoadHistoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoadHistory
        fields = '__all__'


class LoadFilesViewSerializer(serializers.ModelSerializer):
    load = serializers.SerializerMethodField(method_name='get_load')

    class Meta:
        model = LoadFile
        fields = '__all__'

    def get_load(self, obj):
        if obj.load:
            return {
                "id": obj.load.id,
                "carrier": obj.load.carrier,
                "driver": obj.load.driver.full_name
            }
        return None


class LoadFilesWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoadFile
        fields = '__all__'


class LoadUseSerializer(serializers.ModelSerializer):
    booked_by = serializers.SerializerMethodField(method_name='get_booked_by')
    created_by = serializers.SerializerMethodField(method_name='get_created_by')
    from_facility = serializers.SerializerMethodField(method_name='get_from_facility')
    broker = serializers.SerializerMethodField(method_name='get_broker')
    driver = serializers.SerializerMethodField(method_name='get_driver')
    process = serializers.SerializerMethodField(method_name='get_process')

    class Meta:
        model = Load
        fields = '__all__'

    def get_booked_by(self, obj):
        return obj.booked_by.username if obj.booked_by else None

    def get_created_by(self, obj):
        return obj.created_by.username if obj.created_by else None

    def get_from_facility(self, obj):
        return obj.from_facility.name if obj.from_facility else None

    def get_broker(self, obj):
        return obj.broker.name if obj.broker else None

    def get_driver(self, obj):
        return obj.driver.full_name if obj.driver else None

    def get_process(self, obj):
        return obj.process.name if obj.process else None


class LoadStopViewSerializer(serializers.ModelSerializer):
    facility = serializers.SerializerMethodField(method_name='get_facility')
    load = serializers.SerializerMethodField(method_name='get_load')

    class Meta:
        model = LoadStop
        fields = '__all__'

    def get_facility(self, obj):
        if obj.facility:
            return {
                'id': obj.facility.id,
                'name': obj.facility.name,
                'address': obj.facility.address
            }
        return None

    def get_load(self, obj):
        if obj.load:
            return {
                "id": obj.load.id,
                "carrier": obj.load.carrier,
                "driver": obj.load.driver.full_name
            }
        return None


class LoadStopWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoadStop
        fields = '__all__'

    def validate(self, data):
        if data.get('destination'):
            load_id = data.get('load').id if data.get('load') else None
            if LoadStop.objects.filter(load_id=load_id, destination=True).exists():
                raise serializers.ValidationError("Only one LoadStop per Load can have destination set to True.")
        return data
