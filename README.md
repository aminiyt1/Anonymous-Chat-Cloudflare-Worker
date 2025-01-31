# Anonymous-Chat-Cloudflare-Worker
Anonymous Chat Cloudflare Worker Telegram Bot

1. First, create a Python Worker in Cloudflare, delete all the existing code, and paste the code you got from the link above.  
2. Then, go to **Storage & Databases** and create a new database (the name doesn’t matter).  
3. Enter the database and open the **console**.
4.
**Copy the code below:**
   ```sql
CREATE TABLE users (
    "id" integer PRIMARY KEY,
    "telegram_user_id" text,
    "rkey" text,
    "target_user" text
);

5. Then, go to the Worker and in the **Settings**, under **Bindings**, bind the database you created with the name `db`.  
6. Create a bot on Telegram using **@BotFather**.  
7. For **BOT_TOKEN**, put the token of your bot.  
8. For **BOT_ID**, use the bot's ID without the `@`.  
9. Click on **Visit**.  
10. The Worker will open in your browser. Add `/init` at the end of the URL, for example: `https://yourworker.username.workers.dev/init` and press Enter to set the webhook.
