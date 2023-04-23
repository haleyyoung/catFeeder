import os
from twilio.rest import Client

class Texts:
  def __init__(self):
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    self.from_number = os.environ["TWILIO_PHONE_NUMBER"]
    self.client = Client(account_sid, auth_token)

  def phoneNumbers():
    return [os.environ["GARRISON_PHONE"], os.environ["HALEY_PHONE"]]

  def sendText(self, body, numbers=phoneNumbers()):
    print(numbers)
    for number in numbers:
      message = self.client.messages.create(
        body=body,
        from_=self.from_number,
        to=number
      )
