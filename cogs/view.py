import disnake
from disnake import TextInputStyle, Localized
from disnake.ext import commands

details = {
    "mod_name": {"label": "Ваше настоящее имя:", "placeholder": "", "style": TextInputStyle.short},
    "mod_age": {"label": "Возраст (16+):", "placeholder": "", "style": TextInputStyle.short},
    "mod_exp": {"label": "Был ли у Вас опыт в модерировании?", "placeholder": "", "style": TextInputStyle.paragraph},
    "mod_about": {"label": "Кратко расскажите о себе:", "placeholder": "", "style": TextInputStyle.paragraph},
    "mod_tg": {"label": "Ваш телеграм для связи:", "placeholder": "Пример: @user", "style": TextInputStyle.short},
}

class ModModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label = value["label"],
                placeholder = value["placeholder"],
                custom_id = key,
                style = value["style"]
            )
            for key, value in details.items()
        ]
        
        super().__init__(
            title = "Заявка на модератора", components=components
        )
        
    async def callback(self, inter: disnake.ModalInteraction):
        
        await inter.response.send_message("Ваша заявка была получена.\nСпасибо за проявленный интерес!", ephemeral=True)
              
        embed = disnake.Embed(
            title = f"Заявка на модератора",
            color = 0xffffff
        )
        
        embed.set_author(
            name = "Автор: " + inter.author.display_name,
            url = f"https://discordapp.com/users/{inter.author.id}",
            icon_url = inter.author.display_avatar
        )
        
        embed.set_footer(
            text = f"{inter.author.name} | ID: {inter.author.id}"
        )
        
        channel = inter.client.get_channel(1226857649673605170)
        
        for key, value in inter.text_values.items():
            embed.add_field(
                name = details[key]['label'],
                value = "```" + value[:1024] + "```",
                inline=False,
            )
            
        await channel.send(embed = embed)

class View(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        print(f'Модуль {self.__class__.__name__} загружен.')

    @commands.command(name="mod_view")
    async def set_view(self, ctx: commands.Context):
        embed = disnake.Embed(
            title = "test title",
            description="test desc",
            colour=0xffffff
        )
        
        await ctx.send(
            embed=embed,
            components = [
                disnake.ui.Button(
                    label = "Заявка на модератора",
                    style = disnake.ButtonStyle.gray,
                    custom_id = "mod"
                )
            ]
        )
        return
    
    @commands.Cog.listener("on_button_click")
    async def button_interaction(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id == "mod":
            await inter.response.send_modal(modal = ModModal())

def setup(client: commands.Bot):
    client.add_cog(View(client))