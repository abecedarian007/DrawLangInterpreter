import tkinter as tk
from lexer import tokenize
from tkinter import ttk
from src.parser import Parser
from ttkthemes import ThemedTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import numpy as np

class TextRedirector(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, str):
        self.widget.configure(state='normal')
        self.widget.insert('end', str)
        self.widget.configure(state='disabled')
        self.widget.see('end')

    def flush(self):
        pass


def perform_lexical_analysis(code):
    original_stdout = sys.stdout
    sys.stdout = TextRedirector(output_text)
    for token_name in tokenize(code):
        token_name.show()
    sys.stdout = original_stdout
def perform_syntax_analysis(code):
    original_stdout = sys.stdout
    sys.stdout = TextRedirector(output_text)
    parser = Parser()
    parser.parse(code)
    sys.stdout = original_stdout

def perform_drawing(code):
    parser = Parser()
    parser.parse(code,draw=True)
    plt.show(block = False)

# 创建主窗口
# 设置主题
root = ThemedTk(theme="radiance")
root.title("函数绘图语言解释器")
root.grid_columnconfigure(0, weight=1)

# 创建PanedWindow小部件
paned_window = ttk.PanedWindow(root, orient=tk.VERTICAL)
paned_window.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

# 输入框和其滚动条
input_frame = ttk.Frame(paned_window, height=200)
input_frame.pack_propagate(False)  # 防止内部小部件调整框架大小
input_label = ttk.Label(input_frame, text="输入:")
input_label.pack(side=tk.TOP, fill=tk.X)
input_text = tk.Text(input_frame)
input_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
input_scrollbar = ttk.Scrollbar(input_frame, command=input_text.yview)
input_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
input_text['yscrollcommand'] = input_scrollbar.set

# 输出框
output_frame = ttk.Frame(paned_window, height=200)
output_frame.pack_propagate(False)
output_label = ttk.Label(output_frame, text="输出:")
output_label.pack(side=tk.TOP, fill=tk.X)
output_text = tk.Text(output_frame, state='disabled')
output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
output_scrollbar = ttk.Scrollbar(output_frame, command=output_text.yview)
output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
output_text['yscrollcommand'] = output_scrollbar.set

# 将输入框和输出框添加到PanedWindow
paned_window.add(input_frame)
paned_window.add(output_frame)

# 确保PanedWindow能够扩展填满整个根窗口
root.grid_rowconfigure(0, weight=1)

def delete_output():
    output_text.configure(state='normal')
    output_text.delete('1.0', tk.END)
    output_text.configure(state='disabled')
def lexical_analysis():
    delete_output()
    code = input_text.get("1.0", tk.END) #读取文本框全部内容
    perform_lexical_analysis(code)
def syntax_analysis():
    delete_output()
    code = input_text.get("1.0", tk.END)
    perform_syntax_analysis(code)

def drawing():
    code = input_text.get("1.0", tk.END)
    perform_drawing(code)


button_frame = ttk.Frame(root, padding="10")
button_frame.grid(row=2, column=0, sticky="ew")

root.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(0, weight=1)  # 空列，用于居中
button_frame.grid_columnconfigure(1, weight=0)  # 词法分析按钮
button_frame.grid_columnconfigure(2, weight=0)  # 语法分析按钮
button_frame.grid_columnconfigure(3, weight=0)  # 绘图按钮
button_frame.grid_columnconfigure(4, weight=1)  # 空列，用于居中


lexical_button = ttk.Button(button_frame, text="词法分析",command=lexical_analysis)
lexical_button.grid(row=0, column=1, padx=5)

syntax_button = ttk.Button(button_frame, text="语法分析",command=syntax_analysis)
syntax_button.grid(row=0, column=2, padx=5)

draw_button = ttk.Button(button_frame, text="绘图",command=drawing)
draw_button.grid(row=0, column=3, padx=5)



# 运行主循环
root.mainloop()

