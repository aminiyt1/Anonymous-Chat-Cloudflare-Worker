from js import Object, Response , fetch ,JSON
import hashlib
import json
from pyodide.ffi import to_js as _to_js
import re
import random
import string

BOT_TOKEN = "TokenBot"
BOT_ID = "NameBot"
HOOK = hashlib.md5(BOT_TOKEN.encode()).hexdigest()

async def on_fetch(request,env):
    db = env.db
    url = request.url
    path = url.split("://", 1)[1].split("/", 1)[1] if "/" in url.split("://", 1)[1] else ""
    base_url = url.rsplit("/", 1)[0]

    if path == "init":

        body = await postReq("setWebhook",{
            "url":f"{base_url}/{HOOK}"
        })

        return Response.new(body)

    if path == HOOK:
        try:     
            tgResponse = (await request.json()).to_py()
            if "message" in tgResponse:

                message = tgResponse["message"]
                chatId = message["from"]["id"]

                NEWLINK = "✅ ساخت لینک ناشناس برای من"
                default_keyboard = {
                "keyboard": [
                [{"text": NEWLINK}]
                ],
                "resize_keyboard": True,
                 "one_time_keyboard": True
                 }
    
                if "text" in message and message["text"].startswith("/start"):
    
                    startedUser = await db.prepare("SELECT * FROM users WHERE telegram_user_id = ?").bind(str(chatId)).first()
                    if startedUser:
                        startedUserId = startedUser.id
                    else:
                        startedUser = await db.prepare("INSERT INTO users (telegram_user_id, rkey, target_user) VALUES (?, ?, ?)").bind(str(chatId), rndKey(), "").run()
                        startedUserId = startedUser.meta.last_row_id               
    
    
                    match = re.search(r"/start (\w+)_(\w+)", message["text"])
                    if match:
    
                        param_rkey, param_id = match.groups()
                        targetUser = await db.prepare("SELECT * FROM users WHERE id = ? and rkey = ?").bind(revHxId(param_id) , param_rkey).first()
    
                        if targetUser:
    
                            getChatMember = await postReq("getChatMember",{
                             "chat_id":targetUser.telegram_user_id,
                             "user_id":targetUser.telegram_user_id,
                             })
    
                            await db.prepare("update users set target_user = ? WHERE id = ?").bind(targetUser.telegram_user_id , startedUserId).run()   
                            await postReq("sendMessage",{
                                      "chat_id":chatId,
                                      "text":"در حال ارسال پیام ناشناس به "+str(getChatMember["result"]["user"]["first_name"])+" هستی \n هرچی بفرستی ناشناس میره براش میتونی متن ویس یا هرچی خواستی بفرستی"+"\n این پایین بفرست 👇",
                                      "reply_markup":{"remove_keyboard": True}
                                      })
                        else:
                            await postReq("sendMessage",{
                                      "chat_id":chatId,
                                      "text":"کاربر یافت نشد",
                                      "reply_markup":default_keyboard
                                      }) 
    
                    else:
                        await postReq("sendMessage",{
                                      "chat_id":chatId,
                                      "text":"خوش آمدید",
                                      "reply_markup":default_keyboard
                                      })        
                elif "text" in message and message["text"] == NEWLINK:
    
                    user = await db.prepare("SELECT * FROM users WHERE telegram_user_id = ?").bind(str(chatId)).first()
                    
                    if user:
                        mylink = f"https://t.me/{BOT_ID}?start="+user.rkey+"_"+str(hxId(user.id))
                        await postReq("sendMessage",{
                        "chat_id":chatId,
                        "text":f"لینک زیر کپی کن و استفاده کن \n\n بزنی روش کپی میشه 👇\n\n`{mylink}`",
                        "parse_mode":"MarkDownV2"
                        })  
                else:
                    
                    me = await db.prepare("SELECT * FROM users WHERE telegram_user_id = ?").bind(str(chatId)).first()
                    
                    if me.target_user:
    
                        await postReq("sendMessage",{
                         "chat_id":me.target_user,
                         "text":"پیام ناشناس جدید داری 👇"    
                        })   
                        
                        res = await postReq("copyMessage",{
                         "chat_id":me.target_user,
                         "from_chat_id":chatId,
                         "message_id":message["message_id"]
                        })
                        if "ok" in res and res["ok"]:
                            await db.prepare("update users set target_user = ? WHERE id = ?").bind("" , me.id).run()
                            await postReq("sendMessage",{
                                      "chat_id":chatId,
                                      "text":"ارسال شد",
                                      "reply_markup":default_keyboard
                                      })          
              

        except Exception as e:

            """
            # Debugging: Replace "chat_id" with your own to receive error messages on Telegram

            await postReq("sendMessage",{
            "chat_id":"your-chat-id",  # Replace with your actual chat ID  
            "text":f"err: {e} , {tgResponse}"
            })

            """

        return Response.new("idle")
       
    return Response.new("ok")


def to_js(obj):
    return _to_js(obj, dict_converter=Object.fromEntries)

def rndKey():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def hxId(id):
    return (hex(id))[::-1]

def revHxId(hxid):
    return int(hxid[::-1], 16)

async def postReq(tgMethod, payload):

    options = {
    "body": json.dumps(payload),
    "method": "POST",
        "headers": {
        "content-type": "application/json;charset=UTF-8",
        }
    }

    response = await fetch(f"https://api.telegram.org/bot{BOT_TOKEN}/{tgMethod}",to_js(options))
    body = await response.json()
    JSONBody = body.to_py()
    return JSONBody
