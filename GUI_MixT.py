""" MIXING TIME DETERMINATION - Using Colorimetric Method
By Yago Silva, Fernando Cecatto and Elisabeth Augusto
Bioprocess Laboratory with Animal Cells - Science and Technology Institute, Federal University of São Paulo

This program analyzes the global mixing time of the equipment (e.g. reactor, shaker flask).
"""
import os
from tkinter import *
from tkinter import filedialog, messagebox
from subprocess import Popen


class Funcs:
    def parameters(self):
        """Creation of the window to receive the user data"""
        self.frame1 = Toplevel(self.root)
        self.frame1.transient(self.root)
        self.frame1.geometry("700x500")
        self.frame1.title("Data Filling")

        self.lb_video = Label(self.frame1, text='Video', bg='#415A77', fg='White')
        self.lb_video.place(relx=0.001, rely=0.005, relwidth=0.23, relheight=0.10)
        self.video_entry = Label(self.frame1, text="Select the video", bg='#E0E1DD', fg='gray')
        self.video_entry.place(relx=0.250, rely=0.005, relwidth=0.50, relheight=0.10)
        self.bt_search_video = Button(self.frame1, text="Search", command=self.search_video, bg='#1B263B', fg='White',
                                      activebackground='#E0E1DD', activeforeground='Black')
        self.bt_search_video.place(relx=0.77, rely=0.005, relwidth=0.12, relheight=0.10)

        self.lb_folder = Label(self.frame1, text='Folder name', bg='#415A77', fg='White')
        self.lb_folder.place(relx=0.001, rely=0.155, relwidth=0.23, relheight=0.10)
        self.folder_entry = Entry(self.frame1, bg='#E0E1DD', fg='gray')
        self.folder_entry.insert(0, "Enter the name of the frames folder")
        self.folder_entry.place(relx=0.250, rely=0.155, relwidth=0.50, relheight=0.10)
        self.folder_entry.bind("<FocusIn>", self.onclick_temp_text_1)
        self.folder_entry.bind("<FocusOut>", self.outclick_temp_text_1)

        self.lb_areas = Label(self.frame1, text="Select 4 new areas", bg='#415A77', fg='White')
        self.lb_areas.place(relx=0.001, rely=0.305, relwidth=0.23, relheight=0.10)
        self.v = IntVar()
        self.bt_areas = Checkbutton(self.frame1, text="YES", variable=self.v, onvalue=1, offvalue=0, bg='#E0E1DD')
        self.bt_areas.place(relx=0.250, rely=0.305, relwidth=0.10, relheight=0.10)
        self.help_icon = PhotoImage(file="./Icons/help_icon (1).png")
        self.help = Button(self.frame1, image=self.help_icon, bd=0, bg='#778DA9', activebackground='#778DA9')
        self.help.place(relx=0.36, rely=0.31)

        self.lb_cut = Label(self.frame1, text="Cut the end of the video (s):", bg='#415A77', fg='White')
        self.lb_cut.place(relx=0.001, rely=0.455, relwidth=0.23, relheight=0.10)
        self.cut_entry = Entry(self.frame1, bg='#E0E1DD', fg='gray')
        self.cut_entry.insert(0, "Enter 0 (don't cut the end) or the time value")
        self.cut_entry.place(relx=0.250, rely=0.455, relwidth=0.50, relheight=0.10)
        self.cut_entry.bind("<FocusIn>", self.onclick_temp_text_2)
        self.cut_entry.bind("<FocusOut>", self.outclick_temp_text_2)

        self.lb_sheet = Label(self.frame1, text="Worksheet name", bg='#415A77', fg='White')
        self.lb_sheet.place(relx=0.001, rely=0.605, relwidth=0.23, relheight=0.10)
        self.sheet_entry = Entry(self.frame1, bg='#E0E1DD', fg='gray')
        self.sheet_entry.insert(0, "Enter the name of the results worksheet")
        self.sheet_entry.place(relx=0.250, rely=0.605, relwidth=0.50, relheight=0.10)
        self.sheet_entry.bind("<FocusIn>", self.onclick_temp_text_3)
        self.sheet_entry.bind("<FocusOut>", self.outclick_temp_text_3)

        self.bt_run = Button(self.frame1, text='Run', command=self.run, bg='#1B263B', fg='White',
                               activebackground='#E0E1DD', activeforeground='Black')
        self.bt_run.place(relx=0.350, rely=0.755, relwidth=0.13, relheight=0.10)

        self.bt_clean = Button(self.frame1, text='Clean', command=self.clean, bg='#1B263B', fg='White',
                               activebackground='#E0E1DD', activeforeground='Black')
        self.bt_clean.place(relx=0.52, rely=0.755, relwidth=0.13, relheight=0.10)

    def about_the_program(self):
        """Button function to open the 'About the Program.pdf' """
        path = os.getcwd()
        filename = path + "/Scripts/AboutTheProgram.pdf"
        os.startfile(filename)

    def routine(self):
        """Creation of the window of the program steps"""
        self.frame2 = Toplevel(self.root)
        self.frame2.geometry("700x500")
        self.frame_msg = Label(self.frame2, text='', bg='#778DA9', font=('verdana', 8, 'bold'))
        self.frame_msg.place(relx=0.25, rely=0.15, relwidth=0.5, relheight=0.7)
        self.msg_infos()

    def search_video(self):
        """Selection of the experiment video"""
        self.video = filedialog.askopenfilename(title="Select the video")
        self.video_entry.config(text=self.video)

    def clean(self):
        """Erase all data filled in"""
        self.video = ""
        self.video_entry.config(text="Empty")
        self.folder_entry.delete(0, END)
        self.cut_entry.delete(0, END)
        self.sheet_entry.delete(0, END)
        self.bt_areas.deselect()

    def run(self):
        """Start the program"""
        info = (self.video + "§" + self.folder_entry.get() + "§" + self.cut_entry.get() + "§" + str(self.v.get()) + "§"
                + self.sheet_entry.get() + "§")

        doc = open("data_info.ini", "w")
        doc.writelines(info)

        self.active = messagebox.askyesno("Confirmation", "Start the program?")

        if self.active:
            with open('info_msg.ini', 'w') as doc:
                doc.writelines("")
            self.routine()
            self.frame1.destroy()
            main_script = "./Scripts/mix_time_determination.py"
            Popen(["python", main_script])

    def info_button(self):
        """Show information about the authors"""
        self.window = Toplevel(self.root)
        self.window.transient(self.root)
        self.window.geometry('600x100')
        text = ("MIXING TIME DETERMINATION - Using Colorimetric Method\nBy Yago Silva¹, Fernando Cecatto² and "
                "Elisabeth Augusto³\nBioprocess Laboratory with Animal Cells - Science and Technology Institute, "
                "Federal University of São Paulo\nThis program analyzes the global mixing time of the equipment "
                "(e.g. reactor, shaker flask).\n Contacts: ¹yago.gregorio@unifesp.br, ²fernando.assis@unifesp.br, "
                "³elisabeth.augusto@unifesp.br")
        self.label = Label(self.window, text=text, anchor=CENTER, justify=LEFT)
        self.label.pack()

    def msg_infos(self):
        """Updates the step the program is processing"""
        doc = open("info_msg.ini")
        vector = doc.readlines()
        text = ''
        for i in range(len(vector)):
            text += vector[i]
        self.frame_msg.config(text=text)
        self.frame_msg.after(1000, self.msg_infos)

    # onclick and outclick functions to describe what is expected inside the labels of the data
    def onclick_temp_text_1(self, event):
        if self.folder_entry.get() == "Enter the name of the frames folder":
            self.folder_entry.delete(0, END)
            self.folder_entry.insert(0, '')
            self.folder_entry.config(fg='black')

    def outclick_temp_text_1(self, event):
        if self.folder_entry.get() == "":
            self.folder_entry.insert(0, "Enter the name of the frames folder")
            self.folder_entry.config(fg='gray')

    def onclick_temp_text_2(self, event):
        if self.cut_entry.get() == "Enter 0 (don't cut the end) or the time value":
            self.cut_entry.delete(0, END)
            self.cut_entry.insert(0, '')
            self.cut_entry.config(fg='black')

    def outclick_temp_text_2(self, event):
        if self.cut_entry.get() == "":
            self.cut_entry.insert(0, "Enter 0 (don't cut the end) or the time value")
            self.cut_entry.config(fg='gray')

    def onclick_temp_text_3(self, event):
        if self.sheet_entry.get() == "Enter the name of the results worksheet":
            self.sheet_entry.delete(0, END)
            self.sheet_entry.insert(0, '')
            self.sheet_entry.config(fg='black')

    def outclick_temp_text_3(self, event):
        if self.sheet_entry.get() == "":
            self.sheet_entry.insert(0, "Enter the name of the results worksheet")
            self.sheet_entry.config(fg='gray')


