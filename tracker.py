import time
import random
import html
import ssl
import json
import os
import re
import requests
import cloudscraper
from bs4 import BeautifulSoup

# ⚠️ التوكن ومعرف الشات الخاص بك
TOKEN = "8996279782:AAEJ-n3vP4K9bts15GC0_htKMceRC4yHj8E"
CHAT = "5124680786"

# قائمة الروابط الجديدة المحدثة لأمازون مصر
TARGET_URLS = [
    "https://www.amazon.eg/dp/B0C2CYJWY2",
    "https://www.amazon.eg/dp/B09MFLRNLG",
    "https://www.amazon.eg/dp/B098TYYKV6",
    "https://www.amazon.eg/dp/B0FTXSSZNC",
    "https://www.amazon.eg/dp/B0DFGF6R1Y",
    "https://www.amazon.eg/dp/B0CH5GF552",
    "https://www.amazon.eg/dp/B0FNP57TXV",
    "https://www.amazon.eg/dp/B0CSC1THJX",
    "https://www.amazon.eg/dp/B0CQZD4LWQ",
    "https://www.amazon.eg/dp/B0CRPSZ7N6",
    "https://www.amazon.eg/dp/B091J78TZ5",
    "https://www.amazon.eg/dp/B0HJWGYCTN",
    "https://www.amazon.eg/dp/B0B9LDTJJP",
    "https://www.amazon.eg/dp/B0FNNRNQ4B",
    "https://www.amazon.eg/dp/B0FKBYJ64T",
    "https://www.amazon.eg/dp/B0CQ5GKMPL",
    "https://www.amazon.eg/dp/B0B3JMTM3Z",
    "https://www.amazon.eg/dp/B0GDS42Q14",
    "https://www.amazon.eg/dp/B0FTXSNDBZ",
    "https://www.amazon.eg/dp/B0FX75KGV9",
    "https://www.amazon.eg/dp/B0BCQ6L1Y8",
    "https://www.amazon.eg/dp/B0BFNRPJP7",
    "https://www.amazon.eg/dp/B09YKTXFY2",
    "https://www.amazon.eg/dp/B0BXJMGQYK",
    "https://www.amazon.eg/dp/B0BVRTTDT2",
    "https://www.amazon.eg/dp/B0DL69L4RC",
    "https://www.amazon.eg/dp/B09KS3GVHR",
    "https://www.amazon.eg/dp/B0CYPMQT3S",
    "https://www.amazon.eg/dp/B07QFTGGYF",
    "https://www.amazon.eg/dp/B096912R56",
    "https://www.amazon.eg/dp/B0B4PSGD6X",
    "https://www.amazon.eg/dp/B091J7R59S",
    "https://www.amazon.eg/dp/B0DJPZVG8D",
    "https://www.amazon.eg/dp/B0H7Z3MPV8",
    "https://www.amazon.eg/dp/B0BVQ6HCQY",
    "https://www.amazon.eg/dp/B0G6VKVWLK",
    "https://www.amazon.eg/dp/B0FT6NDZCK",
    "https://www.amazon.eg/dp/B0HH8VZQJY",
    "https://www.amazon.eg/dp/B08WJMHSDD",
    "https://www.amazon.eg/dp/B0BG8SS6MC",
    "https://www.amazon.eg/dp/B0FTXT7RS6",
    "https://www.amazon.eg/dp/B0CYPP8GSS",
    "https://www.amazon.eg/dp/B0BJ8C2BTB",
    "https://www.amazon.eg/dp/B0DFG64F2P",
    "https://www.amazon.eg/dp/B0B4PRGZ46",
    "https://www.amazon.eg/dp/B0BRY46RBG",
    "https://www.amazon.eg/dp/B0CRPRWQFM",
    "https://www.amazon.eg/dp/B0CKRYK34Q",
    "https://www.amazon.eg/dp/B0CRPPJSSV",
    "https://www.amazon.eg/dp/B0DH3P2NQZ",
    "https://www.amazon.eg/dp/B0BG8RTDL5",
    "https://www.amazon.eg/dp/B0DG5S8B44",
    "https://www.amazon.eg/dp/B0F6CYBZ9W",
    "https://www.amazon.eg/dp/B0CQ5JYFH2",
    "https://www.amazon.eg/dp/B0GC6SKWCC",
    "https://www.amazon.eg/dp/B07S9GRDXX",
    "https://www.amazon.eg/dp/B0HDZTVR7J",
    "https://www.amazon.eg/dp/B0D3C4Z68W",
    "https://www.amazon.eg/dp/B0DY8DWRTT",
    "https://www.amazon.eg/dp/B0HLXZV3S3",
    "https://www.amazon.eg/dp/B0CL6S3V1J",
    "https://www.amazon.eg/dp/B0CQ5HCC1F",
    "https://www.amazon.eg/dp/B07GC81YFX",
    "https://www.amazon.eg/dp/B0DWYX6KJ5",
    "https://www.amazon.eg/dp/B0GMXZNY9L",
    "https://www.amazon.eg/dp/B0D2D74MTH"
]

