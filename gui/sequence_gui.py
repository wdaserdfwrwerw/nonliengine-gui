import tkinter as tk
from tkinter import ttk, messagebox, Canvas, Entry
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re

SAMPLE_INTERACTIONS = ["중력(지구→물체)", "굽힘(보)", "비틀림(축)"]
SAMPLE_GRAPH_EDGES = [("A", "B"), ("B", "C"), ("A", "D")]

class SafeLogicEngineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("논리엔진 시뮬레이터 (Safe Version)")
        self.root.geometry("1000x600")
        self.build_gui()

    def build_gui(self):
        # 상단 프레임: 시퀀스 다이어그램 영역
        top_frame = tk.Frame(self.root, bg="white", height=250)
        top_frame.pack(fill="x")

        tk.Label(top_frame, text="시퀀스 입력 (예: 중력(지구→물체))", bg="white").pack()
        self.seq_entry = tk.Entry(top_frame, width=80)
        self.seq_entry.pack()
        tk.Button(top_frame, text="다이어그램 생성", command=self.draw_sequence_diagram).pack(pady=5)

        # 중앙 프레임: 네트워크 시각화
        self.canvas_frame = tk.Frame(self.root, bg="lightgray", height=300)
        self.canvas_frame.pack(fill="both", expand=True)

        # 하단 프레임: 가중치 수동 조정
        bottom_frame = tk.Frame(self.root, bg="#ecf0f1", height=100)
        bottom_frame.pack(fill="x")

        tk.Label(bottom_frame, text="강화학습 수동 조정 (Demo)", bg="#ecf0f1").pack()
        self.selected_var = tk.StringVar(value="A → B")
        ttk.Combobox(bottom_frame, textvariable=self.selected_var, values=[
            "A → B", "B → C", "A → D"
        ]).pack()
        tk.Button(bottom_frame, text="+ 강화", command=self.increase_weight).pack(side="left", padx=10)
        tk.Button(bottom_frame, text="- 약화", command=self.decrease_weight).pack(side="left")

    def draw_sequence_diagram(self):
        raw_input = self.seq_entry.get().strip()
        if not raw_input or "(" not in raw_input:
            messagebox.showwarning("입력 오류", "예: 중력(지구→물체) 형식으로 입력하세요.")
            return

        try:
            interaction_name = raw_input.split("(")[0]
            objects = raw_input.split("(")[1].replace(")", "")
            if "→" in objects:
                sender, receiver = objects.split("→")
            else:
                sender = receiver = objects
        except:
            messagebox.showerror("형식 오류", "입력 형식이 잘못되었습니다.")
            return

        # 시퀀스 다이어그램 스타일로 표시
        fig, ax = plt.subplots(figsize=(6, 2))
        ax.set_xlim(0, 3)
        ax.set_ylim(0, 2)
        ax.axis("off")

        # 객체 생명선
        ax.plot([0.5, 0.5], [1.8, 0.2], linestyle='--', color='gray')
        ax.plot([2.5, 2.5], [1.8, 0.2], linestyle='--', color='gray')
        ax.text(0.5, 1.9, sender.strip(), ha='center', fontsize=12, bbox=dict(facecolor='white', edgecolor='black'))
        ax.text(2.5, 1.9, receiver.strip(), ha='center', fontsize=12, bbox=dict(facecolor='white', edgecolor='black'))

        # 상호작용 메시지 (세로 화살표)
        ax.annotate(interaction_name.strip(),
                    xy=(2.5, 1.0), xytext=(0.5, 1.0),
                    arrowprops=dict(arrowstyle="->", lw=2),
                    ha='center', va='center', fontsize=12, color='blue')

        # 기존 캔버스 제거
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()

    def increase_weight(self):
        messagebox.showinfo("가중치 강화", f"{self.selected_var.get()} 경로 강화됨 (Demo Only)")

    def decrease_weight(self):
        messagebox.showinfo("가중치 약화", f"{self.selected_var.get()} 경로 약화됨 (Demo Only)")
