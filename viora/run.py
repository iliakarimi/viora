import os


os.system("xhost +")


from models.gpt import __gpt_model



def run_gpt():
    
    __gpt_model.run()



if __name__ == "__main__":
    run_gpt()
