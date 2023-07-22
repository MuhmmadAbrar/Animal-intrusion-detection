from twilio.rest import Client

account_sid = 'YOUR_TWILIO_ACCOUNT_SID'
auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='',
  body='Elephant detected.',
  to=''
)

print(message.sid)