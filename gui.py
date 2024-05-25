import tkinter as tk
from tkinter import messagebox
from database import Database
from timer import Timer
import time

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación Pomodoro")
        self.db = Database()
        self.timer = Timer()
        self.task_id = None
        self.start_time = None
        self.create_widgets()

    def create_widgets(self):
        self.task_label = tk.Label(self.root, text="Tarea actual:")
        self.task_label.pack()

        self.task_entry = tk.Entry(self.root)
        self.task_entry.pack()

        self.start_button = tk.Button(self.root, text="Iniciar tarea", command=self.start_task)
        self.start_button.pack()

        self.stop_button = tk.Button(self.root, text="Detener tarea", command=self.stop_task)
        self.stop_button.pack()

        self.timer_label = tk.Label(self.root, text="00:00:00")
        self.timer_label.pack()

        self.history_button = tk.Button(self.root, text="Mostrar historial", command=self.show_history)
        self.history_button.pack()

        self.efficiency_label = tk.Label(self.root, text="Eficiencia: 0%")
        self.efficiency_label.pack()

        self.reminder_button = tk.Button(self.root, text="Recordatorio", command=self.remind)
        self.reminder_button.pack()

    def start_task(self):
        task_name = self.task_entry.get()
        if task_name:
            self.task_id = self.db.add_task(task_name)
            self.start_time = time.time()
            self.update_timer()
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingrese el nombre de la tarea.")

    def stop_task(self):
        if self.task_id and self.start_time:
            end_time = time.time()
            duration = int(end_time - self.start_time)
            self.db.update_task(self.task_id, duration)
            self.reset_timer()
            self.task_id = None
            self.start_time = None
        else:
            messagebox.showwarning("Advertencia", "No hay tarea en curso.")

    def update_timer(self):
        if self.start_time:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=self.timer.format_time(elapsed_time))
            self.root.after(1000, self.update_timer)

    def reset_timer(self):
        self.timer_label.config(text="00:00:00")

    def show_history(self):
        history = self.db.get_history()
        history_window = tk.Toplevel(self.root)
        history_window.title("Historial de Tareas")
        for row in history:
            task_info = f"Tarea: {row[1]}, Iniciada: {row[2]}, Finalizada: {row[3]}, Duración: {self.timer.format_time(row[4])}"
            tk.Label(history_window, text=task_info).pack()

    def remind(self):
        if self.task_id:
            messagebox.showinfo("Recordatorio", "¿Estás trabajando en la tarea actual?")
        else:
            messagebox.showinfo("Recordatorio", "No hay tarea en curso.")
