"""
URL configuration for coil app.
"""
from django.urls import path
from . import views

app_name = 'coil'

urlpatterns = [
    path('', views.index, name='index'),
    path('coilin/', views.coilin_list, name='coilin_list'),
    path('coilin/create/', views.CoilInCreateView.as_view(), name='coilin_create'),
    path('coilin/<int:pk>/', views.CoilInDetailView.as_view(), name='coilin_detail'),
    path('coilin/<int:pk>/update/', views.CoilInUpdateView.as_view(), name='coilin_update'),
    path('coilin/<int:pk>/delete/', views.CoilInDeleteView.as_view(), name='coilin_delete'),
    path('coilin/<int:pk>/add-pallet/', views.add_pallet, name='add_pallet'),
    path('coilin/<int:pk>/edit-pallet/<int:pallet_pk>/', views.add_pallet, name='edit_pallet'),
    path('coilin/<int:pk>/print-labels/', views.print_labels, name='print_labels'),
    path('labels/', views.label_list, name='label_list'),
    path('coilout/', views.CoilOutListView.as_view(), name='coilout_list'),
    path('coilout/create/', views.CoilOutCreateView.as_view(), name='coilout_create'),
    path('coilout/<int:pk>/', views.CoilOutDetailView.as_view(), name='coilout_detail'),
    path('coilout/<int:pk>/update/', views.CoilOutUpdateView.as_view(), name='coilout_update'),
    path('coilout/<int:pk>/delete/', views.CoilOutDeleteView.as_view(), name='coilout_delete'),
    path('api/get-sku/<int:pk>/', views.get_coil_sku, name='get_coil_sku'),
    path('api/get-job-details/<int:pk>/', views.get_job_details, name='get_job_details'),
    
    # Job URLs
    path('jobs/', views.JobListView.as_view(), name='job_list'),
    path('jobs/create/', views.JobCreateView.as_view(), name='job_create'),
    path('jobs/<int:pk>/update/', views.JobUpdateView.as_view(), name='job_update'),
    path('jobs/<int:pk>/delete/', views.JobDeleteView.as_view(), name='job_delete'),

    # List Views for Export
    path('sku/', views.SKUListView.as_view(), name='sku_list'),
    path('coilpallet/', views.CoilPalletListView.as_view(), name='coilpallet_list'),
    path('coilnumber/', views.CoilNumberListView.as_view(), name='coilnumber_list'),

    # Export URLs
    path('export/sku/excel/', views.export_sku_excel, name='export_sku_excel'),
    path('export/sku/csv/', views.export_sku_csv, name='export_sku_csv'),
    path('export/coilpallet/excel/', views.export_coilpallet_excel, name='export_coilpallet_excel'),
    path('export/coilpallet/csv/', views.export_coilpallet_csv, name='export_coilpallet_csv'),
    path('export/coilnumber/excel/', views.export_coilnumber_excel, name='export_coilnumber_excel'),
    path('export/coilnumber/csv/', views.export_coilnumber_csv, name='export_coilnumber_csv'),
]
