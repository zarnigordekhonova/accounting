from rest_framework import serializers
from .models import DriverDispatcher


class DriverDispatcherViewSerializer(serializers.ModelSerializer):
    driver = serializers.SerializerMethodField(method_name='get_driver')
    dispatch = serializers.SerializerMethodField(method_name='get_dispatch')

    class Meta:
        model = DriverDispatcher
        fields = '__all__'

    def get_driver(self, obj):
        if obj.driver:
            return {
                "id": obj.driver.id,
                "name": obj.driver.full_name,
                "company": obj.driver.company.name
            }
        return None

    def get_dispatch(self, obj):
        if obj.dispatch:
            return {
                "id": obj.dispatch.id,
                "name": obj.dispatch.name,
                "company": obj.dispatch.company.name
            }
        return None


class DriverDispatcherWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverDispatcher
        fields = '__all__'
