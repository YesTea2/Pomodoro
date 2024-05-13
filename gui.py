import customtkinter
from PIL import Image, ImageTk
from pygame import mixer

rootFrame = []
currentlyDisplayedMainFrame = []
currentlyDisplayedTimerLabel = []
currentlyDisplayedTimerText = []
currentlyDisplayedTopButtons = []
currentlyDisplayedButtonTopFrame = []
currentlyDisplayedButtonBottomFrame = []
currentlyDisplayedBottomButton = []
currentlyDisplayedChoiceFrame = []
currentlyDisplayedTimeDropdown = []
currentlyDisplayedAlarmDropdown = []
currentlyDisplayedSoundDropdown = []
currentlyDisplayedNestedBottomFrame = []
currentlyDisplayedMainButtonFrame = []
currentAlarmSound = ["Alarm Sound 1"]
currentButtonSound = ["Button Sound 1"]
currentTimer = []
buttonSounds = []
alarmSounds = []
soundMixer = []

currentButtonSoundArrayNumber = [0]
currentAlarmSoundArrayNumber = [0]

currentPomodorMaxTime = 1800
currentLongBreakMaxTime = 900
currentShortBreakMaxTime = 300

isPaused = True

isDropDownOpen = False
isSoundDropDownOpen = False
isAlarmDropDownOpen = False

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
        self.isPaused= True
        
        if timerType.lower() == "l":
            self.isSetToLongBreakTime = True
            self.isSetToShortBreakTime = False
            self.isSetToPomodoroTime = False
            self.ResetAllTimers()
            self.UpdateLabel()
        elif timerType.lower() =="s":
            self.isSetToShortBreakTime = True
            self.isSetToPomodoroTime = False
            self.isSetToLongBreakTime = False
            self.ResetAllTimers()
            self.UpdateLabel()
        else:
            self.isSetToPomodoroTime = True
            self.isSetToLongBreakTime = False
            self.isSetToShortBreakTime = False
            self.ResetAllTimers()
            self.UpdateLabel()
            
            
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
        print(self.maxShortBreakTime)
        self.ResetShortBreakTimer()
        self.UpdateLabel()
        
    def SetNewLongBreakTime(self, newTime):
        self.maxLongBreakTime = newTime
        self.ResetLongBreakTimer()
        self.UpdateLabel()
        
    def ResetAllTimers(self):
        self.ResetLongBreakTimer()
        self.ResetShortBreakTimer()
        self.ResetPomodoroTimer()
        
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
                self.ResetAllTimers()
                self.UpdateLabel()
                alarmSounds[currentAlarmSoundArrayNumber[0]].play()
                
                
    def ShortBreakCountDown(self):
        if self.isPaused == False:
            if self.currentShortBreakTimeLeft > 0:
                self.currentShortBreakTimeLeft -= 1
                self.UpdateLabel()
                self.timerDelay = rootFrame[0].after(1000, self.ShortBreakCountDown)
            else:
                self.ResetAllTimers()
                self.UpdateLabel()
                alarmSounds[currentAlarmSoundArrayNumber[0]].play()
                
                
    def LongBreakCountDown(self):
        if self.isPaused == False:
            if self.currentLongBreakTimeLeft > 0:
                self.currentLongBreakTimeLeft -= 1
                self.UpdateLabel()
                self.timerDelay = rootFrame[0].after(1000, self.LongBreakCountDown)
            else:
                self.ResetAllTimers()
                self.UpdateLabel()
                alarmSounds[currentAlarmSoundArrayNumber[0]].play()

    def UpdateLabel(self):
        currentOption = ""
        if self.isSetToShortBreakTime:
            minutes = self.currentShortBreakTimeLeft // 60
            seconds = self.currentShortBreakTimeLeft % 60
            currentOption = "Short Break Time"
        elif self.isSetToLongBreakTime:
            minutes = self.currentLongBreakTimeLeft // 60
            seconds = self.currentLongBreakTimeLeft % 60
            currentOption = "Long Break Time"
        else:
            minutes = self.currentPomodoroTimeLeft // 60
            seconds = self.currentPomodoroTimeLeft % 60
            currentOption = "Pomodoro Time"
        
        currentlyDisplayedTimerText[0].configure(text=currentOption)
        
        timeStr = f"{minutes:02d}:{seconds:02d}"
        currentlyDisplayedTimerLabel[0].configure(text=timeStr)
        
    
    def ReturnPomodoroTime(self)-> str:
        minutes = self.currentPomodoroTimeLeft // 60
        seconds = self.currentPomodoroTimeLeft % 60
        timeStr = f"{minutes:02d}:{seconds:02d}"
        return timeStr
    
    def GetCurrentlValue(self)->str:
        currentValue = ""
        if self.isSetToShortBreakTime:
            if self.maxShortBreakTime == 3600:
                currentValue = "1 Hr"
                
            if self.maxShortBreakTime == 2700:
                currentValue = "45 Min"
                
            if self.maxShortBreakTime == 1800:
                currentValue = "30 Min"
                
            if self.maxShortBreakTime == 900:
                currentValue = "15 Min"
                
            if self.maxShortBreakTime == 300:
                currentValue = "5 Min"
                
        elif self.isSetToLongBreakTime:
            if self.maxLongBreakTime == 3600:
                currentValue = "1 Hr"
                
            if self.maxLongBreakTime == 2700:
                currentValue = "45 Min"
                
            if self.maxLongBreakTime == 1800:
                currentValue = "30 Min"
                
            if self.maxLongBreakTime == 900:
                currentValue = "15 Min"
                
            if self.maxLongBreakTime == 300:
                currentValue = "5 Min"
                
        else:
            if self.maxPomodoroTime == 3600:
                currentValue = "1 Hr"
                
            if self.maxPomodoroTime == 2700:
                currentValue = "45 Min"
                
            if self.maxPomodoroTime == 1800:
                currentValue = "30 Min"
                
            if self.maxPomodoroTime == 900:
                currentValue = "15 Min"
                
            if self.maxPomodoroTime == 300:
                currentValue = "5 Min"
                
        return currentValue      
 
 
