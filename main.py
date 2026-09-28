import discord
from discord.ui import Select, View

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

client = discord.Client(intents=intents)

class TicketSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="شراء بوتات", description="لطلب بوتات من المعروضة بالمتجر", emoji="🤖"),
            discord.SelectOption(label="تجديد بوتات", description="لتجديد اشتراكاتك الحالية", emoji="🔄"),
            discord.SelectOption(label="طلب بوت مخصص", description="لطلب بوت بالمواصفات التي تريدها", emoji="⚙️"),
            discord.SelectOption(label="مشاكل واستفسارات", description="لتقديم الدعم على مشاكل واستفساراتك", emoji="❓"),
            discord.SelectOption(label="لطلب لعبة او سلسلة العاب معينة", description="لطلب ألعاب محددة وتوفيرها", emoji="🎮"),
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
        
        await interaction.response.send_message(f"تم فتح التذكرة بنجاح! توجه إلى هنا: {channel.mention}", ephemeral=True)
        await channel.send(f"أهلاً بك {interaction.user.mention}! تم فتح التذكرة بناءً على خيارك: **{self.values[0]}**. فريق الدعم سيرد عليك قريباً.")

class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("------")

@client.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.content.startswith('!ticket'):
        embed = discord.Embed(
            title="اهلا بكم في ماتريكس",
            description="فريقنا متواجد لخدمتك .. اختر سبب فتح التذكرة وسيتم الرد عليك",
            color=0xf1c40f
        )
        embed.set_image(url="https://cdn.discordapp.com/emojis/1553916794308399125.webp?size=96") 
        
        await message.channel.send(embed=embed, view=TicketView())

# احفظ التوكن هنا (ويفضل تغييره من الموقع لاحقاً للأمان)
import os
client.run(os.getenv('DISCORD_TOKEN'))
