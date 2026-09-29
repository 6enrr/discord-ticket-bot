import discord
from flask import Flask
import threading
from discord.ui import Select, View

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

client = discord.Client(intents=intents)

app = Flask('')

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# قائمة خيارات التحكم داخل التذكرة
class TicketControlSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="استلام التذكرة", description="استلام التذكرة ومباشرتها", emoji="🙋‍♂️"),
            discord.SelectOption(label="إضافة / إزالة عضو", description="إدارة الأعضاء داخل التذكرة", emoji="👥"),
            discord.SelectOption(label="قفل / فتح التذكرة", description="قفل التذكرة أو فتحها مؤقتاً", emoji="🔒"),
            discord.SelectOption(label="إعادة تسمية", description="تغيير اسم روم التذكرة", emoji="✏️"),
            discord.SelectOption(label="حظر من فتح تذكرة", description="حظر العضو من استخدام التذاكر", emoji="🚫"),
            discord.SelectOption(label="إغلاق التذكرة", description="حذف وإغلاق التذكرة نهائياً", emoji="🔴"),
        ]
        super().__init__(placeholder="خيارات التحكم بالتذكرة", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        val = self.values[0]
        if val == "استلام التذكرة":
            await interaction.response.send_message(f"✅ تم استلام التذكرة بواسطة {interaction.user.mention}", ephemeral=False)
        elif val == "إغلاق التذكرة":
            await interaction.response.send_message("🔒 جاري إغلاق التذكرة...", ephemeral=True)
            await interaction.channel.delete()
        else:
            await interaction.response.send_message(f"تم تنفيذ الخيار: **{val}**", ephemeral=True)

class TicketControlView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketControlSelect())

# قائمة اختيار نوع التذكرة الرئيسية
class TicketSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="طلب ألعاب محددة وتوفيرها", description="لطلب ألعاب محددة او سلسلة ألعاب معينة", emoji="🎮"),
            discord.SelectOption(label="شراء بوتات", description="لطلب احد البوتات المعروضة", emoji="🤖"),
            discord.SelectOption(label="تجديد اشتراكاتك الحالية", description="لتجديد اشتراكاتك التي تريدها", emoji="🔄"),
            discord.SelectOption(label="طلب بوت مخصص", description="لطلب بوت بالمواصفات التي تريدها", emoji="⚙️"),
            discord.SelectOption(label="مشاكل واستفسارات", description="لتقديم الدعم بخصوص مشاكلك واستفساراتك", emoji="❓"),
        ]
        super().__init__(placeholder="اختر سبب فتح التذكرة", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        category = discord.utils.get(guild.categories, name="Tickets")
        channel = await guild.create_text_channel(f"ticket-{interaction.user.name}", overwrites=overwrites, category=category)
        
        await interaction.response.send_message(f"تم فتح التذكرة بنجاح! {channel.mention}", ephemeral=True)
        
        # إنشاء الـ Embed والشكل المطابق لفتح التذاكر
        embed = discord.Embed(
            description=f"أهلاً بك {interaction.user.mention} .. تشكرك لتواصلك معنا بخصوص {self.values[0]}.\n\n. سيتم الرد عليك من قبل فريق الدعم الفني أقرب وقت ممكن .",
            color=0x2b2d31
        )
        embed.set_author(name=str(interaction.user.display_name), icon_url=interaction.user.display_avatar.url)
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.title = f"🎫 تذكرة : {self.values[0]}"
        embed.add_field(name="المستلم", value="⏳ لم يتم استلامها بعد", inline=False)
        
        await channel.send(content=f"{interaction.user.mention}", embed=embed, view=TicketControlView())

class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("-------------------")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith('!ticket'):
        embed = discord.Embed(color=0x2b2d31)
        # استبدل الـ LINK أدناه برابط الصورة البانر الذي تريده
        embed.set_image(url="https://cdn.discordapp.com/attachments/1196210736465191084/1554322852814266458/Gemini_Generated_Image_sc9k0sc9k0sc9k0s.jpg?ex=6abc7776&is=6abb25f6&hm=903b2efb434468d34a6c24b64217a9b45b67a2e391c952ac4ebb7d0b69b55401&")
        await message.channel.send(embed=embed, view=TicketView())

if __name__ == "__main__":
    keep_alive()
    import os
    client.run(os.getenv('DISCORD_TOKEN'))