def CreateSoundMixer():
    mixer.init()
    soundMixer.append(mixer)   

def CreateButtonSounds():
    buttonSoundOne = soundMixer[0].Sound("Sounds/Buttons/Button1.wav")
    buttonSoundTwo = soundMixer[0].Sound("Sounds/Buttons/Button2.wav")
    buttonSoundThree = soundMixer[0].Sound("Sounds/Buttons/Button3.wav")
    buttonSoundFour = soundMixer[0].Sound("Sounds/Buttons/Button4.wav")
    buttonSoundFive = soundMixer[0].Sound("Sounds/Buttons/Button5.wav")
    buttonSounds.append(buttonSoundOne)
    buttonSounds.append(buttonSoundTwo)
    buttonSounds.append(buttonSoundThree)
    buttonSounds.append(buttonSoundFour)
    buttonSounds.append(buttonSoundFive)
    
def CreateAlarmSounds():
    alarmSoundOne = soundMixer[0].Sound("Sounds/Alarms/alarm1.wav")
    alarmSoundTwo = soundMixer[0].Sound("Sounds/Alarms/alarm2.wav")
    alarmSoundThree = soundMixer[0].Sound("Sounds/Alarms/alarm3.wav")
    alarmSoundFour = soundMixer[0].Sound("Sounds/Alarms/alarm4.wav")
    alarmSoundFive = soundMixer[0].Sound("Sounds/Alarms/alarm5.wav")
    alarmSounds.append(alarmSoundOne)
    alarmSounds.append(alarmSoundTwo)
    alarmSounds.append(alarmSoundThree)
    alarmSounds.append(alarmSoundFour)
    alarmSounds.append(alarmSoundFive)
    

def CreateTimer():
    if not currentTimer:
        timer = Timer(maxPomodoroTime=1800, maxLongBreakTime=900, maxShortBreakTime=300)
        currentTimer.append(timer)
    else:
        currentTimer.clear()
        timer= Timer(maxTime=1800, maxLongBreakTime=900, maxShortBreakTime=300)
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
    timerText = customtkinter.CTkLabel(master=currentlyDisplayedMainFrame[0], text="Pomodoro Time", font=("Great Vibes", 40))
    timerText.pack(padx=(25, 20), pady=(0,5))
    timerLabel = customtkinter.CTkLabel(master=currentlyDisplayedMainFrame[0], text=currentTimer[0].ReturnPomodoroTime(), font=("Great Vibes", 175))
    timerLabel.pack(padx=(25, 20), pady=(10, 5))
    
    currentlyDisplayedTimerText.clear()
    currentlyDisplayedTimerText.append(timerText)
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
    
