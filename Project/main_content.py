from tkinter import *
from tkinter import Label
import NLP
import db_handler
from PIL import ImageTk, Image
import tkinter.ttk as ttk
import fun_library
import NLP_UI

system_height = fun_library.get_system_height()
system_width = fun_library.get_system_width()

chapter_content = []
speech_flag = 0
root = None


class New_Toplevel:
    def __init__(self, top=None):
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#d9d9d9' # X11 color: 'gray85'
        font11 = "-family Sylfaen -size 12 -weight bold -slant roman "  \
            "-underline 0 -overstrike 0"
        font14 = "-family {Times New Roman} -size 15 -weight bold "  \
            "-slant roman -underline 0 -overstrike 0"

        font_heading = "-family {Segoe UI} -size "+self.font_size(15)


        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        #top.geometry("1366x706+0+0")
        top.title("Intelligent Programming Learning System")
        top.configure(background="#ebebeb")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.Label1 = Label(top)
        self.Label1.place(relx=0.01, rely=0.01, relheight=0.05, relwidth=0.75)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(activeforeground="black")
        self.Label1.configure(background="#38bde9")
        self.Label1.configure(disabledforeground="#3193a4")
        self.Label1.configure(font=font11)
        self.Label1.configure(foreground="#fdfdff")
        self.Label1.configure(highlightbackground="#2bb6c1")
        self.Label1.configure(highlightcolor="#2bb6c1")
        self.Label1.configure(text='''Intelligent Programming Learning System''')

        self.Label2 = Label(top)
        self.Label2.place(relx=0.01, rely=0.07, relheight=0.05, relwidth=0.75)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(activeforeground="black")
        self.Label2.configure(background="#38bde9")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(font=font11)
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(highlightbackground="#06978f")
        self.Label2.configure(highlightcolor="#067370")
        self.Label2.configure(text='Chapter: '+chapter_content["chapter_name"] + '\t Topic Name: '+chapter_content["chapter_content"][0]["topic_name"])
        self.Label2.configure(width=1040)

        self.Button1 = Button(top)
        self.Button1.place(relx=0.01, rely=0.95, relheight=0.04, relwidth=0.08)
        self.Button1.configure(activebackground="#d9d9d9")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#38bde9")
        self.Button1.configure(disabledforeground="#a3a3a3")
        #self.Button1.configure(font=font11)
        self.Button1.configure(foreground="#151515")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''View Theory''')
        self.Button1.configure(command=lambda : view_another_window(self))

        self.Button1 = Button(top)
        self.Button1.place(relx=0.68, rely=0.95, relheight=0.04, relwidth=0.08)
        self.Button1.configure(background="#38bde9")
        self.Button1.configure(text='''Next Chapter''')
        self.Button1.configure(command=lambda: next_chapter())


        self.Button2 = Button(top)
        self.Button2.place(relx=0.77, rely=0.95, relheight=0.04, relwidth=0.22)
        self.Button2.configure(activebackground="#d9d9d9")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#ff0000")
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(text='''EXIT''')
        self.Button2.configure(command = lambda : get_out())


        self.Frame1 = Frame(top)
        self.Frame1.place(relx=0.77, rely=0.07, relheight=0.86, relwidth=0.22)
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(borderwidth="1")
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(background="#e2e2e2")
        self.Frame1.configure(highlightbackground="#d9d9d9")
        self.Frame1.configure(highlightcolor="black")
        self.Frame1.configure(width=305)

        self.Label5 = Label(self.Frame1)
        self.Label5.place(relx=0.03, rely=0.02, height=31, relwidth=0.94)
        self.Label5.configure(activebackground="#f9f9f9")
        self.Label5.configure(activeforeground="black")
        self.Label5.configure(background="#e2e2e2")
        self.Label5.configure(disabledforeground="#a3a3a3")
        self.Label5.configure(font=font14)
        self.Label5.configure(foreground="#000000")
        self.Label5.configure(highlightbackground="#d9d9d9")
        self.Label5.configure(highlightcolor="black")
        self.Label5.configure(text='''MENU''')

        self.current_topic = 0
        self.Button4 = []
        for i in range(0, len(chapter_content['chapter_content'])):
            rly = 0.08 + 0.05*i
            txt = chapter_content['chapter_content'][i]['topic_name']
            topic_id = chapter_content['chapter_content'][i]['topic_id']
            self.Button4.append(Button(self.Frame1))
            self.Button4[i].place(relx=0.03, rely=rly, relheight=0.045, relwidth=0.94)
            self.Button4[i].configure(text=txt)
            self.Button4[i].configure(command= lambda j=i: self.submenu_click(j))

        im = Image.open("content/images/"+chapter_content['chapter_content'][0]['topic_id']+".jpg")
        hsize = int(system_height*0.75)
        wsize = int(system_width*0.75)
        im = im.resize((wsize, hsize), Image.ANTIALIAS)
        im.save("content/temp/current.jpg")

        img = ImageTk.PhotoImage(Image.open("content/temp/current.jpg"))
        self.Text1 = Label(top, image=img)
        self.Text1.image = img
        self.Text1.place(relx=0.01, rely=0.13, relwidth=0.75, relheight=0.75)
        self.Text1.configure(background="#111111")

        self.status = Label(top)
        self.status.place(relx=0.01, rely=0.89, relwidth=0.75, relheight=0.04)
        self.status.configure(background="#d7bde2")

        self.say_button = Button(self.Frame1)
        self.say_button.place(relx=0.01, rely=0.95, relheight=0.04, relwidth=0.48)
        self.say_button.configure(activebackground="#d9d9d9")
        self.say_button.configure(activeforeground="#000000")
        self.say_button.configure(background="#38bde9")
        self.say_button.configure(disabledforeground="#a3a3a3")
        #        self.Button3.configure(foreground="#000000")
        self.say_button.configure(highlightbackground="#d9d9d9")
        self.say_button.configure(highlightcolor="black")
        self.say_button.configure(pady="0")
        self.say_button.configure(text='''Start Listening''')
        self.say_button.configure(command=lambda: self.sayIt())

        self.stop_button = Button(self.Frame1)
        self.stop_button.place(relx=0.51, rely=0.95, relheight=0.04, relwidth=0.48)
        self.stop_button.configure(activebackground="#d9d9d9")
        self.stop_button.configure(activeforeground="#000000")
        self.stop_button.configure(background="#38bde9")
        self.stop_button.configure(disabledforeground="#a3a3a3")
        #        self.Button3.configure(foreground="#000000")
        self.stop_button.configure(highlightbackground="#d9d9d9")
        self.stop_button.configure(highlightcolor="black")
        self.stop_button.configure(pady="0")
        self.stop_button.configure(text='''Stop Listening''')
        self.stop_button.configure(command=lambda: self.stopIt())
        NLP.statusobj.append(self.status)

        self.Button3 = Button(top)
        self.Button3.place(relx=0.30, rely=0.93, relheight=0.06, relwidth=0.20)
        self.Button3.configure(disabledforeground="#a3a3a3")
        self.Button3.configure(foreground="#000000")
        self.Button3.configure(pady="5")
        self.Button3.configure(font=font_heading)
        self.Button3.configure(text='''Ask Question''')
        self.Button3.configure(command=lambda: NLP_UI.start_nlp_ui())

    #User Defined Functions

    def submenu_click(self, i):
        self.current_topic = i
        topic_id = chapter_content['chapter_content'][i]['topic_id']
        self.change_image(topic_id)


    def change_image(self, topic_id):
        im = Image.open("content/images/" + topic_id + ".jpg")
        hsize = int(system_height * 0.75)
        wsize = int(system_width * 0.75)
        im = im.resize((wsize, hsize), Image.ANTIALIAS)
        im.save("content/temp/current.jpg")

        img = ImageTk.PhotoImage(Image.open("content/temp/current.jpg"))
        self.Text1.configure(image=img)
        self.Text1.image = img

    def sayIt(self):
        fun_library.sayIt(chapter_content['chapter_content'][self.current_topic]['topic_content'])

    def stopIt(self):
        fun_library.stopIt()

    def font_size(self,size):
        sw = fun_library.get_system_width()
        mf = sw/1000
        sz = mf*size
        return str(int(sz))


def get_out():
    root.destroy()
    #menu.start_menu_ui()


def view_another_window(ref):
    theroy = Toplevel()
    frame1 = Frame(theroy, relief="sunken")
    frame1.configure(background="#ffffff")
    scrollbar = Scrollbar(frame1)
    editArea = Text(frame1, wrap="word", yscrollcommand=scrollbar.set,
                         borderwidth=0, highlightthickness=0)
    editArea.place(relx=0.02, rely=0.02, relheight=0.96, relwidth=0.96)
    scrollbar.config(command=editArea.yview)
    scrollbar.pack(side="right", fill="y")
    frame1.place(relx=0.02, rely=0.22, relheight=0.70, relwidth=0.96)
    editArea.insert('end', chapter_content['chapter_content'][ref.current_topic]['topic_content'])
    theroy.mainloop()

def next_chapter():
    if int(chapter_content['chapter_id']) is not 8:
        root.destroy()
        cont = db_handler.get_reading_content(int(chapter_content['chapter_id'])+1)
        print(cont)
        start_main_content_ui(cont)


def start_main_content_ui(chapter_content_):
    global chapter_content, root
    db_handler.check_first()
    chapter_content = chapter_content_
    print(chapter_content_)
    root = Toplevel()
    root.attributes('-fullscreen', True)
    t1 = New_Toplevel(root)
    root.mainloop()

'''
db_handler.check_first()
chapter_content_1 = db_handler.get_reading_content(5)
start_main_content_ui(chapter_content_1)
'''
