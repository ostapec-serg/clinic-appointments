from rest_framework.generics import GenericAPIView, ListAPIView

from django_filters.rest_framework import DjangoFilterBackend

from doctors.filters import DoctorsFilter
from doctors.models import Doctor
from doctors.serializers import DoctorSerializer


class DoctorsAPIView(ListAPIView, GenericAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DoctorsFilter

