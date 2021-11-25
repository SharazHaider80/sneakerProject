from django.shortcuts import render,redirect
from sneaerksdata.serializers import *
from .models import vendors,sneakers_data

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view

from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from django.db.models import *

class CustomPaginationClass(PageNumberPagination):
    page_size_query_param = 'size'

class SneakerViewSet(generics.ListAPIView):
    queryset = sneakers_data.objects.exclude(average_price__exact="nan").order_by('sku')
    serializer_class = sneakersSerializer
    pagination_class = CustomPaginationClass
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['product_name', 'sku','release_year','category']
    search_fields = ['product_name', 'sku', 'release_year','category']

class SneakerLow(generics.ListAPIView):
    queryset = sneakers_data.objects.exclude(average_price__exact="nan").order_by('average_price')
    serializer_class = sneakersSerializer
    pagination_class = CustomPaginationClass
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['product_name', 'sku', 'release_year','category']
    search_fields = ['product_name', 'sku', 'release_year','category']

class SneakerHigh(generics.ListAPIView):
    queryset = sneakers_data.objects.exclude(average_price__exact="nan").order_by('-average_price')
    serializer_class = sneakersSerializer
    pagination_class = CustomPaginationClass
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['product_name', 'sku', 'release_year','category']
    search_fields = ['product_name', 'sku', 'release_year','category']

