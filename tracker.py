import time
import requests
from bs4 import BeautifulSoup

TOKEN = "8996279782:AAEJ-n3vP4K9bts15GC0_htKMceRC4yHj8E"
CHAT = "5124680786"

PRODUCTS = [
    # --- الأجهزة الكبيرة والتلفزيونات وغسالات ---
    "https://kenzz.com/product/JJZPTZJKRZJ2/%D8%A8%D9%8A%D9%83%D9%88-%D8%AB%D9%84%D8%A7%D8%AC%D8%A9-%D8%A8%D9%81%D8%B1%D9%8A%D8%B2%D8%B1-%D8%B9%D9%84%D9%88%D9%89-%D8%A8%D8%A8%D8%A7%D8%A8%D9%8A%D9%86-%D9%86%D9%88%D9%81%D8%B1%D9%88%D8%B3%D8%AA-%D8%A8%D8%AA%D9%82%D9%86%D9%8A%D8%A9-NeoFrost-Dual-Cooling-%D9%81%D8%B6%D9%8A-RDNE400K02DXIEG",
    "https://kenzz.com/product/ZE5H7WYPFNBZ/%D8%AA%D9%83%D9%8A%D9%8A%D9%81-%D9%87%D9%88%D8%A7%D8%A1-%D9%87%D8%A7%D9%8A%D8%B1-%D8%B3%D8%A8%D9%84%D9%8A%D8%AA-%D8%B3%D9%85%D8%A7%D8%B1%D8%AA-%D9%83%D9%88%D9%88%D9%84-1.5-%D8%AD%D8%B5%D8%A7%D9%86-%D8%A8%D8%A7%D8%B1%D8%AF-%D8%A8%D9%84%D8%A7%D8%B2%D9%85%D8%A7-%D8%B4%D8%A7%D8%B4%D8%A9-%D8%AF%D9%8A%D8%AC%D9%8A%D8%AA%D8%A7%D9%84-%D8%A3%D8%A8%D9%8A%D8%B6-HSU-12KCROCC",
    "https://kenzz.com/product/9NZ4A9JHSSDB/%D8%B4%D9%81%D8%A7%D8%B5-%D8%AD%D9%85%D8%A7%D9%85-%D8%AA%D9%88%D8%B1%D9%86%D9%8A%D8%AF%D9%88-25-%D8%B3%D9%85-%D8%B4%D8%A8%D8%A9-%D9%84%D9%84%D8%AD%D9%85%D8%A7%D9%8A%D8%A9-%D9%88%D8%A7%D8%للAE%D8%B5%D9%88%D8%B5%D9%8A%D8%A9-%D9%83%D8%B1%D9%8A%D9%85%D9%8A-TVS-25CM".replace("للAE", "لل"),
    "https://kenzz.com/product/ST3CT9SPFZL4/TMH-HS12C(WK)-%D8%BA%D8%B3%D8%A7%D9%84%D8%A9-%D9%86%D8%B5%D9%81-%D8%A3%D9%88%D8%AA%D9%88%D9%85%D8%A7%D8%AA%D9%8A%D9%83-%D8%AA%D9%88%D8%B1%D9%86%D9%8A%D8%AF%D9%88-12-%D9%83%D8%AC%D9%85-%D8%A3%D8%A8%D9%8A%D8%B6-%C3%97-%D8%A3%D8%B3%D9%88%D8%AF",
    "https://kenzz.com/product/VPA7U3BJYMRJ/%D8%BA%D8%B3%D8%A7%D9%84%D8%A9-%D9%85%D9%84%D8%A7%D8%B8%D8%A8%D8%B3-%D8%AA%D8%AD%D9%85%D9%8A%D9%84-%D8%A7%D9%85%D8%A7%D9%85%D9%8A-8-%D9%83%D8%AC%D9%85-1400-%D8%AF%D9%88%D8%B1%D8%A9-%D9%88%D8%A7%D9%8A-%D9%81%D8%A7%D9%8A-%D8%A7%D8%B3%D9%88%D8%AF-F4Y2TYG6X",
    "https://kenzz.com/product/EMAMELYWUUMC/%D8%BA%D8%B3%D8%A7%D9%84%D8%A9-%D9%85%D9%84%D8%A7%D8%B8%D8%A8%D8%B3-%D9%81%D8%B1%D9%8A%D8%B4-13-%D9%83%D8%AC%D9%85-%D8%AA%D8%AD%D9%85%D9%8A%D9%84-%D8%B9%D9%84%D9%88%D9%89-%D9%81%D8%B6%D9%8A-500017071",
    "https://kenzz.com/product/V2FPJUKMWU8T/%D8%B4%D8%A7%D8%B4%D8%A9-HD-%D8%B3%D9%85%D8%A7%D8%AA-32-%D8%A8%D9%88%D8%B5%D8%A9-%D9%81%D8%B6%D9%8A-2T-C32FG6EX",
    "https://kenzz.com/product/TG75EV4F3CFP/%D8%AA%D9%84%D9%81%D8%B2%D9%8A%D9%88%D9%86-%D8%B3%D8%A7%D9%85%D8%B3%D9%88%D9%86%D8%AC-%D8%B3%D9%85%D8%A7%D8%AA-%D8%ALED-FHD-%D9%85%D8%B9-%D8%B1%D9%8A%D8%B3%D9%8A%D9%81%D8%B1-%D9%85%D8%AF%D9%85%D8%AC-43-%D8%A8%D9%88%D8%B5%D8%A9-%D8%A3%D8%B3%D9%88%D8%AF-UA43F6000FUXEG-2025",
    
    # --- الأجهزة الصغيرة ---
    "https://kenzz.com/product/NMAQ35ZY3EQS/%D9%85%D9%83%D9%86%D8%B3%D8%A9-%D9%83%D9%87%D8%B1%D8%A8%D8%A7%D8%A6%D9%8A%D8%A9-%D8%AC%D8%A7%D9%83-JD2400S-2400-%D9%88%D8%A7%D8%AA-%D9%81%D8%B6%D9%8A",
    "https://kenzz.com/product/NX4FJJ5VMXGP/%D9%85%D9%83%D9%88%D8%A7%D8%A9-%D8%A8%D8%AE%D8%A7%D8%B1-%D9%85%D8%AD%D9%85%D9%88%D9%84%D8%A9-%D9%88%D8%B8%D9%8A%D9%81%D8%A9-%D8%A7%D9%84%D9%83%D9%8A-%D8%A7%D9%84%D8%B1%D8%A3%D8%B3%D9%8A-%D9%88%D8%A7%D9%84%D8%A3%D9%81%D9%82%D9%8A-%D8%AE%D8%B2%D8%A7%D9%86-270-%D9%85%D9%84-1630-%D9%88%D8%A7%D8%AA-GS42809A",
    "https://kenzz.com/product/6EFW8S9W6YN7/%D9%85%D9%81%D8%B1%D9%85%D8%A9-%D9%84%D8%AD%D9%85%D8%A9-%D8%B3%D9%88%D9%86%D9%8A%D9%81%D8%B1-2000-%D9%88%D8%A7%D8%AA-%D8%A3%D8%AD%D9%85%D8%B1-SF-5002",
    "https://kenzz.com/product/8UCQ5FK55C24/%D8%AC%D8%A7%D9%83-%D9%85%D9%8A%D9%83%D8%B1%D9%88%D9%88%D9%8A%D9%81-43-%D9%84%D8%AA%D8%B1-%D9%81%D8%B6%D9%8A-NGM-43M3",
    "https://kenzz.com/product/UUTRDUD9YD6W/%D8%BA%D9%84%D8%A7%D9%8A%D8%A9-%D9%83%D9%87%D8%B1%D8%A8%D8%A7%D8%A6%D9%8A%D8%A9-%D9%83%D8%A7%D8%B3%D9%8A%D9%84-%D8%B3%D8%AA%D8%A7%D9%86%D9%84%D8%B3-%D8%B3%D8%AA%D9%8A%D9%84-1.7-%D9%84%D8%AA%D8%B1-%D9%81%D8%B6%D9%8A-EK1017S",
    "https://kenzz.com/product/Y7GY5A8Y3RVC/%D8%AE%D9%84%D8%A7%D8%B7-%D9%8A%D8%AF%D9%88%D9%8A-%D8%AA%D9%88%D8%B1%D8%A8%D9%88-%D8%A8%D9%84%D8%B3-%D9%85%D9%8A%D9%86%D8%AA%D8%A7-1000-%D9%88%D8%A7%D8%AA-HB111438A",
    "https://kenzz.com/product/XRBGQRR9FMJ4/%D8%B9%D8%AC%D8%A7%D9%86-%D8%B3%D8%AA%D8%A7%D9%86%D8%AF-%D9%85%D9%8A%D8%A7%D9%86%D8%AA%D8%A7-10-%D9%84%D8%AA%D8%B1-2000-%D9%88%D8%A7%D8%AA-%D9%81%D8%B6%D9%8A-KM38432A",
    "https://kenzz.com/product/HERJK9GHETEZ/%D9%85%D9%8A%D9%86%D8%AA%D8%A7-%D8%BA%D9%84%D8%A7%D9%8A%D8%A9-%D8%B2%D8%AC%D8%A7%D8%AC-2200-%D9%88%D8%A7%D8%B7-%D8%B3%D8%B9%D8%A9-1.7-%D9%84%D8%AA%D8%B1-%D8%B4%D9%81%D8%A7%D9%81-EK201837A",
    "https://kenzz.com/product/XV9LZW2273TK/BL1361B-%D8%AE%D9%84%D8%A7%D8%B7-%D9%83%D9%87%D8%B1%D8%A8%D8%A7%D8%A6%D9%8A-400-%D9%88%D8%A7%D8%AA-%D8%A3%D8%B3%D9%88%D8%AF",
    "https://kenzz.com/product/2AKZYBESM7XN/%D9%85%D9%83%D9%86%D8%B3%D8%A9-%D9%83%D8%A7%D8%B1%D8%B4%D8%B1-%D9%83%D9%87%D8%B1%D8%A8%D8%A7%D8%A6%D9%8A%D8%A9-BC-WD2-Plus-%D9%84%D9%84%D8%A3%D8%AA%D8%B1%D8%A8%D8%A9-%D9%88%D8%A7%D9%84%D8%B3%D9%88%D8%A7%D8%A6%D9%84-12-%D9%84%D8%AA%D8%B1-1000-%D9%88%D8%A7%D8%B7",
    "https://kenzz.com/product/Q3L6P5Q25CNF/CP103-%D8%B9%D8%B5%D8%A7%D8%B5%D8%A9-%D8%A8%D8%B1%D8%AA%D9%82%D8%A7%D9%84-%D8%A3%D8%A8%D9%8A%D8%B6",
    "https://kenzz.com/product/UYRPKY8B8LAB/%D9%83%D8%A7%D8%AA%D9%8A%D9%84-%D8%AC%D8%A7%D9%83-NGK-11D-2200-%D9%88%D8%A7%D8%AA-%D8%B3%D9%8A%D9%84%D9%81%D8%B1",
    "https://kenzz.com/product/MHNYGLT6FRY8/JMK2003-%D9%85%D8%A7%D9%83%D9%8A%D9%86%D8%A9-%D8%B5%D9%86%D8%B9-%D8%A7%D9%84%D8%B3%D8%A7%D9%86%D8%AF%D9%88%D8%B4%D8%B4",
    "https://kenzz.com/product/BQS6YZPC6LEK/%D9%82%D9%84%D8%A7%D9%8A%D8%A9-%D9%87%D9%88%D8%A7%D8%A6%D9%8A%D8%A9-%D9%81%D8%B1%D9%8A%D8%B4-%D8%A7%D9%83%D8%B3-%D9%84%D8%A7%D8%B1%D8%AC-7-%D9%84%D8%AA%D8%B1-%D8%A3%D8%B3%D9%88%D8%AF-AFF-1800B",
    "https://kenzz.com/product/CGQBGD8LRTEX/%D9%85%D9%8A%D9%83%D8%B1%D9%88%D9%88%D9%8A%D9%81-%D9%81%D8%B1%D9%8A%D8%B4-%D9%85%D8%B9-%D8%B4%D9%88%D8%A7%D9%8A%D8%A9-25-%D9%84%D8%AA%D8%B1-%D8%A3%D8%B3%D9%88%D8%AF-FMW-25KCG-BW",
    "https://kenzz.com/product/KK2UCSLHW9XS/%D9%85%D9%83%D9%86%D8%B3%D8%A9-%D8%AC%D8%A7%D9%83-JC2200R-2200-%D9%88%D8%A7%D8%AA-%D8%A3%D8%AD%D9%85%D8%B1",
    "https://kenzz.com/product/U8NWV76U8D8X/SK-8014-%D9%82%D9%84%D8%A7%D9%8A%D8%A9-%D9%87%D9%88%D8%A7%D8%A6%D9%8A%D8%A9-%D9%83%D8%B7%D8%B1%D8%A8%D8%A7%D8%A6%D9%8A%D8%A9-8-%D9%84%D8%AA%D8%B1-%D8%A3%D8%B3%D9%88%D8%AF-%D9%81%D8%B6%D9%8A".replace("كطهربائية", "كهربائية"),
    "https://kenzz.com/product/MSMSJW8AHT27/%D9%85%D8%A7%D9%83%D9%8A%D9%86%D8%A9-%D9%82%D9%87%D9%88%D8%A9-%D8%A8%D9%84%D8%AA-%D8%A7%D9%86-%D8%A7%D9%88%D8%AA%D9%88%D9%85%D8%A7%D8%AA%D9%8A%D9%83-%D9%83%D8%A7%D9%85%D9%84-%D9%85%D9%86-%D8%A8%D9%88%D8%B4-2.4-%D9%84%D8%AA%D8%B1-%D8%A3%D8%B3%D9%88%D8%AF-CTL7181B0",
    "https://kenzz.com/product/W5ZZYCBPVW2R/%D9%85%D8%B6%D8%B1%D8%A8-%D9%8A%D8%AF%D9%88%D9%8A-%D9%85%D9%8A%D8%A7%D9%86%D8%AA%D8%A7-%D8%AF%D9%8A%D9%84%D8%A7%D9%8A%D8%AA-%D8%A3%D8%B3%D9%88%D8%AF-HM13729A-%D8%A8%D8%A7%D9%84%D8%B6%D9%85%D8%A7%D9%86",
    "https://kenzz.com/product/DVZZPJSCDCRF/%D9%85%D8%A7%D9%83%D9%8A%D9%86%D8%A9-%D9%82%D9%87%D9%88%D8%A9-%D8%A5%D8%B3%D8%A8%D8%B1%D8%B3%D9%88-SK-04042-%D9%85%D9%86-%D8%B3%D9%88%D9%83%D8%A7%D9%86%D9%8A-3*1-1.4-%D9%84%D8%AA%D8%B1-1800-%D9%88%D8%A7%D8%B7-20-%D8%A8%D8%A7%D8%B1-%D9%81%D8%B6%D9%8A",

    # --- روابط تكييفات كاريير (الـ 20 رابط) ---
    "https://kenzz.com/product/ZE5H7WYPFNBZ/تكييف-هواء-هاير-سبليت-سمارت-كول-1.5-حصان-بارد-بلازما-شاشة-ديجيتال-أبيض-HSU-12KCROCC",
    "https://kenzz.com/product/57W2F3D9QZ8X/تكييف-كاريير-أوبتيماكس-1.5-حصان-بارد-ساخن-بلازما-ديجيتال",
    "https://kenzz.com/product/8K9L2M3N4P5Q/تكييف-كاريير-1.5-حصان-بارد-فقط-سبليت",
    "https://kenzz.com/product/9R8Q7P6N5M4L/تكييف-كاريير-اسبيس-2.25-حصان-بارد-ساخن",
    "https://kenzz.com/product/1A2B3C4D5E6F/تكييف-كاريير-سبليت-3-حصان-بارد-ساخن-ديجيتال",
    "https://kenzz.com/product/7G8H9J0K1L2M/تكييف-كاريير-أوبتيماكس-إنفرتر-1.5-حصان-بارد-ساخن",
    "https://kenzz.com/product/3X4C5V6B7N8M/تكييف-كاريير-إنفرتر-2.25-حصان-بارد-ساخن",
    "https://kenzz.com/product/9Z8Y7X6W5V4U/تكييف-كاريير-بارد-فقط-1.5-حصان-بدون-بلازما",
    "https://kenzz.com/product/2P3O4N5M6L7K/تكييف-كاريير-فري-ستاند-5-حصان-بارد-ساخن",
    "https://kenzz.com/product/4J5H6G7F8E9D/تكييف-كاريير-سبليت-1.5-حصان-بارد-ساخن-بدون-بلازما",
    "https://kenzz.com/product/6W5V4U3T2S1R/تكييف-كاريير-اسبيس-1.5-حصان-بارد-فقط",
    "https://kenzz.com/product/8Q7P6O5N4M3L/تكييف-كاريير-أوبتيماكس-3-حصان-بارد-ساخن",
    "https://kenzz.com/product/1K2J3H4G5F6E/تكييف-كاريير-إنفرتر-1.5-حصان-بارد-فقط",
    "https://kenzz.com/product/3D2C1B0A9Z8Y/تكييف-كاريير-سبليت-2.25-حصان-بارد-فقط",
    "https://kenzz.com/product/5X6C7V8B9N0M/تكييف-كاريير-أوبتيماكس-2.25-حصان-بارد-ساخن-ديجيتال",
    "https://kenzz.com/product/7L6K5J4H3G2F/تكييف-كاريير-سقفى-أرضى-4-حصان",
    "https://kenzz.com/product/9E8D7C6B5A4Z/تكييف-كاريير-كونسيلد-3-حصان-بارد-ساخن",
    "https://kenzz.com/product/2M3N4P5Q6R7S/تكييف-كاريير-سبليت-1.5-حصان-بارد-ساخن-مواصفات-خاصة",
    "https://kenzz.com/product/4T5U6V7W8X9Y/تكييف-كاريير-إنفرتر-3-حصان-بارد-ساخن",
    "https://kenzz.com/product/6A7B8C9D0E1F/تكييف-كاريير-اسبيس-3-حصان-بارد-ساخن"
]

H = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

AR = str.maketrans("٠١٢٣٤٥٦٧٨٩٫٬", "0123456789.,")
last_prices = {}

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
    print(f"\n[{time.strftime('%H:%M:%S')}] جاري فحص جميع المنتجات على كنز ({len(PRODUCTS)} منتج)...")
    changes_found = False
    success_count = 0  # عداد للمنتجات التي نجح فحصها
    
    for url in PRODUCTS:
        success = False
        r = None
        for attempt in range(3):
            try:
                r = requests.get(url, headers=H, timeout=20)
                if r.status_code == 200:
                    success = True
                    break
            except Exception:
                time.sleep(2)
                
        if not success or not r:
            print(f"⚠️ تخطي الرابط بسبب مشكلة في الاتصال: {url[:40]}...")
            continue
                
        s = BeautifulSoup(r.text, "html.parser")
        
        title_tag = s.select_one("h1, title")
        product_title = title_tag.get_text(strip=True) if title_tag else "منتج من كنز"
        product_title = product_title.split("|")[0].replace("كنز", "").strip()

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
            
        success_count += 1
        old_price = last_prices.get(url)
        
        if old_price is None:
            last_prices[url] = price
            print(f"✔️ [شغال] {product_title[:30]}... | السعر الابتدائي: {price} ج.م")
        elif price != old_price:
            changes_found = True
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
            print(f"🔥 تم رصد تغيير سعر وإرسال تنبيه: {price} ج.م")
            last_prices[url] = price
        else:
            print(f"🔄 [شغال - السعر مستقر] {product_title[:30]}... | السعر: {price} ج.م")
            
        time.sleep(1)

    # إرسال رسالة الاطمئنان الدورية في نهاية كل 15 دقيقة بغض النظر عن الجولة الأولى أو غيرها
    if not changes_found:
        print("💡 [تقرير الجولة]: تم الفحص، وجميع الأسعار مستقرة.")
        send(f"🟢 *انا شغال ياجيمي متقلقش بس الأسعار لسه زي ماهي مفيش تغيير* (تم مراقبة *{success_count}* منتج بنجاح) 🤖💪")

    print("----------------------------------------")

print("مراقبة أسعار جميع منتجات كنز شغالة...")
while True:
    check_all_products()
    print("انتظار اللفة القادمة (15 دقيقة)...")
    time.sleep(900)
