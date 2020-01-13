from tkinter import *
from tkinter import messagebox
import fun_library
import NLP_processing
import db_handler

level = None


class NLPUi:
    def __init__(self, root):
        self.root = root
        root.title("Question Answer")

        self.exitButton = Button(root)
        self.exitButton.place(relx=0.91, rely=0.95, relheight=0.04, relwidth=0.08)
        self.exitButton.configure(text="Exit")
        self.exitButton.configure(background="#ff4444")
        self.exitButton.configure(command=lambda: destroy_it())

        self.heading = Label(root)
        self.heading.place(relx=0.0, rely=0.0, relheight=0.05, relwidth=1.0)
        self.heading.configure(text="Ask Question")
        self.heading.configure(background="#ffffff")

        self.entry = Entry(root)
        self.entry.place(relx=0.1, rely=0.1, relheight=0.05, relwidth=0.8)

        self.askButton = Button(root)
        self.askButton.place(relx=0.38, rely=0.16, relheight=0.05, relwidth=0.1)
        self.askButton.configure(text="Ask Question")
        self.askButton.configure(background="#ffffff")
        self.askButton.configure(command=lambda: self.process_text_question())

        self.askButton = Button(root)
        self.askButton.place(relx=0.52, rely=0.16, relheight=0.05, relwidth=0.1)
        self.askButton.configure(text="Speak Question")
        self.askButton.configure(background="#ffffff")
        self.askButton.configure(command=lambda: self.take_speech_input())

        self.frame1 = Frame(root, relief="sunken")
        self.frame1.configure(background="#ffffff")
        self.scrollbar = Scrollbar(self.frame1)
        self.editArea = Text(self.frame1, wrap="word", state='disabled', yscrollcommand=self.scrollbar.set,
                             borderwidth=0, highlightthickness=0)
        self.editArea.place(relx=0.02, rely=0.02, relheight=0.96, relwidth=0.96)
        self.scrollbar.config(command=self.editArea.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.frame1.place(relx=0.02, rely=0.22, relheight=0.70, relwidth=0.96)

    def draw_line(self, rx, ry, rh, rw):
        self.line = Label(self.root)
        self.line.place(relx=rx, rely=ry, relheight=rh, relwidth=rw)
        self.line.configure(background="#000000")

    def set_text(self, txt):
        self.editArea.configure(state="normal")
        self.editArea.delete('1.0', 'end')
        self.editArea.insert('1.0', txt)
        self.editArea.configure(state="disabled")

    def append_text(self, txt):
        self.editArea.configure(state="normal")
        self.editArea.insert('end', "\n"+txt)
        self.editArea.configure(state="disabled")

    def process_text_question(self):
        question = self.entry.get()
        self.append_text("Your Question is :"+question)
        ans = NLP_processing.process_question(question)
        if ans[0][0] == 1:
            self.append_text("Answer :" + ans[0][1])
            fun_library.sayIt("Answer for your question is, " + ans[0][1])
        else:
            exp = messagebox.askyesno("Question",
                                      "System couldn't generate answer for your question, "
                                      "do you want to ask the question to expert system? \n"
                                      "Your question was: " + question)
            if exp:
                if db_handler.send_to_expert_system(question, ans[1]):
                    messagebox.showinfo("Answer",
                                        "Question sent to expert system, "
                                        "please check expert system section in menu screen to check for your answers")
                    self.append_text("Answer :" +
                                     "Question sent to expert system, "
                                     "please check expert system section in menu screen to check for your answers")
                else:
                    messagebox.showinfo("Answer",
                                        "Internet connection not available, please check it and try again")
                    self.append_text(
                        "Answer :" + "Internet connection not available, please check it and try again")
            else:
                messagebox.showinfo("Answer",
                                    "System couldn't Generate answer")
                self.append_text("Answer :" + "System couldn't Generate answer")

    def take_speech_input(self):
        speech = fun_library.take_speech_input()
        if speech[0] == 1:
            self.entry.delete(0,END)
            self.entry.insert('end', speech[1])
            self.process_text_question()
        elif speech[0] == 0:
            messagebox.showerror("Speech input error", speech[1])
        else:
            messagebox.showwarning("Speech Engine Error", speech[1])


def destroy_it():
    level.destroy()


def start_nlp_ui():
    global level
    wh = fun_library.get_system_height()
    ww = fun_library.get_system_width()
    level = Toplevel()
    level.attributes('-toolwindow', True)
    level.resizable(False, False)
    level.geometry("%dx%d%+d%+d" % (int(ww*0.8), int(wh*0.8), int(ww*0.1), int(wh*0.1)))
    new_top = NLPUi(level)
    level.mainloop()
