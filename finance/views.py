
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Sum, Q
from .services import process_csv_file
from .serializers import TransactionSerializer
from .models import Transaction

class TransactionUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Upload a CSV file containing bank transactions",
        manual_parameters=[
            openapi.Parameter('file', openapi.IN_FORM, type=openapi.TYPE_FILE, description='CSV File'),
        ]
    )
    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"error": "No file provided."}, status=400)

        try:
            count = process_csv_file(file_obj, request.user)
            return Response({"message": f"Successfully uploaded {count} transactions."}, status=201)
            
        except Exception as e:
            return Response({"error": str(e)}, status=400)

class TransactionListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user).order_by('-date')
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    
class KPIReportView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get Financial KPI Summary",
        manual_parameters=[
            openapi.Parameter('start_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, format='date', description='YYYY-MM-DD'),
            openapi.Parameter('end_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, format='date', description='YYYY-MM-DD'),
        ]
    )
    def get(self, request):
        start_date = request.query_params.get('start_date', '2000-01-01')
        end_date = request.query_params.get('end_date', '2100-01-01')

        queryset = Transaction.objects.filter(
            user=request.user, 
            date__range=[start_date, end_date]
        )

        totals = queryset.aggregate(
            total_income=Sum('amount', filter=Q(transaction_type='credit')),
            total_expense=Sum('amount', filter=Q(transaction_type='debit')),
            net_cash_flow=Sum('amount')
        )

        top_categories = queryset.values('category').annotate(
            total=Sum('amount')
        ).order_by('total')[:5]

        data = {
            "period": {"start": start_date, "end": end_date},
            "total_income": totals['total_income'] or 0,
            "total_expense": totals['total_expense'] or 0,
            "net_cash_flow": totals['net_cash_flow'] or 0,
            "top_categories": top_categories
        }
        
        return Response(data)