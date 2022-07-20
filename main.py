from Training_Validation.training_validation import Training_Validation
from Model.preprocessing import Preprocessor
import os



dir = 'Good_Raw_Files'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))

dir = 'Bad_Raw_Files'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))


tv = Training_Validation()
tv.validate_data()

pr = Preprocessor()
pr.preprocess()

