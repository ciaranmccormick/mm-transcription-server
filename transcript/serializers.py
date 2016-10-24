from django.contrib.auth.models import User
from rest_framework import serializers
from models import Document, Line, Extract, ExtractLines


class LineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Line
        fields = '__all__'
        read_only_fields = ('line_num', 'text')


class ExtractLinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtractLines
        fields = ('line',)


class ReadOnlyExtractLinesSerializer(serializers.ModelSerializer):
    line = LineSerializer()

    class Meta:
        model = ExtractLines
        fields = ('line',)


class ReadOnlyExtractSerializer(serializers.ModelSerializer):
    extract_lines = ReadOnlyExtractLinesSerializer(many=True)

    class Meta:
        model = Extract
        fields = ('document', 'context', 'extract_lines')


class ExtractSerializer(serializers.ModelSerializer):
    extract_lines = ExtractLinesSerializer(many=True)

    class Meta:
        model = Extract
        fields = ('document', 'context', 'extract_lines')

    def create(self, validated_data):
        lines_data = validated_data.pop('extract_lines')
        extract = Extract.objects.create(**validated_data)

        for line_data in lines_data:
            ExtractLines.objects.create(extract=extract, **line_data)

        return extract


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'id')


class DocumentSerializer(serializers.ModelSerializer):
    lines = LineSerializer(many=True, read_only=True)
    extracts = ReadOnlyExtractSerializer(many=True, read_only=True)
    owner = OwnerSerializer(read_only=True)

    class Meta:
        model = Document
        fields = '__all__'


class SimpleDocumentSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)

    class Meta:
        model = Document
        fields = ('id', 'date', 'filename', 'owner')
