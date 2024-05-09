from django.shortcuts import render
from django.db.models import *
from django.db import transaction
from sistema_fcc_api.serializers import *
from sistema_fcc_api.models import *
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.utils.html import strip_tags
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from datetime import datetime
from django.conf import settings
from django.template.loader import render_to_string
import string
import random
import json

import json

    
class MateriasAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        materias = Materia.objects.order_by("id")
        materias = MateriaSerializer(materias, many=True).data
       
        if not materias:
            return Response({}, 400)
        
        for materia in materias:
            materia["dias"] = json.loads(materia["dias"])
   
            
        return Response(materias, 200)

        
    
class MateriasView(generics.CreateAPIView):
    #Obtener usuario por ID
    # permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        materia = get_object_or_404(Materia, id = request.GET.get("id"))
        materia = MateriaSerializer(materia, many=False).data
        materia["dias"] = json.loads(materia["dias"])
        return Response(materia, 200)
    
    #Registrar nuevo usuario
    @transaction.atomic
    def post(self, request, *args, **kwargs):
            
         #Agarra los datos de la materia
        nrc = request.data['nrc']
        nombre_materia = request.data['nombre_materia']
        seccion = request.data['seccion']
        dias = json.dumps(request.data['dias'])
        hora_inicio = request.data ['hora_inicio']
        hora_fin = request.data['hora_fin']
        salon = request.data['salon']
        programa_educativo = request.data['programa_educativo']



        # creacion de la materia 
        materia = Materia.objects.create(
                nrc = nrc,
                nombre_materia = nombre_materia,
                seccion = seccion,
                dias = dias,
                hora_inicio = hora_inicio,
                hora_fin = hora_fin,
                salon = salon,
                programa_educativo = programa_educativo,
        )

        materia.save()

        return Response({"materia_created_id": materia.id}, status=status.HTTP_201_CREATED)
        return Response(materia.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MateriasViewEdit(generics.CreateAPIView):
    permissions_classes = (permissions.IsAuthenticated,)
    
    def put(self, request, *args, **kwargs):
        materia = get_object_or_404(Materia, id=request.data["id"])
        materia.nrc = request.data["nrc"]
        materia.nombre_materia = request.data["nombre_materia"]
        materia.seccion = request.data["seccion"]
        materia.dias = json.dumps(request.data["dias"])
        materia.hora_inicio = request.data["hora_inicio"]
        materia.hora_fin = request.data["hora_fin"]
        materia.salon = request.data["salon"]
        materia.programa_educativo = request.data["programa_educativo"]
        materia.save()


        mat = MateriaSerializer(materia, many=False).data
        
        return Response(mat,200)
        
    
    def delete(self, request, *args, **kwargs):
        materia = get_object_or_404(Materia, id=request.GET.get("id"))
        try:
            materia.delete()
            return Response({"details":"Materia eliminada"},200)
        except Exception as e:
            return Response({"details":"Algo pasó al eliminar"},400)
    
    