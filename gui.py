import customtkinter

rootFrame = []
currentlyDisplayedMainFrame = []
currentlyDisplayedTimerLabel = []
currentlyDisplayedTopButtons = []
currentlyDisplayedButtonTopFrame = []
currentlyDisplayedButtonBottomFrame = []
currentlyDisplayedBottomButton = []
currentlyDisplayedChoiceFrame = []
currentlyDisplayedTimeDropdown = []
currentlyDisplayedNestedBottomFrame = []
currentlyDisplayedMainButtonFrame = []
currentTimer = []

currentPomodorMaxTime = 1800
currentLongBreakMaxTime = 600
currentShortBreakMaxTime = 300

isPaused = True

isDropDownOpen = False

isUpdatingPomodorTime = False
isUpdatingLongBreakTime = False
isUpdatingShortBreakTime = False

class Timer:
    def __init__(self, maxPomodoroTime, maxLongBreakTime, maxShortBreakTime):
        self.maxPomodoroTime = maxPomodoroTime
        self.maxLongBreakTime = maxLongBreakTime
        self.maxShortBreakTime = maxShortBreakTime
        self.currentPomodoroTimeLeft = self.maxPomodoroTime
        self.currentLongBreakTimeLeft = self.maxLongBreakTime
        self.currentShortBreakTimeLeft = self.maxShortBreakTime
        self.timerDelay = None
        self.isPaused = None
        self.isSetToPomodoroTime = True
        self.isSetToLongBreakTime = False
        self.isSetToShortBreakTime = False
    
    def ChangeTimerType(self, timerType:str):
        if timerType.lower() == "l":
            self.isSetToLongBreakTime = True
            self.isSetToShortBreakTime = False
            self.isSetToPomodoroTime = False
        elif timerType.lower() =="s":
            self.isSetToShortBreakTime = True
            self.isSetToPomodoroTime = False
            self.isSetToLongBreakTime = False
        else:
            self.isSetToPomodoroTime = True
            self.isSetToLongBreakTime = False
            self.isSetToShortBreakTime = False
            
            
    def StartTimer(self):
        self.isPaused = False
        if self.isSetToPomodoroTime == True:
            self.PomodoroCountDown()
        elif self.isSetToLongBreakTime == True:
            self.LongBreakCountDown()
        elif self.isSetToShortBreakTime == True:
            self.ShortBreakCountDown()
        
    def StopTimer(self):
        self.isPaused = True
        
    def SetNewPomodorTime(self, newTime):
        self.maxPomodoroTime = newTime
        self.ResetPomodoroTimer()
        self.UpdateLabel()
        
    def SetNewShortBreakTime(self, newTime):
        self.maxShortBreakTime = newTime
        self.ResetShortBreakTimer()
        self.UpdateLabel()
        
    def SetNewLongBreakTime(self, newTime):
        self.maxLongBreakTime = newTime
        self.ResetLongBreakTimer()
        self.UpdateLabel()
        
    def ResetPomodoroTimer(self):
        self.currentPomodoroTimeLeft = self.maxPomodoroTime
    
    def ResetShortBreakTimer(self):
        self.currentShortBreakTimeLeft = self.maxShortBreakTime
        
    def ResetLongBreakTimer(self):
        self.currentLongBreakTimeLeft = self.maxLongBreakTime

    def PomodoroCountDown(self):
        if self.isPaused == False:
            if self.currentPomodoroTimeLeft > 0:
                self.currentPomodoroTimeLeft -= 1
                self.UpdateLabel()
                self.timerDelay = rootFrame[0].after(1000, self.PomodoroCountDown)
            else:
                print("Timer finished.")
                
    def ShortBreakCountDown(self):
        if self.isPaused == False:
            if self.currentShortBreakTimeLeft > 0:
                self.currentShortBreakTimeLeft -= 1
                self.UpdateLabel()
                self.timerDelay = rootFrame[0].after(1000, self.ShortBreakCountDown)
            else:
                print("Timer finished.")
                
    def LongBreakCountDown(self):
        if self.isPaused == False:
            if self.currentLongBreakTimeLeft > 0:
                self.currentLongBreakTimeLeft -= 1
                self.UpdateLabel()
                self.timerDelay = rootFrame[0].after(1000, self.LongBreakCountDown)
            else:
                print("Timer finished.")

    def UpdateLabel(self):
        if self.isSetToShortBreakTime:
            minutes = self.currentShortBreakTimeLeft // 60
            seconds = self.currentShortBreakTimeLeft % 60
        elif self.isSetToLongBreakTime:
            minutes = self.currentLongBreakTimeLeft // 60
            seconds = self.currentLongBreakTimeLeft % 60
        else:
            minutes = self.currentPomodoroTimeLeft // 60
            seconds = self.currentPomodoroTimeLeft % 60
            
        timeStr = f"{minutes:02d}:{seconds:02d}"
        currentlyDisplayedTimerLabel[0].configure(text=timeStr)
    
    def ReturnPomodoroTime(self)-> str:
        minutes = self.currentPomodoroTimeLeft // 60
        seconds = self.currentPomodoroTimeLeft % 60
        timeStr = f"{minutes:02d}:{seconds:02d}"
        return timeStr
    


