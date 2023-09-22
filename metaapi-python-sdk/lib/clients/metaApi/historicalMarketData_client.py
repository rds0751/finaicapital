from ..metaApi_client import MetaApiClient
from ..httpClient import HttpClient
from ..domain_client import DomainClient
from typing import List
from datetime import datetime
from ...metaApi.models import format_date, date, MetatraderCandle, MetatraderTick
from urllib import parse


class HistoricalMarketDataClient(MetaApiClient):

    def __init__(self, http_client: HttpClient, domain_client: DomainClient):
        """Inits historical market data API client instance.

        Args:
            http_client: HTTP client.
            domain_client: Domain client.
        """
        super().__init__(http_client, domain_client)
        self._host = 'https://mt-market-data-client-api-v1'

    async def get_historical_candles(self, account_id: str, region: str, symbol: str, timeframe: str,
                                     start_time: datetime = None, limit: int = None) -> List[MetatraderCandle]:
        """Returns historical candles for a specific symbol and timeframe from a MetaTrader account.
        See https://metaapi.cloud/docs/client/restApi/api/retrieveMarketData/readHistoricalCandles/

        Args:
            account_id: MetaTrader account id.
            region: Account region.
            symbol: Symbol to retrieve candles for (e.g. a currency pair or an index).
            timeframe: Defines the timeframe according to which the candles must be generated. Allowed values
            for MT5 are 1m, 2m, 3m, 4m, 5m, 6m, 10m, 12m, 15m, 20m, 30m, 1h, 2h, 3h, 4h, 6h, 8h, 12h, 1d, 1w, 1mn.
            Allowed values for MT4 are 1m, 5m, 15m 30m, 1h, 4h, 1d, 1w, 1mn.
            start_time: Time to start loading candles from. Note that candles are loaded in backwards direction, so
            this should be the latest time. Leave empty to request latest candles.
            limit: Maximum number of candles to retrieve. Must be less or equal to 1000.

        Returns:
            A coroutine resolving with historical candles downloaded.
        """

        symbol = parse.quote(symbol)
        host = await self._domainClient.get_url(self._host, region)
        qs = {}
        if start_time is not None:
            qs['startTime'] = format_date(start_time)
        if limit is not None:
            qs['limit'] = limit

        opts = {
            'url': f'{host}/users/current/accounts/{account_id}/historical-market-data/symbols/'
                   f'{symbol}/timeframes/{timeframe}/candles',
            'method': 'GET',
            'headers': {
                'auth-token': self._token
            },
            'params': qs
        }
        candles = await self._httpClient.request(opts, 'get_historical_candles')
        candles = candles or []
        for c in candles:
            c['time'] = date(c['time'])
        return candles

    async def get_historical_ticks(self, account_id: str, region: str, symbol: str, start_time: datetime = None,
                                   offset: int = None, limit: int = None) -> List[MetatraderTick]:
        """Returns historical ticks for a specific symbol from a MetaTrader account.
        See https://metaapi.cloud/docs/client/restApi/api/retrieveMarketData/readHistoricalTicks/

        Args:
            account_id: MetaTrader account id.
            region: Account region.
            symbol: Symbol to retrieve ticks for (e.g. a currency pair or an index).
            start_time: Time to start loading ticks from. Note that ticks are loaded in backwards direction, so
            this should be the latest time. Leave empty to request latest ticks.
            offset: Number of ticks to skip (you can use it to avoid requesting ticks from previous request twice)
            limit: Maximum number of ticks to retrieve. Must be less or equal to 1000.

        Returns:
            A coroutine resolving with historical ticks downloaded.
        """

        symbol = parse.quote(symbol)
        host = await self._domainClient.get_url(self._host, region)
        qs = {}
        if start_time is not None:
            qs['startTime'] = format_date(start_time)
        if offset is not None:
            qs['offset'] = offset
        if limit is not None:
            qs['limit'] = limit

        opts = {
            'url': f'{host}/users/current/accounts/{account_id}/historical-market-data/symbols/{symbol}/ticks',
            'method': 'GET',
            'headers': {
                'auth-token': self._token
            },
            'params': qs
        }
        ticks = await self._httpClient.request(opts, 'get_historical_ticks')
        ticks = ticks or []
        for t in ticks:
            t['time'] = date(t['time'])
        return ticks
