from datetime import datetime

class Logger:

    def log(self,file,text):
        self.now = datetime.now()
        self.date = self.now.date()
        self.time = self.now.strftime("%H:%M:%S")
        file.write(str(self.date)+"/"+str(self.time)+"\t\t"+text+"\n")