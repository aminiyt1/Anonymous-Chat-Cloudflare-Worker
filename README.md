# Anonymous-Chat-Cloudflare-Worker
Anonymous Chat Cloudflare Worker Telegram Bot

1. First, create a Python Worker in Cloudflare, delete all the existing code, and paste the code you got from the link above.  
2. Then, go to **Storage & Databases** and create a new database (the name doesn’t matter).  
3. Enter the database and open the **console**.
4. **Copy the code below:**

   ```sql
CREATE TABLE users (
    "id" integer PRIMARY KEY,
    "telegram_user_id" text,
    "rkey" text,
    "target_user" text
);
