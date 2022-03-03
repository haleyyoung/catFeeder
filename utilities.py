from datetime import datetime

class Log:
  @staticmethod
  def info(message):
    now = datetime.now().strftime("%d-%b-%Y %H:%M:%S.%f")
    today = datetime.now().strftime("%m-%d-%Y")
    filename = "/home/pi/logs/{today}.log"
    f = open(filename.format(today=today), "a")
    f.write("INFO   {now}       {message}\n".format(now=now, message=message))
    f.close()
