from http.client import OK
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse

accounts = []

class ResetView(APIView):

    def post(self, request):
        accounts.clear()
        response = HttpResponse("OK", content_type="text/plain")
        return response
        
class EventView(APIView):

    def post(self, request):

        type = request.data.get('type')
        amount = request.data.get('amount')

        if type == "deposit":
            destination = request.data.get('destination')
            
            for account in accounts:
                if account.get('account_id') == destination:
                    account['balance'] += amount
                    return Response({'destination': {'id': destination, 'balance': account.get('balance')}}, status=status.HTTP_201_CREATED)
            
            accounts.append({'account_id': destination, 'balance': amount})
            return Response({'destination': {'id': destination, 'balance': amount}}, status=status.HTTP_201_CREATED)

        elif type == "withdraw":
            origin = request.data.get('origin')
            
            for account in accounts:
                if account.get('account_id') == origin:
                    account['balance'] -= amount
                    return Response({'origin': {'id': origin, 'balance': account.get('balance')}}, status=status.HTTP_201_CREATED)

            return Response(0, status=status.HTTP_404_NOT_FOUND)
        
        elif type == "transfer":
            origin = request.data.get('origin')
            destination = request.data.get('destination')
            origin_balance = 0
            found = False

            for account in accounts:
                if account.get('account_id') == origin:
                    account['balance'] -= amount
                    origin_balance = account.get('balance')
                    found = True
                    break
            
            if not found:
                return Response(0, status=status.HTTP_404_NOT_FOUND)
                
            for acc in accounts:
                if acc.get('account_id') == destination:
                    account['balance'] += amount
                    return Response({'origin': {'id': origin, 'balance': origin_balance}, 'destination': {'id': destination, 'balance': account.get('balance')}}, status=status.HTTP_201_CREATED)
            
            accounts.append({'account_id': destination, 'balance': amount})
            return Response({'origin': {'id': origin, 'balance': origin_balance}, 'destination': {'id': destination, 'balance': amount}}, status=status.HTTP_201_CREATED)

class BalanceDetailsView(APIView):

    def get(self, request):
        
        account_id = self.request.GET.get('account_id') 

        for account in accounts:
            if account.get('account_id') == account_id:
                return Response(account.get('balance'))
        
        return Response(0, status=status.HTTP_404_NOT_FOUND)
        
