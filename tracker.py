import time
import requests
from bs4 import BeautifulSoup

TOKEN = "8996279782:AAEJ-n3vP4K9bts15GC0_htKMceRC4yHj8E"
CHAT = "5124680786"

# قائمة المنتجات الجديدة (الروابط)
PRODUCTS = [
    "https://kenzz.com/product/JJZPTZJKRZJ2/%D8%A8%D9%8A%D9%83%D9%88-%D8%AB%D9%84%D8%A7%D8%AC%D8%A9-%D8%A8%D9%81%D8%B1%D9%8A%D8%B2%D8%B1-%D8%B9%D9%84%D9%88%D9%8A-%D8%A8%D8%A8%D8%A7%D8%A8%D9%8A%D9%86-%D9%86%D9%88%D9%81%D8%B1%D9%88%D8%B3%D8%AA-%D8%A8%D8%AA%D9%82%D9%86%D9%8A%D8%A9-NeoFrost-Dual-Cooling-%D9%81%D8%B6%D9%8A-RDNE400K02DXIEG",
    "https://kenzz.com/product/ZE5H7WYPFNBZ/%D8%AA%D9%83%D9%8A%D9%8A%D9%81-%D9%87%D9%88%D8%A7%D8%A1-%D9%87%D8%A7%D9%8A%D8%B1-%D8%B3%D8%A8%D9%84%D9%8A%D8%AA-%D8%B3%D9%85%D8%A7%D8%B1%D8%AA-%D9%83%D9%88%D9%88%D9%84-1.5-%D8%AD%D8%B5%D8%A7%D9%86-%D8%A8%D8%A7%D8%B1%D8%AF-%D8%A8%D9%84%D8%A7%D8%B2%D9%85%D8%A7-%D8%B4%D8%A7%D8%B4%D8%A9-%D8%AF%D9%8A%D8%AC%D9%8A%D8%AA%D8%A7%D9%84-%D8%A3%D8%A8%D9%8A%D8%B6-HSU-12KCROCC",
    "https://kenzz.com/product/NMAQ35ZY3EQS/%D9%85%D9%83%D9%86%D8%B3%D8%A9-%D9%83%D9%87%D8%B1%D8%A8%D8%A7%D8%A6%D9%8A%D8%A9-%D8%AC%D8%A7%D9%83-JD2400S-2400-%D9%88%D8%A7%D8%AA-%D9%81%D8%B6%D9%8A",
    "https://kenzz.com/product/9NZ4A9JHSSDB/%D8%B4%D9%81%D8%A7%D8%B7-%D8%AD%D9%85%D8%A7%D9%85-%D8%AA%D9%88%D8%B1%D9%86%D9%8A%D8%AF%D9%88-25-%D8%B3%D9%85-%D8%B4%D8%A8%D9%83%D8%A9-%D9%84%D9%84%D8%AD%D9%85%D8%A7%D9%8A%D8%A9-%D9%88%D8%A7%D9%84%D8%AE%D8%B5%D9%88%D8%B5%D9%8A%D8%A9-%D9%83%D8%B1%D9%8A%D9%85%D9%8A-TVS-25CM",
    "https://kenzz.com/product/ST3CT9SPFZL4/TMH-HS12C(WK)-%D8%BA%D8%B3%D8%A7%D9%84%D8%A9-%D9%86%D8%B5%D9%81-%D8%A3%D9%88%D8%AA%D9%88%D9%85%D8%A7%D8%AA%D9%8A%D9%83-%D8%AA%D9%88%D8%B1%D9%86%D9%8A%D8%AF%D9%88-12-%D9%83%D8%AC%D9%85-%D8%A3%D8%A8%D9%8A%D8%B6-%C3%97-%D8%A3%D8%B3%D9%88%D8%AF",
    "https://kenzz.com/product/VPA7U3BJYMRJ/%D8%BA%D8%B3%D8%A7%D9%84%D8%A9-%D9%85%D9%للائحة-%D9%85%D9%84%D8%A7%D8%A8%D8%B3-%D8%AA%D8%AD%D9%85%D9%8A%D9%84-%D8%A7%D9%85%D8%A7%D9%85%D9%8A-8-%D9%83%D8%AC%D9%85-1400-%D8%AF%D9%88%D8%B1%D8%A9-%D9%88%D8%A7%D9%8A-%D9%81%D8%A7%D9%8A-%D8%A7%D8%B3%D9%88%D8%AF-F4Y2TYG6X",
    "https://kenzz.com/product/EMAMELYWUUMC/%D8%BA%D8%B3%D8%A7%D9%84%D8%A9-%D9%85%D9%84%D8%A7%D8%A8%D8%B3-%D9%81%D8%B1%D9%8A%D8%B4-13-%D9%83%D8%AC%D9%85-%D8%AA%D8%AD%D9%85%D9%8A%D9%84-%D8%B9%D9%84%D9%88%D9%89-%D9%81%D8%B6%D9%8A-500017071",
    "https://kenzz.com/product/V2FPJUKMWU8T/%D8%B4%D8%A7%D8%B4%D8%A9-HD-%D8%B3%D9%85%D8%A7%D8%B1%D8%AA-32-%D8%A8%D9%88%D8%B5%D8%A9-%D9%81%D8%B6%D9%8A-2T-C32FG6EX",
    "https://kenzz.com/product/TG75EV4F3CFP/%D8%AA%D9%84%D9%81%D8%B2%D9%8A%D9%88%D9%86-%D8%B3%D8%A7%D9%85%D8%B3%D9%88%D9%86%D8%AC-%D8%B3%D9%85%D8%A7%D8%B1%D8%AA-LED-FHD-%D9%85%D8%B9-%D8%B1%D9%8A%D8%B3%D9%8A%D9%81%D8%B1-%D9%85%D8%AF%D9%85%D8%AC-43-%D8%A8%D9%88%D8%B5%D8%A9-%D8%A3%D8%B3%D9%88%D8%AF-UA43F6000FUXEG-2025"
]

H = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

AR = str.maketrans("٠١٢٣٤٥٦٧٨٩٫٬", "0123456789.,")
last_prices = {} # لتخزين أسعار كل المنتجات

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

def check_all_products():
    print(f"\n[{time.strftime('%H:%M:%S')}] جاري فحص قائمة المنتجات على كنز ({len(PRODUCTS)} منتج)...")
    
    for url in PRODUCTS:
        try:
            r = requests.get(url, headers=H, timeout=20)
            if r.status_code != 200:
                continue
                
            s = BeautifulSoup(r.text, "html.parser")
            
            # استخراج اسم المنتج
            title_tag = s.select_one("h1, title")
            product_title = title_tag.get_text(strip=True) if title_tag else "منتج من كنز"
            product_title = product_title.split("|")[0].replace("كنز", "").strip()

            # البحث عن السعر
            price_tag = s.select_one(".price, span[class*='price'], div[class*='price']")
            price = None
            if price_tag:
                price = clean(price_tag.get_text())
                
            if not price:
                for el in s.find_all(True):
                    t = el.get_text(strip=True)
                    if ("ج.م" in t or "جنيه" in t) and len(t) < 20:
                        p = clean(t)
                        if p and p > 50:
                            price = p
                            break
                            
            if not price:
                continue
                
            print(f"-> تم فحص: {product_title[:35]}... | السعر: {price} ج.م")
            
            old_price = last_prices.get(url)
            
            if old_price is None:
                last_prices[url] = price
                # إشعار أولي عند أول تشغيل لكل منتج للتأكد
                send(
                    f"🟢 *بدء مراقبة منتج جديد!*\n\n"
                    f"📦 {product_title}\n\n"
                    f"💰 السعر الحالي: *{price} ج.م*\n"
                    f"🛒 [رابط المنتج]({url})"
                )
            elif price != old_price:
                diff = price - old_price
                status = "📉 نزل" if diff < 0 else "📈 زاد"
                msg = (
                    f"🚨 *تغيير سعر منتج على كنز!*\n\n"
                    f"📦 {product_title}\n\n"
                    f"الحالة: {status}\n"
                    f"من: `~{old_price}~ ج.م`\n"
                    f"إلى: *{price} ج.م*\n\n"
                    f"🛒 [رابط المنتج]({url})"
                )
                send(msg)
                print(f"*** تم إرسال تنبيه بتغير سعر منتج إلى: {price} ج.م ***")
                last_prices[url] = price
                
            time.sleep(2) # فاصل بسيط بين كل منتج والتاني عشان ريح السيرفر

        except Exception as e:
            print(f"خطأ في فحص رابط: {e}")

    print("----------------------------------------")

print("مراقبة قائمة منتجات كنز شغالة...")
while True:
    check_all_products()
    print("انتظار اللفة القادمة (15 دقيقة)...")
    time.sleep(900)
