import os

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import views, parsers
from rest_framework import viewsets, mixins, permissions
from rest_framework.response import Response

from document_loader import create_document
from models import (Document, Line, Extract, ExtractLines, IType, IMode,
                    Purpose, InformationFlow, RoleExpectation, RoleRelationship,
                    PlaceLocation, PlaceNorm, IAttrRef, IAttr,
                    Recode, RecodeExtract)
from serializers import (DocumentSerializer, LineSerializer, ExtractSerializer,
                         ExtractLinesSerializer, SimpleDocumentSerializer,
                         ReadOnlyExtractSerializer, ITypeSerializer,
                         IModeSerializer, IPurposeSerializer,
                         InformationFlowSerializer, ExpectationSerializer,
                         RelationshipSerializer, PlaceLocationSerializer,
                         PlaceNormSerializer, IAttrRefSerializer,
                         WriteIAttrSerializer, DocumentExtractSerializer,
                         RecodeSerializer, OwnerSerializer,
                         RecodeExtractSerializer)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = OwnerSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


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


class ExtractIdViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentExtractSerializer
    permission_classes = (permissions.IsAuthenticated,)


class TranscriptUploader(views.APIView):
    parser_classes = (parsers.FileUploadParser,)
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        user = request.user
        file_uri = os.path.join(settings.TEMP_DIR, filename)

        with open(file_uri, 'wb+') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)

        doc = create_document(user, file_uri)
        serializer = SimpleDocumentSerializer(doc)
        return Response(serializer.data)


class RecodeViwSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Recode.objects.all()
    serializer_class = RecodeSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.user.id

        user = User.objects.get(id=user_id)
        recode = Recode.objects.create(recoder=user)
        serializer = RecodeSerializer(recode)
        return Response(serializer.data)


class RecodeExtractViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = RecodeExtract.objects.all()
    serializer_class = RecodeExtractSerializer


class ReRecodeExtractViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = get_re_recodes()
    serializer_class = RecodeExtractViewSet


class RecodeContextualLinesViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LineSerializer

    def get_queryset(self):
        extract_id = self.request.query_params.get('extract_id', None)

        if extract_id is not None:
            extract = RecodeExtract.objects.get(id=extract_id).extract
            extract_lines = extract.extract_lines
            document_id = extract_lines.first().line.document.id
            start_line = extract_lines.first().line.id - 3
            end_line = extract_lines.last().line.id + 3

            lines = Line.objects.filter(id__gte=start_line, id__lte=end_line,
                                        document=document_id)

            return lines
        else:
            return Line.objects.all()


def get_re_recodes():
    recodes = get_recodes(include_noc=False)
    recodes = recodes.exclude(
        recode_context__regex='n[be]', extract__context__regex='n[be]').exclude(
        recode_context__regex='p[be]', extract__context__regex='p[be]')

    return recodes


def get_recodes(include_noc=True):
    recodes = RecodeExtract.objects.all()
    if not include_noc:
        recodes = recodes.exclude(extract__context='noc')
    else:
        pass

    return recodes
