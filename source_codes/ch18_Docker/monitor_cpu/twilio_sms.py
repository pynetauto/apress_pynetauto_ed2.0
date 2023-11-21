from twilio.rest import Client
from credentials import account_sid, auth_token, my_smartphone, twilio_trial
client = Client(account_sid, auth_token)
my_message = f"High CPU utilization Alert! R2 has reached 99% CPU utilization!"
message = client.messages.create(body=my_message, from_=twilio_trial, to=my_smartphone)
print(message.sid)
