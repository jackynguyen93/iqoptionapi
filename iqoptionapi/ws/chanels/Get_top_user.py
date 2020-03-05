import datetime
import time
from iqoptionapi.ws.chanels.base import Base


class Get_top_user(Base):
    name = "sendMessage"
    def __call__(self):
        #
        # data ={"name":"request-leaderboard-deals-client","version":"1.0","body":{"country_id":0,"user_country_id":212,"from_position":0,"to_position":64,"near_traders_country_count":64,"near_traders_count":64,"top_country_count":64,"top_count":64,"top_type":2}}
        #
        # self.send_websocket_request("sendMessage", data)
        #
        # data ={"name":"update-user-availability","version":"1.1","body":{"platform_id":"9","idle_duration":18,"selected_asset_id":8,"selected_asset_type":3}}
        #
        # self.send_websocket_request("sendMessage", data)
        #
        # data ={"name":"request-leaderboard-userinfo-deals-client","version":"1.0","body":{"requested_user_id":53940937,"country_ids":[0]}}
        #
        # self.send_websocket_request("sendMessage", data)
        #
        # data ={"name":"expiration-top-computed","version":"1.0","params":{"routingFilters":{"instrument_type":"turbo","asset_id":"7"}}}
        #
        # self.send_websocket_request("subscribeMessage", data)
        #
        # data ={"name":"expiration-top-computed","version":"1.0","params":{"routingFilters":{"instrument_type":"turbo","asset_id":"8"}}}
        #
        # self.send_websocket_request("subscribeMessage", data)
        #
        # data ={"name":"expiration-top-computed","version":"1.0","params":{"routingFilters":{"instrument_type":"turbo","asset_id":"6"}}}
        #
        # self.send_websocket_request("subscribeMessage", data)
        #
        #
        # data ={"name":"live-deal-binary-option-placed","version":"1.0","params":{"routingFilters":{"instrument_type":"turbo","asset_id":"6"}}}
        #
        # self.send_websocket_request("subscribeMessage", data)
        #
        # test_user = 50748012 #top1
        # data ={"name":"portfolio.order-changed","version":"1.0","params":{"routingFilters":{"user_id":test_user,"instrument_type":"turbo"}}}
        #
        # self.send_websocket_request("subscribeMessage", data)
        #
        # data ={"name":"portfolio.position-changed","version":"2.0","params":{"routingFilters":{"user_id":test_user,"user_balance_id":191511597,"instrument_type":"turbo-option"}}}
        #
        # self.send_websocket_request("subscribeMessage", data)
        #
        # data ={"name":"deals-top-user-moved-up","params":{"routingFilters":{"user_id":40624085}}}
        #
        # self.send_websocket_request("subscribeMessage", data)
        #
        # data ={"name":"instruments-changed","version":"5.0","params":{"routingFilters":{"user_group_id":191,"type":"forex","is_regulated":false}}}
        #
        # self.send_websocket_request("subscribeMessage", data)
        #
        #
        # data ={"name":"profit-top-user-moved-up","version":"1.0"}
        #
        # self.send_websocket_request("subscribeMessage", data)
        #
        #
        # data ={"name":"instrument-quotes-generated","version":"1.0","params":{"routingFilters":{"active":5,"kind":"digital-option","expiration_timestamp":1582127160,"expiration_period":60}}}
        #
        # self.send_websocket_request("subscribeMessage", data)

        data ={"name":"request-leaderboard-deals-client","version":"1.0",
               "body":{"country_id":0,"user_country_id":212,"from_position":0,"to_position":100,
                       "near_traders_country_count":100,"near_traders_count":100,"top_country_count":100,"top_count":100,"top_type":2}
               }

        self.send_websocket_request(self.name, data)

        data ={"name":"live-deal-binary-option-placed","version":"1.0",
               "params":{"routingFilters":{
               }}}

        self.send_websocket_request("subscribeMessage", data)