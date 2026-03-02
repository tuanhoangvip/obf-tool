import random
import os
import sys
import time
import re
import threading
from datetime import datetime
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import requests
import warnings
import logging

# Tắt các warning không cần thiết
warnings.filterwarnings("ignore")
logging.getLogger('selenium').setLevel(logging.ERROR)
logging.getLogger('urllib3').setLevel(logging.ERROR)
logging.getLogger('WDM').setLevel(logging.ERROR)

# ═══════════════════════════════════════════════════════════════════════════════
# 🎨 HỆ THỐNG MÀU SẮC CAO CẤP
# ═══════════════════════════════════════════════════════════════════════════════

class Colors:
    """Bảng màu Rainbow đẹp mắt cho giao diện Console"""
    
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    ORANGE = '\033[38;5;208m'
    PINK = '\033[38;5;213m'
    LIME = '\033[38;5;118m'
    PURPLE = '\033[38;5;141m'
    GOLD = '\033[38;5;220m'
    
    RAINBOW = [
        '\033[38;5;196m', '\033[38;5;208m', '\033[38;5;226m', '\033[38;5;46m',
        '\033[38;5;51m', '\033[38;5;21m', '\033[38;5;129m', '\033[38;5;201m',
    ]
    
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

    @staticmethod
    def rainbow_text(text):
        result = ""
        for i, char in enumerate(text):
            if char != ' ':
                result += Colors.RAINBOW[i % len(Colors.RAINBOW)] + char
            else:
                result += char
        return result + Colors.RESET

    @staticmethod
    def gradient_line(char, length):
        result = ""
        for i in range(length):
            result += Colors.RAINBOW[i % len(Colors.RAINBOW)] + char
        return result + Colors.RESET


# ═══════════════════════════════════════════════════════════════════════════════
# 📊 BỘ THEO DÕI THỐNG KÊ
# ═══════════════════════════════════════════════════════════════════════════════

class ThongKe:
    def __init__(self):
        self.lock = threading.Lock()
        self.thanh_cong = 0
        self.that_bai = 0
        self.tong = 0
        self.thoi_gian_bat_dau = None
        self.danh_sach_uid = []

    def them_thanh_cong(self, uid=None):
        with self.lock:
            self.thanh_cong += 1
            self.tong += 1
            if uid:
                self.danh_sach_uid.append(uid)

    def them_that_bai(self):
        with self.lock:
            self.that_bai += 1
            self.tong += 1

    def lay_thong_ke(self):
        with self.lock:
            da_chay = time.time() - self.thoi_gian_bat_dau if self.thoi_gian_bat_dau else 0
            return {
                'thanh_cong': self.thanh_cong,
                'that_bai': self.that_bai,
                'tong': self.tong,
                'thoi_gian': da_chay,
                'toc_do': self.thanh_cong / da_chay * 60 if da_chay > 0 else 0,
                'danh_sach_uid': self.danh_sach_uid.copy()
            }


thong_ke = ThongKe()


# ═══════════════════════════════════════════════════════════════════════════════
# 🖥️ HỆ THỐNG HIỂN THỊ
# ═══════════════════════════════════════════════════════════════════════════════

