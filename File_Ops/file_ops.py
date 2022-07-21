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


