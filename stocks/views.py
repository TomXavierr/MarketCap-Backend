from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.db import IntegrityError

from .models import Stock, Watchlist
from .serializers import StockSerializer, TickerSearchSerializer, StockInfoSerializer
import requests

# Create your views here.
class AddStockToWatchlistAPIView(APIView):
    permission_classes = [AllowAny]
    
    
    def post(self, request):
        stock_symbol = request.data.get('symbol', '')

        try:
            stock = Stock.objects.get(symbol=stock_symbol)
        except Stock.DoesNotExist:
            serializer = StockSerializer(data=request.data)
            if serializer.is_valid():
                stock = serializer.save()  
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        watchlist, created = Watchlist.objects.get_or_create(user=user)
        
        if watchlist.stocks.filter(id=stock.id).exists():
            return Response({'success': False, 'message': 'Stock already exists in watchlist'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            watchlist.stocks.add(stock)
            return Response({'success': True, 'message': 'Stock added to watchlist'}, status=status.HTTP_201_CREATED)
  
class WatchlistStocksAPIView(APIView):
    def get(self, request):
        api_key = 'BAYG7WDR7GLZ6ZI'
        user = request.user
        watchlist = Watchlist.objects.get(user=user)
        symbols = [stock.symbol for stock in watchlist.stocks.all()]

        stock_info = []
        for symbol in symbols:
            response = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={api_key}')
            if response.ok:
                data = response.json()
                
                meta_data = data.get("Meta Data", {})
                time_series = data.get("Time Series (5min)", {})
                latest_timestamp = max(time_series.keys())
                latest_data = time_series[latest_timestamp]
                
                
                stock_dict = {
                    "Name": meta_data.get("2. Symbol", ""),
                    "open": latest_data.get("1. open", ""),
                    "high": latest_data.get("2. high", ""),
                    "low": latest_data.get("3. low", ""),
                    "close": latest_data.get("4. close", ""),
                    
                }
                stock_info.append(stock_dict)

        serializer = StockInfoSerializer(stock_info, many=True)
        return Response(serializer.data)      
        

class TickerSearchAPIView(APIView):
    def get(self, request):
        serializer = TickerSearchSerializer(data=request.query_params)
        if serializer.is_valid():
            keywords = serializer.validated_data['keywords']
            api_url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keywords}&apikey=your_api_key"  
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Failed to fetch data from Alpha Vantage'}, status=response.status_code)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GlobalMarketStatusAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, format=None):
        api_key = 'BAYG7WDR7GLZ6ZI'
        url = f'https://www.alphavantage.co/query?function=MARKET_STATUS&apikey={api_key}'
        
        # response = requests.get(url)
        # data = response.json()
        
        # selected_markets = [market for market in data['markets'] if market['region'] in ['United States', 'United Kingdom', 'India']]
        
        # response_data = {
        #     'endpoint': data['endpoint'],
        #     'markets': selected_markets
        # }
        response_data = {
            "endpoint": "Global Market Open & Close Status",
            "markets": [
                {
                    "market_type": "Equity",
                    "region": "United States",
                    "primary_exchanges": "NASDAQ, NYSE, AMEX, BATS",
                    "local_open": "09:30",
                    "local_close": "16:15",
                    "current_status": "closed",
                    "notes": ""
                },
                {
                    "market_type": "Equity",
                    "region": "Canada",
                    "primary_exchanges": "Toronto, Toronto Ventures",
                    "local_open": "09:30",
                    "local_close": "16:00",
                    "current_status": "closed",
                    "notes": ""
                },
                {
                    "market_type": "Equity",
                    "region": "United Kingdom",
                    "primary_exchanges": "London",
                    "local_open": "08:00",
                    "local_close": "16:30",
                    "current_status": "open",
                    "notes": ""
                },
                {
                    "market_type": "Equity",
                    "region": "Germany",
                    "primary_exchanges": "XETRA, Berlin, Frankfurt, Munich, Stuttgart",
                    "local_open": "08:00",
                    "local_close": "20:00",
                    "current_status": "open",
                    "notes": ""
                },
                
                {
                    "market_type": "Equity",
                    "region": "Japan",
                    "primary_exchanges": "Tokyo",
                    "local_open": "09:00",
                    "local_close": "15:00",
                    "current_status": "closed",
                    "notes": "Noon trading break from 11:30 to 12:30 local time"
                },
                {
                    "market_type": "Equity",
                    "region": "India",
                    "primary_exchanges": "NSE, BSE",
                    "local_open": "09:15",
                    "local_close": "15:30",
                    "current_status": "closed",
                    "notes": ""
                },
            ]
        }
        
        return Response(response_data)
        
        

class TopGainersLosersAPIView(APIView):
    # permission_classes = [AllowAny]

    def get(self, request, format=None):
        api_key = 'BAYG7WDR7GLZ6ZI'
        url = f'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={api_key}'

        # Perform the request
        # response = requests.get(url)
        # data = response.json()

        # Check if the response matches the specified message
        # rate_limit_message = "Thank you for using Alpha Vantage! Our standard API rate limit is 25 requests per day. Please subscribe to any of the premium plans at https://www.alphavantage.co/premium/ to instantly remove all daily rate limits."
        # if data.get('Information') == rate_limit_message:
            # Define dummy data
        data = {
            "metadata": "Dummy data for top gainers, losers, and most actively traded US tickers",
            "last_updated": "2024-05-14 12:00:00",
            "top_gainers":[
                {
                    "ticker": "ZCARW",
                    "price": "0.0347",
                    "change_amount": "0.0234",
                    "change_percentage": "207.0796%",
                    "volume": "1"
                },
                {
                    "ticker": "VHAI+A",
                    "price": "2.27",
                    "change_amount": "1.278",
                    "change_percentage": "128.8306%",
                    "volume": "16767"
                },
                {
                    "ticker": "FGIWW",
                    "price": "0.23",
                    "change_amount": "0.1289",
                    "change_percentage": "127.4975%",
                    "volume": "8012"
                },
                {
                    "ticker": "HSCSW",
                    "price": "0.0579",
                    "change_amount": "0.0279",
                    "change_percentage": "93.0%",
                    "volume": "39"
                },
                {
                    "ticker": "CCLD",
                    "price": "2.32",
                    "change_amount": "1.06",
                    "change_percentage": "84.127%",
                    "volume": "91715834"
                },
                {
                    "ticker": "AMC",
                    "price": "5.23",
                    "change_amount": "2.32",
                    "change_percentage": "79.7251%",
                    "volume": "478354501"
                },
                {
                    "ticker": "IFN^",
                    "price": "0.0091",
                    "change_amount": "0.0039",
                    "change_percentage": "75.0%",
                    "volume": "678839"
                },
                {
                    "ticker": "GME",
                    "price": "30.46",
                    "change_amount": "13.0",
                    "change_percentage": "74.4559%",
                    "volume": "177526846"
                },
                {
                    "ticker": "BNIXR",
                    "price": "0.22",
                    "change_amount": "0.09",
                    "change_percentage": "69.2308%",
                    "volume": "400"
                },
                {
                    "ticker": "FOA+",
                    "price": "0.023",
                    "change_amount": "0.0092",
                    "change_percentage": "66.6667%",
                    "volume": "40441"
                },
                {
                    "ticker": "STSSW",
                    "price": "0.0694",
                    "change_amount": "0.0277",
                    "change_percentage": "66.4269%",
                    "volume": "3152"
                },
                {
                    "ticker": "KVACW",
                    "price": "0.076",
                    "change_amount": "0.0303",
                    "change_percentage": "66.302%",
                    "volume": "639"
                },
                {
                    "ticker": "PAVMZ",
                    "price": "0.0498",
                    "change_amount": "0.0198",
                    "change_percentage": "66.0%",
                    "volume": "1611"
                },
                {
                    "ticker": "GLSTR",
                    "price": "0.1489",
                    "change_amount": "0.0545",
                    "change_percentage": "57.7331%",
                    "volume": "22528"
                },
                {
                    "ticker": "VFS",
                    "price": "4.56",
                    "change_amount": "1.55",
                    "change_percentage": "51.495%",
                    "volume": "14754013"
                },
                {
                    "ticker": "EOSEW",
                    "price": "0.097",
                    "change_amount": "0.032",
                    "change_percentage": "49.2308%",
                    "volume": "15470"
                },
                {
                    "ticker": "NVAX",
                    "price": "13.11",
                    "change_amount": "4.23",
                    "change_percentage": "47.6351%",
                    "volume": "122279048"
                },
                {
                    "ticker": "RVMDW",
                    "price": "0.29",
                    "change_amount": "0.09",
                    "change_percentage": "45.0%",
                    "volume": "4914"
                },
                {
                    "ticker": "PTIXW",
                    "price": "0.026",
                    "change_amount": "0.008",
                    "change_percentage": "44.4444%",
                    "volume": "3250"
                },
                {
                    "ticker": "ACIU",
                    "price": "3.3",
                    "change_amount": "0.99",
                    "change_percentage": "42.8571%",
                    "volume": "31830135"
                }
            ],
            "top_losers": [
                    {
                        "ticker": "CLNNW",
                        "price": "0.026",
                        "change_amount": "-0.0409",
                        "change_percentage": "-61.136%",
                        "volume": "10284"
                    },
                    {
                        "ticker": "RNAZ",
                        "price": "0.6162",
                        "change_amount": "-0.7938",
                        "change_percentage": "-56.2979%",
                        "volume": "6822169"
                    },
                    {
                        "ticker": "TLGYW",
                        "price": "0.0433",
                        "change_amount": "-0.0418",
                        "change_percentage": "-49.1187%",
                        "volume": "4"
                    },
                    {
                        "ticker": "RBOT+",
                        "price": "0.0418",
                        "change_amount": "-0.0382",
                        "change_percentage": "-47.75%",
                        "volume": "149833"
                    },
                    {
                        "ticker": "PUCKW",
                        "price": "0.004",
                        "change_amount": "-0.0036",
                        "change_percentage": "-47.3684%",
                        "volume": "44584"
                    }
                ],
            "most_actively_traded": [
                {
                    "ticker": "AMC",
                    "price": "5.23",
                    "change_amount": "2.32",
                    "change_percentage": "79.7251%",
                    "volume": "478354501"
                },
                {
                    "ticker": "FFIE",
                    "price": "0.061",
                    "change_amount": "0.0149",
                    "change_percentage": "32.321%",
                    "volume": "267625900"
                },
                {
                    "ticker": "GME",
                    "price": "30.46",
                    "change_amount": "13.0",
                    "change_percentage": "74.4559%",
                    "volume": "177526846"
                },
                {
                    "ticker": "NVAX",
                    "price": "13.11",
                    "change_amount": "4.23",
                    "change_percentage": "47.6351%",
                    "volume": "122279048"
                },
                {
                    "ticker": "NKLA",
                    "price": "0.5499",
                    "change_amount": "0.0129",
                    "change_percentage": "2.4022%",
                    "volume": "105381728"
                },
                {
                    "ticker": "CCLD",
                    "price": "2.32",
                    "change_amount": "1.06",
                    "change_percentage": "84.127%",
                    "volume": "91715834"
                }
                
            ]
        }
            # return Response(dummy_data)

        # Otherwise, return the original response from the Alpha Vantage API
        return Response(data)