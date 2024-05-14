"""Pomodoro.py - A pomodoro timer application made with CustomTkinter

This is an application users can use as a study timer, allowing the user to set times for the pomodoro
time, short break and long break. The user can control the length of all three timers, set custom sounds
for the buttons and alarms and toggle between the three types of timers

Name: Joshua Owen
Class: CS162 LBCC Spring 2024



"""



# Importing the customTkinter package that enhances tkinter
import customtkinter
# Importing Image and ImageTk from the Pillow library, this is used for the icons on two fo the buttons
from PIL import Image, ImageTk
# Importing the sound mixer from pygame, this is used to play the alarm sounds and button sounds
from pygame import mixer


# Initilizing arrays that are used for holding the frames, buttons, and labels
# These are used for easy clearing of elements from the screen.
rootFrame = []
currentlyDisplayedMainFrame = []
currentlyDisplayedTimerLabel = []
currentlyDisplayedTimerText = []
currentlyDisplayedTopButtons = []
currentlyDisplayedButtonTopFrame = []
currentlyDisplayedButtonBottomFrame = []
currentlyDisplayedBottomButton = []
currentlyDisplayedTimeDropdown = []
currentlyDisplayedAlarmDropdown = []
currentlyDisplayedSoundDropdown = []
currentlyDisplayedNestedBottomFrame = []
currentlyDisplayedMainButtonFrame = []

# Intilizing arrays to hold string refrences for what alarm and button sound is currently selected.
# These are used for the dropdown menus to have the current value as the default field.
currentAlarmSound = ["Alarm Sound 1"]
currentButtonSound = ["Button Sound 1"]

# Intilizing array to hold the timer class object for easy refrence.
currentTimer = []

# Intilizing arrays to hold all the available button and alarm sounds
# These are used when calling what sound to play by keeping track of what index the user currently has selected
# from inside the array.
buttonSounds = []
alarmSounds = []

# Initilizing an array to hold the global sound mixer, this is used for easy refrence. 
soundMixer = []


# Initilzing arrays for the index numbers the sound and button arrays will refrence.
# This is inside an array to clear the currently selected values during selection of new
# sounds to not store unneeded integers
currentButtonSoundArrayNumber = [0]
currentAlarmSoundArrayNumber = [0]

# Setting the default max times for each timer, in seconds
# The time is converted into minutes inside of the timer class. 
currentPomodorMaxTime = 1800
currentLongBreakMaxTime = 900
currentShortBreakMaxTime = 300


# Initilizing a bool that is used for toggling if the clock is currently paused.
isPaused = True


# Initilizing bool values for the dropdowns, these are toggled during runtime
# if the current dropdown is open
isDropDownOpen = False
isSoundDropDownOpen = False
isAlarmDropDownOpen = False


isUpdatingPomodorTime = False
isUpdatingLongBreakTime = False
isUpdatingShortBreakTime = False

# Initiizing a string value for the color of all text, this is to not create multiple 
# strings that all actually hold the same value for each label and instead just refrence
# the same string.
globalTextColor = "white"