# @csrf_exempt
# @api_view(['GET','POST','DELETE'])
# def sneakers_list(request):
#     if request.method == 'GET':
#         sneakers_list = sneakers_data.objects.all()
#
#         sneakers = sneakersSerializer(sneakers_list, many=True)
#
#         return JsonResponse(sneakers.data, safe=False, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['GET','POST','DELETE'])
def get_sneaker(request,pk):
    if request.method == 'GET':
        sneaker = sneakers_data.objects.filter(pk=pk).first()
        if not sneaker:
            return JsonResponse(data={"message": "Not any record"}, safe=False, status=status.HTTP_200_OK)
        sneaker = sneakersSerializer(sneaker)
        return JsonResponse(sneaker.data, safe=False, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET','POST','DELETE'])
def create_sneaker(request):
    if request.method == "POST":
        sneakers = JSONParser().parse(request)
        sneaker = sneakersSerializer(data = sneakers)

        if sneaker.is_valid():
            sneaker.save()
            return JsonResponse(sneaker.data,status=status.HTTP_201_CREATED)
        return JsonResponse(sneaker.errors,status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET','PUT','DELETE'])
def update_sneaker(request,pk):
    sneaker = sneakers_data.objects.get(pk=pk)
    if request.method == "PUT":
        sneakers = JSONParser().parse(request)

        sneaker = sneakersSerializer(sneaker, data = sneakers)

        if sneaker.is_valid():
            sneaker.save()
            return JsonResponse(sneaker.data,status=status.HTTP_200_OK)
        return JsonResponse(sneaker.errors,status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET','PUT','DELETE'])
def delete_sneaker(request,pk):
    sneaker = sneakers_data.objects.get(pk=pk)
    if request.method == "DELETE":
        sneaker.delete()
        return JsonResponse(data={"message":"Product deleted successfully"},status=status.HTTP_204_NO_CONTENT)



######################
######  Vendor  ######
######################


@csrf_exempt
@api_view(['GET','POST','DELETE'])
def vendors_list(request):
    if request.method == 'GET':
        vendors_list = vendors.objects.all()

        v = vendorsSerializer(vendors_list, many=True)

        return JsonResponse(v.data, safe=False, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['GET','POST','DELETE'])
def get_vendor(request,pk):
    if request.method == 'GET':
        vendor = vendors.objects.filter(pk=pk).first()
        if not vendor:
            return JsonResponse(data={"message":"Not any record"}, safe=False, status=status.HTTP_200_OK)
        vendor = vendorsSerializer(vendor)
        return JsonResponse(vendor.data, safe=False, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET','POST','DELETE'])
def create_vendor(request):
    if request.method == "POST":
        vendors = JSONParser().parse(request)

        vendor = vendorsSerializer(data = vendors)

        if vendor.is_valid():
            vendor.save()
            return JsonResponse(vendor.data,status=status.HTTP_201_CREATED)
        return JsonResponse(vendor.errors,status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET','PUT','DELETE'])
def update_vendor(request,pk):
    vendor = vendors.objects.get(pk=pk)
    if request.method == "PUT":
        data = JSONParser().parse(request)
        vendor = vendorsSerializer(vendor, data = data)

        if vendor.is_valid():
            vendor.save()
            return JsonResponse(vendor.data,status=status.HTTP_200_OK)
        return JsonResponse(vendor.errors,status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET','PUT','DELETE'])
def delete_vendor(request,pk):
    vendor = vendors.objects.get(pk=pk)
    if request.method == "DELETE":
        vendor.delete()
        return JsonResponse({"message":"Vendor deleted successfully"},status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['GET','POST','DELETE'])
def product_vendor(request,sku):
    if request.method == "GET":
        # query = sneakers_data.objects.filter(sku=sku).values_list('vendor_id').all()
        # query= vendors.objects.filter(id__in=query)
        #
        # v = vendorsSerializer(query,many=True)
        #
        # return JsonResponse(data={sku: v.data}, safe=False, status=status.HTTP_200_OK)

        query = sneakers_data.objects.filter(sku=sku).order_by("vendor_id").distinct("vendor_id")
        l = []
        for row in query:
            dict = {"id":row.vendor_id.id,"vendor_name":row.vendor_id.vendor_name,"vendor_url":row.vendor_id.vendor_url,"availability":row.vendor_id.availability,"price":row.average_price}
            l.append(dict)
        return JsonResponse(data={sku: l}, safe=False, status=status.HTTP_200_OK)

##############################################################
##############################################################
################ Excel Insertion and Simplyfy in sheets ###################
################ Excel Insertion and Simplyfy in sheets ###################
##############################################################
##############################################################
@csrf_exempt
@api_view(['GET','POST','DELETE'])
def sheet_simlpyfy(request):
    import pandas as pd
    import csv
    import xlrd
    import numpy as np

    file = 'C:/Users/Umair/Desktop/goat.csv'
    df = pd.read_csv(file)

    df = df.values.tolist()

    for i in df[0]:
        print(type(i))
    ###################
    #Image extract code
    ###################

    # file = 'C:/Users/Umair/Desktop/goat.csv'
    #
    # read_file = pd.read_csv(file)
    # goat = [i for i in read_file["p_id"] if i!="nan"]
    # goat = goat
    # file2 = 'C:/Users/Umair/Desktop/goat_image.xlsx'
    # read_file = pd.read_excel(file2)
    # image = [i for i in read_file2["product_id"] if i!="nan"]
    # image = set(image)
    # unique = goat & image
    # goat = [int(i) for i in unique]
    # read_file1[read_file1['p_id'].isin(goat)].to_csv('C:/Users/Umair/Desktop/goat.csv',index=False)


    # csv_file = 'C:/Users/Umair/Desktop/image.csv'
    # dict_data = list()
    # csv_columns = ['id','image']
    # for i in goat:
    #     r = read_file.query("product_id=={d}".format(d=i))[['url']]
    #     d = {'id':i,'image':[j for j in r['url']]}
    #     dict_data.append(d)

    # print(len(dict_data))
    # with open(csv_file, 'w',newline='') as csvfile:
    #     writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    #     writer.writeheader()
    #     for data in dict_data:
    #         writer.writerow(data)

    ###################
    # price extract code
    ###################
    # file = 'C:/Users/Umair/Desktop/prices.xlsx'
    #
    # df = pd.read_excel(file)
    # df_list = df.values.tolist()
    # l = list()
    # count = 0
    # val1 = 0
    # val2 = 0
    # for row in df_list:
    #     row = np.array(row)
    #     # count+=1
    #     # print(count)
    #     if len(row[np.nonzero(row)]) == 0:
    #         v1 = val1
    #         v2 = val2
    #     else:
    #         v1 = np.min(row[np.nonzero(row)])
    #         v2 = np.max(row[np.nonzero(row)])
    #     val = [v1,v2]
    #     l.append(val)
    #
    # print(len(l))
    #
    # csv_file = 'C:/Users/Umair/Desktop/min.csv'
    # with open(csv_file, 'w',newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     for data in l:
    #         writer.writerow(data)


    return JsonResponse({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(['GET','POST','DELETE'])
def insert_excel_goat(request):
    import pandas as pd

    file = 'sneaerksdata/goat.csv'
    read_file = pd.read_csv(file)
    df_list = read_file.values.tolist()
    vendor = vendors.objects.get(id=1)

    for i in df_list:
        r = i[16]
        r = [i.replace(',', '').replace('\'', '').replace('[', '').replace(']', '') for i in r.split()]
        sneaker = sneakers_data(product_name=i[1], product_type=i[2],
                                lowest_price=i[3],highest_price=i[4],
                                brand_name=i[5],color=i[6],designer=i[7],
                                category=i[8],
                                nick_name=i[9],release_date=i[10],release_year=i[11],
                                slug=i[12],
                                description=i[13],material=i[14],
                                sku=i[15],
                                images=r,
                                vendor_id=vendor)
        sneaker.save(force_insert=True)

    for row in sneakers_data.objects.filter(average_price='nan'):
        row.delete()

    return JsonResponse({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(['GET','POST','DELETE'])
def insert_excel_stadium(request):
    import pandas as pd
    file = 'sneaerksdata/stadiumgoods_data.xlsx'
    read_file = pd.read_excel(file)
    df_list = read_file.values.tolist()
    vendor = vendors.objects.get(id=2)

    for i in df_list:
        r = i[11]
        r = [i.replace(',', '').replace('\'', '').replace('[', '').replace(']', '') for i in r.split()]
        sneaker = sneakers_data(product_name=i[1],
                                lowest_price=i[2], highest_price=i[3],
                                brand_name=i[4], color=i[5],
                                category=i[6],
                                slug=i[7],
                                description=i[8], material=i[9],
                                sku=i[10],
                                images=r,
                                vendor_id=vendor)
        sneaker.save(force_insert=True)

    for row in sneakers_data.objects.filter(average_price='nan'):
        row.delete()

    return JsonResponse({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



@csrf_exempt
@api_view(['GET','POST','DELETE'])
def insert_excel_stockx(request):
    # rows = sneakers_data.objects.filter(vendor_id=4)
    # for row in rows:
    #     row.delete()
    import pandas as pd
    file = 'sneaerksdata/stockx_data.xlsx'
    read_file = pd.read_excel(file)
    df_list = read_file.values.tolist()
    vendor = vendors.objects.get(id=3)

    for i in df_list:
        sneaker = sneakers_data(product_name=i[1], product_type=i[2],
                                lowest_price=i[3], highest_price=i[4],
                                brand_name=i[5], color=i[6],
                                category=i[7],
                                release_date=i[8], release_year=i[9],
                                description=i[10],
                                sku=i[11],
                                images=[i[12]],
                                vendor_id=vendor)
        sneaker.save(force_insert=True)

    for row in sneakers_data.objects.filter(average_price='nan'):
        row.delete()

    return JsonResponse({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


