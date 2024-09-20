from uuid import UUID
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.core.category.application.use_cases.update_category import UpdateCategoryRequest, UpdateCategory
from src.core.category.application.use_cases.create_category import CreateCategory, CreateCategoryRequest
from django_project.category_app.serializers import CreateCategoryRequestSerializer, CreateCategoryResponseSerializer, ListCategoryResponseSerializer, RetrieveCategoryRequestSerializer, RetrieveCategoryResponseSerializer, UpdateCategoryRequestSerializer
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest
from django_project.repository import DjangoORMCategoryRepository
from src.core.category.application.use_cases.list_category import ListCategory, ListCategoryRequest, ListCategoryResponse

# Create your views here.
class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        input = ListCategoryRequest()
        use_case = ListCategory(repository=DjangoORMCategoryRepository())
        output = use_case.execute(request=input)

        # categories = [ 
        #     {
        #         "id": str(category.id),
        #         "name": category.name,
        #         "description": category.description,
        #         "is_active": category.is_active
        #     } for category in output.data
        # ]

        serializer = ListCategoryResponseSerializer(instance=output)
        
        return Response(
            status=HTTP_200_OK,
            data=serializer.data
        )
    
    def retrieve(self, request: Request, pk=None):
            serializer = RetrieveCategoryRequestSerializer(data={"id": pk})
            serializer.is_valid(raise_exception=True)
            
            input = GetCategoryRequest(id=serializer.validated_data["id"])
            use_case = GetCategory(repository=DjangoORMCategoryRepository())

            try:
                result = use_case.execute(request=input)
            except CategoryNotFound:
                return Response(status=HTTP_404_NOT_FOUND)
            
            # category_output = {
            #    "id": str(result.id),
            #    "name": result.name ,
            #    "description": result.description,
            #    "is_active": result.is_active
            # }

            category_output = RetrieveCategoryResponseSerializer(instance=result)
            

            return Response(
                status=HTTP_200_OK,
                data=category_output.data
            )
    
    def create(self, request: Request):
         serializer = CreateCategoryRequestSerializer(data=request.data)
         serializer.is_valid(raise_exception=True)

         input = CreateCategoryRequest(**serializer.validated_data)
         use_case = CreateCategory(repository=DjangoORMCategoryRepository())
         output = use_case.execute(request=input)

         return Response(
              status=HTTP_201_CREATED,
              data=CreateCategoryResponseSerializer(instance=output).data
         )
    
    def update(self, request: Request, pk=None) -> Response:
         serializer = UpdateCategoryRequestSerializer(data={**request.data.dict(),"id": pk})
         serializer.is_valid(raise_exception=True)

         input = UpdateCategoryRequest(**serializer.validated_data)
         use_case = UpdateCategory.execute(repository=DjangoORMCategoryRepository())
         use_case.execute(request=input)
         return Response(
              status=HTTP_204_NO_CONTENT
         )
            
