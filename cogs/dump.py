import disnake, json, datetime
from disnake.ext import commands
from disnake.embeds import EmbedProxy
from disnake.colour import Colour

class Dump(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        print(f'Модуль {self.__class__.__name__} загружен.')
    
    @commands.message_command(name="dump_message", guild_ids=[673119818404200448])
    async def json_message(self, inter: disnake.ApplicationCommandInteraction):
        message = inter.target
        
        data = {
            "content": message.content,
            "embeds": [
                {
                    key: (
                        str(value) if isinstance(value, (datetime.datetime, EmbedProxy, Colour)) else value
                    )
                    for key, value in {
                        "type": embed.type,
                        "title": embed.title,
                        "description": embed.description,
                        "url": embed.url,
                        "timestamp": embed.timestamp.isoformat() if embed.timestamp else None,
                        "color": embed.color,
                        "author": embed.author.name if embed.author else None,
                    }.items()
                    if value is not None
                }
                for embed in message.embeds
            ]
        }
        
        data = json.dumps(data, indent=4, ensure_ascii=False)
        
        await inter.response.send_message(data)

def setup(client: commands.Bot):
    client.add_cog(Dump(client))