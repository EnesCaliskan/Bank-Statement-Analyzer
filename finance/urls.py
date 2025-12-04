from django.urls import path
from .views import TransactionUploadView, TransactionListView, KPIReportView

urlpatterns = [
    path('upload/', TransactionUploadView.as_view(), name='upload-csv'),
    path('list/', TransactionListView.as_view(), name='list-transactions'),
    path('reports/summary/', KPIReportView.as_view(), name='kpi-summary'),
]