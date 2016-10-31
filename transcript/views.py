import os

from django.conf import settings
from rest_framework import views, parsers
from rest_framework import viewsets, mixins, permissions
from rest_framework.response import Response

from document_loader import create_document
from models import (Document, Line, Extract, ExtractLines, IType, IMode,
                    Purpose, InformationFlow, RoleExpectation, RoleRelationship,
                    PlaceLocation, PlaceNorm, IAttrRef, IAttr)
from serializers import (DocumentSerializer, LineSerializer, ExtractSerializer,
                         ExtractLinesSerializer, SimpleDocumentSerializer,
                         ReadOnlyExtractSerializer, ITypeSerializer,
                         IModeSerializer, IPurposeSerializer,
                         InformationFlowSerializer, ExpectationSerializer,
                         RelationshipSerializer, PlaceLocationSerializer,
                         PlaceNormSerializer, IAttrRefSerializer,
                         WriteIAttrSerializer)


class IAttrViewSet(viewsets.ModelViewSet):
    queryset = IAttr.objects.all()
    serializer_class = WriteIAttrSerializer
    permission_classes = (permissions.IsAuthenticated,)


def create_i_attr():
    attributes = [
        {
            'name': 'accurate',
            'label': 'Accurate',
            'description': 'blah blah blah',
        },
        {
            'name': 'complete',
            'label': 'Complete',
            'description': '',
        },

        {
            'name': 'fresh',
            'label': 'Fresh',
            'description': ''
        },

        {
            'name': 'ontime',
            'label': 'On-Time',
            'description': ''
        },
        {
            'name': 'actionable',
            'label': 'Actionable',
            'description': ''
        },
        {
            'name': 'convenience',
            'label': 'Convenience',
            'description': ''
        },
        {
            'name': 'personalised',
            'label': 'Personalised',
            'description': ''
        }]

    for attr in attributes:
        name = attr.pop('name')
        try:
            IAttrRef.objects.get(name=name)
        except IAttrRef.DoesNotExist:
            IAttrRef.objects.create(name=name, **attr)


class IAttrRefViewSet(viewsets.ModelViewSet):
    queryset = IAttrRef.objects.all()
    serializer_class = IAttrRefSerializer
    permission_classes = (permissions.IsAuthenticated,)


class PlaceLocationViewSet(viewsets.ModelViewSet):
    queryset = PlaceLocation.objects.all()
    serializer_class = PlaceLocationSerializer
    permission_classes = (permissions.IsAuthenticated,)


class PlaceNormViewSet(viewsets.ModelViewSet):
    queryset = PlaceNorm.objects.all()
    serializer_class = PlaceNormSerializer
    permission_classes = (permissions.IsAuthenticated,)


class InformationFlowViewSet(viewsets.ModelViewSet):
    queryset = InformationFlow.objects.all()
    serializer_class = InformationFlowSerializer
    permission_classes = (permissions.IsAuthenticated,)


class RelationshipViewSet(viewsets.ModelViewSet):
    queryset = RoleRelationship.objects.all()
    serializer_class = RelationshipSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ExpectationViewSet(viewsets.ModelViewSet):
    queryset = RoleExpectation.objects.all()
    serializer_class = ExpectationSerializer
    permission_classes = (permissions.IsAuthenticated,)


class IPurposeViewSet(viewsets.ModelViewSet):
    queryset = Purpose.objects.all()
    serializer_class = IPurposeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class IModeViewSet(viewsets.ModelViewSet):
    queryset = IMode.objects.all()
    serializer_class = IModeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ITypeViewSet(viewsets.ModelViewSet):
    queryset = IType.objects.all()
    serializer_class = ITypeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class DocumentViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin):
    queryset = Document.objects.all()
    serializer_class = SimpleDocumentSerializer
    permission_classes = (permissions.IsAuthenticated,)


class RetrieveDocumentViewSet(viewsets.GenericViewSet,
                              mixins.RetrieveModelMixin):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = (permissions.IsAuthenticated,)


class LineViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin):
    queryset = Line.objects.all()
    serializer_class = LineSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ExtractViewSet(viewsets.ModelViewSet):
    queryset = Extract.objects.all()
    serializer_class = ExtractSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ReadOnlyExtractViewSet(viewsets.ModelViewSet):
    queryset = Extract.objects.all()
    serializer_class = ReadOnlyExtractSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ExtractLinesViewSet(viewsets.ModelViewSet):
    queryset = ExtractLines.objects.all()
    serializer_class = ExtractLinesSerializer
    permission_classes = (permissions.IsAuthenticated,)


class TranscriptUploader(views.APIView):
    parser_classes = (parsers.FileUploadParser,)
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        user = request.user
        file_uri = os.path.join(settings.TEMP_DIR, filename)

        with open(file_uri, 'w') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)

        doc = create_document(user, file_uri)
        serializer = SimpleDocumentSerializer(doc)
        return Response(serializer.data)