def CreateTimer():
    if not currentTimer:
        timer = Timer(maxPomodoroTime=1800, maxLongBreakTime=600, maxShortBreakTime=300)
        currentTimer.append(timer)
    else:
        currentTimer.clear()
        timer= Timer(maxTime=1800, maxLongBreakTime=600, maxShortBreakTime=300)
        currentTimer.append(timer)

def CreateRootFrame():
    frame = customtkinter.CTk()
    frame.geometry("1366x768")
    frame.title("Pomodoro Timer DX")
    frame.resizable(False, False)
    rootFrame.append(frame)

def CreateMainFrame():
    mainFrame = customtkinter.CTkFrame(master=rootFrame[0])
    mainFrame.pack(fill="both", expand=True)
    mainFrame.configure(fg_color="#03071e")
    currentlyDisplayedMainFrame.clear()
    currentlyDisplayedMainFrame.append(mainFrame)
    
def CreateMainButtonFrame():
    mainButtonFrame = customtkinter.CTkFrame(master=currentlyDisplayedMainFrame[0])
    mainButtonFrame.pack(fill="both", expand=False)
    mainButtonFrame.configure(fg_color="#03071e")
    currentlyDisplayedMainButtonFrame.clear()
    currentlyDisplayedMainButtonFrame.append(mainButtonFrame)
     

def CreateTimerLabel():
    timerLabel = customtkinter.CTkLabel(master=currentlyDisplayedMainFrame[0], text=currentTimer[0].ReturnPomodoroTime(), font=("Great Vibes", 175))
    timerLabel.pack(padx=(25, 20), pady=(40, 5))
    currentlyDisplayedTimerLabel.clear()
    currentlyDisplayedTimerLabel.append(timerLabel)

def CreateTopMenu():
    CreateTopButtonFrame()
    CreateTopLabel()
    CreateTopButtons()
    
def CreateTopLabel():
    topLabel = customtkinter.CTkLabel(master=currentlyDisplayedButtonTopFrame[0], text="SETTINGS", font=("Great Vibes", 40))
    topLabel.pack(pady=0,padx=60)


            
def CreateTopButtonFrame():
    frame = customtkinter.CTkFrame(master=currentlyDisplayedMainFrame[0], height=100, fg_color="transparent")
    frame.pack(pady=(20,40),padx=60, side="top", fill="x", expand=False)
    currentlyDisplayedButtonTopFrame.clear()
    currentlyDisplayedButtonTopFrame.append(frame)
    
