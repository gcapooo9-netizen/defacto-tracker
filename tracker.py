import time
import requests
from bs4 import BeautifulSoup

TOKEN = "8996279782:AAEJ-n3vP4K9bts15GC0_htKMceRC4yHj8E"
CHAT = "5124680786"

PRODUCTS = [
    "https://kenzz.com/en/product/LUBX8N7XUA4Q/LG-Dual-Cool-Split-Air-Conditioner-3-HP%2C-Cooling-%26-Heating-White-S4-W24K22ME",
    "https://kenzz.com/product/44N3SYU6UF7Q/%D8%AA%D9%83%D9%8A%D9%8A%D9%81-%D8%B3%D8%A8%D9%84%D9%8A%D8%AA-%D9%87%D8%A7%D9%8A%D8%B1-1.5-%D8%AD%D8%B5%D8%A7%D9%86-%D8%A8%D8%A7%D8%B1%D8%AF-%D9%88%D8%B3%D8%A7%D8%AE%D9%86-%D8%A3%D8%A8%D9%8A%D8%B6-HSU-12KHROCC",
    "https://kenzz.com/en/product/9STXGD9JPN4W/Midea-Split-Air-Conditioner-1.5-HP-Cooling-Only-White-MSC1T-12CR-N",
    "https://kenzz.com/en/product/2XR8F6QXNC3P/LG-Split-Air-Conditioner-3-HP%2C-Cooling-%26-Heating-Black-S4-W24K2RME",
    "https://kenzz.com/en/product/T8MG5MHABR3B/Midea-Mission-Pro-Air-Conditioner-3-HP-Cooling-and-Heating-White-MSC1T-24HR-N-F",
    "https://kenzz.com/en/product/NQRBU36VQXAA/Carrier-Optimax-Pro-Cooling-Split-Air-Conditioner-1.5-HP-White-53KHCT12N-708",
    "https://kenzz.com/en/product/PB7EMU9ZX59K/Haier-Split-Air-Conditioner-1.5-HP%2C-Cooling-Only-White-HSU-12KCRIC",
    "https://kenzz.com/en/product/S47QVMX8XZZD/Sharp-Split-Air-Conditioner-3-HP%2C-Cooling-%26-Heating-White-AY-A24ZSE",
    "https://kenzz.com/en/product/CMNHCZYZFWP5/Beko-Split-Air-Conditioner-Inverter-Motor-2.25-HP-Cooling-Only-White-BICT1820",
    "https://kenzz.com/en/product/DLKP9QK4XCXM/Sharp-Split-Air-Conditioner-1.5-HP%2C-Cooling-Only-White-AH-AP12ZHE",
    "https://kenzz.com/en/product/ZXU4UF445QRG/Beko-Split-Air-Conditioner-Inverter-Motor-1.5-HP-Cooling-and-Heating-White-BIHT1240",
    "https://kenzz.com/en/product/SA7EE5P97A5B/%D8%AA%D9%83%D9%8A%D9%8A%D9%81-%D8%B3%D8%A8%D9%84%D9%8A%D8%AA-%D9%87%D8%A7%D9%8A%D8%B1-2.25-%D8%AD%D8%B5%D8%A7%D9%86-%D8%A8%D8%A7%D8%B1%D8%AF-%D9%88%D8%B3%D8%A7%D8%AE%D9%86-%D8%A3%D8%A8%D9%8A%D8%B6-HSU-18KHROC",
    "https://kenzz.com/en/product/WMPKMUQ7ABVP/LG-Art-Cool-Inverter-Split-Air-Conditioner-1.5-HP%2C-Cooling-%26-Heating-Gray-S4-W12JARZA",
    "https://kenzz.com/en/product/7ZANQ2MFRJLW/Carrier-Air-Conditioner-1.5-HP-Split-Cool-Optimax-Inverter-53KHCT12DN-708F",
    "https://kenzz.com/en/product/EM8CRL45HWDU/Air-Conditioner-3-Hp-Hot-Cold-White-Ay-Xp24Uhe",
    "https://kenzz.com/en/product/KNWVEWC5UCTM/Carrier-Optimax-Split-Air-Conditioner%2C-Cooling%2C-3-HP%2C-White-53KHCT24N-708",
    "https://kenzz.com/en/product/YRPG3FFBV8L7/LG-Split-Air-Conditioner-2.25-HP%2C-Cooling-%26-Heating-White-S4-H18RZAAA",
    "https://kenzz.com/en/product/4XPMVKAJ7EAQ/Sharp-Inverter-Split-Air-Conditioner-2.25-HP%2C-Cooling-Only-Silver-AH-XP18UHE",
    "https://kenzz.com/en/product/XX5VKC847X8L/Sharp-Split-Air-Conditioner-2.25-HP%2C-Cooling-Digital-Plasma-Cluster-White-AH-AP18ZHE",
    "https://kenzz.com/en/product/6GCM6UAS9YTF/LG-Split-Air-Conditioner-3-HP%2C-Cooling-Only-White-S4-Q24K22ME",
    "https://kenzz.com/en/product/FMULFQUJ2KGR/Beko-Split-Air-Conditioner-Inverter-Motor-3-HP-Cooling-Only-White-BICT2420",
    "https://kenzz.com/en/product/2FXVUX4W8WTT/Tornado-Split-Air-Conditioner-1.5-Hp-Fast-Cooling-White-Th-C12Bee",
    "https://kenzz.com/en/product/ZE5H7WYPFNBZ/%D8%AA%D9%83%D9%8A%D9%8A%D9%81-%D9%87%D9%88%D8%A7%D8%A1-%D9%87%D8%A7%D9%8A%D8%B1-%D8%B3%D8%A8%D9%84%D9%8A%D8%AA-%D8%B3%D9%85%D8%A7%D8%B1%D8%AA-%D9%83%D9%88%D9%88%D9%84-1.5-%D8%AD%D8%B5%D8%A7%D9%86-%D8%A8%D8%A7%D8%B1%D8%AF-%D8%A8%D9%84%D8%A7%D8%B2%D9%85%D8%A7-%D8%B4%D8%A7%D8%B4%D8%A9-%D8%AF%D9%8A%D8%AC%D9%8A%D8%AA%D8%A7%D9%84-%D8%A3%D8%A8%D9%8A%D8%B6-HSU-12KCROCC",
    "https://kenzz.com/en/product/P7CY9X3MXB4N/Hisense-Split-Air-Conditioner-1.5-HP-Cooling-%26-Heating-Digital-Inverter-White-HI-E12INVHP",
    "https://kenzz.com/en/product/T49DJPYPCZ8B/Sharp-Inverter-Split-Air-Conditioner-2.25-HP%2C-Cooling-%26-Heating-Silver-AY-XP18UHE",
    "https://kenzz.com/en/product/ZA6TKBKJH87G/Eta-King-Desert-Air-Conditioner-220-Watts-75-Liters-Ac-075N",
    "https://kenzz.com/en/product/HB2GNHQ77PUT/LG-Hero-Split-Air-Conditioner-1.5-HP%2C-Cooling-%26-Heating-White-S4-H12RZAAA",
    "https://kenzz.com/en/product/SDHV9PETTSXJ/Sharp-Inverter-Digital-Plasma-Cluster-Split-Air-Conditioner-1.5-Hp-White-Ah-Xp12Bme",
    "https://kenzz.com/en/product/DNF4G64GULG2/%D8%AA%D9%83%D9%8A%D9%8A%D9%81-%D8%B3%D8%A8%D9%84%D9%8A%D8%AA-%D9%87%D8%A7%D9%8A%D8%B1-2.25-%D8%AD%D8%B5%D8%A7%D9%86-%D8%A8%D8%A7%D8%B1%D8%AF-%D9%81%D9%82%D8%B7-%D8%A3%D8%A8%D9%8A%D8%B6-HSU-18KCRIC",
    "https://kenzz.com/en/product/735FX38YXKZU/Carrier-Split-Air-Conditioner-1.5-Hp-Optimax%2C-Cooling-%26-Heating-53Qhct-12",
    "https://kenzz.com/en/product/7CPFL2AWR3CN/Sharp-Inverter-Split-Air-Conditioner-2.25-HP%2C-Cooling-Plasma-Cluster-Black-AY-XP18YHEB",
    "https://kenzz.com/en/product/3NLVJXXE2MQN/%D8%AA%D9%83%D9%8A%D9%8A%D9%81-%D8%B3%D8%A8%D9%84%D9%8A%D8%AA-%D9%87%D8%A7%D9%8A%D8%B1-1.5-%D8%AD%D8%B5%D8%A7%D9%86-%D8%A8%D8%A7%D8%B1%D8%AF-%D8%A7%D9%86%D9%81%D8%B1%D8%AA%D8%B1-%D8%A8%D9%84%D8%A7%D8%B2%D9%85%D8%A7-%D8%A3%D8%A8%D9%8A%D8%B6-HSU-12KCRIA",
    "https://kenzz.com/en/product/VVW8PQYLTTFN/Carrier-%D8%AA%D9%83%D9%8A%D9%8A%D9%81-%D8%B3%D8%A8%D9%84%D9%8A%D8%AA-%D8%A3%D9%88%D8%A8%D8%AA%D9%8A%D9%85%D8%A7%D9%83%D8%B3-1.5-%D8%AD%D8%B5%D8%A7%D9%86-%D8%A8%D8%A7%D8%B1%D8%AF-%D8%A3%D8%A8%D9%8A%D8%B6-KHCT-12-OPTIMAX",
    "https://kenzz.com/en/product/VKAVZG7UN64X/LG-Split-Air-Conditioner-2.25-HP%2C-Cooling-Only-White-S4-C18RZAAA",
    "https://kenzz.com/en/product/6FKKTC68ATFK/Media-Split-Air-Conditioner-3-HP%2C-Cooling-Only-White-MSCT-24CR",
    "https://kenzz.com/en/product/KFXBMXGMUAZR/LG-Dual-Cool-Split-Air-Conditioner-1.5-HP%2C-Cooling-%26-Heating-White-S4NW12JA2MA",
    "https://kenzz.com/en/product/2AK92F6VE84S/Fresh-Split-Air-Conditioner-1.5-HP%2C-Cooling-%26-Heating-White-SFW13H-IP-SEW13H-O",
    "https://kenzz.com/en/product/YNSGS7TFK93J/LG-Split-Air-Conditioner-1.5-HP%2C-Cooling-%26-Heating-White-S4-W12JA3AE",
    "https://kenzz.com/en/product/TP6GFPV39NS9/%D8%AA%D9%83%D9%8A%D9%8A%D9%81-%D8%B3%D8%A8%D9%84%D9%8A%D8%AA-%D9%87%D8%A7%D9%8A%D8%B1-3-%D8%AD%D8%B5%D8%A7%D9%86-%D8%A8%D9%84%D8%A7%D8%B2%D9%85%D8%A7-%D8%A8%D8%A7%D8%B1%D8%AF-%D9%81%D9%82%D8%B7-%D8%A3%D8%A8%D9%8A%D8%B6-HSU-24KCROCC",
    "https://kenzz.com/en/product/49ZXBH6FDV68/Sharp-Split-Air-Conditioner-3-HP%2C-Cooling-%26-Heating-Digital-Plasma-Cluster-White-AY-AP24ZHE",
    "https://kenzz.com/en/product/L6SK5FZVEMYF/LG-Split-Air-Conditioner-1.5-HP%2C-Cooling-Only-White-S4-C12RZAAA",
    "https://kenzz.com/en/product/VUY7ZSL88LVV/%D8%AA%D9%83%D9%8A%D9%8A%D9%81-%D9%87%D9%88%D8%A7%D8%A1-%D9%87%D8%A7%D9%8A%D8%B1-%D8%B3%D8%A8%D9%84%D9%8A%D8%AA-%D8%B3%D9%85%D8%A7%D8%B1%D8%AA-%D9%83%D9%88%D9%88%D9%84-2.25-%D8%AD%D8%B5%D8%A7%D9%86-%D8%A8%D8%A7%D8%B1%D8%AF-%D8%A8%D9%84%D8%A7%D8%B2%D9%85%D8%A7-%D8%B4%D8%A7%D8%B4%D8%A9-%D8%AF%D9%8A%D8%AC%D9%8A%D8%AA%D8%A7%D9%84-%D8%A3%D8%A8%D9%8A%D8%B6-HSU-18KCROCC",
    "https://kenzz.com/en/product/CK84SSK22XYU/LG-Split-Air-Conditioner-2.25-HP%2C-Cooling-Only-White-S4-Q18KL2MD",
    "https://kenzz.com/en/product/SA7EE5P97A5B/Haier-Split-Air-Conditioner-2.25-HP%2C-Cooling-%26-Heating-White-HSU-18KHROC",
    "https://kenzz.com/en/product/P948HWR9ZKYC/LG-Inverter-Split-Air-Conditioner-3-HP%2C-Cooling-%26-Heating-White-S4-W24K23AE",
    "https://kenzz.com/en/product/VVW8PQYLTTFN/Air-Conditioner-1.5-Hp-Cold-White-Khct-12-Optimax",
    "https://kenzz.com/en/product/7QJWNHR9MZJZ/Midea-Mission-Pro-Air-Conditioner%2C-1.5-HP%2C-Cooling-and-Heating%2C-White-M1SCT-12HRNF-Q8",
    "https://kenzz.com/en/product/DNF4G64GULG2/Haier-Split-Air-Conditioner-2.25-HP%2C-Cooling-Only-White-HSU-18KCRIC",
    "https://kenzz.com/en/product/QJ7KDUJYVKXR/Haier-HSU-12KHRIBC-1.5-HP-Split-Inverter-Air-Conditioner-WiFi-White",
    "https://kenzz.com/en/product/3NLVJXXE2MQN/Haier-Split-Air-Conditioner-1.5-HP-Cooling-Inverter-Plasma-White-HSU-12KCRIA",
    "https://kenzz.com/en/product/CZ365MA4SSGM/Carrier-Optimax-Air-Conditioner-1.5-HP-Cooling-%26-Heating-White-42QHCT12N-708F",
    "https://kenzz.com/en/product/QJ7KDUJYVKXR/%D8%AA%D9%83%D9%8A%D9%8A%D9%81-%D9%87%D9%88%D8%A7%D8%A1-%D9%87%D8%A7%D9%8A%D8%B1-%D8%B3%D8%A8%D9%84%D9%8A%D8%AA-1.5-%D8%AD%D8%B5%D8%A7%D9%86-%D8%A8%D8%A7%D8%B1%D8%AF-%D8%B3%D8%A7%D8%AE%D9%86-%D8%A5%D9%86%D9%81%D8%B1%D8%AA%D8%B1-%D9%88%D8%A7%D9%8A-%D9%81%D8%A7%D9%8A-%D8%A7%D8%A8%D9%8A%D8%B6-HSU-12KHRIBC",
    "https://kenzz.com/en/product/2GBPPGPLMXK9/Hisense-Split-Air-Conditioner-2.25-Hp-Cold-And-Hot-Hi-E18Invhp",
    "https://kenzz.com/en/product/FNCYAMR8N3BS/Haier-Split-Air-Conditioner-3-HP%2C-Cooling-Only-White-HSU-24KCRIC",
    "https://kenzz.com/en/product/7SJ7S7DEDSPQ/LG-Art-Cool-Inverter-Split-Air-Conditioner-2.25-HP%2C-Cooling-%26-Heating-Gray-S4-W18KLRZA",
    "https://kenzz.com/en/product/PB7EMU9ZX59K/%D8%AA%D9%83%D9%8A%D9%8A%D9%81-%D8%B3%D8%A8%D9%84%D9%8A%D8%AA-%D9%87%D8%A7%D9%8A%D8%B1-1.5-%D8%AD%D8%B5%D8%A7%D9%86-%D8%A8%D8%A7%D8%B1%D8%AF-%D9%81%D9%82%D8%B7-%D8%A3%D8%A8%D9%8A%D8%B6-HSU-12KCRIC",
    "https://kenzz.com/en/product/7H9Z9QZPQ4SG/Sharp-Split-Air-Conditioner-3-HP%2C-Cooling-White-AH-A24ZSE",
    "https://kenzz.com/en/product/4XBS82NWELKA/Sharp-Inverter-Split-Air-Conditioner-2.25-HP%2C-Cooling-%26-Heating-White-AY-XP18YHE",
    "https://kenzz.com/en/product/44N3SYU6UF7Q/Haier-Split-Air-Conditioner-1.5-Hp-Cold-And-Hot-White-Hsu-12Khrocc",
    "https://kenzz.com/en/product/HE6676GTX9BK/LG-Split-Air-Conditioner-1.5-HP%2C-Cooling-Only-White-S4-Q12JA2MC",
    "https://kenzz.com/en/product/WM4BWCMETDWE/Sharp-Split-Air-Conditioner-2.25-HP%2C-Cooling-White-AH-A18ZSE",
    "https://kenzz.com/en/product/FWLPVEQMKZHN/Sharp-Split-Air-Conditioner-1.5-HP%2C-Cooling-White-AH-A12ZSE",
    "https://kenzz.com/en/product/ARZT2CUWDNGU/Fresh-Split-Air-Conditioner-1.5-HP%2C-Cooling-Only-White-SIFW13C-IP--SIFW13C-OX2",
    "https://kenzz.com/en/product/Y3TGAHZJ7433/LG-Split-Air-Conditioner-1.5-HP-Cooling-Only-White-S4-Q12JA3AE",
    "https://kenzz.com/en/product/3TZ96Y9FWZ6X/Fresh-Cooling-Split-Air-Conditioner-2.25-HP-White-FUFW18C-IW-AG-FUFW18C-O-X2",
    "https://kenzz.com/en/product/FNCYAMR8N3BS/%D8%AA%D9%83%D9%8A%D9%8A%D9%81-%D8%B3%D8%A8%D9%84%D9%8A%D8%AA-%D9%87%D8%A7%D9%8A%D8%B1-3-%D8%AD%D8%B5%D8%A7%D9%86-%D8%A8%D8%A7%D8%B1%D8%AF-%D9%81%D9%82%D8%B7-%D8%A3%D8%A8%D9%8A%D8%B6-HSU-24KCRIC",
    "https://kenzz.com/en/product/ZVKF6MWRQD76/Carrier-Xcool-Split-Air-Conditioner-Cooling-and-Heating-Inverter-Technology-1.5-HP-White-53QHEFT12DN8-708F",
    "https://kenzz.com/en/product/JF5G3ECXRGDT/Carrier-Split-Air-Conditioner-2.25-Hp%2C-Cooling-%26-Heating-Digital-White-53QHCT18N-708F",
    "https://kenzz.com/en/product/EHQYZK749Y6G/Carrier-Optimax-Pro-Air-Conditioner-Cooling-and-Heating-3-HP-53QHCT24N-708F",
    "https://kenzz.com/en/product/TP6GFPV39NS9/Haier-Split-Air-Conditioner-3-HP-Plasma-Cooling-Only-White-HSU-24KCROCC",
    "https://kenzz.com/en/product/2QX4UM8AZLHN/LG-Inverter-Split-Air-Conditioner-5-HP%2C-Cooling-%26-Heating-White-S4-W3R43EA",
    "https://kenzz.com/en/product/27AV9LTYPPR9/Sharp-Split-Air-Conditioner-1.5-HP%2C-Cooling-%26-Heating-White-AY-AP12ZHE",
    "https://kenzz.com/en/product/VUY7ZSL88LVV/Haier-Smart-Cool-Split-Air-Conditioner%2C-2.25-HP%2C-Cooling%2C-Plasma%2C-Digital-Display%2C-White-HSU-18KCROCC",
    "https://kenzz.com/en/product/MHZED8D2RXU9/Sharp-Inverter-Split-Air-Conditioner-2.25-HP%2C-Cooling-Plasma-Cluster-Silver-AY-XP18YHES",
    "https://kenzz.com/en/product/W7X5YRB5V2XG/Fresh-Professional-Turbo-Split-Air-Conditioner-Cool-Hot-3-HP-White-FUFW24H-IW-AG",
    "https://kenzz.com/en/product/2B6DUSYBVKSU/Fresh-Split-Air-Conditioner-1.5-HP%2C-Cooling-Only-White-FUFW12C-IW",
    "https://kenzz.com/en/product/W7HGC6MA4AK2/Carrier-Split-Air-Conditioner-4-Hp%2C-Cooling-%26-Heating-Digital-White-42Qhet30N-708F",
    "https://kenzz.com/en/product/34AE5QMYQQ3K/Carrier-Split-Optimax-Inverter-Air-Conditioner-2.25-Hp%2C-Cooling-%26-Heating-White-53Qhct18Dn-708F",
    "https://kenzz.com/en/product/28WJ5S9YZ4Z5/Midea-Mission-Pro-Air-Conditioner-1.5-HP-Cooling-Only-M1SCT-12CRN-Q8",
    "https://kenzz.com/en/product/P2XH3386GLJT/Media-Mission-Pro-Split-Air-Conditioner%2C-Cooling%2C-3-HP%2C-White-MSC1T-24CR-N",
    "https://kenzz.com/en/product/97P3PEYL3BQH/Beko-Split-Air-Conditioner-1.5-Hp-Inverter-Motor-Cold-Only-White-Bict1221X"
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
        requests.post(u, json={"chat_id": CHAT, "text": msg, "parse_mode": "Markdown"}, timeout=5)
    except:
        pass

def clean(text):
    x = text.translate(AR).replace(",", "")
    x = "".join(c for c in x if c.isdigit() or c == ".").strip(".")
    return float(x) if x else None

def get_product_price(soup):
    # محاولة البحث في الكلاسات المعروفة أولاً
    price_tag = soup.select_one(".price, span[class*='price'], div[class*='price'], span[class*='amount']")
    if price_tag:
        p = clean(price_tag.get_text())
        if p and p > 100:
            return p
            
    # لو ملقاش، يبحث في أي عنصر جوه الصفحة جواه كلمة ج.م أو EGP
    for el in soup.find_all(True):
        t = el.get_text(strip=True)
        if ("ج.م" in t or "جنيه" in t or "EGP" in t) and len(t) < 30:
            p = clean(t)
            if p and p > 100:
                return p
    return None

def check_all_products():
    if not PRODUCTS:
        print(f"\n[{time.strftime('%H:%M:%S')}] ⚠️ لستة المنتجات فارغة!")
        return

    print(f"\n[{time.strftime('%H:%M:%S')}] 🔄 جاري فحص الـ {len(PRODUCTS)} تكييف بالترتيب وبدون حظر...")
    success_count = 0  
    
    for i, url in enumerate(PRODUCTS, 1):
        try:
            print(f"⏳ جاري فحص المنتج [{i}/{len(PRODUCTS)}]...")
            r = requests.get(url, headers=H, timeout=8)
            
            if r.status_code != 200:
                print(f"⚠️ تخطي، كود الاستجابة: {r.status_code}")
                continue
                
            s = BeautifulSoup(r.text, "html.parser")
            
            title_tag = s.select_one("h1, title")
            product_title = title_tag.get_text(strip=True) if title_tag else "منتج من كنز"
            product_title = product_title.split("|")[0].replace("كنز", "").strip()

            price = get_product_price(s)
                            
            if not price:
                print(f"[تحذير] تعذر العثور على السعر للمنتج رقم {i}")
                continue
                
            success_count += 1
            old_price = last_prices.get(url)
            
            if old_price is None:
                last_prices[url] = price
                print(f"✔️ [{success_count}] {product_title[:25]}... | السعر: {price} ج.م")
            elif price != old_price:
                diff = price - old_price
                status = "📉 نزل" if diff < 0 else "📈 زاد"
                msg = (
                    f"🚨 *تغيير سعر تكييف على كنز!*\n\n"
                    f"📦 {product_title}\n\n"
                    f"الحالة: {status}\n"
                    f"من: `~{old_price}~ ج.م`\n"
                    f"إلى: *{price} ج.م*\n\n"
                    f"🛒 [رابط المنتج]({url})"
                )
                send(msg)
                print(f"🔥 تغيير سعر! {price} ج.م")
                last_prices[url] = price
            else:
                print(f"🔄 [{success_count}] مستقر: {product_title[:20]}... | {price} ج.م")
                
            time.sleep(1)
            
        except Exception as e:
            print(f"⚠️ خطأ في الرابط رقم {i}: {e}")
            continue

    if success_count > 0:
        send(f"🟢 *تم فحص جميع التكييفات بنجاح!* (تم رصد *{success_count}* تكييف شغال ومستقر) 🤖❄️")

    print(f"----------------------------------------\n💡 انتهت الجولة وتم فحص {success_count} تكييف.")

print("مراقبة أسعار التكييفات المنتظمة شغالة...")
while True:
    check_all_products()
    print("انتظار اللفة القادمة (15 دقيقة)...")
    time.sleep(900)
    
