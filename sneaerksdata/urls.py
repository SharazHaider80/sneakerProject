from django.urls import path,include
from sneaerksdata import views

urlpatterns = [

    # search
    # path('api/search_sneaker',views.search_sneakers),
    path('api/sneaker/', views.SneakerViewSet.as_view()),
    path('api/searchlow/', views.SneakerLow.as_view()),
    path('api/searchhigh/', views.SneakerHigh.as_view()),

    #Sneakers URLS
    # path('api/sneakers_list',views.SneakerList.as_view()),
    path('api/create_sneaker',views.create_sneaker),
    path('api/get_sneaker/<str:pk>',views.get_sneaker),
    path('api/update_sneaker/<str:pk>',views.update_sneaker),
    path('api/delete_sneaker/<str:pk>',views.delete_sneaker),

    #Vendors URLS
    path('api/vendors_list',views.vendors_list),
    path('api/create_vendor',views.create_vendor),
    path('api/get_vendor/<str:pk>',views.get_vendor),
    path('api/update_vendor/<str:pk>',views.update_vendor),
    path('api/delete_vendor/<str:pk>',views.delete_vendor),
    path('api/product_vendor/<str:sku>',views.product_vendor),

    #insertion URLS
    path('api/insert_excel_goat',views.insert_excel_goat),
    path('api/insert_excel_stadium',views.insert_excel_stadium),
    path('api/insert_excel_stockx',views.insert_excel_stockx),
]