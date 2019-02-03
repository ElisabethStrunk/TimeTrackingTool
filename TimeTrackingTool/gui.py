from tkinter import *
from logic import *
from datetime import datetime

class MyGuiClass:
    def __init__(self, window, logger):
        # Window
        self.window = window
        window.geometry('150x100')
        window.title("Bastis Time Tracker")
        window.iconbitmap('Graphicloads-Flat-Finance-Timer.ico')

        # Data logger
        self.logger = logger

        # Buttons
        # Start button
        self.button_text = StringVar()
        self.button_text.set("Start")
        self.button_start = Button(window, textvariable=self.button_text, command=self.button_start_clicked, width=5)
        # Stop button
        self.button_stop = Button(window, text="Stop", command=self.button_stop_clicked, state=DISABLED, width=5)

        # InputBox
        self.inputBox = Entry(window, width=10) #command=self.entry_made,
        self.inputBox.focus()

        # Time
        self.state = State.beginning
        self.main_timer = Timer()
        self.fmt = '%H:%M:%S'
        self.starting_time = '%H:%M:%S'
        self.stop_time = '%H:%M:%S'
        self.task_time = '00:00:00'
        self.time_string = '00:00:00'
        self.time_label = Label(window, text=self.time_string, compound=CENTER)

        # Pack elements in grid
        self.button_start.grid(column=2, row=1, padx=5, pady=5) #columnspan=1, rowspan=2,
        self.button_stop.grid(column=2, row=2, padx=5, pady=5)
        self.inputBox.grid(column=1, row=1, padx=5, pady=5)
        self.time_label.grid(column=1, row=2, padx=5, pady=5)

        # Center grid in window using buffer grid rows and columns
        window.grid_rowconfigure(0, weight=1)
        window.grid_rowconfigure(3, weight=1)
        window.grid_columnconfigure(0, weight=1)
        window.grid_columnconfigure(3, weight=1)

        self.window.mainloop()

    def button_start_clicked(self):
        if self.state == State.beginning:
            self.button_text.set("New")
            self.button_start.config(state=DISABLED)
            self.main_timer.restart()
            self.starting_time = self.main_timer.get_time_hhmmss()
            self.state = State.started
            self.update_clock()
            self.update_buttons()
        elif self.state == State.started:
            # create logging entry
            date = datetime.now().strftime("%Y-%m-%d")
            time = datetime.strptime(self.main_timer.get_time_hhmmss(), self.fmt) - datetime.strptime(self.starting_time, self.fmt)
            task = self.inputBox.get()
            self.logger.write_new_entry(date, time, task)
            self.starting_time = self.main_timer.get_time_hhmmss()
            # update GUI
            self.inputBox.delete(0, 'end')
            self.button_start.config(state=DISABLED)
            self.button_stop.config(state=DISABLED)
        elif self.state == State.stopped:
            return

    def button_stop_clicked(self):
        # create logging entry
        date = datetime.now().strftime("%Y-%m-%d")
        time = datetime.strptime(self.main_timer.get_time_hhmmss(), self.fmt) - datetime.strptime(self.starting_time,
                                                                                                  self.fmt)
        task = self.inputBox.get()
        self.logger.write_new_entry(date, time, task)
        self.starting_time = self.main_timer.get_time_hhmmss()
        self.logger.save()
        # update GUI
        self.inputBox.delete(0, 'end')
        self.button_start.config(state=DISABLED)
        self.button_stop.config(state=DISABLED)
        self.inputBox.config(state=DISABLED)
        self.state = State.stopped

    def update_clock(self):
        if self.state == State.beginning:
            return
        elif self.state == State.started:
            self.time_string = self.main_timer.get_time_hhmmss()
            self.time_label.configure(text=self.time_string)
            self.window.after(1000, self.update_clock)
        elif self.state == State.stopped:
            return

    def update_buttons(self):
        if self.state == State.beginning:
            return
        elif self.state == State.started:
            # check for user entry and reactivate button if entry has been made
            input = self.inputBox.get()
            if self.inputBox.get() != '':
                self.button_start.config(state=ACTIVE)
                self.button_stop.config(state=ACTIVE)
            self.window.after(1000, self.update_buttons)
        elif self.state == State.stopped:
            return
