from twilio.rest import Client

from datetime import datetime

now = datetime.now()

current_time = now.strftime("%H:%M:%S")

account_sid = '[YOUR_TWILLIO_SID]'
auth_token = '[YOUR AUTH_TOKEN]'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='[YOUR TWILLIO NUMBER]',
  body='Elephant detected on '+current_time,
  to='[YOUR PHONE NUMBER]'
)

print(message.sid)