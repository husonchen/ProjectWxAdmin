from shop_admin.util.nsq_producer import NsqProducer

class MessageToUser():
    def __init__(self):
        self.producer = NsqProducer('message_touser')

    def pub_message(self,message):
        self.producer.produce(message)

# class PassNotifier():
#     def __init__(self):
#         self.producer = NsqProducer('pass_notify')
#
#     def pub_message(self,message):
#         self.producer.produce(message)

if __name__ == '__main__':
    notifier = RejectNotifier()
    notifier.pub_message('test')