DB_FILE = "custom_products.json"

H = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Upgrade-Insecure-Requests": "1",
    "Connection": "keep-alive"
}

AR = str.maketrans("٠١٢٣٤٥٦٧٨٩٫٬", "0123456789.,")

if os.path.exists(DB_FILE):
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            last_prices = json.load(f)
        print(f"📂 تم استرجاع {len(last_prices)} منتج محفوظ من قبل.")
    except Exception:
        last_prices = {}
else:
    last_prices = {}

def save_prices():
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(last_prices, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("خطأ في حفظ الملف:", e)

def create_scraper():
    ctx = ssl.create_default_context()
    ctx.set_ciphers("DEFAULT@SECLEVEL=1")
    scraper = cloudscraper.create_scraper(
        browser={"browser": "chrome", "platform": "windows", "desktop": True},
        ssl_context=ctx
    )
    scraper.headers.update(H)
    return scraper

scraper = create_scraper()

def send(msg):
    u = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        res = requests.post(
            u, 
            json={"chat_id": CHAT, "text": msg, "parse_mode": "HTML", "disable_web_page_preview": False}, 
            timeout=15
        )
        if res.status_code != 200:
            print("مشكلة من تيليجرام:", res.text)
        time.sleep(1)
    except Exception as e:
        print("خطأ في إرسال تيليجرام:", e)

def clean(text):
    x = text.translate(AR).replace(",", "")
    m = re.search(r"\d+(?:\.\d+)?", x)
    return float(m.group(0)) if m else None

def extract_product_name(soup, url):
    for selector in ["span#productTitle", "h1.a-size-large", "#title"]:
        tag = soup.select_one(selector)
        if tag:
            text = tag.get_text(strip=True)
            if text:
                return text
    return f"منتج ({url})"

def extract_price(soup):
    for selector in [".a-price .a-offscreen", "#priceblock_ourprice", "#priceblock_dealprice", ".a-color-price"]:
        tag = soup.select_one(selector)
        if tag:
            p = clean(tag.get_text())
            if p is not None and p > 0:
                return p
    return None

def check_products():
    global scraper
    print(f"[{time.strftime('%H:%M:%S')}] جاري فحص المنتجات المخصصة ({len(TARGET_URLS)} رابط)...")
    
    if not TARGET_URLS:
        print("⚠️ قائمة الروابط فارغة!")
        return False

    updated_any = False

    for product_link in TARGET_URLS:
        try:
            r = scraper.get(product_link, timeout=20)
            if r.status_code != 200:
                print(f"تحذير: أمازون ردت بالكود {r.status_code} للرابط: {product_link}")
                continue

            if "api-services-support@amazon.com" in r.text or "Enter the characters you see below" in r.text:
                print("⚠️ أمازون طلبت كابتشا. تجديد الجلسة والانتظار قليلاً...")
                scraper = create_scraper()
                time.sleep(5)
                continue

            soup = BeautifulSoup(r.text, "html.parser")
            price = extract_price(soup)
            
            if price is None:
                print(f"⚠️ تعذر استخراج السعر للرابط: {product_link}")
                continue

            raw_name = extract_product_name(soup, product_link)
            safe_name = html.escape(raw_name)
            old_price = last_prices.get(product_link)

            if old_price is None:
                last_prices[product_link] = price
                updated_any = True
                print(f"✨ تسجيل أول للمنتج: {raw_name} | السعر: {price} ج.م")

            elif price != old_price:
                diff = price - old_price
                
                if diff < 0:
                    discount_percentage = abs(diff) / old_price * 100
                    print(f"📉 نزول سعر: {raw_name} | من {old_price} إلى {price} (نسبة الخصم: {discount_percentage:.1f}%)")
                    
                    if discount_percentage > 20:
                        msg = (
                            f"🔥 <b>لقطة! تخفيض أكتر من 20%!</b>\n\n"
                            f"📦 <a href='{product_link}'>{safe_name}</a>\n"
                            f"📉 نسبة الخصم: <b>{discount_percentage:.1f}%</b>\n"
                            f"من: <s>{old_price}</s> ج.م\n"
                            f"إلى: <b>{price} ج.م</b>"
                        )
                        send(msg)
                else:
                    print(f"📈 زيادة سعر (تم التجاهل): {raw_name} من {old_price} إلى {price} ج.م")

                last_prices[product_link] = price
                updated_any = True
            else:
                print(f"✔️ مستقر: {raw_name} | السعر: {price} ج.م")

            time.sleep(random.uniform(1.5, 3))

        except Exception as e:
            print(f"خطأ أثناء فحص الرابط {product_link}:", e)
            scraper = create_scraper()

    if updated_any:
        save_prices()

    return True

if __name__ == "__main__":
    check_products()