class GiaoDien:
    
    @staticmethod
    def xoa_man_hinh():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def lay_thoi_gian():
        return datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def in_log(cap_do, id_luong, noi_dung, them=""):
        thoi_gian = GiaoDien.lay_thoi_gian()
        
        cau_hinh = {
            'THANH_CONG': (Colors.GREEN, '✅', 'THÀNH CÔNG'),
            'LOI': (Colors.RED, '❌', 'LỖI'),
            'CANH_BAO': (Colors.YELLOW, '⚠️', 'CẢNH BÁO'),
            'THONG_TIN': (Colors.CYAN, '💡', 'THÔNG TIN'),
            'XU_LY': (Colors.MAGENTA, '⏳', 'ĐANG XỬ LÝ'),
            'LUU': (Colors.GREEN, '💾', 'ĐÃ LƯU'),
            'KHOI_DONG': (Colors.ORANGE, '🚀', 'KHỞI ĐỘNG'),
            'CLICK': (Colors.LIME, '👆', 'NHẤN NÚT'),
        }
        
        mau, bieu_tuong, nhan = cau_hinh.get(cap_do, (Colors.WHITE, '•', 'LOG'))
        chuoi_luong = f"{Colors.GOLD}⟨L-{id_luong:02d}⟩{Colors.RESET}" if id_luong >= 0 else f"{Colors.GOLD}⟨CHÍNH⟩{Colors.RESET}"
        
        dong_log = (
            f"  {Colors.DIM}┃{Colors.RESET} "
            f"{Colors.PURPLE}[{thoi_gian}]{Colors.RESET} "
            f"{chuoi_luong} "
            f"{mau}{Colors.BOLD}{bieu_tuong} {nhan:12}{Colors.RESET} "
            f"{Colors.WHITE}│{Colors.RESET} "
            f"{Colors.WHITE}{noi_dung}{Colors.RESET}"
        )
        
        if them:
            dong_log += f" {Colors.DIM}「{them}」{Colors.RESET}"
        
        print(dong_log)

    @staticmethod
    def thanh_cong(id_luong, noi_dung, them=""):
        GiaoDien.in_log('THANH_CONG', id_luong, noi_dung, them)

    @staticmethod
    def loi(id_luong, noi_dung, them=""):
        GiaoDien.in_log('LOI', id_luong, noi_dung, them)

    @staticmethod
    def canh_bao(id_luong, noi_dung, them=""):
        GiaoDien.in_log('CANH_BAO', id_luong, noi_dung, them)

    @staticmethod
    def thong_tin(id_luong, noi_dung, them=""):
        GiaoDien.in_log('THONG_TIN', id_luong, noi_dung, them)

    @staticmethod
    def xu_ly(id_luong, noi_dung, them=""):
        GiaoDien.in_log('XU_LY', id_luong, noi_dung, them)

    @staticmethod
    def luu(id_luong, noi_dung, them=""):
        GiaoDien.in_log('LUU', id_luong, noi_dung, them)

    @staticmethod
    def khoi_dong(id_luong, noi_dung, them=""):
        GiaoDien.in_log('KHOI_DONG', id_luong, noi_dung, them)

    @staticmethod
    def click(id_luong, noi_dung, them=""):
        GiaoDien.in_log('CLICK', id_luong, noi_dung, them)

    @staticmethod
    def duong_ke(ky_tu="═", do_dai=75):
        print(f"  {Colors.gradient_line(ky_tu, do_dai)}")

    @staticmethod
    def thanh_thong_ke():
        s = thong_ke.lay_thong_ke()
        phut = int(s['thoi_gian'] // 60)
        giay = int(s['thoi_gian'] % 60)
        ty_le = (s['thanh_cong'] / s['tong'] * 100) if s['tong'] > 0 else 0
        
        print()
        print(f"  {Colors.CYAN}╔{'═'*71}╗{Colors.RESET}")
        print(f"  {Colors.CYAN}║{Colors.RESET} {Colors.BOLD}{Colors.GOLD}📊 THỐNG KÊ THỜI GIAN THỰC{Colors.RESET}{' '*44}{Colors.CYAN}║{Colors.RESET}")
        print(f"  {Colors.CYAN}╠{'═'*71}╣{Colors.RESET}")
        print(f"  {Colors.CYAN}║{Colors.RESET}  "
              f"{Colors.GREEN}✅ Thành công: {s['thanh_cong']:>4}{Colors.RESET}  │  "
              f"{Colors.RED}❌ Thất bại: {s['that_bai']:>4}{Colors.RESET}  │  "
              f"{Colors.YELLOW}📦 Tổng: {s['tong']:>4}{Colors.RESET}  "
              f"{Colors.CYAN}║{Colors.RESET}")
        print(f"  {Colors.CYAN}║{Colors.RESET}  "
              f"{Colors.MAGENTA}⏱️ Thời gian: {phut:02d}:{giay:02d}{Colors.RESET}   │  "
              f"{Colors.ORANGE}⚡ Tốc độ: {s['toc_do']:.1f}/phút{Colors.RESET}  │  "
              f"{Colors.LIME}📈 Tỷ lệ: {ty_le:.1f}%{Colors.RESET}  "
              f"{Colors.CYAN}║{Colors.RESET}")
        print(f"  {Colors.CYAN}╚{'═'*71}╝{Colors.RESET}")
        print()


# ═══════════════════════════════════════════════════════════════════════════════
# 🎨 BANNER
# ═══════════════════════════════════════════════════════════════════════════════

def hieu_ung_tai():
    khung = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    for _ in range(20):
        for i, f in enumerate(khung):
            mau = Colors.RAINBOW[i % len(Colors.RAINBOW)]
            sys.stdout.write(f"\r  {mau}{f} Đang khởi động hệ thống...{Colors.RESET}  ")
            sys.stdout.flush()
            time.sleep(0.05)
    print()


def hien_thi_banner():
    GiaoDien.xoa_man_hinh()
    
    banner = r"""
          
                    
                 (____)
                (  ☸   )
                 |    |
                 |____|
                /______\
              PHẬT TỊNH TÂM

███╗   ██╗████████╗██╗  ██╗ ██████╗  █████╗ ███╗   ██╗ ██████╗ 
████╗  ██║╚══██╔══╝██║  ██║██╔════╝ ██╔══██╗████╗  ██║██╔════╝ 
██╔██╗ ██║   ██║   ███████║██║  ███╗███████║██╔██╗ ██║██║  ███╗
██║╚██╗██║   ██║   ██╔══██║██║   ██║██╔══██║██║╚██╗██║██║   ██║
██║ ╚████║   ██║   ██║  ██║╚██████╔╝██║  ██║██║ ╚████║╚██████╔╝
╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝
                      N T H O A N G

ूाीू    🗣⊂======3       𓀐🍑𓂸ඞ🥵     𐐘💥╾━╤デ╦︻ඞා    🥛（ ͜.人 ͜.)ᵍⁱᵛᵉ ᵐᵉ ʸᵒᵘʳ ᵖᵘˢˢʸ（ ͜.人 ͜.)🥛
    """
    
    for i, dong in enumerate(banner.strip().split('\n')):
        mau = Colors.RAINBOW[i % len(Colors.RAINBOW)]
        print(f"{mau}{dong}{Colors.RESET}")
    
    print()
    GiaoDien.duong_ke("═", 85)
    
    print(f"""
  {Colors.CYAN}╔══════════════════════════════════════════════════════════════════════════════════╗{Colors.RESET}
  {Colors.CYAN}║{Colors.RESET}   {Colors.rainbow_text("★★★ CÔNG CỤ TỰ ĐỘNG ĐĂNG KÝ TÀI KHOẢN FACEBOOK ★★★")}                      {Colors.CYAN}║{Colors.RESET}
  {Colors.CYAN}║{Colors.RESET}   {Colors.GOLD}🌈 Tool được làm từ NthoangDevxCoder{Colors.RESET}        {Colors.GREEN}📦 Version 3.0 PRO - Iu Ngô Quốc Mạnh:33 {Colors.RESET}                {Colors.CYAN}║{Colors.RESET}
  {Colors.CYAN}╠══════════════════════════════════════════════════════════════════════════════════╣{Colors.RESET}
  {Colors.CYAN}║{Colors.RESET}   {Colors.GREEN}✨ Đăng ký tự động - Không cần thao tác thủ công{Colors.RESET}                         {Colors.CYAN}║{Colors.RESET}
  {Colors.CYAN}║{Colors.RESET}   {Colors.GREEN}✨ Hỗ trợ đa luồng - Tốc độ siêu nhanh{Colors.RESET}                                   {Colors.CYAN}║{Colors.RESET}
  {Colors.CYAN}║{Colors.RESET}   {Colors.GREEN}✨ Đã sửa lỗi nhấn nút đăng ký{Colors.RESET}                                           {Colors.CYAN}║{Colors.RESET}
  {Colors.CYAN}╚══════════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}
    """)
    GiaoDien.duong_ke("─", 85)
    print()


def nhap_du_lieu(loi_nhac, kieu=str, min_val=None, max_val=None, mac_dinh=None):
    while True:
        try:
            bieu_tuong = "💡" if kieu == str else "🔢"
            prompt = f"  {Colors.CYAN}{bieu_tuong} {loi_nhac}{Colors.RESET}"
            if mac_dinh:
                prompt += f" {Colors.DIM}[Mặc định: {mac_dinh}]{Colors.RESET}"
            prompt += f": {Colors.GOLD}"
            
            nhap_vao = input(prompt).strip()
            print(Colors.RESET, end="")
            
            if not nhap_vao and mac_dinh is not None:
                return mac_dinh
            
            gia_tri = kieu(nhap_vao)
            
            if min_val is not None and gia_tri < min_val:
                GiaoDien.canh_bao(-1, f"Giá trị phải >= {min_val}")
                continue
            if max_val is not None and gia_tri > max_val:
                GiaoDien.canh_bao(-1, f"Giá trị phải <= {max_val}")
                continue
            return gia_tri
        except ValueError:
            GiaoDien.canh_bao(-1, "Vui lòng nhập đúng định dạng")


# ═══════════════════════════════════════════════════════════════════════════════
# 🔧 LỚP ĐĂNG KÝ FACEBOOK - ĐÃ SỬA LỖI
# ═══════════════════════════════════════════════════════════════════════════════

class DangKyFacebook:
    
    DANH_SACH_HO = [
        "Nguyễn", "Trần", "Lê", "Phạm", "Huỳnh", "Hoàng", "Phan", "Vũ", 
        "Võ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý", "Đinh",
        "Lương", "Trương", "Cao", "Lâm", "Tô", "Thái", "Hà", "Tạ"
    ]

    TEN_NAM = [
        "Nam", "Long", "Huy", "Tuấn", "Khoa", "Tài", "Duy", "Sơn", 
        "Phúc", "Trí", "Minh", "Đức", "Thành", "Quang", "Việt", "Hoàng",
        "Kiên", "Bảo", "Khang", "Phong", "An", "Hiếu", "Nhân", "Đạt"
    ]

    TEN_NU = [
        "Linh", "Trang", "Lan", "Hương", "Nhung", "Mai", "Yến", "Thảo", 
        "Vy", "Ngân", "Chi", "Hà", "Trinh", "Như", "Ngọc", "Anh",
        "Hạnh", "Vân", "Phương", "Quỳnh", "Trâm", "Thy", "Nhi", "Thủy"
    ]

    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    ]

    def __init__(self, id_luong, mat_khau="MatKhauManh123@@"):
        self.id_luong = id_luong
        self.mat_khau = mat_khau
        self.driver = None
        self.wait = None
        
    def tao_ten_ngau_nhien(self):
        ho = random.choice(self.DANH_SACH_HO)
        gioi_tinh = random.choice([1, 2])
        
        if gioi_tinh == 2:
            ten = random.choice(self.TEN_NAM)
        else:
            ten = random.choice(self.TEN_NU)
        
        return ho, ten, gioi_tinh

    def tao_so_dien_thoai(self):
        dau_so = ['093', '094', '096', '097', '098', '032', '033', '034', 
                  '035', '036', '037', '038', '039', '070', '076', '077', 
                  '078', '079', '081', '082', '083', '084', '085']
        dau = random.choice(dau_so)
        return dau + str(random.randint(1000000, 9999999))

    def khoi_tao_trinh_duyet(self):
        try:
            user_agent = random.choice(self.USER_AGENTS)
            
            options = Options()
            options.add_argument(f"user-agent={user_agent}")
            
            vi_tri_x = (self.id_luong % 5) * 350
            vi_tri_y = (self.id_luong // 5) * 450
            options.add_argument("--window-size=340,800")
            options.add_argument(f"--window-position={vi_tri_x},{vi_tri_y}")
            
            # Anti-detection
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)
            
            # Performance
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-logging")
            options.add_argument("--log-level=3")
            options.add_argument("--silent")
            options.add_argument("--disable-notifications")
            
            # Tắt hình ảnh để nhanh hơn
            prefs = {
                "profile.managed_default_content_settings.images": 2,
                "profile.default_content_setting_values.notifications": 2
            }
            options.add_experimental_option("prefs", prefs)
            
            service = Service(ChromeDriverManager().install())
            service.log_path = os.devnull
            
            self.driver = webdriver.Chrome(service=service, options=options)
            self.wait = WebDriverWait(self.driver, 15)
            
            # Override webdriver
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            GiaoDien.khoi_dong(self.id_luong, "Đã khởi tạo trình duyệt", "Chrome")
            return True
            
        except Exception as e:
            GiaoDien.loi(self.id_luong, "Lỗi khởi tạo trình duyệt", str(e)[:50])
            return False

    def dong_popup(self):
        """Đóng tất cả popup và cookie consent"""
        try:
            # Danh sách các selector cho popup/cookie
            popup_selectors = [
                "button[data-cookiebanner='accept_button']",
                "button[data-testid='cookie-policy-manage-dialog-accept-button']",
                "button[title='Cho phép tất cả cookie']",
                "button[title='Accept All']",
                "button[title='Allow all cookies']",
                "[aria-label='Close']",
                "[aria-label='Đóng']",
            ]
            
            for selector in popup_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for el in elements:
                        if el.is_displayed():
                            el.click()
                            time.sleep(0.3)
                except:
                    pass
            
            # Tìm và click các button có text liên quan
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            for btn in buttons:
                try:
                    text = btn.text.lower()
                    if any(kw in text for kw in ['accept', 'allow', 'đồng ý', 'cho phép', 'ok', 'continue', 'tiếp tục']):
                        if btn.is_displayed() and btn.is_enabled():
                            btn.click()
                            time.sleep(0.3)
                except:
                    pass
                    
        except Exception as e:
            pass

    def dien_truong(self, ten_truong, gia_tri, bang_name=True):
        """Điền giá trị vào trường với xử lý lỗi"""
        try:
            if bang_name:
                element = self.wait.until(EC.presence_of_element_located((By.NAME, ten_truong)))
            else:
                element = self.wait.until(EC.presence_of_element_located((By.ID, ten_truong)))
            
            # Scroll đến element
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.2)
            
            # Clear và điền
            element.clear()
            time.sleep(0.1)
            
            # Gõ từng ký tự để giống người thật
            for char in gia_tri:
                element.send_keys(char)
                time.sleep(random.uniform(0.02, 0.08))
            
            return True
        except Exception as e:
            GiaoDien.loi(self.id_luong, f"Lỗi điền trường {ten_truong}", str(e)[:30])
            return False

    def chon_dropdown(self, id_element, gia_tri):
        """Chọn giá trị trong dropdown"""
        try:
            element = self.wait.until(EC.presence_of_element_located((By.ID, id_element)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.1)
            select = Select(element)
            select.select_by_value(str(gia_tri))
            return True
        except Exception as e:
            GiaoDien.loi(self.id_luong, f"Lỗi chọn {id_element}", str(e)[:30])
            return False

    def click_nut_dang_ky(self):
        """NHẤN NÚT ĐĂNG KÝ - ĐÃ SỬA"""
        GiaoDien.xu_ly(self.id_luong, "Đang tìm và nhấn nút Đăng ký...")
        
        # Danh sách các cách tìm nút submit
        selectors = [
            # Theo name
            (By.NAME, "websubmit"),
            (By.NAME, "submit"),
            
            # Theo CSS selector
            (By.CSS_SELECTOR, "button[name='websubmit']"),
            (By.CSS_SELECTOR, "input[name='websubmit']"),
            (By.CSS_SELECTOR, "button[type='submit']"),
            (By.CSS_SELECTOR, "input[type='submit']"),
            (By.CSS_SELECTOR, "button.signup_btn"),
            (By.CSS_SELECTOR, "[data-sigil='submit_reg']"),
            (By.CSS_SELECTOR, "button[data-sigil*='submit']"),
            
            # Theo class
            (By.CSS_SELECTOR, ".btn.btnS.signup_btn"),
            (By.CSS_SELECTOR, "._54k8._56bs"),
            
            # Theo XPath
            (By.XPATH, "//button[@name='websubmit']"),
            (By.XPATH, "//input[@name='websubmit']"),
            (By.XPATH, "//button[@type='submit']"),
            (By.XPATH, "//button[contains(text(),'Đăng ký')]"),
            (By.XPATH, "//button[contains(text(),'Sign Up')]"),
            (By.XPATH, "//button[contains(text(),'Register')]"),
            (By.XPATH, "//input[@value='Đăng ký']"),
            (By.XPATH, "//input[@value='Sign Up']"),
            (By.XPATH, "//*[contains(@class,'signup')]"),
        ]
        
        for selector_type, selector_value in selectors:
            try:
                elements = self.driver.find_elements(selector_type, selector_value)
                for element in elements:
                    try:
                        if element.is_displayed():
                            # Scroll đến nút
                            self.driver.execute_script(
                                "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", 
                                element
                            )
                            time.sleep(0.5)
                            
                            # Thử click bình thường
                            try:
                                element.click()
                                GiaoDien.click(self.id_luong, "Đã nhấn nút đăng ký", "Click thường")
                                return True
                            except:
                                pass
                            
                            # Thử JavaScript click
                            try:
                                self.driver.execute_script("arguments[0].click();", element)
                                GiaoDien.click(self.id_luong, "Đã nhấn nút đăng ký", "JS Click")
                                return True
                            except:
                                pass
                            
                            # Thử ActionChains
                            try:
                                actions = ActionChains(self.driver)
                                actions.move_to_element(element).click().perform()
                                GiaoDien.click(self.id_luong, "Đã nhấn nút đăng ký", "ActionChains")
                                return True
                            except:
                                pass
                                
                    except:
                        continue
            except:
                continue
        
        # Fallback: Tìm tất cả button và input submit
        try:
            GiaoDien.xu_ly(self.id_luong, "Thử tìm nút bằng cách duyệt tất cả buttons...")
            
            all_buttons = self.driver.find_elements(By.TAG_NAME, "button")
            all_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='submit']")
            
            all_elements = all_buttons + all_inputs
            
            for element in all_elements:
                try:
                    text = element.text.lower() if element.text else ""
                    value = element.get_attribute("value") or ""
                    value = value.lower()
                    name = element.get_attribute("name") or ""
                    
                    # Tìm nút có text hoặc value liên quan đến đăng ký
                    keywords = ['đăng ký', 'sign up', 'register', 'submit', 'tiếp tục', 'continue', 'websubmit']
                    
                    if any(kw in text or kw in value or kw in name for kw in keywords):
                        if element.is_displayed():
                            self.driver.execute_script(
                                "arguments[0].scrollIntoView({block: 'center'});", 
                                element
                            )
                            time.sleep(0.3)
                            self.driver.execute_script("arguments[0].click();", element)
                            GiaoDien.click(self.id_luong, "Đã nhấn nút đăng ký", "Fallback method")
                            return True
                except:
                    continue
        except:
            pass
        
        # Last resort: Submit form
        try:
            GiaoDien.xu_ly(self.id_luong, "Thử submit form trực tiếp...")
            forms = self.driver.find_elements(By.TAG_NAME, "form")
            for form in forms:
                try:
                    form.submit()
                    GiaoDien.click(self.id_luong, "Đã submit form", "Form submit")
                    return True
                except:
                    continue
        except:
            pass
        
        # Cuối cùng: Enter key
        try:
            GiaoDien.xu_ly(self.id_luong, "Thử nhấn Enter...")
            password_field = self.driver.find_element(By.NAME, "reg_passwd__")
            password_field.send_keys(Keys.RETURN)
            GiaoDien.click(self.id_luong, "Đã nhấn Enter", "Enter key")
            return True
        except:
            pass
        
        GiaoDien.loi(self.id_luong, "Không thể tìm/nhấn nút đăng ký")
        return False

    def kiem_tra_uid(self, chuoi_cookie):
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'accept-language': 'vi-VN,vi;q=0.9',
            'user-agent': random.choice(self.USER_AGENTS),
            'cookie': chuoi_cookie,
        }
        
        try:
            response = requests.get(
                'https://www.facebook.com/confirmemail.php', 
                headers=headers, 
                timeout=15
            ).text
            
            patterns = [
                r'"ACCOUNT_ID":\s*"(\d+)"',
                r'"actorID":\s*"(\d+)"',
                r'"userID":\s*"(\d+)"',
                r'c_user=(\d+)',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, response)
                if match:
                    uid = match.group(1)
                    GiaoDien.thanh_cong(self.id_luong, f"Tìm thấy UID", uid)
                    return uid
            
            # Thử lấy từ cookie
            for cookie in chuoi_cookie.split(';'):
                if 'c_user=' in cookie:
                    uid = cookie.split('c_user=')[1].strip()
                    if uid.isdigit():
                        GiaoDien.thanh_cong(self.id_luong, f"Tìm thấy UID từ cookie", uid)
                        return uid
            
            return None
            
        except Exception as e:
            GiaoDien.loi(self.id_luong, "Lỗi kiểm tra UID", str(e)[:40])
            return None

    def dien_form_dang_ky(self):
        try:
            # Truy cập trang đăng ký
            self.driver.get("https://m.facebook.com/reg/")
            time.sleep(random.uniform(2, 4))
            
            GiaoDien.xu_ly(self.id_luong, "Đang tải trang đăng ký")
            
            # Đóng popup nếu có
            self.dong_popup()
            time.sleep(0.5)
            
            # Tạo thông tin ngẫu nhiên
            ho, ten, gioi_tinh = self.tao_ten_ngau_nhien()
            so_dt = self.tao_so_dien_thoai()
            
            GiaoDien.thong_tin(self.id_luong, f"Đăng ký: {ho} {ten}", f"SĐT: {so_dt}")
            
            # Điền họ tên
            self.dien_truong('lastname', ten)
            time.sleep(random.uniform(0.3, 0.6))
            self.dien_truong('firstname', ho)
            time.sleep(random.uniform(0.3, 0.6))
            
            GiaoDien.xu_ly(self.id_luong, "Đã điền họ tên")
            
            # Điền ngày sinh
            self.chon_dropdown("day", random.randint(1, 28))
            self.chon_dropdown("month", random.randint(1, 12))
            self.chon_dropdown("year", random.randint(1970, 2003))
            
            GiaoDien.xu_ly(self.id_luong, "Đã điền ngày sinh")
            
            # Chọn giới tính
            try:
                gender_selector = f"input[name='sex'][value='{gioi_tinh}']"
                gender_element = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, gender_selector))
                )
                self.driver.execute_script("arguments[0].click();", gender_element)
                GiaoDien.xu_ly(self.id_luong, "Đã chọn giới tính")
            except:
                pass
            
            time.sleep(random.uniform(0.3, 0.5))
            
            # Điền SĐT
            self.dien_truong('reg_email__', so_dt)
            time.sleep(random.uniform(0.3, 0.5))
            
            # Điền mật khẩu
            self.dien_truong('reg_passwd__', self.mat_khau)
            
            GiaoDien.xu_ly(self.id_luong, "Đã điền SĐT và mật khẩu")
            
            time.sleep(random.uniform(0.5, 1))
            
            # NHẤN NÚT ĐĂNG KÝ
            if not self.click_nut_dang_ky():
                return None
            
            GiaoDien.xu_ly(self.id_luong, "Đang chờ phản hồi từ Facebook...")
            
            return so_dt
            
        except Exception as e:
            GiaoDien.loi(self.id_luong, "Lỗi điền form", str(e)[:50])
            return None

    def cho_ket_qua(self):
        """Chờ kết quả đăng ký"""
        try:
            # Chờ URL thay đổi hoặc có element xác nhận
            time.sleep(3)
            
            current_url = self.driver.current_url
            
            # Kiểm tra xem đã chuyển trang chưa
            if 'reg' not in current_url.lower() or 'checkpoint' in current_url.lower() or 'confirm' in current_url.lower():
                GiaoDien.thanh_cong(self.id_luong, "Đã chuyển trang", current_url[:50])
                return True
            
            # Chờ thêm
            WebDriverWait(self.driver, 15).until(
                lambda driver: 'reg' not in driver.current_url.lower() or 
                               len(driver.find_elements(By.XPATH, "//*[contains(text(),'code') or contains(text(),'mã') or contains(text(),'xác nhận')]")) > 0
            )
            return True
            
        except:
            return False

    def lay_cookie(self):
        cookies = self.driver.get_cookies()
        return "; ".join(f"{c['name']}={c['value']}" for c in cookies)

    def luu_tai_khoan(self, uid, so_dt, chuoi_cookie):
        try:
            thoi_gian = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open('TK.txt', "a", encoding='utf-8') as f:
                f.write(f"{uid}|{so_dt}|{self.mat_khau}|{chuoi_cookie}|{thoi_gian}\n")
            GiaoDien.luu(self.id_luong, f"Đã lưu tài khoản", f"UID: {uid}")
            return True
        except Exception as e:
            GiaoDien.loi(self.id_luong, "Lỗi lưu file", str(e)[:30])
            return False

    def dang_ky(self):
        try:
            if not self.khoi_tao_trinh_duyet():
                thong_ke.them_that_bai()
                return False
            
            so_dt = self.dien_form_dang_ky()
            if not so_dt:
                thong_ke.them_that_bai()
                return False
            
            self.cho_ket_qua()
            
            time.sleep(random.uniform(2, 4))
            chuoi_cookie = self.lay_cookie()
            uid = self.kiem_tra_uid(chuoi_cookie)
            
            if uid:
                self.luu_tai_khoan(uid, so_dt, chuoi_cookie)
                thong_ke.them_thanh_cong(uid)
                
                print()
                print(f"  {Colors.GREEN}┌{'─'*55}┐{Colors.RESET}")
                print(f"  {Colors.GREEN}│{Colors.RESET} {Colors.BOLD}{Colors.GREEN}🎉 ĐĂNG KÝ THÀNH CÔNG!{Colors.RESET}{' '*33}{Colors.GREEN}│{Colors.RESET}")
                print(f"  {Colors.GREEN}│{Colors.RESET}   UID: {Colors.CYAN}{uid}{Colors.RESET}{' '*(46-len(uid))}{Colors.GREEN}│{Colors.RESET}")
                print(f"  {Colors.GREEN}│{Colors.RESET}   SĐT: {Colors.YELLOW}{so_dt}{Colors.RESET}{' '*(46-len(so_dt))}{Colors.GREEN}│{Colors.RESET}")
                print(f"  {Colors.GREEN}└{'─'*55}┘{Colors.RESET}")
                print()
                
                return True
            else:
                thong_ke.them_that_bai()
                GiaoDien.loi(self.id_luong, "Không lấy được UID")
                return False
                
        except Exception as e:
            thong_ke.them_that_bai()
            GiaoDien.loi(self.id_luong, "Lỗi không xác định", str(e)[:50])
            return False
            
        finally:
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass


