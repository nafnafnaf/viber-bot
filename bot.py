from flask import Flask, request, Response
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest

import time
import logging
import sched
import threading

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = Flask(__name__)
viber = Api(BotConfiguration(
  name='kavala weather',
  avatar='http://viber.com/avatar.jpg',
  auth_token='46d572af7de7d364-14a48b4ad46ef327-d3b88ee49db77f82'
))

@app.route('/', methods=['POST'])
def incoming():
    logger.debug("received request. post data: {0}".format(request.get_data()))
    # every viber message is signed, you can verify the signature using this method
    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    # this library supplies a simple way to receive a request object
    viber_request = viber.parse_request(request.get_data())

    if isinstance(viber_request, ViberMessageRequest):
        message = viber_request.message
        # lets echo back
        viber.send_messages(viber_request.sender.id, [
            message
        ])
    elif isinstance(viber_request, ViberSubscribedRequest):
        viber.send_messages(viber_request.get_user.id, [
            TextMessage(text="thanks for subscribing!")
        ])
    elif isinstance(viber_request, ViberFailedRequest):
        logger.warn("client failed receiving message. failure: {0}".format(viber_request))

    return Response(status=200)

if __name__ == "__main__":
   # context = ('server.crt', 'server.key')
    app.run(host='0.0.0.0', port=443, debug=True)#, ssl_context=context)
#def set_webhook(viber):
#	viber.set_webhook('https://viber-bot-meteokav.herokuapp.com/')

#if __name__ == "__main__":
#	scheduler = sched.scheduler(time.time, time.sleep)
#	scheduler.enter(5, 1, set_webhook, (viber,))
#	t = threading.Thread(target=scheduler.run)
#	t.start()

#	context = ('server.crt', 'server.key')
#	app.run(host='0.0.0.0', port=8443, debug=True, ssl_context=context)
