"""transcript URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from . import views
from rest_framework.authtoken import views as drfviews

router = routers.DefaultRouter()
router.register("documents", views.DocumentViewSet, base_name='documents')
router.register("users", views.UserViewSet, base_name='user')
router.register("document", views.RetrieveDocumentViewSet, base_name='document')
router.register("line", views.LineViewSet, base_name='line')
router.register("extract", views.ExtractViewSet, base_name='extract')
router.register("extract-lines", views.ExtractLinesViewSet,
                base_name='extract-lines')
router.register("read-extract", views.ReadOnlyExtractViewSet,
                base_name='read-extract')
router.register("i-type", views.ITypeViewSet,
                base_name='i-type')
router.register("i-mode", views.IModeViewSet,
                base_name='i-mode')
router.register("info-flow", views.InformationFlowViewSet,
                base_name='info-flow')
router.register("role-relationship", views.RelationshipViewSet,
                base_name='role-relationship')
router.register("role-expectation", views.ExpectationViewSet,
                base_name='role-expectation')
router.register("place-location", views.PlaceLocationViewSet,
                base_name='place-location')
router.register("place-norm", views.PlaceNormViewSet,
                base_name='place-norm')
router.register("i-attr-ref", views.IAttrRefViewSet,
                base_name='i-attr-ref')
router.register("i-attr", views.IAttrViewSet,
                base_name='i-attr')
router.register("i-purpose", views.IPurposeViewSet,
                base_name='i-purpose')
router.register("document-extract", views.ExtractIdViewSet,
                base_name='document-extract')
router.register("recodes", views.RecodeViwSet,
                base_name='recode')
router.register("recode-extracts", views.RecodeExtractViewSet,
                base_name='recode-extract')
router.register("recode-extracts-context", views.RecodeContextualLinesViewSet,
                base_name='recode-extract-context')


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'api/', include(router.urls)),
    url(r'^upload/(?P<filename>[^/]+)$', views.TranscriptUploader.as_view()),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^api-token-auth/', drfviews.obtain_auth_token)
]
