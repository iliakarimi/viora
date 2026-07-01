#Configure User information and Operating System Platform
import json
import textfx
import platform
import termcolor



with open("configs/user_config.json", "r") as l:
    user_conf = json.load(l)


textfx.typeeffect("Welcome To Viora Configuration\n", delay=0.07)
textfx.typeeffect("Please Enter Your name: ")
get_name = str(input())

get_os = platform.system()
print("Get OS Platform...")

user_conf["user_name"] = get_name
user_conf["os"] = get_os


with open("configs/user_config.json", "w") as w:
    json.dump(user_conf, w)


textfx.typeeffect("You can Now Using Viora by Typing:\n")
print(termcolor.colored("python chat.py", color="yellow"))
