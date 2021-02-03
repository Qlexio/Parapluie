from time import sleep
from oscpy.client import OSCClient
from datetime import datetime

from plyer import notification
from plyer import vibrator 


def get_time():
    return datetime.now().strftime("%M")


# def callback(*args):
#     global current_time
    
#     if current_time != get_time():
#         current_time = get_time()
#         osc.sendMsg("/Parapluie", [current_time,], port= 9001)

if __name__ == "__main__":
    current_time = datetime.now().strftime("%M")

    osc = OSCClient("localhost", 8000)
    # osc.listen(address= "127.0.0.1", port= 8000,default= True)

    while True:
        # @osc.address(u"/sender")
        # def sender(*args):
        #     global current_time
    
        if current_time != get_time():
            current_time = get_time()
            
            if vibrator.exists():
                vibrator.vibrate(time=2)
                notification.notify(title="Vibrator testing", message= "Vibrator exists",
                    app_icon= "./umbrella.png", app_name= "Parapluie", toast=False)
            else:
                notification.notify(title="", message= "No vibrator", 
                    app_icon= "./umbrella.png", app_name= "Parapluie", toast=False)

        osc.send_message(b"/listener", [current_time.encode("utf-8"),],)
            
        sleep(1)