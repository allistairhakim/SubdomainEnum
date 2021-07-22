from discord.ext import commands, tasks
import discord



class sendmessage10seconds(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.sendmessage.start()

    @tasks.loop(seconds=10)
    async def sendmessage(self): # You can pass the `ctx` parameter if you want, but there's no point in doing that
        channel = self.client.get_channel(867846950988546088)
        textSave = open("cogs/save.txt").read()
        file = open("outputs/output.txt").read()
        if file != textSave:
            for i in range(len(file.splitlines())):
                try:
                    print(textSave.splitlines()[i] + "o")
                except:
                    res = [element for element in file.splitlines() if file.splitlines().index(element) >= i and element != "" and element != None]
                    for r in res:
                        await channel.send("Hey <@!462231967140806656>! New potential takeover detected.")
                        await channel.send("```" + r + "```")
        output = open("cogs/save.txt", "w")
        output.write(file)
        output.close()

    @sendmessage.before_loop
    async def before_sendmessage(self):
        await self.client.wait_until_ready()

def setup(client):
    client.add_cog(sendmessage10seconds(client))
