import requests
import time
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
        requests.post(u, json={"chat_id": CHAT, "text": msg, "parse_mode": "Markdown"}, timeout=15)
    except Exception as e:
        print("خطأ في إرسال تيليجرام:", e)

def check_messages():
    """التحقق من الرسائل الواردة من تيليجرام والرد عليها"""
    u = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    try:
        r = requests.get(u, timeout=10)
        data = r.json()
        if data.get("ok") and data.get("result"):
            for update in data["result"]:
                message = update.get("message", {})
                msg_text = message.get("text", "")
                sender_id = str(message.get("from", {}).get("id", ""))
                
                # لو الرسالة جاية منك، رد عليه فوراً بالكلمات اللي طلبتها
                if sender_id == CHAT and msg_text:
                    send("اطمن انا شغال وبراقب ياجيمي 🤖⚡")
    except Exception as e:
        print("خطأ في استقبال الرسائل:", e)

def clean(text):
    x = text.translate(AR).replace(",", "")
    x = "".join(c for c in x if c.isdigit() or c == ".").strip(".")
    return float(x) if x else None

def check_search_page():
    print("جاري فحص صفحة منتجات ديفاكتو...")
    try:
        r = requests.get(SEARCH_URL, headers=H, timeout=25)
        if r.status_code != 200:
            send(f"⚠️ تحذير: أمازون ردت بالكود {r.status_code}")
            return
            
        s = BeautifulSoup(r.text, "html.parser")
        items = s.select("div.s-result-item[data-asin]")
        
        found_count = 0
        report = "📦 *تقرير مراقبة DeFacto:* \n\n"
        
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
            if found_count <= 5:
                report += f"▪️ {name[:30]}...\n💰 السعر: {price} ج.م\n🔗 [رابط المنتج](https://www.amazon.eg/dp/{asin})\n\n"
            
        report += f"📊 إجمالي المنتجات المفحوصة: {found_count}"
        send(report)

    except Exception as e:
        send(f"❌ حصل خطأ أثناء الفحص يا جيمي: {str(e)}")

if __name__ == "__main__":
    # أول ما يشتغل، يشيك على الرسائل ويرد، وبعدين يفحص الأسعار
    check_messages()
    check_search_page()
