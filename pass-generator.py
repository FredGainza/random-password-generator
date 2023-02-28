#!/usr/bin/env python
# coding: utf-8
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import messagebox
from tkinter import StringVar
from tkinter import Frame
import string
import random
import base64
import os
import pyperclip
from functions import get_ico, dic_lang

# Language by default
dic = dic_lang("english")

# get ico_file encoded in Base64 (for ico in tkinter window)
ICON = get_ico()
icondata = base64.b64decode(ICON)
## The temp file is icon.ico
TEMPFILE = "icon.ico"
iconfile = open(TEMPFILE, "wb")
## Extract the icon
iconfile.write(icondata)
iconfile.close()

## Possible options for the password
LOWERCASE = list(string.ascii_lowercase)
UPPERCASE = list(string.ascii_uppercase)
NUMBER = list(string.digits)
SYMBOLS = ["@", "#", "$", "%", "&", "_"]
LIST_DATA = [LOWERCASE, UPPERCASE, NUMBER, SYMBOLS]


####################################################
#  START - Fonction to generate random password
####################################################


def reset_form():
    """Form initialization"""
    pass_input.delete(0, tk.END)
    nb.delete(0, tk.END)
    nb.insert(0, 12)
    for c in checks_values:
        c.delete(0, tk.END)


def get_lang():
    """Language change"""
    dico = dic_lang(lang.get())
    # form data
    global_title.config(text=dico["form"]["global_title"])
    label_nb.config(text=dico["form"]["nb_characters"])
    checkboxs_label[0].config(text=dico["form"]["cond1"])
    checkboxs_label[1].config(text=dico["form"]["cond2"])
    checkboxs_label[2].config(text=dico["form"]["cond3"])
    checkboxs_label[3].config(text=dico["form"]["cond4"])
    submit.config(text=dico["form"]["submit"])


def valid_num(str_):
    """Validate data entered by the user"""
    str_ = str_.replace(" ", "")
    lstr_ = list(str_)
    if "-" in str_:
        if lstr_.count("-") == 1:
            ar = str_.split("-")
            ar = [x for x in ar if x != ""]
            for c in ar:
                if c.isdigit():
                    continue
                else:
                    return False

            if len(ar) == 2:
                if int(ar[1]) > int(ar[0]):
                    return True
            else:
                return True
    else:
        if str_.isdigit():
            return True
        else:
            return False
    return False


def get_pass_min(nb):
    """Generate the password that satisfies the character conditions"""
    conditions = [cond1, cond2, cond3, cond4]
    min_pass = ""
    for i, c in enumerate(conditions):
        rg = 0
        if c.get() == 1:
            v = checks_values[i].get()
            v = v.replace(" ", "")
            if v != "":
                if valid_num(v):
                    if v.isdigit():
                        rg = int(v)
                    else:
                        if v.endswith("-"):
                            rg = int(v[:-1])
                        elif "-" in v and v.startswith("-") is not True:
                            rg = int(v.split("-")[0])
                else:
                    return False

        if rg != 0:
            for j in range(int(rg)):
                min_pass += LIST_DATA[i][random.randint(0, len(LIST_DATA[i]) - 1)]

    if len(list(min_pass)) <= nb:
        return min_pass
    else:
        return False


dico_max = {}
def test_car(c, p, dico_max=dico_max):
    """Test for additional characters 
    (if the number of characters in the desired password 
    is greater than the sum of the characters that meet 
    the character requirements)"""
    for k, v in dico_max.items():
        lk = LIST_DATA[k]

        if c in lk:
            nb_pass = 0
            for pp in list(p):
                if pp in lk:
                    nb_pass += 1

            if nb_pass >= v:
                return False
    return True


