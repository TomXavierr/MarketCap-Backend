from django.urls import path


from .views  import TopGainersLosersAPIView, AddStockToWatchlistAPIView, GlobalMarketStatusAPIView, WatchlistStocksAPIView

urlpatterns = [
    path("top-gainers-losers/", TopGainersLosersAPIView.as_view(), name='top_gainers_losers_api'),
    path("add-to-watchlist/", AddStockToWatchlistAPIView.as_view(), name='add_to_watchlist_api' ),
    path("my-watchlist/", WatchlistStocksAPIView.as_view(), name='my_watchlist_api' ),
    path("global-market-status/", GlobalMarketStatusAPIView.as_view(), name='global_market_status_api' ),


]