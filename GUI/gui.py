from io import StringIO
from tkinter import *
from tkinter import scrolledtext as st
from tkinter import filedialog
from tkinter import ttk
from AnalisadorLexico import *
class GUI:

    def __init__(self):
        self.app = Tk()
        self.app.title("Compiler")
        self.app.geometry("800x500")

        # Frames
        self.frame_code = Frame(self.app)
        self.frame_code.place(x=5,y=5)
        self.frame_token = Frame(self.app)
        self.frame_token.place(x=290,y=5)
        self.frame_symbol_table = Frame(self.app)
        self.frame_symbol_table.place(x=575,y=5)
        self.frame_commands = Frame(self.app)
        self.frame_commands.place(x= 1000, y=5)
        # Code
        self.code_label = Label(self.frame_code, text="Code")
        self.code_label.pack(side=TOP)
        self.code_text_area = st.ScrolledText(self.frame_code, height=25, width=30)
        self.code_text_area.pack(side=TOP)
        self.open_code_button = Button(self.frame_code,text="Open code as file", command=self.open_file_code)
        self.open_code_button.pack(side=BOTTOM)
        # Token
        self.token_label = Label(self.frame_token, text="Token")
        self.token_label.pack(side=TOP)
        self.token_text_area = st.ScrolledText(self.frame_token, height=25, width=30)
        self.token_text_area.pack(side=TOP)
        self.open_token_button = Button(self.frame_token,text="Open token as file", command=self.open_file_token)
        self.open_token_button.pack(side=BOTTOM)

        # Symbol Table
        self.symbol_table_label = Label(self.frame_symbol_table, text="Symbol Table")
        self.symbol_table_label.pack(side=TOP)
        self.symbol_table_tree = Frame(self.frame_symbol_table)
        self.symbol_table_tree.pack()
        tree_scroll = Scrollbar(self.symbol_table_tree)
        self.symbol_table = ttk.Treeview(self.symbol_table_tree, height=20, yscrollcommand=tree_scroll.set)
        tree_scroll.pack(side=RIGHT,fill=Y)
        tree_scroll.config(command=self.symbol_table.yview)
        self.symbol_table.pack(side=TOP)
        self.symbol_table['columns'] = ("Lexema", "Token")
        self.symbol_table.column("#0", width=0,stretch=NO)
        self.symbol_table.column("Lexema",anchor=W,width=100)
        self.symbol_table.column("Token", anchor=W, width=100)
        self.symbol_table.heading("Lexema", text="Lexema")
        self.symbol_table.heading("Token", text="Token")
    
        # Command Buttons - Not implement yet
        self.button_start = Button(self.frame_symbol_table, text="Start", command=self.start_analyzer)
        self.button_start.pack(pady=10,side=BOTTOM)
        mainloop()

    def open_file_code(self):
        filepath = filedialog.askopenfilename()
        file = open(filepath, 'r')
        text = file.read()
        self.code_text_area.delete("1.0","end")
        self.code_text_area.insert(INSERT, text)
        file.close()

    def open_file_token(self):
        filepath = filedialog.askopenfilename()
        file = open(filepath, 'r')
        text = file.read()
        self.token_text_area.delete("1.0","end")
        self.token_text_area.insert(INSERT, text)
        file.close()

    def start_analyzer(self):
        text_code = self.code_text_area.get("1.0", "end")
        text_token = self.token_text_area.get("1.0", "end")
        afd = insert_token_GUI(StringIO(text_token))
        symbol_table_output = start_lexical_analyzer_GUI(StringIO(text_code), afd)
        for i in symbol_table_output:
            self.symbol_table.insert('','end',values=(i[0],i[1]))
