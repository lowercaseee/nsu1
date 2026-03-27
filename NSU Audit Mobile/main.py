from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
import os
import json
from datetime import datetime
from pathlib import Path

Window.size = (400, 700)
Window.softinput_mode = 'below_target'

NSU_BLUE = "#1a365d"
NSU_GOLD = "#d69e2e"
NSU_LIGHT_BLUE = "#2b6cb0"

GRADE_POINTS = {'A+': 4.0, 'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7, 'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D': 1.0, 'F': 0.0}

HISTORY_FILE = Path.home() / ".nsu-audit" / "mobile_history.json"

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_ui()
    
    def init_ui(self):
        main_layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        
        with main_layout.canvas.before:
            Color(*get_color_from_hex(NSU_BLUE))
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        
        main_layout.add_widget(Label(text="", size_hint_y=0.15))
        
        logo_layout = BoxLayout(orientation='vertical', size_hint_y=0.35, spacing=10)
        logo_layout.add_widget(Label(text="[color=#d69e2e][b]NSU[/b][/color][color=#ffffff] Audit Core[/color]", 
                                     markup=True, font_size='32sp', halign='center'))
        logo_layout.add_widget(Label(text="Student Graduation\nEligibility Checker", 
                                    font_size='14sp', color=(1,1,1,0.8), halign='center'))
        main_layout.add_widget(logo_layout)
        
        main_layout.add_widget(Label(text="", size_hint_y=0.1))
        
        login_btn = Button(text="Sign in with Google", 
                         background_color=get_color_from_hex(NSU_GOLD),
                         color=(0,0,0,1), font_size='16sp', 
                         size_hint_y=0.08, halign='center')
        login_btn.bind(on_press=self.do_login)
        main_layout.add_widget(login_btn)
        
        main_layout.add_widget(Label(text="", size_hint_y=0.15))
        
        footer = Label(text="Secure login using\n@northsouth.edu credentials", 
                      font_size='11sp', color=(1,1,1,0.5), halign='center')
        main_layout.add_widget(footer)
        
        self.add_widget(main_layout)
    
    def do_login(self, instance):
        self.save_login_history()
        self.manager.get_screen('dashboard').load_data()
        self.manager.current = 'dashboard'
    
    def save_login_history(self):
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        history = []
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, 'r') as f:
                    history = json.load(f)
            except:
                history = []
        
        history.insert(0, {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'credits': 130,
            'cgpa': 3.85,
            'status': 'GRADUATED'
        })
        
        history = history[:10]
        
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)