def CreateChoiceFrame():
    frame = customtkinter.CTkFrame(master=currentlyDisplayedMainFrame[0], height=50, fg_color="transparent")
    frame.pack(pady=(10,0),padx=60, side="top", expand=False)
    currentlyDisplayedChoiceFrame.clear()
    currentlyDisplayedChoiceFrame.append(frame)
    
def CreateBottomButtonFrame():
    frame = customtkinter.CTkFrame(master=currentlyDisplayedMainButtonFrame[0], height=100, fg_color="transparent")
    frame.pack(pady=20,padx=60, side="bottom", fill="x", expand=False)
    currentlyDisplayedButtonBottomFrame.clear()
    currentlyDisplayedButtonBottomFrame.append(frame)
    
def CreateNestedBottomButtonFrame():
    frame = customtkinter.CTkFrame(master=currentlyDisplayedButtonBottomFrame[0], height=100, fg_color="transparent")
    frame.pack(pady=20,padx=60, side="bottom", fill="x", expand=False)
    currentlyDisplayedNestedBottomFrame.clear()
    currentlyDisplayedNestedBottomFrame.append(frame)

def ButtonClicked():
    print("Button clicked")
    
def optionmenu_callback(choice):
    print("optionmenu dropdown clicked:", choice)
    
    if choice =="1 Hr":
        if isUpdatingPomodorTime == True:
            currentTimer[0].SetNewPomodorTime(3600)
            ToggleButtonTypeBoolsOff()
            ClearDropdown()
            
        elif isUpdatingLongBreakTime == True:
            currentTimer[0].SetNewLongBreakTime(300)
            ToggleButtonTypeBoolsOff()
            ClearDropdown()
            
        elif isUpdatingShortBreakTime == True:
            currentTimer[0].SetNewShortBreakTime(300)
            ToggleButtonTypeBoolsOff()
            ClearDropdown()
            pass

        
    if choice =="45 Min":
        if isUpdatingPomodorTime == True:
            currentTimer[0].SetNewPomodorTime(2700)
            ToggleButtonTypeBoolsOff()
            ClearDropdown()
            
        elif isUpdatingLongBreakTime == True:
            currentTimer[0].SetNewLongBreakTime(300)
            ToggleButtonTypeBoolsOff()
            ClearDropdown()
            
        elif isUpdatingShortBreakTime == True:
            currentTimer[0].SetNewShortBreakTime(300)
            ToggleButtonTypeBoolsOff()
            ClearDropdown()
            pass

        
    if choice =="30 Min":
        if isUpdatingPomodorTime == True:
            currentTimer[0].SetNewPomodorTime(1800)
            ToggleButtonTypeBoolsOff()
            ClearDropdown()
            
        elif isUpdatingLongBreakTime == True:
            currentTimer[0].SetNewLongBreakTime(300)
            ToggleButtonTypeBoolsOff()
            ClearDropdown()
            
        elif isUpdatingShortBreakTime == True:
            currentTimer[0].SetNewShortBreakTime(300)
            ToggleButtonTypeBoolsOff()
            ClearDropdown()
            pass

        
    if choice =="15 Min":
        if isUpdatingPomodorTime == True:
            currentTimer[0].SetNewPomodorTime(900)
            ToggleButtonTypeBoolsOff()
            ClearDropdown()
            
        elif isUpdatingLongBreakTime == True:
            currentTimer[0].SetNewLongBreakTime(300)
            ToggleButtonTypeBoolsOff()
            ClearDropdown()
            
        elif isUpdatingShortBreakTime == True:
            currentTimer[0].SetNewShortBreakTime(300)
            ToggleButtonTypeBoolsOff()
            ClearDropdown()
            pass

        
    if choice =="5 Min":
        if isUpdatingPomodorTime == True:
            currentTimer[0].SetNewPomodorTime(300)
            ToggleButtonTypeBoolsOff()
            ClearDropdown()
            
        elif isUpdatingLongBreakTime == True:
            currentTimer[0].SetNewLongBreakTime(300)
            ToggleButtonTypeBoolsOff()
            ClearDropdown()
            
        elif isUpdatingShortBreakTime == True:
            currentTimer[0].SetNewShortBreakTime(300)
            ToggleButtonTypeBoolsOff()
            ClearDropdown()
            pass


