import time
import requests
from bs4 import BeautifulSoup

TOKEN = "8996279782:AAEJ-n3vP4K9bts15GC0_htKMceRC4yHj8E"
CHAT = "5124680786"

# قائمة روابط المنتجات المباشرة
URLS_LIST = [
    "https://www.amazon.eg/%D8%AA%D9%83%D9%8A%D9%8A%D9%81-%D8%B3%D8%A8%D9%84%D9%8A%D8%AA-%D8%AD%D8%B5%D8%A7%D9%86-%D8%AA%D8%A8%D8%B1%D9%8A%D8%AF-IW-HFW12CO-X2/dp/B09TSM2JMC",
    "https://www.amazon.eg/%D9%81%D8%B1%D9%8A%D8%B4-%D8%AA%D9%83%D9%8A%D9%8A%D9%81-%D8%A7%D8%AD%D8%AA%D8%B1%D8%A7%D9%81%D9%8A-FUFW12H-%D8%A8%D9%84%D8%A7%D8%B2%D9%85%D8%A7/dp/B0CGXBMZ5T",
    "https://www.amazon.eg/%D9%81%D8%B1%D9%8A%D8%B4-%D8%A7%D9%86%D9%81%D8%B1%D8%AA%D8%B1-%D9%84%D9%84%D8%AA%D8%A8%D8%B1%D9%8A%D8%AF-%D9%88%D8%A7%D9%84%D8%AA%D8%B3%D8%AE%D9%8A%D9%86-SFW13H/dp/B08XS1LRCB",
    "https://www.amazon.eg/%D9%81%D8%B1%D9%8A%D8%B4-%D8%AA%D9%83%D9%8A%D9%8A%D9%81-%D8%B3%D8%A8%D9%84%D9%8A%D8%AA-%D9%86%D8%B8%D8%A7%D9%85-%D8%AA%D8%B1%D8%A8%D9%88%D8%8C/dp/B093FT3RWD",
    "https://www.amazon.eg/%D8%AA%D9%83%D9%8A%D9%8A%D9%81-%D8%A8%D9%86%D8%B8%D8%A7%D9%85-%D8%AA%D9%8A%D8%B1%D8%A8%D9%88-%D9%81%D8%B1%D9%8A%D8%B4%D8%8C-FUFW24H/dp/B09BJRPRRF",
    "https://www.amazon.eg/%D8%AA%D9%83%D9%8A%D9%8A%D9%81-%D8%B3%D8%A8%D9%84%D9%8A%D8%AA-%D9%81%D8%B1%D9%8A%D8%B4-SFW24C-IP/dp/B08Z47SF55"
]

# قائمة بالبروكسيات (اختياري، اتركه فارغاً للاستخدام المباشر)
PROXIES_LIST = []

H = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-align",
    "Upgrade-Insecure-Requests": "1"
}

AR = str.maketrans("٠١٢٣٤٥٦٧٨٩٫٬", "0123456789.,")

def send(msg):
    u = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        response = requests.post(u, json={"chat_id": CHAT, "text": msg, "parse_mode": "Markdown"}, timeout=15)
        if response.status_code == 200:
            print("تم إرسال الإشعار إلى تيليجرام بنجاح.")
        else:
            print(f"فشل إرسال تيليجرام، كود الرد: {response.status_code}")
    except Exception as e:
        print("خطأ في إرسال تيليجرام:", e)

def clean(text):
    x = text.translate(AR).replace(",", "")
    x = "".join(c for c in x if c.isdigit() or c == ".").strip(".")
    return float(x) if x else None

def check_products():
    print(f"[{time.strftime('%H:%M:%S')}] جاري فحص أسعار التكييفات...")
    session = requests.Session()
    results_msg = f"❄️ *تقرير أسعار التكييفات (${time.strftime('%Y-%m-%d %H:%M')})*\n\n"
    
    success_count = 0
    
    for url in URLS_LIST:
        r = None
        # تجربة الاتصال المباشر أو عبر البروكسي
        if not PROXIES_LIST:
            try:
                r = session.get(url, headers=H, timeout=20)
            except Exception as e:
                print(f"خطأ في الاتصال بالرابط: {e}")
        else:
            for p in PROXIES_LIST:
                try:
                    r = session.get(url, headers=H, proxies=p, timeout=15)
                    if r.status_code == 200:
                        break
                except:
                    continue
        
        if not r or r.status_code != 200:
            results_msg += f"⚠️ تعذر الوصول لرابط منتج\n"
            continue
            
        try:
            s = BeautifulSoup(r.text, "html.parser")
            
            # استخراج اسم المنتج
            title_tag = s.select_one("#productTitle")
            name = title_tag.get_text(strip=True) if title_tag else "منتج بدون اسم"
            # اختصار الاسم قليلاً للوضوح في تيليجرام
            short_name = name[:50] + "..." if len(name) > 50 else name
            
            # استخراج السعر
            price_tag = s.select_one(".a-price .a-offscreen") or s.select_one("#priceblock_ourprice") or s.select_one(".a-price-whole")
            price_str = price_tag.get_text(strip=True) if price_tag else "غير متوفر"
            
            results_msg += f"🔹 [{short_name}]({url})\n💰 السعر: *{price_str}*\n\n"
            success_count += 1
            
        except Exception as e:
            print(f"خطأ في تحليل الصفحة: {e}")
            
    results_msg += f"✅ تم فحص {success_count} منتج بنجاح."
    send(results_msg)

if __name__ == "__main__":
    check_products()
    
