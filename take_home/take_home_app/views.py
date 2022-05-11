from http.client import OK
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

accounts = []

class ResetView(APIView):

    def post(self, request):
        accounts.clear()
        return Response()

class EventView(APIView):

    def post(self, request):

        type = request.data.get('type')
        if type == "deposit":
            destination = request.data.get('destination')
            amount = request.data.get('amount')

            for account in accounts:
                if account.get('account_id') == destination:
                    account['balance'] += amount
                    return Response({'destination': {'id': destination, 'balance': account.get('balance')}}, status=status.HTTP_201_CREATED)
            
            accounts.append({'account_id': destination, 'balance': amount})
            return Response({'destination': {'id': destination, 'balance': amount}}, status=status.HTTP_201_CREATED)

class BalanceDetailsView(APIView):

    def get(self, request):
        
        account_id = self.request.GET.get('account_id') 

        for account in accounts:
            if account.get('account_id') == account_id:
                return Response(account.get('balance'))
        
        return Response(0, status=status.HTTP_404_NOT_FOUND)
        
