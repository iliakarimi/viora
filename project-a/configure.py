#Configure User information and Operating System Platform
import json
import platform
import termcolor
from textfx import typeeffect
from utils.clear import cleart


cleart()


with open("configs/user_config.json", "r") as l:
    user_conf = json.load(l)

get_os = platform.system()


def main():
    if user_conf["user_name"] is None and user_conf["os"] is None:
        
        typeeffect("Welcome To Viora Configuration\n", delay=0.06)
        typeeffect("Please Enter Your name: ", delay=0.06)
        get_name = str(input())


        print("Get OS Platform...")

        user_conf["user_name"] = get_name
        user_conf["os"] = get_os


        with open("configs/user_config.json", "w") as w:
            json.dump(user_conf, w)

    elif user_conf["user_name"] is not None and user_conf["os"] is not None:    
        typeeffect("You already have Configured your Information.\n", delay=0.06)
        typeeffect("Do you Want to change your information (y / yes, n / no): ", delay=0.06)
        
        user_awnser = str(input())

        loop_t = True
        while loop_t:
            if user_awnser.lower() in ("y", "Y", "yes"):
                typeeffect("Please Enter your new Name: ", delay=0.06)
                
                get_new_name = str(input())
                
                user_conf["user_name"] = get_new_name
                user_conf["os"] = get_os

                with open("configs/user_config.json", "w") as wn:
                    json.dump(user_conf, wn)
                loop_t = False

            elif user_awnser.lower() in ("n", "N", "no"):
                print("OK!")
                loop_t = False            
            else:
                user_awnser = str(input("Type (y / yes , n / no): "))



if __name__ == "__main__":
    try:
        main()
        typeeffect("You can Now Using Viora by Typing:\n\n")
        print(termcolor.colored("python chat.py", color="yellow"))
        
    except Exception as e:
        print("\nAn unexpected error occurred. Please try again. If the problem persists, please open issue issue on GitHub.")
        print(e)
