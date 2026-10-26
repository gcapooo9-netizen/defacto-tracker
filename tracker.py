import time
import requests
from bs4 import BeautifulSoup

TOKEN = "8996279782:AAEJ-n3vP4K9bts15GC0_htKMceRC4yHj8E"
CHAT = "5124680786"

SEARCH_URL = "https://www.amazon.eg/s?k=defacto"

H = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
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

def check_search_page():
    print(f"[{time.strftime('%H:%M:%S')}] جاري فحص صفحة منتجات ديفاكتو...")
    try:
        r = requests.get(SEARCH_URL, headers=H, timeout=25)
        if r.status_code != 200:
            error_msg = f"⚠️ تحذير: أمازون ردت بالكود {r.status_code} ولم يتم الفحص."
            print(error_msg)
            send(error_msg)
            return
            
        s = BeautifulSoup(r.text, "html.parser")
        items = s.select("div.s-result-item[data-asin]")
        
        found_count = 0
        for item in items:
            asin = item.get("data-asin")
            if not asin or len(asin) != 10:
                continue
                
            name_tag = item.select_one("h2 a span, .a-text-normal")
            name = name_tag.get_text(strip=True) if name_tag else f"منتج {asin}"
            
            price_tag = item.select_one(".a-price-whole")
            if not price_tag:
                continue
                
            price = clean(price_tag.get_text())
            if price is None:
                continue
                
            found_count += 1
            
        print(f"تم فحص {found_count} منتج بنجاح.")
        
        # 🔔 رسالة تأكيد تعمل في كل مرة يتشغيل فيها السكربت لكي تطمئن أنه شغال
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        send(f"✅ *السكربت يعمل الآن بنجاح!*\n\nوقت الفحص: `{current_time}`\nالمنتجات التي تم رصدها: *{found_count} منتج*")

    except Exception as e:
        err_msg = f"❌ حدث خطأ أثناء فحص الصفحة: {e}"
        print(err_msg)
        send(err_msg)

if __name__ == "__main__":
    check_search_page()
    
