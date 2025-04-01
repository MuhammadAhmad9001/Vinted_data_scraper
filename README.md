# Vinted Scraper with Telegram group

## Description
This script scrapes **Vinted** for new items matching specific search criteria, stores the results, and sends notifications to a **Telegram** group. The script also uses **PIA VPN** to rotate IPs, ensuring uninterrupted access to the site.

## Features
- **Scrapes Vinted** for new items based on predefined filters.
- **Compares URLs** to detect newly listed items.
- **Stores new items** in a JSON file.
- **Sends notifications** about new items to a Telegram chat.
- **Uses PIA VPN** to prevent getting blocked.

## Requirements
Ensure you have the following dependencies installed:

```bash
pip install pyVinted piapy requests
```

## Configuration
### 1. **Vinted Search Criteria**
Modify the `base_url` variable to adjust search filters:

```python
base_url = "https://www.vinted.es/catalog?time=1743193539&catalog_from=0&page={}&catalog[]=5&brand_ids[]=417&brand_ids[]=671&brand_ids[]=15430438&brand_ids[]=481&brand_ids[]=46323&brand_ids[]=4785&order=newest_first"
```

### 2. **Telegram Bot Setup**
Replace the following variables with your **Telegram Bot Token** and **Chat ID**:

```python
BOT_TOKEN = "your_telegram_bot_token"
CHAT_ID = "your_chat_id"
```

To create a bot, follow these steps:
1. Open Telegram and search for **BotFather**.
2. Use the command `/newbot` and follow the instructions to get your bot token.
3. Add the bot to a Telegram group/channel and get the chat ID.

## Usage
Run the script with:

```bash
python vinted_scraper.py
```

The script will:
1. Scrape new items.
2. Compare with previous results.
3. Send new item details to Telegram.
4. Repeat the process every **10 seconds**.

## JSON Output Files
- `vinted_urls_old.json`: Stores previously found item URLs.
- `vinted_urls_new.json`: Stores newly found item URLs.
- `matched_items.json`: Stores details of items that will be sent to Telegram.

## VPN Integration
The script utilizes **PIA VPN** to change the IP before making requests. Ensure **PIA VPN** is installed and running.

## Troubleshooting
- **Script not running?** Ensure all dependencies are installed.
- **No new items found?** Adjust the search parameters.
- **Bot not sending messages?** Check if the bot has permission in the chat.

## License
This project is licensed under the MIT License.

## Contact
[LinkedIn: Muhammad Ahmad](https://www.linkedin.com/in/muhammad-ahmad-137b36241/)