class Timer:
    def __init__(self, maxPomodoroTime:int, maxLongBreakTime:int, maxShortBreakTime:int):
        """ Initilizing a new timer

            Arguments:
                int(maxPomodoroTime): The max time for the pomodoro timer.
                int(maxLongBreakTime): The max time for the long break timer.
                int(maxShortBreakTime): The max time for the short break timer.
                
        """
        self.maxPomodoroTime = maxPomodoroTime
        self.maxLongBreakTime = maxLongBreakTime
        self.maxShortBreakTime = maxShortBreakTime

        # Setting the current time to the max time for each timer
        self.currentPomodoroTimeLeft = self.maxPomodoroTime
        self.currentLongBreakTimeLeft = self.maxLongBreakTime
        self.currentShortBreakTimeLeft = self.maxShortBreakTime
        self.timerDelay = None
        self.isPaused = None

        # Setting the timer to start as a Pomorodo timer
        self.isSetToPomodoroTime = True

        self.isSetToLongBreakTime = False
        self.isSetToShortBreakTime = False
    
    def ChangeTimerType(self, timerType:str):
        """ Toggles the type of timer the user is currently using
        
            Arguments:
                str(timerType): A string value of l, s, or "", used for knowing what timer
                to toggle to.
        """

        # Pausing the timer
        self.isPaused= True

        # If the string argument is l, than change to long break timer 
        if timerType.lower() == "l":
            # Enabling the bool for the long break timer
            self.isSetToLongBreakTime = True
            # Setting the other timer bools false
            self.isSetToShortBreakTime = False
            self.isSetToPomodoroTime = False
            # Resetting all timers to their max values
            self.ResetAllTimers()
            # Uodating the label that displays the current timers time.
            self.UpdateLabel()
        
        # If the string argument is s, than change to short break timer.
        elif timerType.lower() =="s":
            # Enabling the bool for the short break timer.
            self.isSetToShortBreakTime = True
            # Setting the other timer bools false.
            self.isSetToPomodoroTime = False
            self.isSetToLongBreakTime = False
            # Resetting all timers to their max values.
            self.ResetAllTimers()
            # Updating the label that displays the current timers time.
            self.UpdateLabel()
        else:
            # Else the current argument is blank, enable the pomodor timer.
            self.isSetToPomodoroTime = True
            # Setting the other timer bools false.
            self.isSetToLongBreakTime = False
            self.isSetToShortBreakTime = False
            # Resetting all timers to their max values.
            self.ResetAllTimers()
            # Updating the label that displays the current timers time.
            self.UpdateLabel()
            
            
    def StartTimer(self):
        "Starts the currently enabled timer bools timer"

        # Toggle the timer to be unpaused.
        self.isPaused = False

        # The timer is currently set to pomodoro time, start the pomodor countdown.
        if self.isSetToPomodoroTime == True:
            self.PomodoroCountDown()
        # The timer is currently set to long break time, start the long break countdown.
        elif self.isSetToLongBreakTime == True:
            self.LongBreakCountDown()
        # The timer is currently set to the short break time, start the short break countdown.
        elif self.isSetToShortBreakTime == True:
            self.ShortBreakCountDown()
        
    def StopTimer(self):
        """ Pauses the current timer"""
        # Setting the bool for pausing the timer to True
        self.isPaused = True
        
    def SetNewPomodorTime(self, newTime):
        """ Updates the max time for the Pomodor timer
        and resets the timer to the new value.
        
            Arguments:
                int(newTime): An integer value for the new time for the
                    max time, this is in seconds and converted into minutes
                    during the updating of the label.
        """

        # Setting the max time of the pomodoro to the passed in arguments value.
        self.maxPomodoroTime = newTime

        # Resetting the pomodoro timer to update the new value.
        self.ResetPomodoroTimer()

        # Updating the label to display the new time.
        self.UpdateLabel()
        
    def SetNewShortBreakTime(self, newTime):
        """ Updates the max time for the short break timer
        and resets the timer to the new value.
        
            Arguments:
                int(newTime): An integer value for the new time for the
                    max time, this is in seconds and converted into minutes
                    during the updating of the label
        """

        #Setting the max time of the short break to the passed in arguments value.
        self.maxShortBreakTime = newTime
        # Resetting the short break timer to update the new value.
        self.ResetShortBreakTimer()
        # Updating the label to display the new time.
        self.UpdateLabel()
        
    def SetNewLongBreakTime(self, newTime):
        """ Updates the max time for the long break timer
        and resets the timer to the new value.
        
            Arguments:
                int(newTime): An integer value for the new time for the 
                    max time, this is in seconds and converted into minutes
                    during the updating of the label.
        
        """

        #Setting the max time of the long break to the passed in arguments value.
        self.maxLongBreakTime = newTime
        # Resetting the long break timer to update the new value.
        self.ResetLongBreakTimer()
        # Updating the label to display the new time.
        self.UpdateLabel()
        
    def ResetAllTimers(self):
        """ Runs all the methods for resetting all three timers"""
        self.ResetLongBreakTimer()
        self.ResetShortBreakTimer()
        self.ResetPomodoroTimer()
        
    def ResetPomodoroTimer(self):
        """ Sets the time left of the pomodoro timer, to its max time"""
        self.currentPomodoroTimeLeft = self.maxPomodoroTime
    
    def ResetShortBreakTimer(self):
        """ Sets the time left of the short break timer, to its max time"""
        self.currentShortBreakTimeLeft = self.maxShortBreakTime
        
    def ResetLongBreakTimer(self):
        """ Sets the time left of the long break timer, to its max time"""
        self.currentLongBreakTimeLeft = self.maxLongBreakTime

    def PomodoroCountDown(self):
        """ Timer countdown for the pomodoro timer"""

        # Run this logic only if the timer is currently unpaused.
        if self.isPaused == False:
            # If the current time left on the pomodor timer is greater than zero.
            if self.currentPomodoroTimeLeft > 0:
                # Subtract 1 second from the time.
                self.currentPomodoroTimeLeft -= 1
                # Update the label to display the new time value.
                self.UpdateLabel()
                # After one second, redraw all the frames attached to the root frame and rerun this method
                # its slightly recursive, but this allowed for the timer to run without locking the application
                # as the display frame is also dependent on the same thread.
                self.timerDelay = rootFrame[0].after(1000, self.PomodoroCountDown)
            else:
                # If the timer is at 0 run this logic.

                # Reset the time on all of the timers.
                self.ResetAllTimers()
                # Update the label for the time.
                self.UpdateLabel()
                # Run the method for the pause button, this pauses the timer as well as updates the Start/Stop button
                PauseButtonClicked()
                # Play the sound for the currently selected alarm.
                alarmSounds[currentAlarmSoundArrayNumber[0]].play()
                
                
    def ShortBreakCountDown(self):
        """ Timer countdown for the short break timer"""

        # Run this logic only if the timer is currently unpaused.
        if self.isPaused == False:
            # If the current time on the short break timer is greater than zero.
            if self.currentShortBreakTimeLeft > 0:
                # Subtract 1 second from the time.
                self.currentShortBreakTimeLeft -= 1
                # Update the label to display the new time value.
                self.UpdateLabel()
                #After one second, redraw all the frames attached to the root frame and rerun this method
                # its slightly recursive, but this allowed for the timer to run without locking the application
                # as the display frame is also dependent on the same thread.
                self.timerDelay = rootFrame[0].after(1000, self.ShortBreakCountDown)
            else:
                # If the timer is at 0 run this logic.

                # Reset the time on all of the timers
                self.ResetAllTimers()
                # Update the label for the time.
                self.UpdateLabel()
                # Run the method for the pause button, this pauses the timer as well as updates the Start/Stop button
                PauseButtonClicked()
                # Play the sound for the currently selected alarm.
                alarmSounds[currentAlarmSoundArrayNumber[0]].play()
                
                
    def LongBreakCountDown(self):
        """ Timer countdown for the long break timer"""

        # Run this logic only if the timr is  currently unapused.
        if self.isPaused == False:
            # If the current time on the long break timer is greater than zero.
            if self.currentLongBreakTimeLeft > 0:
                # Subtract 1 second from the time
                self.currentLongBreakTimeLeft -= 1
                # Update the label to display the new time value.
                self.UpdateLabel()
                # After one second, redraw all the frames attached to the root frame and rerun this method
                # its slightly recursive, but this allowed for the timer to run without locking the application
                # as the display frame is also dependent on the same thread.
                self.timerDelay = rootFrame[0].after(1000, self.LongBreakCountDown)
            else:
                # If the timer is at 0 run this logic.

                # Reset the time on all of the timers.
                self.ResetAllTimers()
                # Update the label for the time.
                self.UpdateLabel()
                # Run this method for the pause button, this pauses the timer as well as updates the Start/Stop button
                PauseButtonClicked
                # Play the sound for the currently selected alarm.
                alarmSounds[currentAlarmSoundArrayNumber[0]].play()

    def UpdateLabel(self):
        """ Updates the label that displays the current timers time"""

        # Create a blank variable that will be used as a string for the label of the current timer
        currentOption = None

        # If the timer is set to short break
        if self.isSetToShortBreakTime:
            # Convert the current time of the short break into minutes and seconds
            minutes = self.currentShortBreakTimeLeft // 60
            seconds = self.currentShortBreakTimeLeft % 60
            # Change the currentOption string to Short Break Time for the label.
            currentOption = "Short Break Time"

        # If the timer is set to long break time
        elif self.isSetToLongBreakTime:
            # Convert the current time of the long break into minutes and seconds.
            minutes = self.currentLongBreakTimeLeft // 60
            seconds = self.currentLongBreakTimeLeft % 60

            # Change the currentOption string to Long Break Time for the label.
            currentOption = "Long Break Time"

        # Its set to Pomodoro time
        else:
            # Conver the current time of the pomodoro into minutes and seconds.
            minutes = self.currentPomodoroTimeLeft // 60
            seconds = self.currentPomodoroTimeLeft % 60

            # Change the currentOption string to Pomodoro Time for the label
            currentOption = "Pomodoro Time"
        
        # Update the label with the string of currentOption
        currentlyDisplayedTimerText[0].configure(text=currentOption)
        
        # Create a string for the current minutes and seconds of whatever timer is running
        timeStr = f"{minutes:02d}:{seconds:02d}"
        # Update the label that is used for displaying the time, with the created string.
        currentlyDisplayedTimerLabel[0].configure(text=timeStr)
        
    
    def ReturnPomodoroTime(self)-> str:
        """ Returns the current value of the timer labels text
        
            Returns:
                str: the current timers time in minutes and seconds
                
        """
        minutes = self.currentPomodoroTimeLeft // 60
        seconds = self.currentPomodoroTimeLeft % 60
        timeStr = f"{minutes:02d}:{seconds:02d}"
        return timeStr
    
    def GetCurrentlValue(self)->str:
        """ Finds and returns a string value for whatever current timer
        is running with respect to its max time.
        
        This is used for the dropdown menu so it knows what the currently selected value is to update the default 
        option at runtime.
        
            Returns:
                str: A string value of what the current max time of the selected timer is
                
        """

        # Creating a variable that will be used to hold a string representing the current max time 
        currentValue = None

        # If the timer is set to Short Break
        if self.isSetToShortBreakTime:
            # Checking what value is currently set as the max value of the short break timer
            # Depending on the value returned, sets a string for that value as the currentValue
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
        
        # If the timer is set to Long Break
        elif self.isSetToLongBreakTime:
            # Checking what value is currently set as the max value of the long break timer
            # Depending on the value returned, sets a string for that value as the currentValue
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

        # Else the timer is currently Pomodoro.      
        else:
            # Checking what value is curently set as the max value of the Pomodoro timer
            # Depending on the value returned, sets a string for that value as the currentValue
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
                
        # Returning the string that contains the current time value
        return currentValue      
 
 
