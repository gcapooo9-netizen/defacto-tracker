def check_search_page():
    print(f"[{time.strftime('%H:%M:%S')}] جاري فحص صفحة البحث والتصنيف...")
    session = requests.Session()
    
    r = None
    try:
        r = session.get(SEARCH_URL, headers=H, timeout=25)
    except Exception as e:
        err_msg = f"⚠️ تحذير: خطأ في الاتصال بالشبكة أو السيرفر: {e}"
        print(err_msg)
        send(err_msg)
        return

    # فحص كود الاستجابة (لو أمازون حظر الـ IP هيجيب 403 أو 503)
    if not r or r.status_code != 200:
        status_code = r.status_code if r else "مجهول"
        error_msg = f"🚨 **تنبيه حظر من أمازون!**\nكود الاستجابة: `{status_code}`\nتم حظر الطلب أو كشف السكربت في هذه الدورة ({time.strftime('%Y-%m-%d %H:%M')})."
        print(error_msg)
        send(error_msg)
        return
        
    try:
        s = BeautifulSoup(r.text, "html.parser")
        
        # التأكد مما إذا كانت الصفحة عبارة عن كابتشا (Captcha) أو حظر بشري
        if "captcha" in r.text.lower() or s.select_one("input#captchacharacters"):
            captcha_msg = f"🤖 **أمازون كشف السكربت وطلب التحقق (Captcha)!**\nالتوقيت: `{time.strftime('%Y-%m-%d %H:%M')}`"
            print(captcha_msg)
            send(captcha_msg)
            return

        items = s.select("div.s-result-item[data-asin]")
        
        # لو أمازون فتح الصفحة بس مراجعش منتجات (احتمال تغير التصميم أو حظر جزئي)
        if not items:
            empty_msg = f"⚠️ **تنبيه:** الصفحة فتحت ولكن لم يتم العثور على منتجات (قد يكون تم تغيير تصميم الصفحة أو حجب المحتوى).\nالتوقيت: `{time.strftime('%Y-%m-%d %H:%M')}`"
            print(empty_msg)
            send(empty_msg)
            return

        found_count = 0
        results_msg = f"🛍️ *تقرير فحص منتجات أمازون ({time.strftime('%Y-%m-%d %H:%M')})*\n\n"
        
        for item in items:
            asin = item.get("data-asin")
            if not asin or len(asin) != 10:
                continue
                
            name_tag = item.select_one("h2 a span, .a-text-normal")
            name = name_tag.get_text(strip=True) if name_tag else f"منتج {asin}"
            short_name = name[:45] + "..." if len(name) > 45 else name
            
            price_tag = item.select_one(".a-price-whole")
            if not price_tag:
                continue
                
            price_str = price_tag.get_text(strip=True)
            
            product_url = f"https://www.amazon.eg/dp/{asin}"
            results_msg += f"🔹 [{short_name}]({product_url})\n💰 السعر: *{price_str} جنية*\n\n"
            
            found_count += 1
            if found_count >= 10:
                break
                
        results_msg += f"✅ تم رصد {found_count} منتج من الصفحة بنجاح."
        send(results_msg)

    except Exception as e:
        err_msg = f"❌ حدث خطأ أثناء تحليل الصفحة: {e}"
        print(err_msg)
        send(err_msg)
