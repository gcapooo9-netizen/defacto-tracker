import time
import requests
from bs4نهاراً import BeautifulSoup  # اسم مكتبة الـ bs4 العادية BeautifulSoup
from bs4 import BeautifulSoup

TOKEN = "8996279782:AAEJ-n3vP4K9bts15GC0_htKMceRC4yHj8E"
CHAT = "5124680786"
SEARCH_URL = "https://www.amazon.eg/s?k=defacto"

# تحسين الـ Headers لتكون أقرب ما يكون لمتصفح حقيقي فايرفوكس أو كروم
H = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
    ),
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://www.amazon.eg/",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
}

AR = str.maketrans("٠١٢٣٤٥٦٧٨٩٫٬", "0123456789.,")


def send(msg):
  u = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
  try:
    requests.post(
        u, json={"chat_id": CHAT, "text": msg, "parse_mode": "Markdown"}, timeout=15
    )
  except Exception as e:
    print("خطأ في إرسال تيليجرام:", e)


def clean(text):
  x = text.translate(AR).replace(",", "")
  x = "".join(c for c in x if c.isdigit() or c == ".").strip(".")
  return float(x) if x else None


def check_search_page():
  send("🤖 **اطمن انا شغال وبراقب ياجيمي** ⚡\nجاري جلب وفحص منتجات DeFacto بدقة...")

  # استخدام Session للحفاظ على الكوكيز وتفادي الحظر السريع
  session = requests.Session()
  session.headers.update(H)

  try:
    # محاولة فتح الصفحة الرئيسية الأول (تثبيت كوكيز أمان أمازون) ثم الدخول على صفحة البحث
    session.get("https://www.amazon.eg/", timeout=15)
    time.sleep(2)  # فاصل بسيط كبشري

    r = session.get(SEARCH_URL, timeout=25)
    print(f"Amazon Status Code: {r.status_code}")

    if r.status_code != 200:
      send(f"⚠️ أمازون ردت بالكود {r.status_code} (حظر حماية)")
      return

    s = BeautifulSoup(r.text, "html.parser")

    # البحث عن كل المنتجات بطريقة أشمل
    items = s.select("div.s-main-slot div.s-result-item[data-asin]")
    if not items:
      items = s.select("div[data-asin]")

    found_count = 0
    report = "📦 *نتائج فحص DeFacto:* \n\n"

    for item in items:
      asin = item.get("data-asin")
      if not asin or len(asin) != 10:
        continue

      # جلب اسم المنتج
      name_tag = item.select_one("h2 a span, h2 span, .a-text-normal")
      name = name_tag.get_text(strip=True) if name_tag else f"منتج {asin}"

      # جلب السعر بطرق مختلفة لضمان ظهوره
      price_tag = item.select_one(".a-price .a-offscreen, .a-price-whole")
      if not price_tag:
        continue

      price_text = price_tag.get_text(strip=True)
      price = clean(price_text)
      if price is None:
        continue

      found_count += 1
      if found_count <= 5:
        report += (
            f"▪️ {name[:30]}...\n💰 السعر: {price}"
            f" ج.م\n🔗 [رابط المنتج](https://www.amazon.eg/dp/{asin})\n\n"
        )

      if found_count >= 10:
        break

    report += f"📊 إجمالي المنتجات المعروضة: {found_count}"
    send(report)