def CreateSoundMixer():
    """ Creates an instance of a sound mixer from pygame,
    than adds the mixer to an array for easy refrence during the script.
    
    """

    # Initilizing a new mixer
    mixer.init()

    # Adding the new mixer to an array for easy refrence.
    soundMixer.append(mixer)   

def CreateButtonSounds():
    """ Creates instances of all the button sounds as Sound classes inside the sound mixer that 
    is currently inside the list of soundMixer.
    
    """

    # Initilizing all of the button sounds as new Sound classes inside of the current Sound Mixer
    buttonSoundOne = soundMixer[0].Sound("Sounds/Buttons/Button1.wav")
    buttonSoundTwo = soundMixer[0].Sound("Sounds/Buttons/Button2.wav")
    buttonSoundThree = soundMixer[0].Sound("Sounds/Buttons/Button3.wav")
    buttonSoundFour = soundMixer[0].Sound("Sounds/Buttons/Button4.wav")
    buttonSoundFive = soundMixer[0].Sound("Sounds/Buttons/Button5.wav")

    # Appending each Sound class object to a list containing all of the available button sounds.
    # This is used to swap between the different sounds when the user selects from the dropdown.
    buttonSounds.append(buttonSoundOne)
    buttonSounds.append(buttonSoundTwo)
    buttonSounds.append(buttonSoundThree)
    buttonSounds.append(buttonSoundFour)
    buttonSounds.append(buttonSoundFive)
    
