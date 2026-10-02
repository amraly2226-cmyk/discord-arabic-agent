import 【entity-discord¦canonical_name=discord】
import os
from groq import Groq

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_KEY = os.getenv("GROQ_KEY")

client = 【entity-discord¦canonical_name=discord】.Client(intents=【entity-discord¦canonical_name=discord】.Intents.all())
groq = Groq(api_key=GROQ_KEY)

@client.event
async def on_ready():
    print(f"ONLINE {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.attachments:
        f = message.attachments[0]
        if f.filename.endswith(('.ogg','.mp3','.wav','.m4a','.webm')):
            await f.save("voice.ogg")
            await message.channel.send("سمعت الفويس... بحوله")
            try:
                with open("voice.ogg","rb") as audio:
                    tr = groq.audio.transcriptions.create(file=audio, model="whisper-large-v3", language="ar", prompt="لهجة مصرية")
                text = tr.text
                await message.channel.send(f"فهمت: {text}")
                chat = groq.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"system","content":"انت ادمن ديسكورد مصري. حول الكلام ل JSON فقط. الاوامر: create_channel مع name, purge مع amount, lock_thread. رد JSON فقط."},{"role":"user","content":text}])
                import json
                data = json.loads(chat.choices[0].message.content)
                if data.get("action") == "create_channel":
                    await message.guild.create_text_channel(data.get("name","new-room"))
                    await message.channel.send("عملت الروم")
                elif data.get("action") == "purge":
                    await message.channel.purge(limit=int(data.get("amount",10)))
                elif data.get("action") == "lock_thread" and isinstance(message.channel, discord.Thread):
                    await message.channel.edit(locked=True, archived=True)
            except Exception as e:
                await message.channel.send(f"مشكلة: {e}")

client.run(DISCORD_TOKEN)