def ClearDropdown():
    global isDropDownOpen
    for dropdown in currentlyDisplayedTimeDropdown:
        dropdown.destroy()
    currentlyDisplayedTimeDropdown.clear()
    isDropDownOpen = False
    ResetBottomButtons()
    
def ToggleButtonTypeBoolsOff():
    global isUpdatingLongBreakTime, isUpdatingShortBreakTime, isUpdatingPomodorTime
    
    isUpdatingLongBreakTime = False
    isUpdatingShortBreakTime = False
    isUpdatingPomodorTime = False

def TimeOptionClicked(buttonType:str):
    global isUpdatingLongBreakTime, isUpdatingPomodorTime, isUpdatingShortBreakTime, isDropDownOpen
    if isDropDownOpen == True:
        return
    else:
        isDropDownOpen = True
        RemoveBottomButtons()

        
        if buttonType == "p":
            isUpdatingPomodorTime = True
        if buttonType =="l":
            isUpdatingLongBreakTime = True
        if buttonType =="s":
            isUpdatingShortBreakTime = True
            
        optionMenuVar = customtkinter.StringVar(value="30 Min")
        optionMenu = customtkinter.CTkOptionMenu(currentlyDisplayedMainButtonFrame[0],values=["1 Hr","45 Min","30 Min","15 Min","5 Min"],
                                                command=optionmenu_callback,
                                                variable=optionMenuVar,
                                                height= 50,
                                                width = 500,
                                                fg_color="#9d0208",
                                                dropdown_fg_color="#9d0208",
                                                dropdown_font=("Great Vibes", 50),
                                                dropdown_hover_color="#370617",
                                                button_color="#370617",
                                                button_hover_color="#370617",
                                                font=("Great Vibes", 50)
    )
        optionMenu.pack(side="bottom", pady=(50, 0), padx=90)
        currentlyDisplayedTimeDropdown.append(optionMenu)

def CreateTopButtons():
    buttonPomodoro = customtkinter.CTkButton(currentlyDisplayedButtonTopFrame[0], text="Pomodoro", font=("Great Vibes", 30), command=lambda option="p":TimeOptionClicked(option), border_color="#370617", border_width=3, fg_color="#9d0208", hover_color="#370617", corner_radius=10)
    buttonPomodoro.configure(height=75, width=200)
    buttonPomodoro.pack(side="left", pady=12, padx=(270, 40))
    buttonShortBreak = customtkinter.CTkButton(currentlyDisplayedButtonTopFrame[0], text="Short Break", font=("Great Vibes", 30), command=lambda option="s":TimeOptionClicked(option), border_color="#370617", border_width=3, fg_color="#9d0208", hover_color="#370617", corner_radius=10)
    buttonShortBreak.configure(height=75, width=200)
    buttonShortBreak.pack(side="left", pady=12, padx=(20, 40))
    buttonLongBreak = customtkinter.CTkButton(currentlyDisplayedButtonTopFrame[0], text="Long Break", font=("Great Vibes", 30), command=lambda option="l":TimeOptionClicked(option), border_color="#370617", border_width=3, fg_color="#9d0208", hover_color="#370617", corner_radius=10)
    buttonLongBreak.configure(height=75, width=200)
    buttonLongBreak.pack(side="left", pady=12, padx=20)
    currentlyDisplayedTopButtons.append(buttonPomodoro)
    currentlyDisplayedTopButtons.append(buttonShortBreak)
    currentlyDisplayedTopButtons.append(buttonLongBreak)
    
def StartButtonClicked():
    global isPaused
    isPaused = False
    currentTimer[0].StartTimer()
    print("Starting")
    ResetBottomButtons()
    
