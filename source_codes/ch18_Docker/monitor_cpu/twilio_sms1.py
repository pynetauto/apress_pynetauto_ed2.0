from twilio.rest import Client
from credentials import account_sid, auth_token, my_smartphone, twilio_trial

client = Client(account_sid, auth_token)
my_message = f"R2 has reached 99% CPU utilization! Investigate the root cause immediately!"
message = client.messages.create(body=my_message, from_=twilio_trial, to=my_smartphone)
print(message.sid)
