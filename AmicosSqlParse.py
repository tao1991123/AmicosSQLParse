# -*- coding: UTF-8 -*-
import tkinter as tk
from SQLParse import *
from SQLParseConst import *


class SQLParseWindow(object):
    def __init__(self, master):
        self.__copyed = False
        self.__isEmpty = True
        self.__transferedText = ''
        frame_choice = tk.Frame(master)
        frame_choice.grid(row=0, column=0)

        frame_input = tk.Frame(master, pady=5)
        frame_input.grid(row=1, column=0)

        frame_button = tk.Frame(master, pady=5)
        frame_button.grid(row=2, column=0)

        frame_output = tk.Frame(master, pady=5)
        frame_output.grid(row=3, column=0)

        self.text_input = tk.Text(frame_input, width=60, height=10, font=('Microsoft YaHei', 12))
        self.text_input.pack()

        self.text_output = tk.Text(frame_output, width=60, height=10, font=('Microsoft YaHei', 12))
        self.text_output.pack()

        self.button_transfer = tk.Button(frame_button, text='转换', width=10, font=('Microsoft YaHei', 10),
                                         command=self.__transfer)
        self.button_transfer.grid(row=0, column=0, padx=10)
        self.button_clear = tk.Button(frame_button, text='清空', width=10, font=('Microsoft YaHei', 10),
                                      command=self.__textClear)
        self.button_clear.grid(row=0, column=1, padx=10)

        self.button_copy = tk.Button(frame_button, text='提取', width=10, font=('Microsoft YaHei', 10),
                                      command=self.__copy)
        self.button_copy.grid(row=0, column=2, padx=10)

        self.clearVar = tk.IntVar()
        self.clearVar.set(0)
        self.checkButton = tk.Checkbutton(frame_button, text='转换完成后清空输入', variable=self.clearVar)
        self.checkButton.grid(row=0, column=3, padx=10)

        self.choice = tk.IntVar()
        self.choice.set(0)
        for i in SQLTYPEDICT.keys():
            temp = tk.Radiobutton(frame_choice, text=SQLTYPEDICT[i], variable=self.choice, value=i)
            temp.grid(row=0, column=i)


    def __textClear(self):
        self.text_input.delete('1.0', tk.END)
        self.text_output.delete('1.0', tk.END)
        self.__copyed = False
        self.__isEmpty = True

    def __transfer(self):
        originText = self.text_input.get('1.0', tk.END)
        self.__transferedText = ''
        try:
            self.__transferedText = SQLParse(originText, self.choice.get())
            self.__isEmpty = False
        except Exception:
            self.__transferedText = SQLParseError[1]
            self.__isEmpty = True
        finally:
            self.text_output.delete('1.0', tk.END)
            self.text_output.insert('1.0', self.__transferedText)
            self.__copyed = False
            if self.clearVar.get() == 1:
                self.text_input.delete('1.0', tk.END)

    def __copy(self):
        if not self.__isEmpty:
            copyToClipboard(self.__transferedText)
            if not self.__copyed :
                self.__copyed = True
                self.text_output.insert('1.0',SqlIndecationInfo[0])
                self.text_output.tag_add("info",'1.0','1.end')
                self.text_output.tag_config("info",foreground="red")


def main():
    rootWindow = tk.Tk()
    rootWindow.title('Amicos SQL语句转换')

    sqlWindow = SQLParseWindow(rootWindow)
    rootWindow.resizable(tk.FALSE, tk.FALSE)
    rootWindow.mainloop()


if __name__ == '__main__':
    main()