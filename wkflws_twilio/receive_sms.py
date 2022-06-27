import json
import sys
from typing import Any


async def receive_message(
    data: dict[str, Any],
    context: dict[str, Any],
) -> dict[str, Any]:
    """Process an SMS from Twilio.

    Args:
        data: The message payload from Twilio.
        context: Contextual information about the workflow being executed.
    """
    return data


if __name__ == "__main__":
    import asyncio

    try:
        message = json.loads(sys.argv[1])
    except IndexError:
        raise ValueError("missing required `message` argument") from None

    try:
        context = json.loads(sys.argv[2])
    except IndexError:
        raise ValueError("missing `context` argument") from None

    output = asyncio.run(receive_message(message, context))

    if output is None:
        sys.exit(1)

    print(json.dumps(output))
