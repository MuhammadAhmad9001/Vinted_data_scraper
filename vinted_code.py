import json
import time
from pyVinted import Vinted
import json
import requests
import time
from piapy import PiaVpn


vpn = PiaVpn()

vinted = Vinted()

# Define search parameters
base_url = "https://www.vinted.es/catalog?time=1743193539&catalog_from=0&page={}&catalog[]=5&brand_ids[]=417&brand_ids[]=671&brand_ids[]=15430438&brand_ids[]=481&brand_ids[]=46323&brand_ids[]=4785&order=newest_first"
number_of_items = 190

while True:
    all_urls = set()
    
    # Load old URLs if file exists
    try:
        with open("vinted_urls_old.json", "r") as f:
            old_urls = set(json.load(f))  # Use set for quick lookup
    except (FileNotFoundError, json.JSONDecodeError):
        old_urls = set()
    
    # Loop through pages 1 to 5
    for page_number in range(1, 6):
        url = base_url.format(page_number)
        items = vinted.items.search(url, number_of_items, page_number)
        
        # Extract URLs
        all_urls.update(item.url for item in items)
    
    # Find new URLs
    new_urls = all_urls - old_urls  # Set difference for efficiency
    
    # Save new URLs to a separate file
    if new_urls:
        with open("vinted_urls_new.json", "w") as f:
            json.dump(list(new_urls), f, indent=4)
    
    # Append new URLs to old URLs and save
    updated_old_urls = old_urls | new_urls  # Set union
    with open("vinted_urls_old.json", "w") as f:
        json.dump(list(updated_old_urls), f, indent=4)
    
    print(f"Scraped {len(all_urls)} URLs. Found {len(new_urls)} new items.")

    new_items_details = []
    page1 = vinted.items.search(
        "https://www.vinted.es/catalog?time=1743206654&catalog_from=0&page=1&catalog[]=5&brand_ids[]=417&brand_ids[]=671&brand_ids[]=15430438&brand_ids[]=481&brand_ids[]=46323&brand_ids[]=4785&order=newest_first", 
        10
    )

    for item in page1:
        new_items_details.append({
            "title": item.title,
            "id": item.id,
            "url": item.url,
            "photo": item.photo,
            "price": item.price,
            "currency": item.currency,
            "brand_title": item.brand_title
        })

    # Load URLs from the JSON file
    try:
        with open("vinted_urls_new.json", "r") as file:
            vinted_urls_new = json.load(file)
            if not isinstance(vinted_urls_new, list):
                raise ValueError("Invalid JSON format: Expected a list of URLs.")
    except FileNotFoundError:
        print("Warning: vinted_urls_new.json not found. Creating a new file.")
        vinted_urls_new = []
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in vinted_urls_new.json.")
        vinted_urls_new = []

    # Compare URLs and store only matching item details
    matched_items = [item for item in new_items_details if item["url"] in vinted_urls_new]

    # Avoid resending duplicate items by keeping track of sent URLs
    sent_urls = set()

    # Print matched item details
    print(json.dumps(matched_items, indent=4, ensure_ascii=False))

    # Save matched items to a new JSON file
    with open("matched_items.json", "w", encoding="utf-8") as file:
        json.dump(matched_items, file, indent=4, ensure_ascii=False)

    ### **2️⃣ Send Unique Items to Telegram**
    BOT_TOKEN = ""
    CHAT_ID = ""

    # Read matched items only once
    with open("matched_items.json", "r") as ffile:
        data = json.load(ffile)

    for item in data:
        url = item.get("url", "").strip()  # Define url before use
        if url in sent_urls:  # Skip if already sent
            continue
        sent_urls.add(url)  # Mark as sent

        required_fields = ["title", "id", "url", "photo", "price", "currency", "brand_title"]
        if all(field in item for field in required_fields):
            title = item.get("title", "").strip()
            photo = item.get("photo", "").strip()
            price = item.get("price", "").strip()
            currency = item.get("currency", "").strip()
            brand_title = item.get("brand_title", "").strip()

            message = (
                f"📌 *Item Details:*\n"
                f"🏷 *Title:* {title}\n"
                f"🔗 [View Product]({url})\n"
                f"🏷 *Brand:* {brand_title}\n"
                f"💰 *Price:* {price} {currency}\n"
            )

            telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
            payload = {
                "chat_id": CHAT_ID,
                "caption": message,
                "parse_mode": "Markdown",
                "photo": photo
            }
            
            try:

                time.sleep(2)
                vpn.connect(verbose=False, timeout=20)
                time.sleep(5)
                
            except Exception as e:
                print(f"❌ Change Failed: {e}")
            
            response = requests.post(telegram_url, json=payload)
            if response.status_code == 200:
                print(f"✅ Sent: {title}")
            else:
                print(f"❌ Failed to send: {title}, Error: {response.status_code} - {response.text}")

            time.sleep(2)  # Prevent spamming API requests
    vpn.disconnect()
    # Wait for 5 minutes before scraping again
    time.sleep(10)