from io import StringIO
from tkinter import *
from tkinter import scrolledtext as st
from tkinter import filedialog
from tkinter import ttk
from tkinter.font import Font
from AnalisadorLexico import insert_token, start_lexical_analyzer
from Gramatica import *

class GUI:

    def __init__(self):
        self.app = Tk()
        self.app.title("Compiler")
        self.app.geometry("800x500")

        # Frames
        self.frame_code = Frame(self.app)
        self.frame_code.place(x=5, y=5)
        self.frame_token = Frame(self.app)
        self.frame_token.place(x=290, y=5)
        self.frame_symbol_table = Frame(self.app)
        self.frame_symbol_table.place(x=575, y=5)
     
        
        # Code
        self.code_label = Label(self.frame_code, text="Code")
        self.code_label.pack(side=TOP)
        self.code_text_area = st.ScrolledText(
            self.frame_code, height=25, width=30)
        self.code_text_area.pack(side=TOP)
        self.open_code_button = Button(
            self.frame_code, text="Open code as file", command=self.open_file_code)
        self.open_code_button.pack(side=BOTTOM)
        # Token
        self.token_label = Label(self.frame_token, text="Token")
        self.token_label.pack(side=TOP)
        self.token_text_area = st.ScrolledText(
            self.frame_token, height=25, width=30)
        self.token_text_area.pack(side=TOP)
        self.open_token_button = Button(
            self.frame_token, text="Open token as file", command=self.open_file_token)
        self.open_token_button.pack(side=BOTTOM)

        # Symbol Table
        self.symbol_table_label = Label(
            self.frame_symbol_table, text="Symbol Table")
        self.symbol_table_label.pack(side=TOP)
        self.symbol_table_tree = Frame(self.frame_symbol_table)
        self.symbol_table_tree.pack()
        tree_scroll = Scrollbar(self.symbol_table_tree)
        self.symbol_table = ttk.Treeview(
            self.symbol_table_tree, height=20, yscrollcommand=tree_scroll.set)
        tree_scroll.pack(side=RIGHT, fill=Y)
        tree_scroll.config(command=self.symbol_table.yview)
        self.symbol_table.pack(side=TOP)
        self.symbol_table['columns'] = ("Lexema", "Token")
        self.symbol_table.column("#0", width=0, stretch=NO)
        self.symbol_table.column("Lexema", anchor=W, width=100)
        self.symbol_table.column("Token", anchor=W, width=100)
        self.symbol_table.heading("Lexema", text="Lexema")
        self.symbol_table.heading("Token", text="Token")

        # Command Buttons
        self.button_start = Button(
            self.frame_symbol_table, text="Start", command=self.start_analyzer)
        self.button_start.pack(pady=10, side=BOTTOM)

        self.bold_font = Font(family="Helvetica", weight="bold")
        self.code_text_area.tag_configure("BOLD", font=self.bold_font)

        mainloop()

    def open_file_code(self):
        filepath = filedialog.askopenfilename()
        file = open(filepath, 'r')
        text = file.read()
        self.code_text_area.delete("1.0", "end")
        self.code_text_area.insert(INSERT, text)
        file.close()

    def open_file_token(self):
        filepath = filedialog.askopenfilename()
        file = open(filepath, 'r')
        text = file.read()
        self.token_text_area.delete("1.0", "end")
        self.token_text_area.insert(INSERT, text)
        file.close()

    def set_error(self, coords):
        self.code_text_area.tag_add(
            "BOLD", f"{coords[0]}.{coords[1]}", f"{coords[0]}.{coords[1]+1}")

    def start_analyzer(self):
        # clear set errors and old symbol table
        self.code_text_area.tag_remove("BOLD", "1.0", END)
        self.symbol_table.delete(*self.symbol_table.get_children())
        # get text areas values
        text_code = self.code_text_area.get("1.0", "end")
        text_token = self.token_text_area.get("1.0", "end")
        # get tokens AFD from file
        afd = insert_token(StringIO(text_token))
        # use result from last step to create the symbol table and insert on component
        symbol_table_output = start_lexical_analyzer(
            StringIO(text_code), afd, self.set_error)
        for i in symbol_table_output:
            self.symbol_table.insert('', 'end', values=(i[0], i[1]))

    def create_parsing_table(self, action, goto, symbols):
        def get_last_state_index():
            action_last_state_index = sorted(list(action.keys()))[-1][0]
            goto_last_state_index = sorted(list(goto.keys()))[-1][0]
            state_index = 0
            if action_last_state_index > goto_last_state_index:
                state_index = action_last_state_index
            else:
                state_index = goto_last_state_index
            return state_index

        def action_goto_empty_filled():

            state_index = get_last_state_index()
            dict_action_goto = {**action, **goto}
            for i in range(state_index + 1):
                for symbol in symbols:
                    if (i,symbol) not in dict_action_goto:
                        dict_action_goto[(i,symbol)] = '-'
            dict_action_goto = sorted(dict_action_goto.items())
            return dict_action_goto

        def create_parsing_table_formatted():
            parsing_table = {}
            dict_action_goto = action_goto_empty_filled()
            parsing_table_formatted = []
            for x,y in dict_action_goto:
                if x[0] in parsing_table:
                    parsing_table[x[0]].append(y)
                else:
                    parsing_table[x[0]] = [y]

            for x in parsing_table.items():
                a = x[1].copy()
                a.insert(0, x[0])
                parsing_table_formatted.append(tuple(a))
                

            return parsing_table_formatted

        parsing_table = create_parsing_table_formatted()

        # Parsing Table
        self.parsing_table_window = Toplevel(self.app)
        self.parsing_table_window.title("Parsing Table")
        self.frame_parsing_table = Frame(self.parsing_table_window)
        self.frame_parsing_table.pack(fill='x')
        self.parsing_table_label = Label(
        self.frame_parsing_table, text="Parsing Table")
        self.parsing_table_label.pack(side=TOP)
        self.parsing_table_frame = Frame(self.frame_parsing_table)
        self.parsing_table_frame.pack(fill='x')
        table_scroll = Scrollbar(self.parsing_table_frame)
        table_scrollx = Scrollbar(self.parsing_table_frame, orient=HORIZONTAL)
        self.parsing_table = ttk.Treeview(
            self.parsing_table_frame, height=20,
            yscrollcommand=table_scroll.set,
            xscrollcommand=table_scrollx.set)
        table_scrollx.pack(side=BOTTOM, fill=X)
        table_scrollx.config(command=self.parsing_table.xview)
        table_scroll.pack(side=RIGHT, fill=Y)
        table_scroll.config(command=self.parsing_table.yview)
        self.parsing_table.pack(side=TOP, fill='x')

        self.parsing_table['columns'] = tuple(["States"]+symbols)
        self.parsing_table.column("#0", width=0, stretch=NO)
        self.parsing_table.column("States", anchor=CENTER, width=120)
        self.parsing_table.heading("States", text="States")

        for i in symbols:
            self.parsing_table.column(i, anchor=CENTER, width=120)
            self.parsing_table.heading(i, text=i)

        for i in parsing_table:
            self.parsing_table.insert('', 'end', values=i)