def SoundMenu(choice):
    print(choice)
    
def AlarmMenu(choice):
    
    if choice == "Alarm Sound 1":
        currentAlarmSound.clear()
        currentAlarmSound.append("Alarm Sound 1")
        currentAlarmSoundArrayNumber.clear()
        currentAlarmSoundArrayNumber.append(0)
        alarmSounds[0].play()
        
    if choice =="Alarm Sound 2":
        currentAlarmSound.clear()
        currentAlarmSound.append("Alarm Sound 2")
        currentAlarmSoundArrayNumber.clear()
        currentAlarmSoundArrayNumber.append(1)
        alarmSounds[1].play()
        
    if choice =="Alarm Sound 3":
        currentAlarmSound.clear()
        currentAlarmSound.append("Alarm Sound 3")
        currentAlarmSoundArrayNumber.clear()
        currentAlarmSoundArrayNumber.append(2)
        alarmSounds[2].play()
        
    if choice =="Alarm Sound 4":
        currentAlarmSound.clear()
        currentAlarmSound.append("Alarm Sound 4")
        currentAlarmSoundArrayNumber.clear()
        currentAlarmSoundArrayNumber.append(3)
        alarmSounds[3].play()
        
    if choice =="Alarm Sound 5":
        currentAlarmSound.clear()
        currentAlarmSound.append("Alarm Sound 5")
        currentAlarmSoundArrayNumber.clear()
        currentAlarmSoundArrayNumber.append(4)
        alarmSounds[4].play()
        
    print(choice)
    
