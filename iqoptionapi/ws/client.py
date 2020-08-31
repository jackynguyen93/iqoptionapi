"""Module for IQ option websocket."""

import json
import logging
import websocket
import iqoptionapi.constants as OP_code
import iqoptionapi.global_value as global_value


                
class WebsocketClient(object):
    """Class for work with IQ option websocket."""

    def __init__(self, api):
        """
        :param api: The instance of :class:`IQOptionAPI
            <iqoptionapi.api.IQOptionAPI>`.
        """
        self.api = api
        self.wss = websocket.WebSocketApp(
            self.api.wss_url, on_message=self.on_message,
            on_error=self.on_error, on_close=self.on_close,
            on_open=self.on_open)
    def dict_queue_add(self,dict,maxdict,key1,key2,key3,value):
        if key3 in dict[key1][key2]:
                    dict[key1][key2][key3]=value
        else:
            while True:
                try:
                    dic_size=len(dict[key1][key2])
                except:
                    dic_size=0
                if dic_size<maxdict:
                    dict[key1][key2][key3]=value
                    break
                else:
                    #del mini key
                    del dict[key1][key2][sorted(dict[key1][key2].keys(), reverse=False)[0]]   
    def on_message(self, message): # pylint: disable=unused-argument
        """Method to process websocket messages."""
        logger = logging.getLogger(__name__)

        message = json.loads(str(message))
        #### for testing
        if message["name"] not in ["timeSync", "candle-generated", "options", "candles-generated", "heartbeat",
                                   "profile", "candles", 'commission-changed', 'option-archived', 'option-closed',
                                   'socket-option-closed', 'socket-option-opened', 'option-opened',
                                   "leaderboard-deals-client", 'api_option_init_all_result', 'live-deal-binary-option-placed', 'balance-changed']:
            print(message)
        #####
        if message["name"] == "timeSync":
            self.api.timesync.server_timestamp = message["msg"]
        elif message["name"] == "leaderboard-deals-client":
            try:
                self.api.top_user = message["msg"]["result"]["top"]
            except:
                logger.error("Cannot get leaderboard")
                pass
        elif message["name"] == "live-deal-binary-option-placed":
            try:
                self.api.running_id = message["msg"]['user_id']
                if len(self.api.user_filter) > 0 :
                    if message["msg"]['user_id'] in self.api.user_filter:
                        self.api.top_orders.append(message["msg"])
                else:
                    self.api.top_orders.append(message["msg"])
                # logger.info(message)
                # if message["msg"]['user_id'] in  self.api.top_user_ids:
                #     logger.info(message["msg"])
                #     self.api.top_orders.append(message["msg"])
            except:
                logger.error("Cannot get top order")
                pass
    #######################################################
        #---------------------for_realtime_candle______________
        #######################################################
        elif message["name"] == "candle-generated":
            Active_name=list(OP_code.ACTIVES.keys())[list(OP_code.ACTIVES.values()).index(message["msg"]["active_id"])]            
            
            active=str(Active_name)
            size=int(message["msg"]["size"])
            from_=int(message["msg"]["from"])
            msg=message["msg"]
            maxdict=self.api.real_time_candles_maxdict_table[Active_name][size]

            self.dict_queue_add(self.api.real_time_candles,maxdict,active,size,from_,msg)
            self.api.candle_generated_check[active][size]=True
            
        elif message["name"]=="options":
            self.api.get_options_v2_data=message
        elif message["name"] == "candles-generated":
            Active_name=list(OP_code.ACTIVES.keys())[list(OP_code.ACTIVES.values()).index(message["msg"]["active_id"])] 
            active=str(Active_name)      
            for k,v in message["msg"]["candles"].items():
                v["active_id"]=message["msg"]["active_id"]
                v["at"]=message["msg"]["at"]
                v["ask"]=message["msg"]["ask"]
                v["bid"]=message["msg"]["bid"]
                v["close"]=message["msg"]["value"]
                v["size"]=int(k)
                size=int(v["size"])
                from_=int(v["from"])
                maxdict=self.api.real_time_candles_maxdict_table[Active_name][size]
                msg=v
                self.dict_queue_add(self.api.real_time_candles,maxdict,active,size,from_,msg)
            self.api.candle_generated_all_size_check[active]=True 
        elif message["name"]=="commission-changed":
            instrument_type=message["msg"]["instrument_type"]
            active_id=message["msg"]["active_id"]
            Active_name=list(OP_code.ACTIVES.keys())[list(OP_code.ACTIVES.values()).index(active_id)]            
            commission=message["msg"]["commission"]["value"]
            self.api.subscribe_commission_changed_data[instrument_type][Active_name][self.api.timesync.server_timestamp]=int(commission)
            
        #######################################################
        #______________________________________________________
        #######################################################
        elif message["name"] =="heartbeat":
            try:
                self.api.heartbeat(message["msg"])
            except:
                pass
        elif message["name"] == "profile":
            #--------------all-------------
            self.api.profile.msg=message["msg"]
            #---------------------------
            try:
                self.api.profile.balance = message["msg"]["balance"]
            except:
                pass
            
            try:
                self.api.profile.balance_id=message["msg"]["balance_id"]
            except:
                pass
            
            try:
                self.api.profile.balance_type=message["msg"]["balance_type"]
            except:
                pass

            try:
                self.api.profile.balances=message["msg"]["balances"]
            except:
                pass

        elif message["name"] == "candles":
            try:
                self.api.candles.candles_data = message["msg"]["candles"]
            except:
                pass
        #Make sure ""self.api.buySuccessful"" more stable
        #check buySuccessful have two fail action
        #if "user not authorized" we get buyV2_result !!!need to reconnect!!!
        #elif "we have user authoget_balancerized" we get buyComplete
        #I Suggest if you get selget_balancef.api.buy_successful==False you need to reconnect iqoption server
        elif message["name"] == "buyComplete":
            try:
                self.api.buy_successful = message["msg"]["isSuccessful"]
                self.api.buy_id= message["msg"]["result"]["id"]
            except:
                pass
        elif message["name"] == "buyV2_result":
            self.api.buy_successful = message["msg"]["isSuccessful"]
        #*********************buyv3
        #buy_multi_option
        elif message["name"] == "option":
            self.api.buy_multi_option[int(message["request_id"])] = message["msg"]
            try:
                if 'act' in message["msg"]:
                    ACTIVE = message["msg"]['act']
                    if 'id' in message["msg"]:
                        self.api.buy_successful[ACTIVE] = True
                        self.api.buy_id[ACTIVE] =  message["msg"]['id']
                    else:
                        self.api.buy_successful[ACTIVE] = False
            except Exception as e:

                logger.error('fail to request buy' , e)

        #**********************************************************
        elif message["name"] == "listInfoData":
           for get_m in message["msg"]:
               self.api.listinfodata.set(get_m["win"],get_m["game_state"],get_m["id"])
        elif message["name"] == "socket-option-opened":
            id=message["msg"]["id"]
            self.api.socket_option_opened[id]=message
             
        elif message["name"] == "api_option_init_all_result":
            self.api.api_option_init_all_result = message["msg"]
        elif message["name"] == "initialization-data":
            self.api.api_option_init_all_result_v2 = message["msg"]
        elif message["name"] == "underlying-list":
            self.api.underlying_list_data=message["msg"]
        elif message["name"] == "instruments":
            self.api.instruments=message["msg"]
        elif message["name"]=="financial-information":
            self.api.financial_information=message
        elif message["name"]=="position-changed":
            self.api.position_changed_data[int(message["msg"]["order_ids"][0])]=message["msg"]
        elif message["name"]=="option-opened":
            self.api.microserviceName_binary_options_name_option[int(message["msg"]["option_id"])]=message
        elif message["name"]=="option-closed":
            self.api.listinfodata.set( message["msg"]["result"],1,message["msg"]["option_id"], message["msg"]["profit_amount"])
            self.api.microserviceName_binary_options_name_option[int(message["msg"]["option_id"])]=message
        elif message["name"]=="top-assets-updated":
            self.api.top_assets_updated_data[str(message["msg"]["instrument_type"])]=message["msg"]["data"]
        elif message["name"]=="strike-list":  
            self.api.strike_list=message
        elif message["name"]=="api_game_betinfo_result":
            try:
                self.api.game_betinfo.isSuccessful=message["msg"]["isSuccessful"]
                self.api.game_betinfo.dict=message["msg"]
                if message["msg"]['isSuccessful']:
                    data = message["msg"]['result']['data']
                    #print(data)
                    key = list(data.keys())[0]
                    print('result ' + data[key]['win'])
                    self.api.game_betinfo.isSuccessful= data[key]['win'] != ''#message["msg"]["isSuccessful"]
                else:
                    self.api.game_betinfo.isSuccessful = False
            except:
                logger.error('fail api_game_betinfo_result', e)
                pass
        elif message["name"]=="traders-mood-changed":
            self.api.traders_mood[message["msg"]["asset_id"]]=message["msg"]["value"]
        #------for forex&cfd&crypto..
        elif message["name"]=="order-placed-temp":
            self.api.buy_order_id= message["msg"]["id"]
        elif message["name"]=="order":
            self.api.order_data=message
        elif message["name"]=="positions":
            self.api.positions=message
        elif message["name"]=="position":
            self.api.position=message
        elif message["name"]=="deferred-orders":
            self.api.deferred_orders=message

        elif message["name"]=="position-history":
            self.api.position_history=message
        elif message["name"]=="history-positions":
            self.api.position_history_v2=message
        elif message["name"]=="available-leverages":
            self.api.available_leverages=message
        elif message["name"]=="order-canceled":
            self.api.order_canceled=message
        elif message["name"]=="position-closed":
            self.api.close_position_data=message
        elif message["name"]=="overnight-fee":
            self.api.overnight_fee=message
        elif message["name"]=="api_game_getoptions_result":
            self.api.api_game_getoptions_result=message
        elif message["name"]=="sold-options":
            self.api.sold_options_respond=message
        elif message["name"]=="tpsl-changed":
            self.api.tpsl_changed_respond=message
        elif message["name"]=="position-changed":
            self.api.position_changed=message
        elif message["name"]=="auto-margin-call-changed":
            self.api.auto_margin_call_changed_respond=message
        elif message["name"]=="digital-option-placed":
            try:
                self.api.digital_option_placed_id=message["msg"]["id"]
            except:
                logger.error('fail digital-option-placed')
                self.api.digital_option_placed_id="error"
        elif message["name"]=="result":
            self.api.result=message["msg"]["success"]
        elif message["name"]=="instrument-quotes-generated":
             
            Active_name=list(OP_code.ACTIVES.keys())[list(OP_code.ACTIVES.values()).index(message["msg"]["active"])]  
            period=message["msg"]["expiration"]["period"] 
            ans={}
            for data in message["msg"]["quotes"]:
                #FROM IQ OPTION SOURCE CODE
                #https://github.com/Lu-Yi-Hsun/Decompiler-IQ-Option/blob/master/Source%20Code/5.5.1/sources/com/iqoption/dto/entity/strike/Quote.java#L91
                if data["price"]["ask"]==None:
                    ProfitPercent=None
                else:
                    askPrice=(float)(data["price"]["ask"])
                    ProfitPercent=((100-askPrice)*100)/askPrice
                
                for symble in data["symbols"]:
                    try:
                        """
                        ID SAMPLE:doUSDJPY-OTC201811111204PT1MC11350481
                        """

                        """
                        dict ID-prodit:{ID:profit}
                        """

                        ans[symble]=ProfitPercent
                    except:
                        pass
            self.api.instrument_quites_generated_timestamp[Active_name][period]=message["msg"]["expiration"]["timestamp"]
            self.api.instrument_quites_generated_data[Active_name][period]=ans

            self.api.instrument_quotes_generated_raw_data[Active_name][period]=message
        elif message["name"]=="training-balance-reset":
            self.api.training_balance_reset_request=message["msg"]["isSuccessful"]
        elif message["name"] == "balance-changed":
            try:
                self.api.profile.balance = message["msg"]["current_balance"]["amount"]
            except:
                pass
            
    
    @staticmethod
    def on_error(wss, error): # pylint: disable=unused-argument
        """Method to process websocket errors."""
        logger = logging.getLogger(__name__)
        logger.error(error)
        global_value.check_websocket_if_connect=-1
    @staticmethod
    def on_open(wss): # pylint: disable=unused-argument
        """Method to process websocket open."""
        logger = logging.getLogger(__name__)
        logger.debug("Websocket client connected.")
        global_value.check_websocket_if_connect=1
    @staticmethod
    def on_close(wss): # pylint: disable=unused-argument
        """Method to process websocket close."""
        logger = logging.getLogger(__name__)
        logger.debug("Websocket connection closed.")
        global_value.check_websocket_if_connect=0