class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.courses = []
        self.total_credits = 0
        self.cgpa = 0.0
        self.status = "GRADUATED"
        self.grade_counts = {}
    
    def load_data(self):
        self.courses = [
            ("CSE115", "Introduction to Programming", 3, "A", "Valid", "Fall 2020"),
            ("CSE115L", "Programming Lab", 1, "A", "Valid", "Fall 2020"),
            ("CSE173", "Discrete Mathematics", 3, "A-", "Valid", "Spring 2021"),
            ("CSE215", "Data Structures", 3, "B+", "Valid", "Fall 2021"),
            ("CSE215L", "Data Structures Lab", 1, "A-", "Valid", "Fall 2021"),
            ("CSE225", "Algorithms", 3, "A", "Valid", "Spring 2022"),
            ("CSE299", "Junior Design", 1, "A", "Valid", "Spring 2022"),
            ("CSE311", "Database Systems", 3, "B", "Valid", "Fall 2022"),
            ("CSE311L", "Database Lab", 1, "B+", "Valid", "Fall 2022"),
            ("CSE323", "Software Engineering", 3, "A-", "Valid", "Spring 2023"),
            ("CSE327", "Web Development", 3, "A", "Valid", "Fall 2023"),
            ("CSE331", "Computer Networks", 3, "B+", "Valid", "Spring 2024"),
            ("CSE332", "Operating Systems", 3, "A", "Valid", "Fall 2024"),
            ("CSE332L", "OS Lab", 1, "A-", "Valid", "Fall 2024"),
            ("CSE399", "Senior Design I", 1, "A", "Valid", "Fall 2024"),
            ("CSE425", "Capstone Project I", 3, "A", "Valid", "Spring 2025"),
            ("CSE426", "Capstone Project II", 3, "A-", "Valid", "Spring 2025"),
            ("CSE427", "Compiler Design", 3, "B+", "Valid", "Spring 2025"),
            ("CSE435", "Machine Learning", 3, "A", "Valid", "Spring 2025"),
            ("MAT116", "Calculus I", 3, "B+", "Valid", "Fall 2020"),
            ("MAT125", "Calculus II", 3, "B", "Valid", "Spring 2021"),
            ("STA201", "Statistics", 3, "A-", "Valid", "Fall 2021"),
            ("PHY107", "Physics I", 3, "B", "Valid", "Fall 2020"),
            ("PHY108", "Physics II", 3, "B+", "Valid", "Spring 2021"),
            ("ENG101", "English Writing", 3, "A", "Valid", "Fall 2020"),
            ("CSE101", "Computer Fundamentals", 3, "A", "Valid", "Fall 2019"),
            ("CSE102", "Computer Fundamentals Lab", 1, "A", "Valid", "Fall 2019"),
            ("CSE103", "Introduction to Engineering", 2, "A-", "Valid", "Fall 2019"),
            ("CSE104", "Engineering Drawing", 1, "A", "Valid", "Fall 2019"),
            ("MAT1161", "Calculus III", 3, "B+", "Valid", "Fall 2021"),
            ("MAT216", "Linear Algebra", 3, "A-", "Valid", "Spring 2022"),
            ("PHY107L", "Physics Lab I", 1, "A", "Valid", "Fall 2020"),
            ("PHY108L", "Physics Lab II", 1, "B+", "Valid", "Spring 2021"),
            ("CHY101", "Chemistry", 3, "B", "Valid", "Fall 2019"),
            ("CHY102", "Chemistry Lab", 1, "A-", "Valid", "Fall 2019"),
            ("BIO101", "Biology", 3, "B+", "Valid", "Fall 2019"),
            ("ENG102", "Technical Writing", 3, "A", "Valid", "Spring 2021"),
            ("ECO101", "Principles of Economics", 3, "B", "Valid", "Fall 2020"),
            ("ACC101", "Financial Accounting", 3, "A-", "Valid", "Spring 2021"),
            ("BUS101", "Business Communication", 3, "A", "Valid", "Fall 2021"),
            ("CSE450", "Artificial Intelligence", 3, "A", "Valid", "Fall 2024"),
            ("CSE451", "Cloud Computing", 3, "A-", "Valid", "Fall 2024"),
            ("CSE460", "Cybersecurity", 3, "B+", "Valid", "Fall 2024"),
            ("CSE470", "Data Science", 3, "A", "Valid", "Spring 2025"),
            ("CSE480", "Mobile App Development", 3, "A-", "Valid", "Spring 2025"),
            ("CSE490", "Software Testing", 3, "B+", "Valid", "Spring 2025"),
            ("CSE400", "Internship", 3, "A", "Valid", "Summer 2023"),
            ("CSE445", "Data Mining", 3, "A-", "Valid", "Fall 2023"),
            ("CSE455", "Deep Learning", 3, "A", "Valid", "Fall 2023"),
            ("CSE465", "Network Security", 3, "B+", "Valid", "Spring 2024"),
            ("CSE475", "Cloud Architecture", 3, "A", "Valid", "Spring 2024"),
        ]
        
        self.calculate_stats()
        Clock.schedule_once(lambda dt: self.init_ui(), 0)
    
    def calculate_stats(self):
        total_credits = 0
        total_points = 0
        self.grade_counts = {}
        
        for course in self.courses:
            code, name, credits, grade, status, semester = course
            gp = GRADE_POINTS.get(grade, 0)
            total_credits += credits
            total_points += gp * credits
            self.grade_counts[grade] = self.grade_counts.get(grade, 0) + 1
        
        self.total_credits = total_credits
        self.cgpa = total_points / total_credits if total_credits > 0 else 0
        self.status = "GRADUATED" if self.total_credits >= 130 else "NOT GRADUATED"
    
    def on_enter(self):
        if not self.courses:
            self.load_data()
    
    def init_ui(self, dt=None):
        self.clear_widgets()
        
        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        header = BoxLayout(orientation='horizontal', size_hint_y=0.08, padding=10)
        with header.canvas.before:
            Color(*get_color_from_hex(NSU_BLUE))
            header.canvas.before.children[-1] = Rectangle(pos=header.pos, size=header.size)
        
        title = Label(text="[color=#d69e2e][b]NSU Audit Core[/b][/color]", 
                     markup=True, font_size='18sp', size_hint_x=0.7)
        header.add_widget(title)
        
        logout_btn = Button(text="Logout", size_hint_x=0.3, 
                          background_color=(0.9, 0.2, 0.2, 1), color=(1,1,1,1), font_size='12sp')
        logout_btn.bind(on_press=self.logout)
        header.add_widget(logout_btn)
        main_layout.add_widget(header)
        
        status_card = BoxLayout(orientation='vertical', padding=15, size_hint_y=0.22)
        with status_card.canvas.before:
            Color(1, 1, 1, 1)
            status_card.canvas.before.children[-1] = Rectangle(pos=status_card.pos, size=status_card.size)
        with status_card.canvas.before:
            Color(*get_color_from_hex('#48bb78'))
            Rectangle(pos=(status_card.x, status_card.y), size=(5, status_card.height))
        
        status_label = Label(text=self.status, font_size='26sp', 
                           color=get_color_from_hex('#48bb78'), bold=True)
        status_card.add_widget(Label(text="GRADUATION STATUS", font_size='11sp', color=(0,0,0,0.5)))
        status_card.add_widget(status_label)
        
        stats_row = BoxLayout(orientation='horizontal', size_hint_y=0.5)
        stats_row.add_widget(BoxLayout(orientation='vertical', children=[
            Label(text=f"{self.total_credits}", font_size='20sp', color=get_color_from_hex(NSU_BLUE), bold=True),
            Label(text="Credits", font_size='10sp', color=(0,0,0,0.6))
        ]))
        stats_row.add_widget(BoxLayout(orientation='vertical', children=[
            Label(text=f"{self.cgpa:.2f}", font_size='20sp', color=get_color_from_hex(NSU_GOLD), bold=True),
            Label(text="CGPA", font_size='10sp', color=(0,0,0,0.6))
        ]))
        stats_row.add_widget(BoxLayout(orientation='vertical', children=[
            Label(text=f"{len(self.courses)}", font_size='20sp', color=get_color_from_hex('#805ad6'), bold=True),
            Label(text="Courses", font_size='10sp', color=(0,0,0,0.6))
        ]))
        status_card.add_widget(stats_row)
        main_layout.add_widget(status_card)
        
        btn_layout = GridLayout(cols=2, size_hint_y=0.12, spacing=10, padding=5)
        
        cert_btn = Button(text="Download Certificate", background_color=get_color_from_hex('#48bb78'),
                        color=(1,1,1,1), font_size='12sp')
        cert_btn.bind(on_press=self.download_certificate)
        btn_layout.add_widget(cert_btn)
        
        trans_btn = Button(text="Download Transcript", background_color=get_color_from_hex('#dd6b20'),
                          color=(1,1,1,1), font_size='12sp')
        trans_btn.bind(on_press=self.download_transcript)
        btn_layout.add_widget(trans_btn)
        main_layout.add_widget(btn_layout)
        
        tabs = TabbedPanel(size_hint_y=0.53, tab_pos='top')
        
        courses_tab = TabbedPanelItem(text="Courses", background_color=get_color_from_hex(NSU_BLUE))
        courses_scroll = ScrollView()
        courses_layout = GridLayout(cols=1, spacing=8, size_hint_y=None, padding=10)
        courses_layout.bind(minimum_height=courses_layout.setter('height'))
        
        for course in self.courses:
            code, name, credits, grade, status, semester = course
            course_card = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, padding=10)
            with course_card.canvas.before:
                Color(1, 1, 1, 1)
                course_card.canvas.before.children[-1] = Rectangle(pos=course_card.pos, size=course_card.size)
            
            grade_color = '#48bb78' if grade.startswith('A') else ('#3182ce' if grade.startswith('B') else '#718096')
            left_panel = BoxLayout(orientation='vertical', size_hint_x=0.25)
            left_panel.add_widget(Label(text=code, font_size='11sp', color=get_color_from_hex(NSU_BLUE), bold=True))
            left_panel.add_widget(Label(text=str(credits) + " cr", font_size='9sp', color=(0,0,0,0.5)))
            course_card.add_widget(left_panel)
            
            center_panel = BoxLayout(orientation='vertical', size_hint_x=0.5)
            name_label = name if len(name) <= 28 else name[:25] + "..."
            center_panel.add_widget(Label(text=name_label, font_size='10sp', shorten=True))
            center_panel.add_widget(Label(text=semester, font_size='9sp', color=(0,0,0,0.5)))
            course_card.add_widget(center_panel)
            
            right_panel = BoxLayout(orientation='vertical', size_hint_x=0.25)
            right_panel.add_widget(Label(text=grade, font_size='16sp', color=get_color_from_hex(grade_color), bold=True))
            right_panel.add_widget(Label(text=status, font_size='8sp', color=(0,0,0,0.5)))
            course_card.add_widget(right_panel)
            
            courses_layout.add_widget(course_card)
        
        courses_scroll.add_widget(courses_layout)
        courses_tab.content = courses_scroll
        tabs.add_widget(courses_tab)
        
        grades_tab = TabbedPanelItem(text="Grades", background_color=get_color_from_hex(NSU_BLUE))
        grades_scroll = ScrollView()
        grades_layout = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=15)
        grades_layout.bind(minimum_height=grades_layout.setter('height'))
        
        total = sum(self.grade_counts.values())
        
        grade_colors = {'A+': '#48bb78', 'A': '#48bb78', 'A-': '#68d391',
                       'B+': '#3182ce', 'B': '#3182ce', 'B-': '#63b3ed',
                       'C+': '#ecc94b', 'C': '#ecc94b', 'C-': '#f6e05e',
                       'D': '#ed8936', 'F': '#fc8181'}
        
        for grade in ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D', 'F']:
            if grade in self.grade_counts:
                count = self.grade_counts[grade]
                percent = (count / total) * 100
                
                grade_card = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=10)
                with grade_card.canvas.before:
                    Color(1, 1, 1, 1)
                    grade_card.canvas.before.children[-1] = Rectangle(pos=grade_card.pos, size=grade_card.size)
                
                grade_card.add_widget(Label(text=grade, font_size='18sp', 
                                          color=get_color_from_hex(grade_colors.get(grade, '#000000')), 
                                          bold=True, size_hint_x=0.2))
                grade_card.add_widget(Label(text=str(count), font_size='16sp', size_hint_x=0.2))
                
                bar_bg = BoxLayout(size_hint_x=0.4)
                with bar_bg.canvas.before:
                    Color(0.9, 0.9, 0.9, 1)
                    bar_bg.canvas.before.children[-1] = RoundedRectangle(pos=bar_bg.pos, size=bar_bg.size, radius=[5]))
                bar_fill = BoxLayout(size_hint_x=percent/100, pos=bar_bg.pos)
                with bar_fill.canvas.before:
                    Color(*get_color_from_hex(grade_colors.get(grade, '#000000')))
                    bar_fill.canvas.before.children[-1] = RoundedRectangle(pos=bar_fill.pos, size=bar_fill.size, radius=[5])
                grade_card.add_widget(bar_bg)
                grade_card.add_widget(bar_fill)
                
                grade_card.add_widget(Label(text=f"{percent:.1f}%", font_size='12sp', size_hint_x=0.2))
                
                grades_layout.add_widget(grade_card)
        
        grades_scroll.add_widget(grades_layout)
        grades_tab.content = grades_scroll
        tabs.add_widget(grades_tab)
        
        history_tab = TabbedPanelItem(text="History", background_color=get_color_from_hex(NSU_BLUE))
        history_scroll = ScrollView()
        history_layout = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=15)
        history_layout.bind(minimum_height=history_layout.setter('height'))
        
        history = []
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, 'r') as f:
                    history = json.load(f)
            except:
                history = []
        
        if not history:
            history_layout.add_widget(Label(text="No login history yet", font_size='14sp', color=(0,0,0,0.5)))
        else:
            for entry in history:
                hist_card = BoxLayout(orientation='vertical', size_hint_y=None, height=80, padding=15)
                with hist_card.canvas.before:
                    Color(1, 1, 1, 1)
                    hist_card.canvas.before.children[-1] = Rectangle(pos=hist_card.pos, size=hist_card.size)
                
                status_color = '#48bb78' if entry.get('status') == 'GRADUATED' else '#fc8181'
                hist_card.add_widget(Label(text=f"{entry.get('date', 'N/A')}", font_size='12sp', color=(0,0,0,0.7), halign='left'))
                hist_card.add_widget(Label(text=f"Credits: {entry.get('credits', 0)} | CGPA: {entry.get('cgpa', 0):.2f}", font_size='12sp'))
                hist_card.add_widget(Label(text=entry.get('status', 'N/A'), font_size='14sp', 
                                          color=get_color_from_hex(status_color), bold=True))
                history_layout.add_widget(hist_card)
        
        history_scroll.add_widget(history_layout)
        history_tab.content = history_scroll
        tabs.add_widget(history_tab)
        
        main_layout.add_widget(tabs)
        
        self.add_widget(main_layout)
    
    def download_certificate(self, instance):
        try:
            from reportlab.lib.pagesizes import landscape, A4
            from reportlab.lib.colors import HexColor
            from reportlab.pdfgen import canvas
            from android.permissions import request, PERMISSIONS
            request(PERMISSIONS)
            from android.storage import primary_external_storage_path
            
            output_dir = primary_external_storage_path() + "/Download"
            os.makedirs(output_dir, exist_ok=True)
            filename = os.path.join(output_dir, f"NSU_Certificate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
            
            pw, ph = landscape(A4)
            c = canvas.Canvas(filename, pagesize=landscape(A4))
            
            NSU_BL = HexColor('#1a365d')
            NSU_GLD = HexColor('#d69e2e')
            WHITE = HexColor('#ffffff')
            
            c.setFillColor(NSU_BL)
            c.rect(0, 0, pw, ph, fill=True, stroke=False)
            c.setStrokeColor(NSU_GLD)
            c.setLineWidth(15)
            c.rect(10, 10, pw-20, ph-20, fill=False, stroke=True)
            
            c.setFillColor(NSU_GLD)
            c.setFont("Helvetica-Bold", 12)
            c.drawCentredString(pw/2, ph-140, "NORTH SOUTH UNIVERSITY")
            
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 30)
            c.drawCentredString(pw/2, ph-190, "CERTIFICATE OF")
            c.drawCentredString(pw/2, ph-230, "GRADUATION")
            
            c.setFont("Helvetica", 12)
            c.drawCentredString(pw/2, ph-270, "This certifies that")
            
            c.setFillColor(NSU_GLD)
            c.setFont("Helvetica-Bold", 24)
            c.drawCentredString(pw/2, ph-305, "Student Name")
            
            c.setFillColor(WHITE)
            c.setFont("Helvetica", 11)
            c.drawCentredString(pw/2, ph-335, "student@northsouth.edu")
            
            c.setFont("Helvetica-Bold", 18)
            c.setFillColor(HexColor('#48bb78'))
            c.drawCentredString(pw/2, ph-380, self.status)
            
            info_y = ph-430
            c.setFillColor(WHITE)
            c.setFont("Helvetica", 11)
            c.drawCentredString(pw/2, info_y, f"Total Credits: {self.total_credits}  |  CGPA: {self.cgpa:.2f}  |  Date: {datetime.now().strftime('%B %d, %Y')}")
            
            c.setFillColor(NSU_GLD)
            c.rect(pw/2-80, info_y-40, 160, 2, fill=True, stroke=False)
            
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 10)
            c.drawCentredString(pw/2, info_y-60, "NSU Audit Core Mobile")
            
            c.save()
            
            popup = Popup(title='Success', content=Label(text=f'Certificate saved to Downloads folder!'),
                        size_hint=(0.8, 0.3))
            popup.open()
            
        except Exception as e:
            popup = Popup(title='Error', content=Label(text=f'Failed: {str(e)}'),
                        size_hint=(0.8, 0.4))
            popup.open()
    
    def download_transcript(self, instance):
        try:
            from reportlab.lib.pagesizes import landscape, A4
            from reportlab.lib.colors import HexColor
            from reportlab.pdfgen import canvas
            from android.permissions import request, PERMISSIONS
            request(PERMISSIONS)
            from android.storage import primary_external_storage_path
            
            output_dir = primary_external_storage_path() + "/Download"
            os.makedirs(output_dir, exist_ok=True)
            filename = os.path.join(output_dir, f"NSU_Transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
            
            c = canvas.Canvas(filename, pagesize=landscape(A4))
            pw, ph = landscape(A4)
            
            NSU_BLUE = HexColor('#1a365d')
            NSU_GOLD = HexColor('#d69e2e')
            
            c.setFillColor(NSU_BLUE)
            c.rect(0, ph - 80, pw, 80, fill=True, stroke=False)
            
            c.setFillColor(NSU_GOLD)
            c.setFont("Helvetica-Bold", 20)
            c.drawString(95, ph - 45, "NORTH SOUTH UNIVERSITY")
            c.setFillColor(HexColor('#ffffff'))
            c.setFont("Helvetica", 13)
            c.drawString(95, ph - 68, "Official Academic Transcript")
            
            left_margin = 30
            right_margin = pw - 30
            
            y = ph - 110
            c.setFillColor(HexColor('#000000'))
            c.setFont("Helvetica-Bold", 11)
            c.drawString(left_margin, y, "Student: Student Name")
            c.drawRightString(right_margin, y, f"Total Credits: {self.total_credits} / 130")
            
            y = y - 20
            c.drawString(left_margin, y, "Email: student@northsouth.edu")
            c.drawRightString(right_margin, y, f"CGPA: {self.cgpa:.2f}")
            
            y = y - 20
            c.drawRightString(right_margin, y, f"Status: {self.status}")
            
            y = y - 35
            c.setStrokeColor(NSU_BLUE)
            c.setLineWidth(2)
            c.line(left_margin, y, right_margin, y)
            
            c.setFillColor(NSU_BLUE)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(left_margin + 5, y - 12, "Code")
            c.drawString(left_margin + 70, y - 12, "Course Name")
            c.drawString(left_margin + 300, y - 12, "Credits")
            c.drawString(left_margin + 360, y - 12, "Grade")
            c.drawString(left_margin + 420, y - 12, "Status")
            c.drawString(left_margin + 500, y - 12, "Semester")
            
            y = y - 18
            c.setFont("Helvetica", 9)
            c.setStrokeColor(HexColor('#e2e8f0'))
            c.setLineWidth(0.5)
            
            for course in self.courses:
                code, name, credits, grade, status, semester = course
                
                if y < 60:
                    c.showPage()
                    y = ph - 50
                
                c.drawString(left_margin + 5, y, code)
                c.drawString(left_margin + 70, y, name[:42] if len(name) > 42 else name)
                c.drawString(left_margin + 300, y, str(credits))
                c.drawString(left_margin + 360, y, grade)
                c.drawString(left_margin + 420, y, status)
                c.drawString(left_margin + 500, y, semester)
                c.line(left_margin, y - 3, right_margin, y - 3)
                
                y = y - 16
            
            c.setFillColor(NSU_BLUE)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(left_margin, 35, f"Total Credits: {self.total_credits}  |  CGPA: {self.cgpa:.2f}  |  Status: {self.status}")
            
            c.save()
            
            popup = Popup(title='Success', content=Label(text=f'Transcript saved to Downloads folder!'),
                        size_hint=(0.8, 0.3))
            popup.open()
            
        except Exception as e:
            popup = Popup(title='Error', content=Label(text=f'Failed: {str(e)}'),
                        size_hint=(0.8, 0.4))
            popup.open()
    
    def logout(self, instance):
        self.manager.current = 'login'


class NSUAuditMobileApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        return sm


if __name__ == '__main__':
    NSUAuditMobileApp().run()