def CreateAlarmSounds():
    """ Creates instances of all the alarm sounds as Sound classes inside the sound mixer that
    is currently inside the list of soundMixer
    
    """

    # Initilizing all of the alarl sounds as new Sound classes inside of the current Sound Mixer.
    alarmSoundOne = soundMixer[0].Sound("Sounds/Alarms/alarm1.wav")
    alarmSoundTwo = soundMixer[0].Sound("Sounds/Alarms/alarm2.wav")
    alarmSoundThree = soundMixer[0].Sound("Sounds/Alarms/alarm3.wav")
    alarmSoundFour = soundMixer[0].Sound("Sounds/Alarms/alarm4.wav")
    alarmSoundFive = soundMixer[0].Sound("Sounds/Alarms/alarm5.wav")

    # Appending each Sound class object to a list containing all of the available alarm sounds.
    # This is used to swap between the different sounds when the user selects from the dropdown.
    alarmSounds.append(alarmSoundOne)
    alarmSounds.append(alarmSoundTwo)
    alarmSounds.append(alarmSoundThree)
    alarmSounds.append(alarmSoundFour)
    alarmSounds.append(alarmSoundFive)
    

def CreateTimer():
    """ Initilizes a new Timer class object and sets its default values"""


    # If there is currently no timer held inside the currentTimer list
    # (this should always be the case but is a catch all)

    if not currentTimer:
        # Creating a new timer object, with default values for the pomodor time, short break time, and long break time
        timer = Timer(maxPomodoroTime=1800, maxLongBreakTime=900, maxShortBreakTime=300)

        # Appending the newly created timer object to the currentTimer list
        currentTimer.append(timer)
    else:
        # If the currentTimer list is for some reason not empty, clear it
        currentTimer.clear()
        # Creating a new timer ojbect, with default values for the pomodor time, short break time, and long break time
        timer= Timer(maxTime=1800, maxLongBreakTime=900, maxShortBreakTime=300)

        # Appending the newly created timer ojbect to the currentTimer list
        currentTimer.append(timer)

def CreateRootFrame():
    """" Creates the root frame that all other frames are children of."""

    # Initilizing a new instance of cTK
    frame = customtkinter.CTk()
    # Setting the x and y values for the entire application window
    frame.geometry("1366x768")
    # Giving the window a title
    frame.title("Pomodoro Timer DX")
    # Setting the window to not allow resizing
    frame.resizable(False, False)
    # Adding the newly created frame to the rootFrame list, this is for easy refrence between methods.
    rootFrame.append(frame)

def CreateMainFrame():
    """ Creates the main sub frame of root, all frames inheret from this frame"""

    # Initilizing a new frame, setting its parent to the root frame
    mainFrame = customtkinter.CTkFrame(master=rootFrame[0])

    # Packing the frame to the screen, setting it to fill the length and width of the window and to expand to max value
    mainFrame.pack(fill="both", expand=True)

    # Setting the color for the entire window
    mainFrame.configure(fg_color="#03071e")

    # On the off chance there is already a main frame held inside the list for the main frame, clear it.
    currentlyDisplayedMainFrame.clear()

    # Appending the newly created main frame to the list of main frame
    currentlyDisplayedMainFrame.append(mainFrame)
    
def CreateMainButtonFrame():
    """ Creates the frame that the bottom buttons will nest inside of"""

    # Initilizing a new frame and setting its parent to the main frame
    mainButtonFrame = customtkinter.CTkFrame(master=currentlyDisplayedMainFrame[0])

    # Setting it to fill its width and height to the parent frame
    mainButtonFrame.pack(fill="both", expand=False)

    # Setting the background color of the frame ( this could also be set as transparent as
    # its the same color as the parent frame, but its the same amount of memory either way).
    mainButtonFrame.configure(fg_color="#03071e")

    # Clearing the list of main button frames, on the off chance that one is already held.
    currentlyDisplayedMainButtonFrame.clear()
    # Appending the frame to the list of main button frames.
    currentlyDisplayedMainButtonFrame.append(mainButtonFrame)
     

def CreateTimerLabel():
    """ Creates the default labels for the timer at the center of the scree 
    """

    # Initilizing a new label for the timer text
    timerText = customtkinter.CTkLabel(master=currentlyDisplayedMainFrame[0],text_color=globalTextColor, text="Pomodoro Time", font=("Great Vibes", 40))
    timerText.pack(padx=(25, 20), pady=(0,5))
    # Initilzing a new label for the timers time text
    timerLabel = customtkinter.CTkLabel(master=currentlyDisplayedMainFrame[0],text_color =globalTextColor, text=currentTimer[0].ReturnPomodoroTime(), font=("Great Vibes", 175))
    timerLabel.pack(padx=(25, 20), pady=(10, 5))
    
    # Clearing both lists for the text and label ( this is used during resets)
    currentlyDisplayedTimerText.clear()
    # Adding the newly created timer text label to the list of timer texts
    currentlyDisplayedTimerText.append(timerText)
    currentlyDisplayedTimerLabel.clear()
    # Adding the newly created timer label to the list of timer labels
    currentlyDisplayedTimerLabel.append(timerLabel)

