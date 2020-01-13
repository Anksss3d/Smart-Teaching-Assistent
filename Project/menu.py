from tkinter import *
from tkinter import messagebox
import db_handler
import main_content
import NLP_UI
import fun_library
from PIL import ImageTk, Image

level = None


class MenuUi:
    def __init__(self, root):
        self.root = root
        root.title("Menu for program")

        font_menu = "-family {Comic Sans MS} -size "+self.font_size(12)
        font_heading = "-family {Impact} -size "+self.font_size(21)
        font_title = "-family {Georgia} -weight bold -size "+self.font_size(16)
        font_exp = "-family {Georgia} -weight bold -size " + self.font_size(6)

        self.menuTitle1 = Label(root)
        self.menuTitle1.place(relx=0.0, rely=0.0, relheight=0.08, relwidth=1.0)
        self.menuTitle1.configure(text="INTELLIGENT PROGRAMMING LEARNING SYSTEM")
        self.menuTitle1.configure(background="#ffffff")
        self.menuTitle1.configure(foreground="#1b5ba4")
        self.menuTitle1.configure(font=font_heading)

        self.draw_line(root, 0.0, 0.075, 0.001, 1.0)

        self.menuTitle2 = Label(root)
        self.menuTitle2.place(relx=0.30, rely=0.1, relheight=0.04, relwidth=0.40)
        self.menuTitle2.place(relx=0.30, rely=0.1, relheight=0.04, relwidth=0.40)
        self.menuTitle2.configure(text="BROWSE CHAPTERS")
        self.menuTitle2.configure(font=font_title)
        self.menuTitle2.configure(background="#ffffff")
        self.menuTitle2.configure(foreground="#1b4f72 ")

        chapters = db_handler.get_all_chapters()
        self.chapterButtons = []
        for i in range(0, len(chapters)):
            ry = 0.17 + 0.25*int(i/4)
            rrx = (25*i + 1) % 100
            rx = rrx/100

            ht = fun_library.get_system_height()
            hw = fun_library.get_system_width()
            imgh = int(ht/10 * 1.5)
            imgw = int(hw/19 * 1.9)

            og = Image.open("content/java3.png")
            resized = og.resize((imgw, imgh), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(resized)

            self.chapterButtons.append(Button(root))
            # self.chapterButtons.append(Button(root, image=img, compound="top"))
            self.chapterButtons[i].place(relx=rx, rely=ry, relheight=0.20, relwidth=0.23)
            # self.chapterButtons[i].image = img
            self.chapterButtons[i].configure(text=chapters[i][1])
            self.chapterButtons[i].configure(font=font_menu)
            self.chapterButtons[i].configure(borderwidth=0)
            self.chapterButtons[i].configure(background="#38bde9")
            self.chapterButtons[i].configure(foreground="#ffffff")
            self.chapterButtons[i].configure(command=lambda j=i: start_main_content(chapters[j][0]))

        self.testButton = Button(root)
        self.testButton.place(relx=0.01, rely=0.85, relheight=0.12, relwidth=0.14)
        self.testButton.configure(text="Ask Question")
        self.testButton.configure(background="#6fb2ff")
        self.testButton.configure(command=lambda: start_nlp())
        self.testButton.configure(font=font_exp)

        self.refButton = Button(root)
        self.refButton.place(relx=0.01, rely=0.70, relheight=0.12, relwidth=0.14)
        self.refButton.configure(text="Refresh Expert System Question")
        self.refButton.configure(background="#6fb2ff")
        self.refButton.configure(command=lambda: self.refreshExp())
        self.refButton.configure(font=font_exp)

        self.synButton = Button(root)
        self.synButton.place(relx=0.85, rely=0.70, relheight=0.12, relwidth=0.14)
        self.synButton.configure(text="Synchronize With Global Data")
        self.synButton.configure(background="#6fb2ff")
        self.synButton.configure(command=lambda: syn_with_global_db())
        self.synButton.configure(font=font_exp)

        self.exitButton = Button(root)
        self.exitButton.place(relx=0.85, rely=0.85, relheight=0.12, relwidth=0.14)
        self.exitButton.configure(text="Exit")
        self.exitButton.configure(background="#ff4444")
        self.exitButton.configure(command=lambda: destroyIt())
        self.exitButton.configure(font=font_exp)

        self.expTitle = Label(root)
        self.expTitle.place(relx=0.18, rely=0.70, relheight=0.05, relwidth=0.66)
        self.expTitle.configure(text="Expert System Question Answers")
        self.expTitle.configure(background="#ffffff")
        self.expTitle.configure(font=font_exp)
        
        self.frame1 = Frame(root, relief="sunken" )
        self.frame1.configure(background="#ffffff", borderwidth=1)
        self.scrollbar = Scrollbar(self.frame1)
        self.editArea = Text(self.frame1, wrap="word", yscrollcommand=self.scrollbar.set,
                             borderwidth=0, highlightthickness=0)
        self.editArea.place(relx=0.02, rely=0.02, relheight=0.96, relwidth=0.96)
        self.editArea.configure(font=font_exp)
        self.scrollbar.config(command=self.editArea.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.frame1.place(relx=0.18, rely=0.75, relheight=0.24, relwidth=0.66)

        self.refreshExp()

    def font_size(self,size):
        sw = fun_library.get_system_width()
        mf = sw/1000
        sz = mf*size
        return str(int(sz))

    def draw_line(self, rt, rx, ry, rh, rw):
        self.line = Label(rt)
        self.line.place(relx=rx, rely=ry, relheight=rh, relwidth=rw)
        self.line.configure(background="#000000")

    def refreshExp(self):
        if(db_handler.internet_on()):
            self.editArea.configure(state='normal')
            self.editArea.delete('1.0', 'end')
            que = db_handler.get_exp_user_data()
            ans = []
            j=0
            if que['check'] == 1:
                for i in que['data']:
                    self.editArea.insert('end', '\n'+i['question']+': '+i['answer'])
            else:
                print("no answer")
                self.editArea.insert('end', 'No Question Asked')
            self.editArea.configure(state='disabled')
        else:
            print("Internet is Not Conected")


def destroyIt():
    level.destroy()
    exit()


def start_nlp():
    NLP_UI.start_nlp_ui()


def syn_with_global_db():
    syn = db_handler.synchronize_database()
    if(syn):
        messagebox.showinfo("Synchronization", "Synchronization with global data is successful")
    else:
        messagebox.showerror("Synchronization", "Synchronization with global data has been failed, please check your internet connectivity")


def start_main_content(chapter_id):
    print("chapter ID: "+str(chapter_id))
    chapter_content = db_handler.get_reading_content(chapter_id)
    main_content.start_main_content_ui(chapter_content)


def start_menu_ui():
    global level
    level = Tk()
    level.attributes("-fullscreen", True)
    level.configure(background="#ffffff")
    menu_ui = MenuUi(level)
    level.mainloop()


db_handler.check_first()
start_menu_ui()