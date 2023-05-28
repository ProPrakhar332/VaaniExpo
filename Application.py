# Importing Libraries

import numpy as np

import cv2
import os, sys
import time
import operator

from string import ascii_uppercase

import tkinter as tk
from PIL import Image, ImageTk

from hunspell import Hunspell
import enchant

from keras.models import model_from_json

os.environ["THEANO_FLAGS"] = "device=cuda, assert_no_cpu_op=True"

#Application :

class Application:

    def __init__(self):

        self.hs = Hunspell('en_US')
        self.vs = cv2.VideoCapture(0)
        self.current_image = None
        self.current_image2 = None
        self.json_file = open("Models\model_new.json", "r")
        self.model_json = self.json_file.read()
        self.json_file.close()

        self.loaded_model = model_from_json(self.model_json)
        self.loaded_model.load_weights("Models\model_new.h5")

        self.json_file_dru = open("Models\model-bw_dru.json" , "r")
        self.model_json_dru = self.json_file_dru.read()
        self.json_file_dru.close()

        self.loaded_model_dru = model_from_json(self.model_json_dru)
        self.loaded_model_dru.load_weights("Models\model-bw_dru.h5")
        self.json_file_tkdi = open("Models\model-bw_tkdi.json" , "r")
        self.model_json_tkdi = self.json_file_tkdi.read()
        self.json_file_tkdi.close()

        self.loaded_model_tkdi = model_from_json(self.model_json_tkdi)
        self.loaded_model_tkdi.load_weights("Models\model-bw_tkdi.h5")
        self.json_file_smn = open("Models\model-bw_smn.json" , "r")
        self.model_json_smn = self.json_file_smn.read()
        self.json_file_smn.close()

        self.loaded_model_smn = model_from_json(self.model_json_smn)
        self.loaded_model_smn.load_weights("Models\model-bw_smn.h5")

        self.ct = {}
        self.ct['blank'] = 0
        self.blank_flag = 0

        for i in ascii_uppercase:
          self.ct[i] = 0
        
        print("Loaded model from disk")

        self.root = tk.Tk()
        self.root.title("Vaani")
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)

        #self.root.geometry("900x900")
        self.MainFrame = tk.Frame(background="#e8f0fe")
        self.RightFrame = tk.Frame(master=self.MainFrame,background="#e8f0fe",pady=25,padx=100,width=800)
        self.LeftFrame = tk.Frame(master=self.MainFrame,background="#e8f0fe",pady=25,padx=100,width=800)

        #video frame
        self.panel = tk.Label(master=self.RightFrame, background="#e8f0fe", width = 500, height = 500)
        #self.panel.place(x = 100, y = 10, width = 580, height = 580)
        #self.panel.place()
        #black and white frame
        self.panel2 = tk.Label(master=self.RightFrame,background="#e8f0fe", width = 500, height = 500) # initialize image panel
        #self.panel2.place(x = 400, y = 65, width = 275, height = 275)
        #heading
        self.T = tk.Label(self.MainFrame)
        self.SubHeading = tk.Label(self.MainFrame)
        #self.T.place(x = 60, y = 5)

        #self.panel.pack()



        self.T.config(text = "Vaani", font = ("Algerian", 40, "bold"),foreground="#2b8ada",background="#e8f0fe")
        self.SubHeading.config(text="Sign Language to Text", font=("Matura M7 Script Capitals", 30, "bold"), foreground="#2b8ada", background="#e8f0fe")

        self.T.pack()
        self.SubHeading.pack()
        self.panel2.pack()




        self.LetterFrame = tk.Frame(master=self.LeftFrame,background="#e8f0fe",padx=5,pady=5)
        self.LetterButtonsFrame = tk.Frame(master=self.LeftFrame,background="#e8f0fe",padx=5,pady=5)
        self.CurrentLetterFrame = tk.Frame(master=self.LeftFrame,background="#e8f0fe",padx=5,pady=5)
        self.WordFrame = tk.Frame(master=self.LeftFrame,background="#e8f0fe",padx=5,pady=5)
        self.WordActionsFrame = tk.Frame(master=self.LeftFrame,background="#e8f0fe",padx=5,pady=5)
        self.SentenceFrame = tk.Frame(master=self.LeftFrame,background="#e8f0fe",padx=5,pady=5)
        self.WordSuggestFrame = tk.Frame(master=self.LeftFrame,background="#e8f0fe",padx=5,pady=5)
        self.WordButtonsFrame = tk.Frame(master=self.LeftFrame,background="#e8f0fe",padx=5,pady=5)

        #predicted letter
        self.pannel3Title = tk.Label(self.CurrentLetterFrame)
        self.pannel3Title.config(text="Predicted Letter :", font=("Bookman Old Style", 18, "bold"),background="#e8f0fe")
        self.panel3 = tk.Label(self.CurrentLetterFrame, font=("Seogoe UI Historic", 18, "bold"),background="#e8f0fe")  # Current Symbol

        # self.panel3.place(x = 500, y = 540)
        self.pannel3Title.pack(side=tk.LEFT,padx=5,pady=5)
        self.panel3.pack(side=tk.RIGHT,padx=5,pady=5)




        #word label
        self.T1 = tk.Label(self.LetterFrame,background="#e8f0fe")
        self.T1.config(text = "Word :", font = ("Bookman Old Style", 18, "bold"))
        self.T1.pack(side=tk.LEFT,padx=5,pady=5)
        self.panel4 = tk.Label(self.LetterFrame,background="#e8f0fe")
        self.panel4.pack(side=tk.LEFT,padx=5,pady=5)

        #buttons

        #clear letter
        self.clearLetter = tk.Button(self.LetterButtonsFrame, command=self.actionclearletter, height=0, width=0, pady=5, padx=5,
                                     foreground="white", background="gray", font=("Bookman Old Style", 10, "bold"), text="Clear")
        self.clearLetter.pack(side=tk.LEFT, pady=5, padx=15)
        # clear all
        self.clearWord = tk.Button(self.LetterButtonsFrame, command=self.actionclearall, height=0, width=0, pady=5, padx=5,
                             foreground="white", background="red", font=("Bookman Old Style", 10, "bold"),
                             text="Clear All")
        self.clearWord.pack(side=tk.LEFT, pady=5, padx=15)
        # enter
        self.enterWord = tk.Button(self.LetterButtonsFrame, command=self.actionenterword, height=0, width=0, pady=5, padx=5,
                             foreground="white", background="#2b8ada", font=("Bookman Old Style", 10, "bold"),
                             text="Enter")
        self.enterWord.pack(side=tk.LEFT, pady=5, padx=15)


        #sentence label
        self.T2 = tk.Label(self.WordFrame,background="#e8f0fe")
        self.T2.pack(side=tk.LEFT)
        self.T2.config(text = "Sentence :",foreground="red", font = ("Bookman Old Style", 18, "bold"))
        self.panel5 = tk.Label(self.WordFrame,background="#e8f0fe") # Sentence
        self.panel5.pack(side=tk.LEFT)

        #sentence buttons

        # clear letter
        self.clearLastWord = tk.Button(self.WordActionsFrame, command=self.actionclearlastword, height=0, width=0, pady=5,
                                     padx=5,
                                     foreground="white", background="gray", font=("Bookman Old Style", 10, "bold"),
                                     text="Clear")
        self.clearLastWord.pack(side=tk.LEFT, pady=5, padx=15)
        # clear all
        self.clearAllWords = tk.Button(self.WordActionsFrame, command=self.actionclearallwords, height=0, width=0, pady=5,
                                   padx=5,
                                   foreground="white", background="red", font=("Bookman Old Style", 10, "bold"),
                                   text="Clear All")
        self.clearAllWords.pack(side=tk.LEFT, pady=5, padx=15)


        #word suggestion label
        self.T4 = tk.Label(self.WordSuggestFrame,background="#e8f0fe")
        self.T4.pack(side=tk.LEFT)
        self.T4.config(text = "Word Suggestion :", fg = "black", font = ("Bookman Old Style", 18, "bold"))

        #word suggestion 1
        self.bt1 = tk.Button(self.WordButtonsFrame, command = self.action1, height = 0, width = 0,pady=5,padx=10,foreground="white",background="#2b8ada",font = ("Algerian", 16, "bold"))
        self.bt1.pack(side=tk.LEFT,pady=5,padx=15)

        # word suggestion 2
        self.bt2 = tk.Button(self.WordButtonsFrame, command = self.action2, height = 0, width = 0,pady=5,padx=10,foreground="white",background="#2b8ada",font = ("Algerian", 16, "bold"))
        self.bt2.pack(side=tk.LEFT,pady=5,padx=15)

        # word suggestion 3
        self.bt3 = tk.Button(self.WordButtonsFrame, command = self.action3, height = 0, width = 0,pady=5,padx=10,foreground="white",background="#2b8ada",font = ("Algerian", 16, "bold"))
        self.bt3.pack(side=tk.LEFT,pady=5,padx=15)

        self.CurrentLetterFrame.pack(side=tk.TOP,pady=5,padx=100,fill=tk.BOTH)
        self.LetterFrame.pack(side=tk.TOP,pady=5,padx=100,fill=tk.BOTH)
        self.LetterButtonsFrame.pack(side=tk.TOP,pady=5,padx=100,fill=tk.BOTH)

        self.WordSuggestFrame.pack(side=tk.TOP,pady=5,padx=100,fill=tk.BOTH)
        self.WordButtonsFrame.pack(side=tk.TOP, pady=5, padx=100, fill=tk.BOTH)
        self.WordFrame.pack(side=tk.TOP, pady=5, padx=100, fill=tk.BOTH)

        self.WordActionsFrame.pack(side=tk.TOP, pady=5, padx=100, fill=tk.BOTH)



        self.LeftFrame.pack(side=tk.LEFT,pady=50,fill=tk.BOTH)
        self.RightFrame.pack(side=tk.LEFT,pady=50,fill=tk.BOTH)
        self.MainFrame.pack(fill=tk.BOTH)


        self.str = ""
        self.word = " "
        self.current_symbol = "Empty"
        self.photo = "Empty"
        self.video_loop()


    def video_loop(self):
        ok, frame = self.vs.read()

        if ok:
            cv2image = cv2.flip(frame, 1)

            x1 = int(0.5 * frame.shape[1])
            y1 = 10
            x2 = frame.shape[1] - 10
            y2 = int(0.5 * frame.shape[1])

            cv2.rectangle(frame, (x1 - 1, y1 - 1), (x2 + 1, y2 + 1), (255, 0, 0) ,1)
            cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGBA)

            self.current_image = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image = self.current_image)

            self.panel.imgtk = imgtk
            self.panel.config(image = imgtk)

            cv2image = cv2image[y1 : y2, x1 : x2]

            gray = cv2.cvtColor(cv2image, cv2.COLOR_BGR2GRAY)

            blur = cv2.GaussianBlur(gray, (5, 5), 2)

            th3 = cv2.adaptiveThreshold(blur, 255 ,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

            ret, res = cv2.threshold(th3, 70, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            
            self.predict(res)

            self.current_image2 = Image.fromarray(res)

            imgtk = ImageTk.PhotoImage(image = self.current_image2)

            self.panel2.imgtk = imgtk
            self.panel2.config(image = imgtk)

            self.panel3.config(text = self.current_symbol, font = ("Seogoe UI Historic", 14))

            self.panel4.config(text = self.word, font = ("Seogoe UI Historic", 14))

            self.panel5.config(text = self.str,font = ("Seogoe UI Historic", 14))

            predicts = self.hs.suggest(self.word)
            
            if(len(predicts) > 1):

                self.bt1.config(text = predicts[0], font = ("Seogoe UI Historic", 14))

            else:

                self.bt1.config(text = "")

            if(len(predicts) > 2):

                self.bt2.config(text = predicts[1], font = ("Seogoe UI Historic", 14))

            else:

                self.bt2.config(text = "")

            if(len(predicts) > 3):

                self.bt3.config(text = predicts[2], font = ("Seogoe UI Historic", 14))

            else:

                self.bt3.config(text = "")


        self.root.after(5, self.video_loop)

    def predict(self, test_image):

        test_image = cv2.resize(test_image, (128, 128))

        result = self.loaded_model.predict(test_image.reshape(1, 128, 128, 1))


        result_dru = self.loaded_model_dru.predict(test_image.reshape(1 , 128 , 128 , 1))

        result_tkdi = self.loaded_model_tkdi.predict(test_image.reshape(1 , 128 , 128 , 1))

        result_smn = self.loaded_model_smn.predict(test_image.reshape(1 , 128 , 128 , 1))

        prediction = {}

        prediction['blank'] = result[0][0]

        inde = 1

        for i in ascii_uppercase:

            prediction[i] = result[0][inde]

            inde += 1

        #LAYER 1

        prediction = sorted(prediction.items(), key = operator.itemgetter(1), reverse = True)

        self.current_symbol = prediction[0][0]


        #LAYER 2

        if(self.current_symbol == 'D' or self.current_symbol == 'R' or self.current_symbol == 'U'):

        	prediction = {}

        	prediction['D'] = result_dru[0][0]
        	prediction['R'] = result_dru[0][1]
        	prediction['U'] = result_dru[0][2]

        	prediction = sorted(prediction.items(), key = operator.itemgetter(1), reverse = True)

        	self.current_symbol = prediction[0][0]

        if(self.current_symbol == 'D' or self.current_symbol == 'I' or self.current_symbol == 'K' or self.current_symbol == 'T'):

        	prediction = {}

        	prediction['D'] = result_tkdi[0][0]
        	prediction['I'] = result_tkdi[0][1]
        	prediction['K'] = result_tkdi[0][2]
        	prediction['T'] = result_tkdi[0][3]

        	prediction = sorted(prediction.items(), key = operator.itemgetter(1), reverse = True)

        	self.current_symbol = prediction[0][0]

        if(self.current_symbol == 'M' or self.current_symbol == 'N' or self.current_symbol == 'S'):

        	prediction1 = {}

        	prediction1['M'] = result_smn[0][0]
        	prediction1['N'] = result_smn[0][1]
        	prediction1['S'] = result_smn[0][2]

        	prediction1 = sorted(prediction1.items(), key = operator.itemgetter(1), reverse = True)

        	if(prediction1[0][0] == 'S'):

        		self.current_symbol = prediction1[0][0]

        	else:

        		self.current_symbol = prediction[0][0]
        
        if(self.current_symbol == 'blank'):

            for i in ascii_uppercase:
                self.ct[i] = 0

        self.ct[self.current_symbol] += 1

        if(self.ct[self.current_symbol] > 60):

            for i in ascii_uppercase:
                if i == self.current_symbol:
                    continue

                tmp = self.ct[self.current_symbol] - self.ct[i]

                if tmp < 0:
                    tmp *= -1

                if tmp <= 20:
                    self.ct['blank'] = 0

                    for i in ascii_uppercase:
                        self.ct[i] = 0
                    return

            self.ct['blank'] = 0

            for i in ascii_uppercase:
                self.ct[i] = 0

            if self.current_symbol == 'blank':

                if self.blank_flag == 0:
                    self.blank_flag = 1

                    if len(self.str) > 0:
                        self.str += " "

                    self.str += self.word

                    self.word = ""

            else:

                if(len(self.str) > 16):
                    self.str = ""

                self.blank_flag = 0

                self.word += self.current_symbol

    def actionclearletter(self):
        self.word = self.word[0:len(self.word)-1]

    def actionclearall(self):
        self.word = ''

    def actionenterword(self):
        if(self.word != ''):
            self.str= self.str+' '+self.word
            self.word = ''

    def actionclearlastword(self):
        if(self.str != ''):
          self.str=  self.str.rsplit(' ',1)[0]

    def actionclearallwords(self):
        self.str=''

    def action1(self):

    	predicts = self.hs.suggest(self.word)

    	if(len(predicts) > 0):

            self.word = ""

            self.str += " "

            self.str += predicts[0]

    def action2(self):

    	predicts = self.hs.suggest(self.word)

    	if(len(predicts) > 1):
            self.word = ""
            self.str += " "
            self.str += predicts[1]

    def action3(self):

    	predicts = self.hs.suggest(self.word)

    	if(len(predicts) > 2):
            self.word = ""
            self.str += " "
            self.str += predicts[2]

    def action4(self):

    	predicts = self.hs.suggest(self.word)

    	if(len(predicts) > 3):
            self.word = ""
            self.str += " "
            self.str += predicts[3]

    def action5(self):

    	predicts = self.hs.suggest(self.word)

    	if(len(predicts) > 4):
            self.word = ""
            self.str += " "
            self.str += predicts[4]
            
    def destructor(self):

        print("Closing Application...")

        self.root.destroy()
        self.vs.release()
        cv2.destroyAllWindows()
    
print("Starting Application...")

(Application()).root.mainloop()