# ═══════════════════════════════════════════════════════════════════════════════
# 🚀 HÀM XỬ LÝ
# ═══════════════════════════════════════════════════════════════════════════════

def xu_ly_luong(tham_so):
    id_luong, so_tai_khoan, mat_khau = tham_so
    
    GiaoDien.khoi_dong(id_luong, f"Bắt đầu", f"{so_tai_khoan} tài khoản")
    
    for i in range(so_tai_khoan):
        GiaoDien.xu_ly(id_luong, f"Tài khoản {i+1}/{so_tai_khoan}")
        
        dang_ky = DangKyFacebook(id_luong, mat_khau)
        dang_ky.dang_ky()
        
        time.sleep(random.uniform(3, 6))
    
    GiaoDien.thanh_cong(id_luong, "🏁 Hoàn thành!")


def chay_dang_ky():
    print()
    GiaoDien.duong_ke("═", 85)
    
    print(f"""
  {Colors.GOLD}╔══════════════════════════════════════════════════════════════════════════════════╗{Colors.RESET}
  {Colors.GOLD}║{Colors.RESET}                      {Colors.BOLD}⚙️  CẤU HÌNH ĐĂNG KÝ TÀI KHOẢN  ⚙️{Colors.RESET}                         {Colors.GOLD}║{Colors.RESET}
  {Colors.GOLD}╚══════════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}
    """)
    
    so_luong = nhap_du_lieu("Số luồng chạy đồng thời (1-10)", int, 1, 10, 2)
    tong_tk = nhap_du_lieu("Tổng số tài khoản cần tạo", int, 1, 500, 5)
    mat_khau = nhap_du_lieu("Mật khẩu cho các tài khoản", str, mac_dinh="MatKhau123@@")
    
    tk_moi_luong = (tong_tk + so_luong - 1) // so_luong
    
    print()
    print(f"""
  {Colors.GREEN}╔══════════════════════════════════════════════════════════════════════════════════╗{Colors.RESET}
  {Colors.GREEN}║{Colors.RESET}                            {Colors.BOLD}📋 TÓM TẮT CẤU HÌNH{Colors.RESET}                                 {Colors.GREEN}║{Colors.RESET}
  {Colors.GREEN}╠══════════════════════════════════════════════════════════════════════════════════╣{Colors.RESET}
  {Colors.GREEN}║{Colors.RESET}      🧵 Số luồng:          {Colors.CYAN}{Colors.BOLD}{so_luong:>10}{Colors.RESET}                                       {Colors.GREEN}║{Colors.RESET}
  {Colors.GREEN}║{Colors.RESET}      📦 Tổng tài khoản:    {Colors.CYAN}{Colors.BOLD}{tong_tk:>10}{Colors.RESET}                                       {Colors.GREEN}║{Colors.RESET}
  {Colors.GREEN}║{Colors.RESET}      📊 Mỗi luồng:         {Colors.CYAN}{Colors.BOLD}{tk_moi_luong:>10}{Colors.RESET}                                       {Colors.GREEN}║{Colors.RESET}
  {Colors.GREEN}║{Colors.RESET}      🔑 Mật khẩu:          {Colors.YELLOW}{Colors.BOLD}{mat_khau[:20]:>20}{Colors.RESET}                         {Colors.GREEN}║{Colors.RESET}
  {Colors.GREEN}╚══════════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}
    """)
    
    xac_nhan = nhap_du_lieu("Xác nhận bắt đầu? (y/n)", str, mac_dinh="y")
    if xac_nhan.lower() != 'y':
        GiaoDien.canh_bao(-1, "Đã hủy bỏ")
        return
    
    print()
    GiaoDien.duong_ke("═", 85)
    hieu_ung_tai()
    GiaoDien.duong_ke("═", 85)
    print()
    
    thong_ke.thoi_gian_bat_dau = time.time()
    
    danh_sach_tham_so = [(i, tk_moi_luong, mat_khau) for i in range(so_luong)]
    
    with ThreadPoolExecutor(max_workers=so_luong) as executor:
        futures = [executor.submit(xu_ly_luong, ts) for ts in danh_sach_tham_so]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                GiaoDien.loi(-1, f"Lỗi luồng", str(e)[:40])
    
    print()
    GiaoDien.duong_ke("═", 85)
    GiaoDien.thanh_thong_ke()
    
    s = thong_ke.lay_thong_ke()
    if s['danh_sach_uid']:
        print(f"  {Colors.CYAN}╔{'═'*71}╗{Colors.RESET}")
        print(f"  {Colors.CYAN}║{Colors.RESET} {Colors.BOLD}{Colors.GREEN}📋 DANH SÁCH UID ĐÃ TẠO{Colors.RESET}{' '*47}{Colors.CYAN}║{Colors.RESET}")
        print(f"  {Colors.CYAN}╠{'═'*71}╣{Colors.RESET}")
        for i, uid in enumerate(s['danh_sach_uid'][:10], 1):
            print(f"  {Colors.CYAN}║{Colors.RESET}   {Colors.GOLD}{i:2}.{Colors.RESET} {Colors.GREEN}{uid}{Colors.RESET}{' '*(63-len(uid))}{Colors.CYAN}║{Colors.RESET}")
        if len(s['danh_sach_uid']) > 10:
            print(f"  {Colors.CYAN}║{Colors.RESET}   {Colors.DIM}... và {len(s['danh_sach_uid'])-10} UID khác{Colors.RESET}{' '*52}{Colors.CYAN}║{Colors.RESET}")
        print(f"  {Colors.CYAN}╚{'═'*71}╝{Colors.RESET}")
    
    GiaoDien.duong_ke("═", 85)
    print(f"\n  {Colors.rainbow_text('🎊 HOÀN THÀNH! Tài khoản đã lưu vào TK.txt 🎊')}\n")


