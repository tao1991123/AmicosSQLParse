# -*- coding: UTF-8 -*-
import tkinter as tk
from SQLParse import SQLParse
from SQLParseConst import *


class SQLParseWindow(object):
    def __init__(self, master):
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
        self.button_transfer.grid(row=0, column=0, padx=40)
        self.button_clear = tk.Button(frame_button, text='清空', width=10, font=('Microsoft YaHei', 10),
                                      command=self.__textClear)
        self.button_clear.grid(row=0, column=1, padx=40)
        self.clearVar = tk.IntVar()
        self.clearVar.set(0)
        self.checkButton = tk.Checkbutton(frame_button, text='转换完成后清空输入', variable=self.clearVar)
        self.checkButton.grid(row=0, column=2, padx=40)

        self.choice = tk.IntVar()
        self.choice.set(0)
        for i in SQLTYPEDICT.keys():
            temp = tk.Radiobutton(frame_choice, text=SQLTYPEDICT[i], variable=self.choice, value=i)
            temp.grid(row=0, column=i)


    def __textClear(self):
        self.text_input.delete('1.0', tk.END)
        self.text_output.delete('1.0', tk.END)

    def __transfer(self):
        originText = self.text_input.get('1.0', tk.END)
        try:
            transferedText = SQLParse(originText, self.choice.get())
        except Exception:
            transferedText = SQLParseError[1]
        finally:
            self.text_output.delete('1.0', tk.END)
            self.text_output.insert('1.0', transferedText)
            if self.clearVar.get() == 1:
                self.text_input.delete('1.0', tk.END)


def main():
    rootWindow = tk.Tk()
    rootWindow.title('Amicos SQL语句转换')

    sqlWindow = SQLParseWindow(rootWindow)
    rootWindow.resizable(tk.FALSE, tk.FALSE)
    rootWindow.mainloop()


if __name__ == '__main__':
    main()