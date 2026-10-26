import requests
from bs4 import BeautifulSoup

TOKEN = "8996279782:AAEJ-n3vP4K9bts15GC0_htKMceRC4yHj8E"
CHAT = "5124680786"

# رابط بحث مباشر لديفاكتو
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
        requests.post(u, json={"chat_id": CHAT, "text": msg, "parse_mode": "Markdown"}, timeout=15)
    except Exception as e:
        print("خطأ في إرسال تيليجرام:", e)

def clean(text):
    x = text.translate(AR).replace(",", "")
    x = "".join(c for c in x if c.isdigit() or c == ".").strip(".")
    return float(x) if x else None

def check_search_page():
    print("جاري فحص صفحة منتجات ديفاكتو...")
    try:
        r = requests.get(SEARCH_URL, headers=H, timeout=25)
        if r.status_code != 200:
            print(f"تحذير: أمازون ردت بالكود {r.status_code}")
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
                
            product_link = f"https://www.amazon.eg/dp/{asin}"
            
            # طباعة وتنبيه تجريبي للفحص
            print(f"تم رصد منتج: {name[:25]}... بسعر {price}")
            found_count += 1
            
        print(f"تم فحص {found_count} منتج بنجاح.")
        send(f"🟢 *تم فحص أمازون بنجاح*\nتم العثور وفحص {found_count} منتج لـ DeFacto.")

    except Exception as e:
        print("خطأ أثناء فحص الصفحة:", e)

if __name__ == "__main__":
    check_search_page()
    
