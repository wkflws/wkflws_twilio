# wkflws_twilio
This node provides ...

## wkflws_twilio.send_sms

### Parameters
The following parameters are available.
| name | required | description |
|-|-|-|
| `from` | ✅ | a twilio number to send the message from. |
| `to` | ✅ | the phone number to send to. |
| `body` | ✅ | the body of the sms. |


### Context Properities
The following context properties are required for this node.
| name | required | description |
|-|-|-|
| `twilio_account_sid` | ✅ | your twilio account sid. |
| `twilio_auth_token` | ✅ | your twilio auth token. |

### Example Input
```json
{
}

```

### Example Output
```json
{
}
```
