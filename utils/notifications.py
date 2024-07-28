from firebase_admin import messaging
import traceback
import json
from accounts.models import User
from django.conf import settings
from order.models import *
class NotificationsHelper:
    # send message to fcm api
    @classmethod
    def __sendMessage(cls,msg:messaging.Message):
        try:
            messaging.send(message = msg ,dry_run=False)
        except Exception as exc:
            print(exc)


    # create Message object with localization data
    @classmethod
    def __localizedMsg(cls,title:str,body:str,titleArgs:list[str]=[],bodyArgs:list[str]=[],data:dict={}):
        msg=messaging.Message(
            data={
                **data,
                'title':title,
                'titleArgs':json.dumps(titleArgs),
                'body':body,
                'bodyArgs':json.dumps(bodyArgs),
                'localized':str(True)
            },
            android=messaging.AndroidConfig(
                notification=messaging.AndroidNotification(
                    title_loc_key=title,
                    title_loc_args=titleArgs,
                    body_loc_key=body,
                    body_loc_args=bodyArgs
                )
            ),
            apns=messaging.APNSConfig(
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(
                        messaging.ApsAlert(
                            title_loc_key=title,
                            title_loc_args=titleArgs,
                            loc_key=body,
                            loc_args=bodyArgs
                        )
                    )
                )
            )
        )
        return msg
    #send not localized notification to topic
    #! this function currently for test, don't use it in the dashboard for now :) 
    @classmethod
    def sendBroadcast(cls,title,body,topic):
        data={
            'type':"BROADCAST",
            'localized':str(False)

        }
        msg=messaging.Message(

                    notification=messaging.Notification(
                        title=title,
                        body=body,

                    ),
                    topic=topic,
                    data=data,
                    )
        cls.__sendMessage(msg)

    @classmethod
    def sendDriverAcceptUpdate(cls,update:str,order:Order,target:User):
          data={
            'type':"Driver_Accept",
            "order-id":str(order.id),
            'update':update
        }
          bodyArgs=[str(order.id)]
          msg=cls.__localizedMsg( title=update+'_TITLE',
                                body=update+'_BODY',
                                bodyArgs=bodyArgs,
                                data=data,
                                )
          if target.fcmToken:
            msg.token=target.fcmToken
            cls.__sendMessage(msg)
            Notification.objects.create(
                                    title=update+'_TITLE',
                                    body=update+'_BODY',
                                    bodyArgs=bodyArgs,
                                    localized=True,
                                    user=target,
                                    order=order,
                                    )
          
    #send new update about order to user
    # update is value from OrdersUpdates class
    @classmethod
    def sendOrderUpdate(cls,update:str,orderId:Order,target:User):
        data={
            'type':"ORDER_UPDATE",
            "order-id":str(orderId.id),
            'update':update
        }
        bodyArgs=[str(orderId.id)]
        msg=cls.__localizedMsg( title=update+'_TITLE',
                                body=update+'_BODY',
                                bodyArgs=bodyArgs,
                                data=data,
                                )
        if target.fcm_token:
            msg.token=target.fcm_token
            cls.__sendMessage(msg)
            Notification.objects.create(
                                    title=update+'_TITLE',
                                    body=update+'_BODY',
                                    bodyArgs=bodyArgs,
                                    localized=True,
                                    user=target,
                                    order=orderId,
                                    )

class OrdersUpdates:
    Driver_ON_WAY='Driver_ON_WAY' #send to client when the driver on way
    OFFER_RECEIVED='OFFER_RECEIVED' #send to client when new offer is sent
    OFFER_SELECTED='OFFER_SELECTED' #send to driver when his offer is selected    
    DRIVER_CANCEL_ORDER='DRIVER_CANCEL_ORDER' #send to client when driver cancel 
    CLIENT_CANCEL_ORDER='CLIENT_CANCEL_ORDER' #send to driver when client cancel 
    DRIVER_ASK_CANCEL_ORDER='DRIVER_ASK_CANCEL_ORDER' #send to client when driver ask to cancel 
    CLIENT_ASK_CANCEL_ORDER='CLIENT_ASK_CANCEL_ORDER' #send to driver when client ask to cancel 
    ORDER_COMPLETE='ORDER_COMPLETE' #send to client when driver finish order
    ORDER_COMPLETE_DRIVER='ORDER_COMPLETE_DRIVER' #send to driver when driver finish order
    CANCEL_REJECTED='CANCEL_REJECTED' #send when cancel rejected
    
