from customtkinter import *
import socket
import threading
import os

CONN = "7.tcp.eu.ngrok.io"
PORT = 10858

cs = None


WIDTH, HEIGHT = 400, 400

window = CTk()
window.configure(fg_color="#8A5C32")
window.geometry(f"{WIDTH}x{HEIGHT}")

name_label = None
name_entry = None
button_conect = None

def conect_server():
    global cs
    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cs.connect((CONN, PORT))
    name = name_entry.get()
    cs.send(name.encode())

menu_select = False
def open_menu():
    global menu_select, name_label, name_entry, button_conect, cs
    if side_frame.winfo_width() <= 130 and not menu_select:
        side_frame.configure(width = side_frame.winfo_width() + 20)
        if side_frame.winfo_width() == 130:
            name_label = CTkLabel(side_frame, text="Ім'я", width=120, height=35, fg_color="#FFF8CE", text_color="#5C3B1D")
            name_label.place(x=10, y=130)  
            name_entry = CTkEntry(side_frame, width=120, fg_color="#FFF8CE", text_color="#5C3B1D")
            name_entry.place(x=10, y=160)
            button_conect= CTkButton(side_frame, text="увійти",width = 120, height=35, fg_color="#E4DDB6", text_color="#5C3B1D", hover_color="#FFEAC3", corner_radius=10, command=conect_server)
            button_conect.place(x=10, y=200)
            op_menu_btn.configure(text= "<-")
            
            menu_select = True
            return
        window.after(50, open_menu)
    if side_frame.winfo_width() >= 50 and menu_select:
        side_frame.configure(width=side_frame.winfo_width() - 20)
        if side_frame.winfo_width() == 50:
            name_label.destroy()
            name_entry.destroy()
            button_conect.destroy()
            name_label = None
            name_entry = None
            button_conect = None
            op_menu_btn.configure(text= "->")
            menu_select = False
            return
        window.after(50, open_menu)

def send_message(event = None):
    print(1)
    text = msg_entry.get().strip()
    if text:
        cs.send(text.encode())
        max_width = int(chat_frame.winfo_width() * 0.6) if chat_frame.winfo_width()> 50 else 180
        msg_label = CTkLabel(chat_frame, text= text, padx= 10, pady=5, wraplength=max_width, justify= "left", fg_color = "#E2A76F")
        msg_label.pack(anchor="e",padx=5, pady=10)
        msg_entry.delete(0,END)
        chat_frame._parent_canvas.yview_moveto(1.0)


def res_msg():
    while True:
        try:
            print(2)
            data = cs.recv(1024).decode()
            if data:
                print(data)
                max_width = int(chat_frame.winfo_width() * 0.6) if chat_frame.winfo_width()> 50 else 180
                msg_label = CTkLabel(chat_frame, text= data, padx= 10, pady=5, wraplength=max_width,
                                      justify= "right", fg_color = "#C09975")
                msg_label.pack(anchor="e",padx=5, pady=10)
                msg_entry.delete(0,END)
                chat_frame._parent_canvas.yview_moveto(1.0)
            else:
                print("\nЗ'єднання з сервером розірвано.")
        except:
            pass

threading.Thread(target=res_msg).start()


side_frame = CTkFrame(window, width=30, height= HEIGHT, fg_color="#AA784F", corner_radius=0)
side_frame.place(x=0, y=30) 
btn_2 = CTkLabel(window, text="ToTalk", fg_color="#FDF5E6", text_color="#5C3B1D", font=("Arial Narrow", 15), width= 400, height=30)
btn_2.place(x=0, y= 0)
op_menu_btn = CTkButton(side_frame, text="->", width=35, height=35, fg_color="#E4DDB6", text_color="#5C3B1D", corner_radius=10, command=open_menu)
op_menu_btn.place(x=0, y=0)
btn = CTkButton(window, text="Надіслати", fg_color="#FDF5E6", text_color="#5C3B1D", hover_color="#FFEAC3", font=("Arial Narrow", 15), width=30, height=30, command= send_message)
btn.place(x=100, y=10)
msg_entry = CTkEntry(window, height=30, placeholder_text="Введіть повідомлення")
msg_entry.place(x=3838, y=34)
msg_entry.bind("<Return>", send_message)
chat_frame= CTkScrollableFrame(window)
def adaptive_ui():
    side_frame.configure(height=window.winfo_height())
    chat_frame.configure(width= window.winfo_width()- side_frame.winfo_width()- 20, height=window.winfo_height() - 65)
    chat_frame.place(x=side_frame.winfo_width() + 10, y = 10)
    msg_entry.configure(width=window.winfo_width()- side_frame.winfo_width()- btn.winfo_width())
    msg_entry.place(x=side_frame.winfo_width() + 10, y=window.winfo_height() - 40)
    btn.place(x=msg_entry.winfo_x()+ msg_entry.winfo_width() + 10, y=window.winfo_height() - 40)
    window.after(50,adaptive_ui)
adaptive_ui()

window.mainloop()
cs.close()