def PauseButtonClicked():
    global isPaused
    isPaused = True
    currentTimer[0].StopTimer()
    print("Pausing")
    ResetBottomButtons()
    

    
def ResetBottomButtons():
    for button in currentlyDisplayedBottomButton:
        button.destroy()
    currentlyDisplayedBottomButton.clear()
    CreateBottomButton()
    CreateNestedBottomButtons()
    
def RemoveBottomButtons():
    for button in currentlyDisplayedBottomButton:
        button.destroy()
    currentlyDisplayedBottomButton.clear()
    
def ShortBreakButtonClicked():
    global isPaused
    isPaused = False
    currentTimer[0].ChangeTimerType("s")
    currentTimer[0].StartTimer()
    print("Starting")
    ResetBottomButtons()


def LongBreakButtonClicked():
    return
    
def CreateBottomButton():
    global isPaused
    if isPaused == True:
        buttonStart = customtkinter.CTkButton(currentlyDisplayedButtonBottomFrame[0], text="START", font=("Great Vibes", 50), command=StartButtonClicked, border_color="#370617", border_width=3, fg_color="#9d0208", hover_color="#370617", corner_radius=10)
        buttonStart.configure(height=175, width=250)
        buttonStart.pack(side="bottom", pady=(20, 40), padx=90, expand=True)
        currentlyDisplayedBottomButton.append(buttonStart)
    else:
        buttonPause = customtkinter.CTkButton(currentlyDisplayedButtonBottomFrame[0], text="PAUSE", font=("Great Vibes", 50), command=PauseButtonClicked, border_color="#370617", border_width=3, fg_color="#9d0208", hover_color="#370617", corner_radius=10)
        buttonPause.configure(height=175, width=250)
        buttonPause.pack(side="bottom", pady=(50, 40), padx=90)
        currentlyDisplayedBottomButton.append(buttonPause)
        
def CreateNestedBottomButtons():
    

    buttonShortBreak = customtkinter.CTkButton(currentlyDisplayedNestedBottomFrame[0], text="Pomodoro", font=("Great Vibes", 30), command=ShortBreakButtonClicked, border_color="#370617", border_width=3, fg_color="#9d0208", hover_color="#370617", corner_radius=10)
    buttonShortBreak.configure(height=75, width=200)
    buttonShortBreak.pack(side="left", pady=(0, 0), padx=(200,40))
    currentlyDisplayedBottomButton.append(buttonShortBreak)
    
    buttonStudy = customtkinter.CTkButton(currentlyDisplayedNestedBottomFrame[0], text="Short Break", font=("Great Vibes", 30), command=ShortBreakButtonClicked, border_color="#370617", border_width=3, fg_color="#9d0208", hover_color="#370617", corner_radius=10)
    buttonStudy.configure(height=75, width=200)
    buttonStudy.pack(side="left", pady=(0, 0), padx=(20,40))
    currentlyDisplayedBottomButton.append(buttonStudy)
    
    
    buttonLongBreak = customtkinter.CTkButton(currentlyDisplayedNestedBottomFrame[0], text="Long Break", font=("Great Vibes", 30), command=LongBreakButtonClicked, border_color="#370617", border_width=3, fg_color="#9d0208", hover_color="#370617", corner_radius=10)
    buttonLongBreak.configure(height=75, width=200)
    buttonLongBreak.pack(side="left", pady=(0, 0), padx=20)
    currentlyDisplayedBottomButton.append(buttonLongBreak)



def Main():
    CreateRootFrame()
    CreateMainFrame()
    CreateTopMenu()
    CreateTimer()
    CreateTimerLabel()
    CreateMainButtonFrame()
    CreateBottomButtonFrame()
    CreateNestedBottomButtonFrame()
    CreateBottomButton()
    CreateNestedBottomButtons()
    CreateChoiceFrame()



    rootFrame[0].mainloop()

if __name__ == "__main__":
    Main()
