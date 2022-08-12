import os
import pickle
import shutil

class File_Ops:

    def save_model(self,model,file_name):
        path = os.path.join("Model/",file_name)
        if os.path.isdir(path):

            for f in os.listdir(path):
                os.remove(os.path.join(path, f))

            os.rmdir(path)
            os.makedirs(path)
        else:
            os.makedirs(path)
        with open(path + '/' + file_name + '.sav','wb') as f:
            pickle.dump(model, f)


    def load_model(self,name):
        path = os.path.join("Model",name,name+".sav")
        with open(path,'rb') as f:
            return pickle.load(f)

    def find_model(self,i):
        for filename in os.listdir("Model"):
            if(str(filename).__contains__(str(i))):
                return filename


