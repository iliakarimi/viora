from models import gpt_model
import os




def run_gpt():
    

    os.system("sudo xhost +")
    
    gpt_model.run()




if __name__ == "__main__":
    run_gpt()