def CreateTopMenu():
    """ Runs all the methods needed to create the objects held at top of screen"""

    # Creating the frame for the buttons that are on the top of the screen
    CreateTopButtonFrame()

    # Creating the label that sits at the to[ of the screen.
    CreateTopLabel()

    # Creating the buttons that sit at the top of the screen.
    CreateTopButtons()
    
def CreateTopLabel():
    """ Creates the label that sits at the top of the screen"""

    # Initilizing the label and packing to the screen
    topLabel = customtkinter.CTkLabel(master=currentlyDisplayedButtonTopFrame[0], text_color=globalTextColor, text="SETTINGS", font=("Great Vibes", 40))
    topLabel.pack(pady=0,padx=60)


            
def CreateTopButtonFrame():
    """ Creates the frame the top buttons will nest inside"""

    # Initilizing a new frame with its parent set to the main frame
    frame = customtkinter.CTkFrame(master=currentlyDisplayedMainFrame[0], height=100, fg_color="transparent")
    # Packing it to the screen, including setting it to sit at the top of its parent frame
    frame.pack(pady=(20,40),padx=60, side="top", fill="x", expand=False)

    # Clearing any frames inside the top frame list
    currentlyDisplayedButtonTopFrame.clear()
    # Appending the newly created frame to the list of top frames.
    currentlyDisplayedButtonTopFrame.append(frame)
    

    
def CreateBottomButtonFrame():
    """ Creates the frame the bottom buttons will nest inside"""

    # Initilizing a new frame with its parent set tot he main button frame
    frame = customtkinter.CTkFrame(master=currentlyDisplayedMainButtonFrame[0], height=100, fg_color="transparent")
    frame.pack(pady=20,padx=60, side="bottom", fill="x", expand=False)

    # Clearing any bottom button frames already contained in the list of bottom buttons
    currentlyDisplayedButtonBottomFrame.clear()

    # Appending the newly created bottom button frame to the list of bottom button frames
    currentlyDisplayedButtonBottomFrame.append(frame)
    
def CreateNestedBottomButtonFrame():
    """ Creates the frame for the nested objects that sit inside the button bottom frame
    The reason for the nesting is to center the buttons horizontally
    """

    # Initilizing a new frame and setting its parent to the bottom button frame
    frame = customtkinter.CTkFrame(master=currentlyDisplayedButtonBottomFrame[0], height=100, fg_color="transparent")
    frame.pack(pady=20,padx=60, side="bottom", fill="x", expand=False)

    # Clearing the list of nested bottom frames
    currentlyDisplayedNestedBottomFrame.clear()

    # Appending the newly created frame to the list of nested bottom frames
    currentlyDisplayedNestedBottomFrame.append(frame)
    
def SoundMenu(choice):
    """ Finds what the user has selected for the new button sound, and changes the sound for all of the buttons
    to the newly selected sound.
    """

    # Each if statement below uses the logic in the bellow comments

    # Depending on the users choice, clear the current sound
    # Append the newly chosen sound
    # Clear the list that holds the current index number for what sound to play
    # Add the number for the position in the list of sounds to the refrence list

    if choice == "Button Sound 1":
        currentButtonSound.clear()
        currentButtonSound.append("Button Sound 1")
        currentButtonSoundArrayNumber.clear()
        currentButtonSoundArrayNumber.append(0)
        buttonSounds[0].play()
        
    if choice =="Button Sound 2":
        currentButtonSound.clear()
        currentButtonSound.append("Button Sound 2")
        currentButtonSoundArrayNumber.clear()
        currentButtonSoundArrayNumber.append(1)
        buttonSounds[1].play()
        
    if choice =="Button Sound 3":
        currentButtonSound.clear()
        currentButtonSound.append("ButtonSound 3")
        currentButtonSoundArrayNumber.clear()
        currentButtonSoundArrayNumber.append(2)
        buttonSounds[2].play()
        
    if choice =="Button Sound 4":
        currentButtonSound.clear()
        currentButtonSound.append("Button Sound 4")
        currentButtonSoundArrayNumber.clear()
        currentButtonSoundArrayNumber.append(3)
        buttonSounds[3].play()
        
    if choice =="Button Sound 5":
        currentButtonSound.clear()
        currentButtonSound.append("Button Sound 5")
        currentButtonSoundArrayNumber.clear()
        currentButtonSoundArrayNumber.append(4)
        buttonSounds[4].play()

    # Clearing any dropdown open from the screen, renabling the bottom buttons.
    ClearDropdown()
    
    
def AlarmMenu(choice):
    """ Finds what the user has selected for the new alarm sound, and changes the sound fo the alarm
    to the newly selected sound.
    """

    # Each if statement below uses the logic in the bellow comments

    # Depending on the users choice, clear the current alarm sound
    # Append the newly chosen alarm sound
    # Clear the list that holds the current index number for what alarm sound to play
    # Add the number for the position in the list of sounds to the refrence list
    
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

    # Clear any open dropdown from the screen, re-enable the bottom buttons.
    ClearDropdown()
    
    
