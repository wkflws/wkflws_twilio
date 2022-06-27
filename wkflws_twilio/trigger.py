import json
from typing import Any, Optional
from urllib.parse import parse_qs


from twilio.twiml.messaging_response import MessagingResponse
from wkflws.events import Event
from wkflws.http import http_method, Request, Response
from wkflws.triggers.webhook import status, WebhookTrigger

from . import __identifier__, __version__


async def process_webhook_request(
    request: Request, response: Response
) -> Optional[Event]:
    """Accept and process an HTTP request returning a event for the bus."""
    # Most webhooks include a header with a unique id that can be used as the event's
    # id. This would allow tracing back to the source.

    # headers:
    # {
    # 'accept': '*/*',
    # 'accept-encoding': 'gzip',
    # 'content-length': '436',
    # 'content-type': 'application/x-www-form-urlencoded',
    # 'host': 'abcdefg.ngrok.io',
    # 'i-twilio-idempotency-token': '4d342e56-e09e-4d9b-827a-0213c3f6ee5b',
    # 'user-agent': 'TwilioProxy/1.1',
    # 'x-forwarded-for': '1.2.3.4',
    # 'x-forwarded-proto': 'https',
    # 'x-home-region': 'us1',
    # 'x-twilio-signature': 'XddRCFyRUl4WkJIqakQHe5I='}

    # Body:
    # {
    #     "ToCountry": ["US"],
    #     "ToState": ["AL"],
    #     "SmsMessageSid": ["6d218292733526df26c2466"],
    #     "NumMedia": ["0"],
    #     "ToCity": ["GOODWATER"],
    #     "FromZip": ["35072"],
    #     "SmsSid": ["SM76d2187e9a8292733526daa8"],
    #     "FromState": ["AL"],
    #     "SmsStatus": ["received"],
    #     "FromCity": ["GOODWATER"],
    #     "Body": ["hello2"],
    #     "FromCountry": ["US"],
    #     "To": ["+12567436888"],
    #     "ToZip": ["35072"],
    #     "NumSegments": ["1"],
    #     "ReferralNumMedia": ["0"],
    #     "MessageSid": ["SM76d2187e9a8292733526"],
    #     "AccountSid": ["AC5738f06bf44f91ac6e3b"],
    #     "From": ["+12567436889"],
    #     "ApiVersion": ["2010-04-01"],
    # }

    identifier = request.headers["i-twilio-idempotency-token"]

    metadata = request.headers.copy()
    data = parse_qs(request.body)
    metadata["to"] = data["To"][0]

    response.status_code = status.HTTP_200_OK
    response.body = str(MessagingResponse())

    return Event(identifier, metadata, data)


async def accept_event(event: Event) -> tuple[Optional[str], dict[str, Any]]:
    """Accept and process data from the event bus."""
    cleaned_data = {}

    for k, v in event.data.items():
        cleaned_data[k] = v[0] if len(v) == 1 else v

    return "wkflws_twilio.receive_sms", cleaned_data


webhook = WebhookTrigger(
    client_identifier=__identifier__,
    client_version=__version__,
    process_func=accept_event,
    routes=(
        (
            (http_method.POST,),
            "/twilio/sms/",
            process_webhook_request,
        ),
    ),
)
