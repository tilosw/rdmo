from rest_framework import serializers

from ..models import Project, Snapshot, Value


class ValueSerializer(serializers.ModelSerializer):

    attribute = serializers.CharField(source='attribute.uri', default=None, read_only=True)
    option = serializers.CharField(source='option.uri', default=None, read_only=True)

    class Meta:
        model = Value
        fields = (
            'attribute',
            'set_index',
            'collection_index',
            'text',
            'option',
            'value_type',
            'unit',
            'created',
            'updated'
        )


class SnapshotSerializer(serializers.ModelSerializer):

    values = serializers.SerializerMethodField()

    class Meta:
        model = Snapshot
        fields = (
            'title',
            'description',
            'values',
            'created',
            'updated'
        )

    def get_values(self, obj):
        values = Value.objects.filter(snapshot=obj)
        serializer = ValueSerializer(instance=values, many=True)
        return serializer.data


class ProjectSerializer(serializers.ModelSerializer):

    snapshots = SnapshotSerializer(many=True)
    values = serializers.SerializerMethodField()

    catalog = serializers.CharField(source='catalog.uri', default=None)

    class Meta:
        model = Project
        fields = (
            'title',
            'description',
            'catalog',
            'snapshots',
            'values',
            'created',
            'updated'
        )

    def get_values(self, obj):
        values = Value.objects.filter(project=obj, snapshot=None)
        serializer = ValueSerializer(instance=values, many=True)
        return serializer.data