def TimerMenu(choice):
    """ Grabs the users choice for what time the selected timer should be set to
    and sets the new time.
    """
    
    # Each statement below, checks what the users choice was
    # depending on the choice of the user, checks what the timer is currently set to for type of timer.
    # updates the selected timer with the new time
    # toggles the bools off for the dropdown choices
    # then clears the dropdowns.
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
    """ Clears all the possible dropdowns from the screen"""

    # Setting the isDropDownOpen bool to global to edit inside the method
    global isDropDownOpen

    # If there is a dropdown inside of the TimeDropdown list destroy it and clear the list
    for dropdown in currentlyDisplayedTimeDropdown:
        dropdown.destroy()
    currentlyDisplayedTimeDropdown.clear()
    isDropDownOpen = False

    # If there is a dropdown inside of the AlarmDropdown list, destroy it and clear the list.
    for alarmSetting in currentlyDisplayedAlarmDropdown:
        alarmSetting.destroy()
    currentlyDisplayedAlarmDropdown.clear()

    # If there is a dropdown inside of the SoundDropdown list, destroy it and clear the list.
    for soundSetting in currentlyDisplayedSoundDropdown:
        soundSetting.destroy()
    currentlyDisplayedSoundDropdown.clear()

    # Reset all of the bottom buttons back onto the screen
    ResetBottomButtons()
    
def ToggleButtonTypeBoolsOff():
    """" Toggles all of the bools related to changing time values for all three alarms off"""

    # Setting all three bools to global to change inside of the method globally
    global isUpdatingLongBreakTime, isUpdatingShortBreakTime, isUpdatingPomodorTime
    
    # Setting each bool for the updating of the alarms to false
    isUpdatingLongBreakTime = False
    isUpdatingShortBreakTime = False
    isUpdatingPomodorTime = False

def TimeOptionClicked(buttonType:str):
    """ Creates the dropdown for the time options, including checking what time option the 
    user is currently wanting to update
    
        Arguments:
            str(buttonType): A string containing single characters, used for knowing
            what type of timer the user is changing.
    """
    # Setting all of the used bools to global to change globally while used inside the method
    global isUpdatingLongBreakTime, isUpdatingPomodorTime, isUpdatingShortBreakTime, isDropDownOpen, isPaused, isAlarmDropDownOpen, isSoundDropDownOpen
    
    # Creating a blank variable that will eventually store a string for the timer type.
    timerType = None

    # Playing the current sound assigned for button presses
    buttonSounds[currentButtonSoundArrayNumber[0]].play()

    
    # If there is already a timer dropdown open, destroy it
    if isDropDownOpen == True:
        for dropdown in currentlyDisplayedTimeDropdown:
            dropdown.destroy()
        currentlyDisplayedTimeDropdown.clear()
        ToggleButtonTypeBoolsOff()
    else:
    # else, toggle the bools for a new dropdown
        isDropDownOpen = True
        isPaused = True

        # Stop the current timer
        currentTimer[0].StopTimer()

        # Clearing the bottom buttons from the screen.
        RemoveBottomButtons()
        
    # If there was an alarm dropdown on the screen clear it and reset its bool
    if isAlarmDropDownOpen == True:
        for dropdown in currentlyDisplayedAlarmDropdown:
            dropdown.destroy()
        currentlyDisplayedAlarmDropdown.clear()
        isAlarmDropDownOpen = False

    # If the passed in value was p, set the blank timerType to "Pomodoro"
    # and change the type of timer assigned to the current timer class.
    if buttonType == "p":
        timerType = "Pomodoro"
        currentTimer[0].ChangeTimerType("p")
        isUpdatingPomodorTime = True
    # If the passed in value was l, set the blank timerType to "Long Break"
    # and change the type of timer assigned to the current timer class.
    if buttonType =="l":
        timerType = "Long Break"
        currentTimer[0].ChangeTimerType("l")
        isUpdatingLongBreakTime = True
    # If the passed in value was s, set the blank timerType to "Short Break"
    # and change the type of timer assigned to the current timer class.
    if buttonType =="s":
        timerType = "Short Break"
        currentTimer[0].ChangeTimerType("s")
        isUpdatingShortBreakTime = True
            
    # Grabbing the current time of the timer as a string to set as the default value of the dropdown.
    currentlySelectedValue = currentTimer[0].GetCurrentlValue()
    # Creating the variable that is passed into the dropdown, setting its text to the above string.
    timerMenuVar = customtkinter.StringVar(value=currentlySelectedValue)
    # Creating the label that displays what type of timer the user is updating the time for.
    timerMenuLabel = customtkinter.CTkLabel(currentlyDisplayedMainButtonFrame[0],text_color= globalTextColor, text=f"Select Time For {timerType}", font=("Great Vibes", 40))
    # Initilizing a new dropdown menu, settings its command to run the TimerMenu method and its variable to the timerMenuVar created above.
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
    # Packing both the timerMenuLabel and the dropdown onto the screen
    timerMenuLabel.pack(side="top", pady=10, padx=90)
    timerMenu.pack(side="bottom", pady=(20, 0), padx=90)

    # Appending both the created dropdown and its label to the list of displayed dropdowns for easy clearing.
    currentlyDisplayedTimeDropdown.append(timerMenuLabel)
    currentlyDisplayedTimeDropdown.append(timerMenu)


