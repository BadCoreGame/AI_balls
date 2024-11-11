# Import module
import tkinter as tk
from tkinter import Tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import torch
import numpy as np
import os

# Create object
root = Tk()
root.bind("<Escape>", lambda e: root.quit())
root.title("Распознавание изображений используя YOLOv5")

# Установить размеры окна
root.geometry("800x600")  # You can change this to any desired size
root.resizable(True, True)  # Разрешает изменение окна

# Загрузить YOLOv5 модель с верификацией
try:
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    print("YOLOv5 модель загружена успешно.")
except Exception as e:
    print("Ошибка загрузки YOLOv5 модели:", e)

def main_page():
    def upload_vid_func():
        def browse_file():
            def run_yolov5_on_video():
                 def go_back_to_main_frame():
                    cap.release()
                    display_frame1.place_forget()
                    display_frame2.place_forget()
                    back_frame.place_forget()
                    main_frame.place(relx=0.5, rely=0.5, width = 500, height = 500, anchor=tk.CENTER)
                 
                 browse_frame.place_forget()
                 width, height = 700, 700
                #  print(file_path)
                 cap = cv2.VideoCapture(file_path)
                 cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                 cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

                 display_frame1 = tk.Frame(root)
                 display_frame1.place(relx=0.2, rely=0.5, width = 600, height = 700, anchor=tk.CENTER)

                 display_frame1_label = tk.Label(display_frame1, text = "Оригинал", font = ('Arial', 16), bg = "yellow")
                 display_frame1_label.pack(side=tk.TOP)

                 display_frame2 = tk.Frame(root)
                 display_frame2.place(relx=0.8, rely=0.5, width = 600, height = 700, anchor=tk.CENTER)

                 display_frame2_label = tk.Label(display_frame2, text = "Обнаружение", font = ('Arial', 16), bg = "yellow")
                 display_frame2_label.pack(side=tk.TOP)

                 back_frame = tk.Frame(root)
                 back_frame.pack(side=tk.TOP, anchor=tk.NW)
                 back_button = tk.Button(back_frame, text= "BACK", font=("Rockwell", 12), command=go_back_to_main_frame)
                 back_button.pack()


                 lmain = tk.Label(display_frame1)
                 lmain1 = tk.Label(display_frame2)
                 lmain.place(x = 0, y = 100, width=600, height=600)
                 lmain1.place(x = 0, y = 100, width=600, height=600)
        
                 def show_frame():
                    
                    _, frame = cap.read()
                    # frame2 = cv2.flip(frame, 1)
                    frame2 = frame
                    cv2image = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGBA)
                    img = Image.fromarray(cv2image)

                    imgtk = ImageTk.PhotoImage(image=img)
                    lmain.imgtk = imgtk
                    lmain.configure(image=imgtk)
                    
                    # Perform inference
                    results = model(frame)

                    # Parse results and draw bounding boxes
                    for *xyxy, conf, cls in results.xyxy[0]:
                        if conf>0.5:
                            label = f'{model.names[int(cls)]} {conf:.2f}'
                            cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (255,0,0), 2)
                            cv2.putText(frame, label, (int(xyxy[0]), int(xyxy[1])-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)

                    # frame3 = cv2.flip(frame, 1)
                    frame3 = frame
                    cv2image2 = cv2.cvtColor(frame3, cv2.COLOR_BGR2RGBA)
                    img2 = Image.fromarray(cv2image2)

                    imgtk2 = ImageTk.PhotoImage(image=img2)

                    lmain1.imgtk = imgtk2
                    lmain1.configure(image=imgtk2)
                
                    lmain.after(1, show_frame)
                
                 show_frame()

            filename = filedialog.askopenfilename(filetypes=[("video files", "*.*")])
            file_path = os.path.abspath(filename)

            run_yolov5_on_video()
        
        main_frame.place_forget()

        browse_frame = tk.Frame(root, bg = "orange")
        browse_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        browse_button = tk.Button(browse_frame, text="Browse", font= ("Arial", 20), bg="Yellow", fg="white", command=browse_file)
        browse_button.pack()

    main_frame = tk.Frame(root, bg="orange")

    main_frame.place(relx=0.5, rely=0.5, width = 500, height = 500, anchor=tk.CENTER)
    
    
    upload_vid = tk.Button(main_frame, text = "Загрузить файл", command = upload_vid_func, bg = "yellow", fg = "purple", font=('Arial', 18))
    
    upload_vid.place(x = 180, y = 100)

main_page()

Title_label = tk.Label(root, text = "YOLOv5 Object detection", font = ('Arial', 20), bg = "yellow")
Title_label.pack(side=tk.TOP)

IsBowling_label = tk.Label(root, text = "аавыаыв", font = ('Arial', 20), bg = "yellow")
IsBowling_label.pack(side=tk.BOTTOM)

# Execute tkinter
root.mainloop()