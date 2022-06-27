import json
from typing import Any

from twilio.rest import Client  # type:ignore  # no stubs
from wkflws.logging import getLogger

from . import __identifier__


async def send_sms(message: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    """Process some incoming data."""
    # All debugging information MUST be output in stderr. you can just use the logging
    # module or if you are a die hard print debugger use this instead:
    # print("My debug!", file=sys.stderr)

    logger = getLogger(f"{__identifier__}.send_sms")

    try:
        account_sid = context["Task"]["twilio_account_sid"]
    except KeyError:
        raise ValueError("Required 'twilio_account_sid' credential missing.") from None

    try:
        auth_token = context["Task"]["twilio_auth_token"]
    except KeyError:
        raise ValueError("Required 'twilio_auth_token' credential missing.") from None

    try:
        body = message["body"]
    except KeyError:
        raise ValueError("Required 'body' parameter missing.") from None

    try:
        from_number = message["from"]
    except KeyError:
        raise ValueError("Required 'from' parameter missing.") from None

    try:
        to_number = message["to"]
    except KeyError:
        raise ValueError("Required 'to' parameter missing.") from None

    client = Client(account_sid, auth_token)

    response = client.messages.create(
        body=body,
        from_=from_number,
        to=to_number,
    )

    logger.debug(dir(response))
    logger.debug(response)
    return {}


if __name__ == "__main__":
    import asyncio
    import sys

    # message is the input to your function. This is the output from the previous
    # function plus any transformations the user defined in their workflow. Parameters
    # should be documented in the parameters.json file so they can be used in the UI.
    try:
        message = json.loads(sys.argv[1])
    except IndexError:
        raise ValueError("missing required `message` argument") from None

    # this contains some contextual information about the workflow and the current
    # state. required secrets should be defined in the README so users can write their
    # lookup class with this node's unique requirements in mind.
    try:
        context = json.loads(sys.argv[2])
    except IndexError:
        raise ValueError("missing `context` argument") from None

    output = asyncio.run(send_sms(message, context))

    # Non-zero exit codes indicate to the executor there was an unrecoverable error and
    # workflow execution should terminate.
    if output is None:
        sys.exit(1)

    # The output of your function is input for a potential next state. It must be in
    # JSON format and be the only thing output on stdout. This value is picked up by the
    # executor and processed.
    print(json.dumps(output))