def main():
    """Generate the random password"""
    data = []
    password = ""

    ## dict error messages
    dic_msg = dic_lang("english")["messages"] if lang.get() == "english" else dic_lang("français")["messages"]

    # Selected options for the password
    conditions = [cond1, cond2, cond3, cond4]

    nb_car_str = nb.get()

    if nb_car_str != "":
        if nb_car_str.isdigit():
            nb_car = int(nb_car_str)
            if 5 <= nb_car <= 50:
                password = get_pass_min(nb_car)

                if password is not False:
                    for i, c in enumerate(conditions):
                        max_ = None
                        if c.get() == 1:

                            ## check if some values are indicated
                            v = checks_values[i].get()
                            v = v.replace(" ", "")
                            if v != "" and "-" in v:
                                lv = list(v)
                                if lv[0] == "-":
                                    max_ = int("".join(lv[1:]))
                                elif lv[-1] != "-":
                                    ar = v.split("-")
                                    max_ = int(ar[1])

                                if max_ is not None:
                                    data.extend(LIST_DATA[i])
                                    dico_max[i] = max_

                            if v == "" or v.endswith("-"):
                                data.extend(LIST_DATA[i])

                    if len(data) != 0:
                        # number of characters remaining
                        nb_shuffle = nb_car - len(list(password))

                        def car_temp():
                            return data[random.randint(0, len(data) - 1)]

                        for j in range(nb_shuffle):
                            car_t = data[random.randint(0, len(data) - 1)]
                            while test_car(car_t, password) is not True:
                                car_t = car_temp()
                            password += car_t

                    l_pass = list(password)
                    random.shuffle(l_pass)
                    password = "".join(l_pass)

                    pass_input.delete(0, tk.END)
                    pass_input.insert(0, password)
                    pyperclip.copy(password)

                else:
                    reset_form()
                    messagebox.showerror(
                        "Error Password", dic_msg["msg_cond_fail"]
                    )
            else:
                reset_form()
                messagebox.showerror(
                    "Error Password Length", dic_msg["msg_pass_lenght"]
                )
        else:
            reset_form()
            messagebox.showerror("Error Password Format", dic_msg["msg_pass_format"])
    else:
        reset_form()
        messagebox.showerror("Error Password Empty", dic_msg["msg_pass_empty"])


####################################################
#  END - Fonction to generate random password
####################################################


def instructions():
    """Generate the help page"""

    # dict help page
    dic_help = dic_lang("english")["help"] if lang.get() == "english" else dic_lang("français")["help"]

    inst = tk.Tk()
    inst.title(dic_help["help_title_page"])
    inst.geometry("600x400")

    help_title = tk.Label(inst, text=dic_help["help_title"])
    help_title.pack(anchor="center", pady=(20, 5))
    font_help_title = ("Helvetica", 16, "bold")
    help_title.configure(font=font_help_title)

    canvas = tk.Canvas(inst, width=600, height=15)
    canvas.create_line(10, 5, 590, 5, fill="black")
    canvas.pack()

    help_step1 = tk.Label(
        inst,
        text=dic_help["help_step1"],
    )
    help_step1.pack(anchor="w", padx=(20, 10), pady=(10, 5))
    font_help_step1 = ("Source Sans Pro", 11, "bold")
    help_step1.configure(font=font_help_step1)

    help_step2 = tk.Label(
        inst,
        text=dic_help["help_step2"],
    )
    help_step2.pack(anchor="w", padx=(20, 10), pady=(5, 2))
    font_help_step2 = ("Source Sans Pro", 11, "bold")
    help_step2.configure(font=font_help_step2)

    help_ex_step2 = tk.Label(inst, text=dic_help["text_ex_step2"], justify="left")
    help_ex_step2.pack(anchor="w", padx=(45, 10), pady=(2, 5))
    font_help_ex_step2 = ("Source Sans Pro", 11)
    help_ex_step2.configure(font=font_help_ex_step2)

    help_step3 = tk.Label(inst, text=dic_help["help_step3"])
    help_step3.pack(anchor="w", padx=(20, 10), pady=(5, 10))
    font_help_step3 = ("Source Sans Pro", 11, "bold")
    help_step3.configure(font=font_help_step3)

    help_step4 = tk.Label(
        inst,
        text=dic_help["help_step4"],
        justify="left",
    )
    help_step4.pack(anchor="w", padx=(20, 10), pady=(10, 10))
    font_help_step4 = ("Source Sans Pro", 11)
    help_step4.configure(font=font_help_step4)


## Window settings
root = tk.Tk()
root.title("Pass-Generator")
root.config(bg="#07566e")
root.iconbitmap(TEMPFILE)
root.geometry("400x570")
root.maxsize(400, 570)
root.minsize(400, 570)

