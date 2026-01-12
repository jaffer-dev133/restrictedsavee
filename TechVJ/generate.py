# Don't Remove Credit Tg - @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ

import traceback
import asyncio
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from config import API_ID, API_HASH
from database.db import db

SESSION_STRING_SIZE = 351

@Client.on_message(filters.private & ~filters.forwarded & filters.command(["logout"]))
async def logout(client, message):
    user_id = message.from_user.id
    user_data = await db.get_session(user_id)  
    if user_data is None:
        return await message.reply("<b>❌ You are not logged in!</b>")
    
    await db.set_session(user_id, session=None)  
    await message.reply("<b>✅ Logout Successfully 🤝</b>")

@Client.on_message(filters.private & ~filters.forwarded & filters.command(["login"]))
async def main(bot: Client, message: Message):
    user_id = message.from_user.id
    
    # Check already logged in
    user_data = await db.get_session(user_id)
    if user_data is not None:
        return await message.reply("<b>⚠️ You are already logged in. Use /logout first.</b>")
    
    try:
        # Step 1: API ID
        api_id_msg = await bot.ask(user_id, "<b>Send Your API ID.\n\nClick /skip to use default.</b>", filters=filters.text, timeout=300)
        if api_id_msg.text == "/skip":
            api_id = API_ID
            api_hash = API_HASH
        else:
            api_id = int(api_id_msg.text)
            api_hash_msg = await bot.ask(user_id, "<b>Now Send Your API HASH</b>", filters=filters.text, timeout=300)
            api_hash = api_hash_msg.text

        # Step 2: Phone Number
        phone_msg = await bot.ask(user_id, "<b>Send your Phone Number with Country Code\nExample: <code>+9171828181889</code></b>", filters=filters.text, timeout=300)
        phone_number = phone_msg.text

        # Step 3: Send Code
        temp_client = Client(":memory:", api_id=api_id, api_hash=api_hash)
        await temp_client.connect()
        await message.reply("<b>📨 Sending OTP...</b>")
        
        code = await temp_client.send_code(phone_number)
        
        # Step 4: Ask OTP
        otp_msg = await bot.ask(user_id, "<b>Enter OTP in format: <code>1 2 3 4 5</code>\n(Add spaces between digits)</b>", filters=filters.text, timeout=600)
        otp = otp_msg.text.replace(" ", "")

        # Step 5: Sign In
        try:
            await temp_client.sign_in(phone_number, code.phone_code_hash, otp)
        except SessionPasswordNeeded:
            pwd_msg = await bot.ask(user_id, "<b>🔒 Enter 2-Step Verification Password:</b>", filters=filters.text, timeout=300)
            await temp_client.check_password(password=pwd_msg.text)

        # Success: Save Session
        string_session = await temp_client.export_session_string()
        await db.set_session(user_id, session=string_session)
        await db.set_api_id(user_id, api_id=api_id)
        await db.set_api_hash(user_id, api_hash=api_hash)
        
        await temp_client.disconnect()
        await message.reply("<b>✅ Login Successful!🎊</b>")

    except Exception as e:
        await message.reply(f"<b>❌ Error:</b> <code>{e}</code>")
