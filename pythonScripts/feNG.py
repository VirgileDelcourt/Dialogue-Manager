from pythonScripts.beNG import *
from tkinter import *
from tkinter import ttk
from functools import partial


class DialogueManager:
    def __init__(self):
        self.window = Tk()
        self.window.title("New Gaem")
        self.window.geometry("830x530")
        self.bg = "#f42069"
        self.window.config(bg=self.bg)
        self.window.columnconfigure(1, weight=3)

        self.go_choose_button = Button(self.window, text="return to choice", command=self.show_select, width=13, height=1)
        self.go_create_button = Button(self.window, text="go to create", command=self.show_create, width=13, height=1)

        # initializing stuff for kill
        self.go_delete_button = Button(self.window, text="go to delete", command=self.show_delete, width=13, height=1)
        self.delete_box = Frame(self.window, bg=self.bg)
        self.del_cbbox = ttk.Combobox(self.delete_box, textvariable=StringVar(), width=50)
        self.del_button = Button(self.delete_box, text="delete", command=self.delete_line, width=13, height=1)

        # initializing stuff to create new dialogues
        self.create_box = Frame(self.window, bg=self.bg)
        self.script_creation_info = Label(self.create_box, bg=self.bg, text="Dialogue :")
        self.new_line_script_cbbox = ttk.Combobox(self.create_box, textvariable=StringVar(), width=50)
        self.script_creation_tip = Label(self.create_box, bg=self.bg, text="(if you put an non-existant script, a new one will be created)")

        self.title_creation_info = Label(self.create_box, bg=self.bg, text="Character talking :")
        self.new_line_title = Entry(self.create_box, textvariable=StringVar(), font=("Helvetica", 10), width=45)

        self.text_creation_info = Label(self.create_box, bg=self.bg, text="Text :")
        self.new_line_text = Entry(self.create_box, textvariable=StringVar(), font=("Helvetica", 10), width=45)

        self.img_creation_info = Label(self.create_box, bg=self.bg, text="Images :")
        self.img1_character = ttk.Combobox(self.create_box, textvariable=StringVar(), width=50)
        self.img1_action = ttk.Combobox(self.create_box, textvariable=StringVar(), width=50)
        self.img_creation_info2 = Label(self.create_box, bg=self.bg, text="--")
        self.img2_character = ttk.Combobox(self.create_box, textvariable=StringVar(), width=50)
        self.img2_action = ttk.Combobox(self.create_box, textvariable=StringVar(), width=50)

        self.follow_creation_info = Label(self.create_box, bg=self.bg, text="Next Dialogues :")
        self.follow1_text = Entry(self.create_box, textvariable=StringVar(), font=("Helvetica", 10), width=45)
        self.follow1_id = ttk.Combobox(self.create_box, textvariable=StringVar(), width=50)
        self.follow_creation_info2 = Label(self.create_box, bg=self.bg, text="--")
        self.follow2_text = Entry(self.create_box, textvariable=StringVar(), font=("Helvetica", 10), width=45)
        self.follow2_id = ttk.Combobox(self.create_box, textvariable=StringVar(), width=50)
        self.follow_creation_info3 = Label(self.create_box, bg=self.bg, text="--")
        self.follow3_text = Entry(self.create_box, textvariable=StringVar(), font=("Helvetica", 10), width=45)
        self.follow3_id = ttk.Combobox(self.create_box, textvariable=StringVar(), width=50)
        self.follow_creation_info4 = Label(self.create_box, bg=self.bg, text="--")
        self.follow4_text = Entry(self.create_box, textvariable=StringVar(), font=("Helvetica", 10), width=45)
        self.follow4_id = ttk.Combobox(self.create_box, textvariable=StringVar(), width=50)
        self.creation_button = Button(self.create_box, text="Create Line", command=self.creation_line, width=30, height=1)

        # initializing stuff to choose dialogue
        self.choose_box = Frame(self.window, bg=self.bg)
        self.select_cbbox = ttk.Combobox(self.choose_box, textvariable=StringVar())
        self.update_cbbox()
        self.select_cbbox.bind('<<ComboboxSelected>>', self.transition_select_to_read)
        self.select_text_info = Label(self.choose_box, text="Use this to choose a dialogue", font=("Consolas", 15), bg=self.bg)

        # initializing stuff for dialogue
        self.dialogue_box = Frame(self.window, bg=self.bg)
        self.main_text = Label(self.dialogue_box, text="hehehe", font=("Consolas", 15), bg=self.bg)

        self.button_box = Frame(self.dialogue_box, bg=self.bg)
        self.buttons = []
        for i in range(4):
            new_button = Button(self.button_box, text=str(i), command=partial(self.button_click, i), width=50, height=3)
            self.buttons.append(new_button)

        self.current_script = None
        self.loaded_follows = []

    def init_pack(self):
        self.go_choose_button.grid(column=1, row=0, sticky=NE)
        self.go_create_button.grid(column=0, row=0, sticky=NW)
        self.main_text.pack(pady=40)
        for i in range(len(self.buttons)):
            self.buttons[i].grid(column=i % 2, row=i // 2)
        self.button_box.pack()

        self.select_text_info.pack(pady=20)
        self.select_cbbox.pack()

        self.creation_box_pack()
        
        self.del_cbbox.pack()
        self.del_button.pack()

    def creation_box_pack(self):
        self.script_creation_info.grid(column=0, row=0, sticky=E, pady=1.5)
        self.new_line_script_cbbox.grid(column=1, row=0, pady=1.5)
        self.script_creation_tip.grid(column=0, row=1, sticky=E, columnspan=2, pady=1.5)

        self.title_creation_info.grid(column=0, row=2, sticky=E, pady=1.5)
        self.new_line_title.grid(column=1, row=2, pady=1.5)

        self.text_creation_info.grid(column=0, row=3, sticky=E, pady=1.5)
        self.new_line_text.grid(column=1, row=3, pady=1.5)

        self.img_creation_info.grid(column=0, row=4, sticky=E, pady=1.5)
        self.img1_character.grid(column=1, row=4, pady=1.5)
        self.img1_action.grid(column=1, row=5, pady=1.5)
        self.img_creation_info2.grid(column=0, row=6, sticky=E, pady=1.5)
        self.img2_character.grid(column=1, row=6, pady=1.5)
        self.img2_action.grid(column=1, row=7, pady=1.5)

        self.follow_creation_info.grid(column=0, row=8, sticky=E, pady=1.5)
        self.follow1_text.grid(column=1, row=8, pady=1.5)
        self.follow1_id.grid(column=1, row=9, pady=1.5)
        self.follow_creation_info2.grid(column=0, row=10, sticky=E, pady=1.5)
        self.follow2_text.grid(column=1, row=10, pady=1.5)
        self.follow2_id.grid(column=1, row=11, pady=1.5)
        self.follow_creation_info3.grid(column=0, row=12, sticky=E, pady=1.5)
        self.follow3_text.grid(column=1, row=12, pady=1.5)
        self.follow3_id.grid(column=1, row=13, pady=1.5)
        self.follow_creation_info4.grid(column=0, row=14, sticky=E, pady=1.5)
        self.follow4_text.grid(column=1, row=14, pady=1.5)
        self.follow4_id.grid(column=1, row=15, pady=1.5)

        self.creation_button.grid(column=1, row=16, pady=3, columnspan=2)

    def button_click(self, id_button):
        self.current_script.follow_up(id_button)
        self.update()
        return id_button

    def update(self):
        self.load_follows()
        self.unpack_buttons()
        self.main_text.config(
            text=self.get_current_line().get_title() + " says: " + self.get_current_line().get_text())
        for i in self.loaded_follows:
            index = self.loaded_follows.index(i)
            self.buttons[index].grid(column=index % 2, row=index // 2)
            self.buttons[index].config(text=i[0])

    def load_script(self, script):
        assert type(script) == Script, "tried to load " + str(type(script)) + " instead of script"
        self.current_script = script

    def load_follows(self):
        self.loaded_follows = self.get_current_line().get_all_follows()
        if len(self.loaded_follows) < 1:
            self.loaded_follows = [("", self.get_current_line().get_id() + 1)]

    def update_cbbox(self):
        ans = []
        for i in get_all_scripts():
            ans.append(i[1])
        self.select_cbbox["values"] = ans
        self.select_cbbox.config(textvariable=StringVar())

    def update_creation_box(self):
        self.new_line_script_cbbox["values"] = [i[1] for i in get_all_scripts()]
        self.new_line_script_cbbox.config(textvariable=StringVar())

        self.new_line_title.config(textvariable=StringVar())

        self.new_line_text.config(textvariable=StringVar())

        #self.img1_character
        self.img1_action["values"] = ["idle", "angry", "surpised", "chocked"]
        #self.img2_character
        self.img2_action["values"] = ["idle", "angry", "surpised", "chocked"]

        self.follow1_text.config(textvariable=StringVar())
        self.follow1_id.config(textvariable=StringVar())
        self.follow1_id["values"] = [read_line(i[0]) for i in get_all_lines(0)]
        self.follow2_text.config(textvariable=StringVar())
        self.follow2_id.config(textvariable=StringVar())
        self.follow2_id["values"] = [read_line(i[0]) for i in get_all_lines(0)]
        self.follow3_text.config(textvariable=StringVar())
        self.follow3_id.config(textvariable=StringVar())
        self.follow3_id["values"] = [read_line(i[0]) for i in get_all_lines(0)]
        self.follow4_text.config(textvariable=StringVar())
        self.follow4_id.config(textvariable=StringVar())
        self.follow4_id["values"] = [read_line(i[0]) for i in get_all_lines(0)]

    def creation_line(self):
        try:
            id_script = get_script_by_name(self.new_line_script_cbbox.get())[0]
        except:
            id_script = create_script(self.new_line_script_cbbox.get())
        text = self.new_line_text.get()
        title = self.new_line_title.get()
        images = (self.img1_character.get() + "." + self.img1_action.get(),
                  self.img2_character.get() + "." + self.img2_action.get())
        follows = [(self.follow1_text.get(), self.follow1_id.get()),
                   (self.follow2_text.get(), self.follow2_id.get()),
                   (self.follow3_text.get(), self.follow3_id.get()),
                   (self.follow4_text.get(), self.follow4_id.get())]
        for i in range(len(follows)):
            try:
                i = int(follows[i][1])
                i += 1
            except:
                if len(follows[i][1]) > 3:
                    if follows[i][1][0] == "[" and follows[i][1][2] == "]":
                        follows[i] = (follows[i][0], follows[i][1][1])
        add_line(id_script, text, title, images, follows)
        self.show_select()

    def delete_line(self):
        to_delete = self.del_cbbox.get()
        if len(to_delete) > 3:
            if to_delete[0] == "[" and to_delete[2] == "]":
                to_delete = to_delete[1]
        try:
            int(to_delete)
        except:
            pass
        else:
            delete_line(to_delete)

    def get_current_line(self):
        return self.current_script.current

    def unpack_buttons(self):
        for i in self.buttons:
            i.grid_forget()

    def show_dialogue(self):
        self.choose_box.grid_forget()
        self.create_box.grid_forget()
        self.delete_box.grid_forget()
        self.go_delete_button.grid_forget()

        self.dialogue_box.grid(column=0, row=1, columnspan=2)

        self.update()

        self.go_choose_button.grid(column=1, row=0, sticky=NE)
        self.go_create_button.grid(column=0, row=0, sticky=NW)

    def show_select(self):
        self.go_choose_button.grid_forget()
        self.dialogue_box.grid_forget()
        self.create_box.grid_forget()
        self.delete_box.grid_forget()
        self.go_delete_button.grid_forget()

        self.update_cbbox()

        self.choose_box.grid(column=0, row=1, columnspan=2)

        self.go_create_button.grid(column=0, row=0, sticky=NW)

    def show_create(self):
        self.go_create_button.grid_forget()
        self.dialogue_box.grid_forget()
        self.choose_box.grid_forget()
        self.delete_box.grid_forget()

        self.create_box.grid(column=0, row=1, columnspan=2)

        self.go_choose_button.grid(column=1, row=0, sticky=NE)
        self.go_delete_button.grid(column=0, row=0, sticky=NW)

        self.update_creation_box()
        
    def show_delete(self):
        self.choose_box.grid_forget()
        self.create_box.grid_forget()
        self.dialogue_box.grid_forget()
        self.go_delete_button.grid_forget()

        self.delete_box.grid(column=0, row=1, columnspan=2)

        self.go_choose_button.grid(column=1, row=0, sticky=NE)
        self.go_create_button.grid(column=0, row=0, sticky=NW)

        self.del_cbbox["values"] = [read_line(i[0]) for i in get_all_lines(0)]

    def transition_select_to_read(self, event):
        new_script_id = get_script_by_name(self.select_cbbox.get())[0]
        self.load_script(convert_script(new_script_id))
        self.show_dialogue()

    def mainloop(self):
        self.init_pack()
        self.show_select()
        self.window.mainloop()