def TimerMenu(choice):
    print("optionmenu dropdown clicked:", choice)
    
    if choice =="1 Hr":
        if isUpdatingPomodorTime == True:
            currentTimer[0].SetNewPomodorTime(3600)
            ToggleButtonTypeBoolsOff()
            ClearDropdown()
            
        elif isUpdatingLongBreakTime == True:
            currentTimer[0].SetNewLongBreakTime(3600)
            ToggleButtonTypeBoolsOff()
            ClearDropdown()
            
        elif isUpdatingShortBreakTime == True:
            currentTimer[0].SetNewShortBreakTime(3600)
            ToggleButtonTypeBoolsOff()
            ClearDropdown()
            

        
    if choice =="45 Min":
        if isUpdatingPomodorTime == True:
            currentTimer[0].SetNewPomodorTime(2700)
            ToggleButtonTypeBoolsOff()
            ClearDropdown()
            
        elif isUpdatingLongBreakTime == True:
            currentTimer[0].SetNewLongBreakTime(2700)
            ToggleButtonTypeBoolsOff()
            ClearDropdown()
            
        elif isUpdatingShortBreakTime == True:
            currentTimer[0].SetNewShortBreakTime(2700)
            ToggleButtonTypeBoolsOff()
            ClearDropdown()
            
        
    if choice =="30 Min":
        if isUpdatingPomodorTime == True:
            currentTimer[0].SetNewPomodorTime(1800)
            ToggleButtonTypeBoolsOff()
            ClearDropdown()
            
        elif isUpdatingLongBreakTime == True:
            currentTimer[0].SetNewLongBreakTime(1800)
            ToggleButtonTypeBoolsOff()
            ClearDropdown()
            
        elif isUpdatingShortBreakTime == True:
            currentTimer[0].SetNewShortBreakTime(1800)
            ToggleButtonTypeBoolsOff()
            ClearDropdown()
           

        
    if choice =="15 Min":
        if isUpdatingPomodorTime == True:
            currentTimer[0].SetNewPomodorTime(900)
            ToggleButtonTypeBoolsOff()
            ClearDropdown()
            
        elif isUpdatingLongBreakTime == True:
            currentTimer[0].SetNewLongBreakTime(900)
            ToggleButtonTypeBoolsOff()
            ClearDropdown()
            
        elif isUpdatingShortBreakTime == True:
            currentTimer[0].SetNewShortBreakTime(900)
            ToggleButtonTypeBoolsOff()
            ClearDropdown()
          

        
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
    buttonSounds[1].play() 


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
    global isUpdatingLongBreakTime, isUpdatingPomodorTime, isUpdatingShortBreakTime, isDropDownOpen, isPaused, isAlarmDropDownOpen, isSoundDropDownOpen
    
    timerType = ""
    buttonSounds[currentButtonSoundArrayNumber[0]].play()

    
    
    if isDropDownOpen == True:
        for dropdown in currentlyDisplayedTimeDropdown:
            dropdown.destroy()
        currentlyDisplayedTimeDropdown.clear()
        ToggleButtonTypeBoolsOff()
    else:
        isDropDownOpen = True
        isPaused = True
        currentTimer[0].StopTimer()
        RemoveBottomButtons()
        
    if isAlarmDropDownOpen == True:
        for dropdown in currentlyDisplayedAlarmDropdown:
            dropdown.destroy()
        currentlyDisplayedAlarmDropdown.clear()
        isAlarmDropDownOpen = False

    if buttonType == "p":
        timerType = "Pomodoro"
        currentTimer[0].ChangeTimerType("p")
        isUpdatingPomodorTime = True
    if buttonType =="l":
        timerType = "Long Break"
        currentTimer[0].ChangeTimerType("l")
        isUpdatingLongBreakTime = True
    if buttonType =="s":
        timerType = "Short Break"
        currentTimer[0].ChangeTimerType("s")
        isUpdatingShortBreakTime = True
            
    currentlySelectedValue = currentTimer[0].GetCurrentlValue()
    timerMenuVar = customtkinter.StringVar(value=currentlySelectedValue)
    timerMenuLabel = customtkinter.CTkLabel(currentlyDisplayedMainButtonFrame[0], text=f"Select Time For {timerType}", font=("Great Vibes", 40))
    timerMenu = customtkinter.CTkOptionMenu(currentlyDisplayedMainButtonFrame[0],values=["1 Hr","45 Min","30 Min","15 Min","5 Min"],
                                            command=TimerMenu,
                                            variable=timerMenuVar,
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
    timerMenuLabel.pack(side="top", pady=10, padx=90)
    timerMenu.pack(side="bottom", pady=(20, 0), padx=90)
    currentlyDisplayedTimeDropdown.append(timerMenuLabel)
    currentlyDisplayedTimeDropdown.append(timerMenu)


def AlarmButtonClicked():
    global isSoundDropDownOpen, isDropDownOpen, isAlarmDropDownOpen, isPaused
    
    buttonSounds[currentButtonSoundArrayNumber[0]].play()

    
    
    if isDropDownOpen == True:
        for dropdown in currentlyDisplayedTimeDropdown:
            dropdown.destroy()
        currentlyDisplayedTimeDropdown.clear()
        ToggleButtonTypeBoolsOff()
        isDropDownOpen = False
        
    if isSoundDropDownOpen == True:
        for dropdown in currentlyDisplayedSoundDropdown:
            dropdown.destroy()
        currentlyDisplayedSoundDropdown.clear()
        isSoundDropDownOpen = False
        
    if isAlarmDropDownOpen == True:
        for dropdown in currentlyDisplayedAlarmDropdown:
            dropdown.destroy()
        currentlyDisplayedAlarmDropdown.clear()
        
    isAlarmDropDownOpen = True
    isPaused = True
    currentTimer[0].StopTimer()
    RemoveBottomButtons()

    alarmMenuVar = customtkinter.StringVar(value=currentAlarmSound[0])
    alarmMenuLabel = customtkinter.CTkLabel(currentlyDisplayedMainButtonFrame[0], text=f"Select Alarm Sound", font=("Great Vibes", 40))
    alarmMenu = customtkinter.CTkOptionMenu(currentlyDisplayedMainButtonFrame[0],values=["Alarm Sound 1","Alarm Sound 2","Alarm Sound 3","Alarm Sound 4","Alarm Sound 5"],
                                            command=AlarmMenu,
                                            variable=alarmMenuVar,
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
    alarmMenuLabel.pack(side="top", pady=10, padx=90)
    alarmMenu.pack(side="bottom", pady=(20, 0), padx=90)
    currentlyDisplayedAlarmDropdown.append(alarmMenuLabel)
    currentlyDisplayedAlarmDropdown.append(alarmMenu)
    return

def SoundButtonClicked():
    global isSoundDropDownOpen, isDropDownOpen, isAlarmDropDownOpen, isPaused
    
    buttonSounds[currentButtonSoundArrayNumber[0]].play()

    if isDropDownOpen == True:
        for dropdown in currentlyDisplayedTimeDropdown:
            dropdown.destroy()
        currentlyDisplayedTimeDropdown.clear()
        ToggleButtonTypeBoolsOff()
        isDropDownOpen = False
        
        
    if isAlarmDropDownOpen == True:
        for dropdown in currentlyDisplayedAlarmDropdown:
            dropdown.destroy()
        currentlyDisplayedAlarmDropdown.clear()
        isAlarmDropDownOpen = False
        
    if isSoundDropDownOpen == True:
        for dropdown in currentlyDisplayedSoundDropdown:
            dropdown.destroy()
        currentlyDisplayedSoundDropdown.clear()
        
    isSoundDropDownOpen = True
    isPaused = True
    currentTimer[0].StopTimer()
    RemoveBottomButtons()

    soundMenuVar = customtkinter.StringVar(value=currentButtonSound[0])
    soundMenuLabel = customtkinter.CTkLabel(currentlyDisplayedMainButtonFrame[0], text=f"Select Button Sound", font=("Great Vibes", 40))
    soundMenu = customtkinter.CTkOptionMenu(currentlyDisplayedMainButtonFrame[0],values=["Button Sound 1","Button Sound 2","Button Sound 3","Button Sound 4","Button Sound 5"],
                                            command=SoundMenu,
                                            variable=soundMenuVar,
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
    soundMenuLabel.pack(side="top", pady=10, padx=90)
    soundMenu.pack(side="bottom", pady=(20, 0), padx=90)
    currentlyDisplayedSoundDropdown.append(soundMenuLabel)
    currentlyDisplayedSoundDropdown.append(soundMenu)
    return

def CreateTopButtons():
    buttonPomodoro = customtkinter.CTkButton(currentlyDisplayedButtonTopFrame[0], text_color="white", text="Pomodoro", font=("Great Vibes", 30), command=lambda option="p":TimeOptionClicked(option), border_color="#370617", border_width=3, fg_color="#9d0208", hover_color="#370617", corner_radius=10)
    buttonPomodoro.configure(height=75, width=200)
    buttonPomodoro.pack(side="left", pady=12, padx=(260, 40))
    
    buttonLongBreak = customtkinter.CTkButton(currentlyDisplayedButtonTopFrame[0], text_color="white", text="Long Break", font=("Great Vibes", 30), command=lambda option="l":TimeOptionClicked(option), border_color="#370617", border_width=3, fg_color="#9d0208", hover_color="#370617", corner_radius=10)
    buttonLongBreak.configure(height=75, width=200)
    buttonLongBreak.pack(side="left", pady=12, padx=20)
    
    buttonShortBreak = customtkinter.CTkButton(currentlyDisplayedButtonTopFrame[0], text_color="white", text="Short Break", font=("Great Vibes", 30), command=lambda option="s":TimeOptionClicked(option), border_color="#370617", border_width=3, fg_color="#9d0208", hover_color="#370617", corner_radius=10)
    buttonShortBreak.configure(height=75, width=200)
    buttonShortBreak.pack(side="left", pady=12, padx=(40, 40))
    
    alarmImage = customtkinter.CTkImage(Image.open("Imgs/alarm.png"), size=(30, 30))
    soundImage = customtkinter.CTkImage(Image.open("Imgs/sound.png"), size=(30, 30))
    
    alarmButton = customtkinter.CTkButton(master=currentlyDisplayedButtonTopFrame[0], text="",image=alarmImage, fg_color="#9d0208", hover_color="#370617", command=AlarmButtonClicked, border_color="#370617", border_width=3)
    alarmButton.configure(height=50, width=50)
    alarmButton.pack(side="left", pady=(0,0), padx=(20,20))
    
    soundButton = customtkinter.CTkButton(master=currentlyDisplayedButtonTopFrame[0], text="",image=soundImage, fg_color="#9d0208", hover_color="#370617", command=SoundButtonClicked, border_color="#370617", border_width=3)
    soundButton.configure(height=50, width=50)
    soundButton.pack(side="left", pady=(0,0), padx=(10,40))

    currentlyDisplayedTopButtons.append(alarmButton)
    currentlyDisplayedTopButtons.append(soundButton)
    currentlyDisplayedTopButtons.append(buttonPomodoro)
    currentlyDisplayedTopButtons.append(buttonShortBreak)
    currentlyDisplayedTopButtons.append(buttonLongBreak)
    
    
    
def StartButtonClicked():
    global isPaused
    isPaused = False
    currentTimer[0].StartTimer()
    print("Starting")
    ResetBottomButtons()
    buttonSounds[1].play()
    
def PauseButtonClicked():
    global isPaused
    isPaused = True
    currentTimer[0].StopTimer()
    print("Pausing")
    ResetBottomButtons()
    buttonSounds[1].play()
    

    
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
    isPaused = True
    currentTimer[0].ChangeTimerType("s")
    ResetBottomButtons()
    buttonSounds[currentButtonSoundArrayNumber[0]].play()
    
def PomodoroButtonClicked():
    global isPaused
    isPaused = True
    currentTimer[0].ChangeTimerType("")
    ResetBottomButtons()
    buttonSounds[currentButtonSoundArrayNumber[0]].play()
    
def LongBreakButtonClicked():
    global isPaused
    isPaused = True
    currentTimer[0].ChangeTimerType("l")
    ResetBottomButtons()
    buttonSounds[currentButtonSoundArrayNumber[0]].play()



    
def CreateBottomButton():
    global isPaused
    if isPaused == True:
        buttonStart = customtkinter.CTkButton(currentlyDisplayedButtonBottomFrame[0], text_color="white", text="START", font=("Great Vibes", 50), command=StartButtonClicked, border_color="#370617", border_width=3, fg_color="#9d0208", hover_color="#370617", corner_radius=10)
        buttonStart.configure(height=175, width=250)
        buttonStart.pack(side="bottom", pady=(20, 40), padx=90, expand=True)
        currentlyDisplayedBottomButton.append(buttonStart)
    else:
        buttonPause = customtkinter.CTkButton(currentlyDisplayedButtonBottomFrame[0], text_color="white", text="PAUSE", font=("Great Vibes", 50), command=PauseButtonClicked, border_color="#370617", border_width=3, fg_color="#9d0208", hover_color="#370617", corner_radius=10)
        buttonPause.configure(height=175, width=250)
        buttonPause.pack(side="bottom", pady=(20, 40), padx=90)
        currentlyDisplayedBottomButton.append(buttonPause)
        
def CreateNestedBottomButtons():
    

    buttonPomodoro = customtkinter.CTkButton(currentlyDisplayedNestedBottomFrame[0], text_color="white", text="Pomodoro", font=("Great Vibes", 30), command=PomodoroButtonClicked, border_color="#370617", border_width=3, fg_color="#9d0208", hover_color="#370617", corner_radius=10)
    buttonPomodoro.configure(height=75, width=200)
    buttonPomodoro.pack(side="left", pady=(0, 0), padx=(200,40))
    currentlyDisplayedBottomButton.append(buttonPomodoro)
    
    buttonLongBreak = customtkinter.CTkButton(currentlyDisplayedNestedBottomFrame[0], text_color="white", text="Long Break", font=("Great Vibes", 30), command=LongBreakButtonClicked, border_color="#370617", border_width=3, fg_color="#9d0208", hover_color="#370617", corner_radius=10)
    buttonLongBreak.configure(height=75, width=200)
    buttonLongBreak.pack(side="left", pady=(0, 0), padx=20)
    currentlyDisplayedBottomButton.append(buttonLongBreak)

    
    buttonShortBreak = customtkinter.CTkButton(currentlyDisplayedNestedBottomFrame[0], text_color="white", text="Short Break", font=("Great Vibes", 30), command=ShortBreakButtonClicked, border_color="#370617", border_width=3, fg_color="#9d0208", hover_color="#370617", corner_radius=10)
    buttonShortBreak.configure(height=75, width=200)
    buttonShortBreak.pack(side="left", pady=(0, 0), padx=(20,40))
    currentlyDisplayedBottomButton.append(buttonShortBreak)
    
    



def Main():
    CreateSoundMixer()
    CreateButtonSounds()
    CreateAlarmSounds()
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