class Application(Funcs):
    """Creation of the main class of the GUI"""
    def __init__(self):
        self.root = Tk()
        self.window()
        self.window_commands()
        self.root.mainloop()

    def window(self):
        """Creation of the main window"""
        self.root.title('Mixing Time Determination')
        self.root.geometry("700x500")
        self.root.configure(background='#E0E1DD')

    def window_commands(self):
        """Creation of the main interface of the program"""
        self.title = Label(self.root, text="MIXING TIME DETERMINATION\nUsing Colorimetric Method", bg='#E0E1DD',
                           fg='#1B263B', font=('verdana', 14, 'bold'))
        self.title.place(relx=0.25, rely=0.02, relwidth=0.5)
        self.info = PhotoImage(file="./Icons/Information_icon (1).png")
        self.infomations = Button(self.root, bd=0, bg='#E0E1DD', activebackground='#E0E1DD', image=self.info,
                                  command=self.info_button)
        self.infomations.place(relx=0.8, rely=0.025)
        self.btn1 = Button(self.root, bd=4, bg='#778DA9', text='Start Program', command=self.parameters)
        self.btn1.place(relx=0.02, rely=0.30, relwidth=0.96, relheight=0.18)
        self.btn2 = Button(self.root, bd=4, bg='#778DA9', text='About the Program', command=self.about_the_program)
        self.btn2.place(relx=0.02, rely=0.60, relwidth=0.96, relheight=0.18)


Application()