def AlarmButtonClicked():
    """ Creates a new dropdown for choosing what alarm sound the user wants"""

    # Setting all the needed bools to global to be updated globally while inside the method.
    global isSoundDropDownOpen, isDropDownOpen, isAlarmDropDownOpen, isPaused
    
    # Play the current sound the user has set for button presses
    buttonSounds[currentButtonSoundArrayNumber[0]].play()

    
    # If there is a time dropdown open, destroy it and toggle its bool off
    if isDropDownOpen == True:
        for dropdown in currentlyDisplayedTimeDropdown:
            dropdown.destroy()
        currentlyDisplayedTimeDropdown.clear()
        ToggleButtonTypeBoolsOff()
        isDropDownOpen = False
        
    # If there is a sound dropdown open, destroy it and toggle its bool off
    if isSoundDropDownOpen == True:
        for dropdown in currentlyDisplayedSoundDropdown:
            dropdown.destroy()
        currentlyDisplayedSoundDropdown.clear()
        isSoundDropDownOpen = False
        
    # If there is already an alarm dropdown open, destroy it then continue with logic
    if isAlarmDropDownOpen == True:
        for dropdown in currentlyDisplayedAlarmDropdown:
            dropdown.destroy()
        currentlyDisplayedAlarmDropdown.clear()
        
    # Setting the bool for updating the alarm to true
    isAlarmDropDownOpen = True
    # Pausing the current timer
    isPaused = True
    currentTimer[0].StopTimer()
    # Removing the buttons from the bottom of the screen.
    RemoveBottomButtons()

    # Grabs the value of the currently stored string for the alarm sound, and sets it to the default value for the dropdown.
    alarmMenuVar = customtkinter.StringVar(value=currentAlarmSound[0])
    # Initilizing a new label to say "Select Alarm Sound"
    alarmMenuLabel = customtkinter.CTkLabel(currentlyDisplayedMainButtonFrame[0],text_color=globalTextColor, text=f"Select Alarm Sound", font=("Great Vibes", 40))
    # Creating a new dropdown menu for alarm sound choices, setting its command on selection to the AlarmMenu method
    # and its variable to the created alarmMenuVar above.
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
    # Packing the created label and dropdown onto the screen
    alarmMenuLabel.pack(side="top", pady=10, padx=90)
    alarmMenu.pack(side="bottom", pady=(20, 0), padx=90)

    # Appending both into the AlarmDropdown list for easy clearing later
    currentlyDisplayedAlarmDropdown.append(alarmMenuLabel)
    currentlyDisplayedAlarmDropdown.append(alarmMenu)
    

def SoundButtonClicked():
    """ Creates the dropdown for the user to select the sound for button presses"""

    # Setting all neeeded bools to global for updating outside the method.
    global isSoundDropDownOpen, isDropDownOpen, isAlarmDropDownOpen, isPaused
    
    # Playing the currently selected sound for button presses.
    buttonSounds[currentButtonSoundArrayNumber[0]].play()

    # If there is a time dropdown open, clear it and set its bool to false
    if isDropDownOpen == True:
        for dropdown in currentlyDisplayedTimeDropdown:
            dropdown.destroy()
        currentlyDisplayedTimeDropdown.clear()
        ToggleButtonTypeBoolsOff()
        isDropDownOpen = False
        
        
    # If there is an alarm dropdown open, clear it and set its bool false
    if isAlarmDropDownOpen == True:
        for dropdown in currentlyDisplayedAlarmDropdown:
            dropdown.destroy()
        currentlyDisplayedAlarmDropdown.clear()
        isAlarmDropDownOpen = False
        
    # If there is already a sound dropdown open, clear it and continue with logic
    if isSoundDropDownOpen == True:
        for dropdown in currentlyDisplayedSoundDropdown:
            dropdown.destroy()
        currentlyDisplayedSoundDropdown.clear()
        
    # Setting the bool for the sound dropdown to True
    isSoundDropDownOpen = True
    # Pausing the current timer
    isPaused = True
    currentTimer[0].StopTimer()
    # Removing the bottom buttons.
    RemoveBottomButtons()

    # Grabbing the current string value of the current buttoun sound that is in use and setting it to the default dropdown variable
    soundMenuVar = customtkinter.StringVar(value=currentButtonSound[0])
    # Creating a label to say "Select Button Sound"
    soundMenuLabel = customtkinter.CTkLabel(currentlyDisplayedMainButtonFrame[0],text_color=globalTextColor, text=f"Select Button Sound", font=("Great Vibes", 40))
    # Creating a new dropdown containing all of the choices of button sounds, setting its command to run the SoundMenu method
    # and its variable to be the created soundMenuVar above.
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
    # Packing both created label and dropdown onto the screen.
    soundMenuLabel.pack(side="top", pady=10, padx=90)
    soundMenu.pack(side="bottom", pady=(20, 0), padx=90)

    # Appending the newly created label and dropdown to the list of SoundDropdowns for easy clearing later.
    currentlyDisplayedSoundDropdown.append(soundMenuLabel)
    currentlyDisplayedSoundDropdown.append(soundMenu)
    return

def CreateTopButtons():
    """ Creates all of the buttons that rest on the top of the screen"""

    # Creating new buttons for the Pomodor, long break, short break, alarm sound, and button sound dropdowns,
    # Setting them to to the top of the screen, with their parent as the TopFrame

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

    # Appending each of the created buttons to the list of current buttons on the top of the screen.
    currentlyDisplayedTopButtons.append(alarmButton)
    currentlyDisplayedTopButtons.append(soundButton)
    currentlyDisplayedTopButtons.append(buttonPomodoro)
    currentlyDisplayedTopButtons.append(buttonShortBreak)
    currentlyDisplayedTopButtons.append(buttonLongBreak)
    
    
    