# ═══════════════════════════════════════════════════════════════════════════════
# 🎯 MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    try:
        while True:
            hien_thi_banner()
            
            print(f"""
  {Colors.MAGENTA}╔══════════════════════════════════════════════════════════════════════════════════╗{Colors.RESET}
  {Colors.MAGENTA}║{Colors.RESET}        {Colors.BOLD}{Colors.CYAN}[1]{Colors.RESET}  {Colors.GREEN}🚀 BẮT ĐẦU ĐĂNG KÝ TÀI KHOẢN{Colors.RESET}                                    {Colors.MAGENTA}║{Colors.RESET}
  {Colors.MAGENTA}║{Colors.RESET}        {Colors.BOLD}{Colors.CYAN}[0]{Colors.RESET}  {Colors.RED}🚪 THOÁT CHƯƠNG TRÌNH{Colors.RESET}                                           {Colors.MAGENTA}║{Colors.RESET}
  {Colors.MAGENTA}╚══════════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}
            """)
            
            lua_chon = nhap_du_lieu("Nhập lựa chọn", int, 0, 1)
            
            if lua_chon == 1:
                chay_dang_ky()
                input(f"\n  {Colors.DIM}Nhấn Enter để tiếp tục...{Colors.RESET}")
                
            elif lua_chon == 0:
                print(f"\n  {Colors.rainbow_text('★★★ Tạm biệt! ★★★')}\n")
                break
                
    except KeyboardInterrupt:
        print(f"\n  {Colors.YELLOW}Đã dừng bởi người dùng{Colors.RESET}\n")


if __name__ == "__main__":
    main()