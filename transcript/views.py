import os

from rest_framework import views, parsers
from rest_framework import viewsets, mixins, permissions
from rest_framework.response import Response
from django.conf import settings

from models import Document, Line, Extract, ExtractLines
from serializers import (DocumentSerializer, LineSerializer, ExtractSerializer,
                         ExtractLinesSerializer, SimpleDocumentSerializer)

from document_loader import create_document


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

        with open(file_uri, 'wb+') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)

        doc = create_document(user, file_uri)
        serializer = SimpleDocumentSerializer(doc)
        return Response(serializer.data)
