from twilio.rest import Client

from datetime import datetime

now = datetime.now()

current_time = now.strftime("%H:%M:%S")

account_sid = 'AC5eba9221c451d967e1825bfbee67328c'
auth_token = 'ff715bd2c5598d66af3dba1ce3faead5'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='+13253265391',
  body='Elephant detected on '+current_time,
  to='+917305366617'
)

print(message.sid)