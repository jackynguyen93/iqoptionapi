import datetime
import time
from iqoptionapi.ws.chanels.base import Base
import logging

from iqoptionapi.expiration import get_expiration_time
class Buyv4(Base):

    name = "sendMessage"

    def __call__(self, price, active, direction, expire, option_type, request_id):

        if option_type == 'turbo':
            option = 3#"turbo"
        else:
            option = 1#"binary"
        data = {
            "body": {"price": price,
                     "active_id": int(active),
                     "expired": int(expire),
                     "direction": direction.lower(),
                     "option_type_id":option,
                     "user_balance_id": int(self.api.profile.balance_id)
                     },
            "name": "binary-options.open-option",
            "version": "1.0"
        }
        # print(data)
        self.send_websocket_request(self.name, data,str(request_id))