## Delete the TEMPFILE
os.remove(TEMPFILE)

## Fonts
helv10 = tkFont.Font(family="Source Sans Pro", size=10, weight="normal")
helv10_bold = tkFont.Font(family="Source Sans Pro", size=10, weight="bold")
helv12 = tkFont.Font(family="Source Sans Pro", size=12, weight="normal")
helv12_bold = tkFont.Font(family="Source Sans Pro", size=12, weight="bold")
helv14 = tkFont.Font(family="Source Sans Pro", size=14, weight="normal")
helv16_bold = tkFont.Font(family="Helvetica", size=16, weight="bold")

## Title
global_title = tk.Label(
    root,
    text=dic["form"]["global_title"],
    font=helv16_bold,
    fg="#14181a",
    pady=16,
    bg="#468ea4",
    activebackground="#468ea4",
)
global_title.pack(fill="x")

## Frame on the top (select language and help button)
top_frame_left = Frame(width="350", bg="#022c3b")
top_frame_left.pack(fill="x")

## Change language
lang = StringVar()
lang.set("english")
lang_values = ["français", "english"]

for i in range(2):
    x = tk.Radiobutton(
        top_frame_left,
        text=lang_values[i],
        value=lang_values[i],
        anchor="w",
        font=helv10,
        variable=lang,
        fg="white",
        bg="#022c3b",
        activebackground="#022c3b",
        selectcolor="#1f3038",
        command=get_lang,
    )
    if i == 0:
        x.pack(anchor="w", side="left", padx=(25, 10), pady=(3, 3))
    else:
        x.pack(anchor="w", padx=(0, 100), pady=(3, 3))

## Help button
button = tk.Button(
    root, text="?", width=2, height=1, relief="flat", command=instructions
)
button.place(x="365", y="63")

## Number of characters - label
label_nb = tk.Label(
    root,
    text=dic["form"]["nb_characters"],
    font=helv12,
    fg="White",
    bg="#07566e",
    activebackground="#07566e",
)
label_nb.pack(anchor="w", padx=(30, 10), pady=(15, 0))

## Number of characters - default value
nb_default = tk.StringVar(root)
nb_default.set(12)

ttk.Style().configure("nb.TSpinbox", padding="10 1 1 0")
nb = ttk.Spinbox(
    root, font=helv12, from_=5, to=50, textvariable=nb_default, style="nb.TSpinbox"
)
nb.pack(anchor="w", padx=(33, 250), pady=(5, 20))

## Checkboxese
cond1 = tk.IntVar(value=1)
cond2 = tk.IntVar(value=1)
cond3 = tk.IntVar(value=1)
cond4 = tk.IntVar(value=0)

checks = [cond1, cond2, cond3, cond4]
checks_text = []
for i in range(4):
    checks_text.append(dic["form"]["cond"+str(i+1)])
checks_values = []
checkboxs_label = []

for i in range(4):
    z = tk.Checkbutton(
        root,
        text=checks_text[i],
        anchor="w",
        font=helv12,
        onvalue=1,
        offvalue=0,
        variable=checks[i],
        fg="white",
        bg="#07566e",
        activebackground="#07566e",
        selectcolor="#0c232d",
    )
    checkboxs_label.append(z)

    # Checkbox
    z.pack(anchor="w", pady=(5, 0), padx=(30, 60), side="top")

    # Input box
    zz = tk.Entry(root, font=helv10_bold, bg="#d6e3e5")
    checks_values.append(zz)
    zz.pack(anchor="w", side="top", pady=(0, 5), padx=(55, 280))

## Submit button
submit = tk.Button(
    root,
    text=dic['form']['submit'],
    font=helv12,
    bg="#022a3b",
    fg="White",
    activebackground="#07566e",
    width=50,
    relief="groove",
    command=main,
)
submit.pack(padx=25, pady=(30, 5))

ttk.Style().configure("pass.TEntry", padding="10 1 1 0", foreground="darkred")
pass_input = ttk.Entry(font=helv12_bold, style="pass.TEntry")
pass_input.pack(pady=15, padx=25, fill="x")
# pyinstaller --icon=exe.ico -F --noconsole pass-generator.py

root.mainloop()
