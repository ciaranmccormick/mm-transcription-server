from django.contrib.auth.models import User
from rest_framework import serializers
from models import (Document, Line, Extract, ExtractLines, IType, IMode,
                    Purpose, InformationFlow, RoleExpectation, RoleRelationship,
                    PlaceLocation, PlaceNorm, IAttrRef, IAttr)


class IAttrRefSerializer(serializers.ModelSerializer):
    class Meta:
        model = IAttrRef
        fields = '__all__'


class IAttrSerializer(serializers.ModelSerializer):
    attr = IAttrRefSerializer()

    class Meta:
        model = IAttr
        fields = '__all__'


class WriteIAttrSerializer(serializers.ModelSerializer):
    class Meta:
        model = IAttr
        fields = '__all__'


class PlaceLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceLocation
        fields = '__all__'


class PlaceNormSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceNorm
        fields = '__all__'


class InformationFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformationFlow
        fields = '__all__'


class ITypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IType
        fields = '__all__'


class IPurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purpose
        fields = '__all__'


class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleRelationship
        fields = '__all__'


class ExpectationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleExpectation
        fields = '__all__'


class IModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IMode
        fields = '__all__'


class LineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Line
        fields = '__all__'


class ExtractLinesSerializer(serializers.ModelSerializer):
    line = LineSerializer()

    class Meta:
        model = ExtractLines
        fields = '__all__'
        read_only_fields = ('extract',)


class ReadOnlyExtractSerializer(serializers.ModelSerializer):
    extract_lines = ExtractLinesSerializer(many=True)
    i_type = ITypeSerializer()
    i_mode = IModeSerializer()
    i_purpose = IPurposeSerializer(many=True)
    relationships = RelationshipSerializer(many=True)
    expectations = ExpectationSerializer(many=True)
    info_flow = InformationFlowSerializer()
    locations = PlaceLocationSerializer(many=True)
    norms = PlaceNormSerializer(many=True)
    i_attrs = IAttrSerializer(many=True)

    class Meta:
        model = Extract
        fields = ('id', 'document', 'context', 'extract_lines', 'completed',
                  'i_type', 'i_mode', 'i_purpose', 'info_flow', 'relationships',
                  'expectations', 'locations', 'norms', 'i_attrs', 'tag')


class ExtractSerializer(serializers.ModelSerializer):
    extract_lines = ExtractLinesSerializer(many=True)

    class Meta:
        model = Extract
        fields = '__all__'
        include = ('extract_lines',)

    def create(self, validated_data):
        lines_data = validated_data.pop('extract_lines')
        extract = Extract.objects.create(**validated_data)

        for line_data in lines_data:
            line = line_data.pop('line')
            line = Line.objects.get(**line)
            ExtractLines.objects.create(extract=extract, line=line)

        return extract


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'id')


class DocumentSerializer(serializers.ModelSerializer):
    lines = LineSerializer(many=True, read_only=True)
    extracts = ExtractSerializer(many=True, read_only=True)
    owner = OwnerSerializer(read_only=True)

    class Meta:
        model = Document
        fields = '__all__'


class DocumentExtractSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = ('id', 'extracts',)


class SimpleDocumentSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)

    class Meta:
        model = Document
        fields = ('id', 'date', 'filename', 'owner')