def StartButtonClicked():
    """ Logic for when the user clicks the Start timer button"""
    # Unpausing the current timer
    global isPaused
    isPaused = False
    currentTimer[0].StartTimer()
    print("Starting")
    # Resetting the bottom button so it will say Pause
    ResetBottomButtons()
    # Playing the currently selected sound for button presses.
    buttonSounds[1].play()
    
def PauseButtonClicked():
    """ Logic for when the user clicks the Pause timer button"""
    # Pausing the current timer
    global isPaused
    isPaused = True
    currentTimer[0].StopTimer()
    print("Pausing")
    # Resetting the bottom button to say "Start"
    ResetBottomButtons()
    # Playing the currently selected sound for button presses.
    buttonSounds[1].play()
        
def ResetBottomButtons():
    """ Destroys the current bottom buttons and runs the methods needed
    to create new bottom buttons"""

    # For all of the buttons inside bottomButton, destroy than clear the list.
    for button in currentlyDisplayedBottomButton:
        button.destroy()
    currentlyDisplayedBottomButton.clear()
    # Create new bottom button
    CreateBottomButton()
    # Create the buttons that nest below the Start/Pause button
    CreateNestedBottomButtons()
    
def RemoveBottomButtons():
    """ Clears the buttons from the bottom of the screen"""

    # Destroy any button inside the list
    for button in currentlyDisplayedBottomButton:
        button.destroy()

    # Clear the list
    currentlyDisplayedBottomButton.clear()
    
def ShortBreakButtonClicked():
    """ User has clicked to change the timer to a short break"""

    # Pause the timer
    global isPaused
    isPaused = True

    # Change the timer type to short break timer
    currentTimer[0].ChangeTimerType("s")

    # Reset the bottom buttons
    ResetBottomButtons()

    # Play the current sound assigned to button presses.
    buttonSounds[currentButtonSoundArrayNumber[0]].play()
    
def PomodoroButtonClicked():
    """ User has clicked to change the timer to Pomodoro"""

    # Pause the current timer
    global isPaused
    isPaused = True

    # Change the timer to Pomodoro
    currentTimer[0].ChangeTimerType("")

    # Reset the bottom buttons
    ResetBottomButtons()

    # Play the current sound assigned to button presses.
    buttonSounds[currentButtonSoundArrayNumber[0]].play()
    
def LongBreakButtonClicked():
    """ User has clicked to change the timer to Long Break"""

    # Pause the current timer
    global isPaused
    isPaused = True
    # Change the timer to Long Break
    currentTimer[0].ChangeTimerType("l")

    # Reset the bottom buttons
    ResetBottomButtons()

    # Play the current sound assigned to button presses.
    buttonSounds[currentButtonSoundArrayNumber[0]].play()

    
def CreateBottomButton():
    """ Creates the Start/ Pause button depending on what isPaused is currently set to"""

    global isPaused
    # If isPaused is true, create a button that says Start, pack to the screen, add to the list
    if isPaused == True:
        buttonStart = customtkinter.CTkButton(currentlyDisplayedButtonBottomFrame[0], text_color="white", text="START", font=("Great Vibes", 50), command=StartButtonClicked, border_color="#370617", border_width=3, fg_color="#9d0208", hover_color="#370617", corner_radius=10)
        buttonStart.configure(height=175, width=250)
        buttonStart.pack(side="bottom", pady=(20, 40), padx=90, expand=True)
        currentlyDisplayedBottomButton.append(buttonStart)
    else:
    # Else create a button that says Pause, pack to the screen, add to the list
        buttonPause = customtkinter.CTkButton(currentlyDisplayedButtonBottomFrame[0], text_color="white", text="PAUSE", font=("Great Vibes", 50), command=PauseButtonClicked, border_color="#370617", border_width=3, fg_color="#9d0208", hover_color="#370617", corner_radius=10)
        buttonPause.configure(height=175, width=250)
        buttonPause.pack(side="bottom", pady=(20, 40), padx=90)
        currentlyDisplayedBottomButton.append(buttonPause)
        
def CreateNestedBottomButtons():
    """ Creates the buttons that sit at the bottom of the screen for timer options"""

    # Creating a button for Pomodoro, Short Break, and Long Break, packing onto the screen and adding to a list
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
    """ Runs all of the main methods for displaying the application"""

    # Creating a sound mixer
    CreateSoundMixer()
    # Creating the list of button sounds
    CreateButtonSounds()
    # Creating the list of alarm sounds
    CreateAlarmSounds()
    # Creating the root frame
    CreateRootFrame()
    # Creating the main frame
    CreateMainFrame()
    # Creating the top menu
    CreateTopMenu()
    # Creating a new timer object
    CreateTimer()
    # Creating a new label to display the time
    CreateTimerLabel()
    # Creating the main frame the buttons nest into
    CreateMainButtonFrame()
    # Creating the frame for the buttons
    CreateBottomButtonFrame()
    # Creating the nested button frame
    CreateNestedBottomButtonFrame()
    # Creating the bottom buttons
    CreateBottomButton()
    # Creating the nested bottom buttons
    CreateNestedBottomButtons()
    # Looping the root frame to constantly display the application onto the screen until user closes.
    rootFrame[0].mainloop()

if __name__ == "__main__":
    Main()
