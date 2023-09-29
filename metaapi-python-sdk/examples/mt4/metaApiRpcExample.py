import os
import asyncio
from metaapi_cloud_sdk import MetaApi
from metaapi_cloud_sdk.clients.metaApi.tradeException import TradeException
from datetime import datetime, timedelta

# Note: for information on how to use this example code please read https://metaapi.cloud/docs/client/usingCodeExamples/

token = os.getenv('TOKEN') or 'eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2OGMxMmYwYzgxY2Q0Y2NlYjdjYWM3MzE5MTIyNDdkZiIsInBlcm1pc3Npb25zIjpbXSwiYWNjZXNzUnVsZXMiOlt7ImlkIjoidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpIiwibWV0aG9kcyI6WyJ0cmFkaW5nLWFjY291bnQtbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZXN0LWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1ycGMtYXBpIiwibWV0aG9kcyI6WyJtZXRhYXBpLWFwaTp3czpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZWFsLXRpbWUtc3RyZWFtaW5nLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFzdGF0cy1hcGkiLCJtZXRob2RzIjpbIm1ldGFzdGF0cy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoicmlzay1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsicmlzay1tYW5hZ2VtZW50LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJjb3B5ZmFjdG9yeS1hcGkiLCJtZXRob2RzIjpbImNvcHlmYWN0b3J5LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtdC1tYW5hZ2VyLWFwaSIsIm1ldGhvZHMiOlsibXQtbWFuYWdlci1hcGk6cmVzdDpkZWFsaW5nOio6KiIsIm10LW1hbmFnZXItYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX1dLCJ0b2tlbklkIjoiMjAyMTAyMTMiLCJpbXBlcnNvbmF0ZWQiOmZhbHNlLCJyZWFsVXNlcklkIjoiNjhjMTJmMGM4MWNkNGNjZWI3Y2FjNzMxOTEyMjQ3ZGYiLCJpYXQiOjE2OTUyOTI2NDksImV4cCI6MTcwMzA2ODY0OX0.YPwfCaHWXS3Reb6L98kn7GWuvQX8Fnaqrqq57dC16bj9kYeP7X62SKh9RtBW33LXv1M5D5EGrpBLZMWcXrd0LP6pKhAYlSh3XhU59XRiOsrpmHNSPwIUcgA6PPLTkg1aGrpoVH2notjAlaMLMJQHpWtrpAALIc0P8M2nUBTwurMp5Si9DyoSk7fr1BkytHIRaNC-R3KXJfOe0NVIbvKuGSUTxsNhGbsxNa8BgsiqDuV1EMizUPy-17dcjIxOxH4IMki_KC71z3lLBYPq3LIaK7FTBlSTZLHsKDqBCoFfg8NXjVxHsA2w5Uzeh-XLjkGLf1l592I9s5Ztmb9fF6fihtOLhT2fMPdH_dJcq8fxljHKBAr5938Tgv6KK71s0AmG62DZelyxwaketd90nP3mBokD_PvHQ7MeKOBaf1QEqWAOZWMtZGK9vpvn1nP3hBaBMbosEZ3xPANuYPsAH7VTphl0ypw8v5XzVmqkyz6mtpXy-R-b6dnvZfmAMr81qiPhmjwp7e1H-nCYpLeg82rqsIw20xC6dpJKpqT48bhv71VU2ovsCKpclifCokTaMRVUj-Q_mWSMlDw6jYAb0z3tj3TmivFgKaXw9aKyDFydLJDSsZx5K0kXcRehxmCiKVv5y5VHE77DPZ2nMnZqgCNpoW2_VXhA_sV0DwDvgtkgg54'
login = os.getenv('LOGIN') or '19677087'
password = os.getenv('PASSWORD') or 'robot1234'
server_name = os.getenv('SERVER') or 'OctaFX-Real7'


async def meta_api_synchronization():
    api = MetaApi(token)
    try:
        # Add test MetaTrader account
        accounts = await api.metatrader_account_api.get_accounts()
        account = None
        for item in accounts:
            if item.login == login and item.type.startswith('cloud'):
                account = item
                break
        if not account:
            print('Adding MT4 account to MetaApi')
            account = await api.metatrader_account_api.create_account({
                'name': 'Test account',
                'type': 'cloud',
                'login': login,
                'password': password,
                'server': server_name,
                'platform': 'mt4',
                'magic': 1000
            })
        else:
            print('MT4 account already added to MetaApi')

        #  wait until account is deployed and connected to broker
        print('Deploying account')
        await account.deploy()
        print('Waiting for API server to connect to broker (may take couple of minutes)')
        await account.wait_connected()

        # connect to MetaApi API
        connection = account.get_rpc_connection()
        await connection.connect()

        # wait until terminal state synchronized to the local state
        print('Waiting for SDK to synchronize to terminal state (may take some time depending on your history size)')
        await connection.wait_synchronized()

        # invoke RPC API (replace ticket numbers with actual ticket numbers which exist in your MT account)
        print('Testing MetaAPI RPC API')
        print('account information:', await connection.get_account_information())
        print('positions:', await connection.get_positions())
        # print(await connection.get_position('1234567'))
        print('open orders:', await connection.get_orders())
        # print(await connection.get_order('1234567'))
        print('history orders by ticket:', await connection.get_history_orders_by_ticket('1234567'))
        print('history orders by position:', await connection.get_history_orders_by_position('1234567'))
        print('history orders (~last 3 months):',
              await connection.get_history_orders_by_time_range(datetime.utcnow() - timedelta(days=90),
                                                                datetime.utcnow()))
        print('history deals by ticket:', await connection.get_deals_by_ticket('1234567'))
        print('history deals by position:', await connection.get_deals_by_position('1234567'))
        print('history deals (~last 3 months):',
              await connection.get_deals_by_time_range(datetime.utcnow() - timedelta(days=90), datetime.utcnow()))

        print('server time', await connection.get_server_time())

        # calculate margin required for trade
        print('margin required for trade', await connection.calculate_margin({
            'symbol': 'GBPUSD',
            'type': 'ORDER_TYPE_BUY',
            'volume': 0.1,
            'openPrice': 1.1
        }))

        # trade
        print('Submitting pending order')
        try:
            result = await connection.create_limit_buy_order('GBPUSD', 0.07, 1.0, 0.9, 2.0,
                                                             {'comment': 'comm', 'clientId': 'TE_GBPUSD_7hyINWqAlE'})
            print('Trade successful, result code is ' + result['stringCode'])
        except Exception as err:
            print('Trade failed with error:')
            print(api.format_error(err))

        # finally, undeploy account after the test
        print('Undeploying MT4 account so that it does not consume any unwanted resources')
        await connection.close()
        await account.undeploy()
    except Exception as err:
        # process errors
        if hasattr(err, 'details'):
            # returned if the server file for the specified server name has not been found
            # recommended to check the server name or create the account using a provisioning profile
            if err.details == 'E_SRV_NOT_FOUND':
                print(err)
            # returned if the server has failed to connect to the broker using your credentials
            # recommended to check your login and password
            elif err.details == 'E_AUTH':
                print(err)
            # returned if the server has failed to detect the broker settings
            # recommended to try again later or create the account using a provisioning profile
            elif err.details == 'E_SERVER_TIMEZONE':
                print(err)
        print(api.format_error(err))
    exit()

asyncio.run(meta_api_synchronization())