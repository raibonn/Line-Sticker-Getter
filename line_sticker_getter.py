import requests
import os
import discord
from discord.utils import get
from discord.ui import Button, View
from discord.ext import commands, tasks
from datetime import datetime
import re
intents=discord.Intents.all()
bot = commands.Bot(command_prefix='r!line_sticker ', case_insensitive=True, intents = intents)
bot.remove_command('help')
Token = "YourTokenHere"

@bot.event
async def on_ready():
    print(bot.guilds)
    print("起動に成功")
    print(f"Bot導入リンク:https://discord.com/api/oauth2/authorize?client_id={bot.application_id}&permissions=8&scope=bot%20applications.commands")


@bot.command()
async def get(ctx, link: str):
    if not "https://store.line.me/stickershop/product/" in link:
        await ctx.send("無効なリンク")
    else:
        if not "/ja" in link:
            link = link + "/ja"
        id = link.replace("https://store.line.me/stickershop/product/", "").replace("/", "").replace("ja", "")
        print(id)
        data = requests.get(link)
        if data.status_code != 200:
            await ctx.send("Linkが存在しないか壊れています")
        else:
            func = Button(style=discord.ButtonStyle.primary, label="サーバーに追加")
            async def callback_function(interaction):
                await interaction.response.edit_message(view = None)
                sticker_list = re.findall("background-image:url\(https://stickershop.line-scdn.net/stickershop/v1/sticker/\d+/.+/sticker.png", data.text)[1::2]
                temp_list = []
                for i in sticker_list:
                    temp_list.append(i.replace("background-image:url(", ""))
                sticker_list = temp_list
                stickers = len(sticker_list)
                for i, url in enumerate(sticker_list):
                    with open(f"temp/{id}/{i}.png", "wb") as f:
                        f.write(requests.get(url).content)
                for i in range(stickers):
                    file = discord.File(fp=f"temp/{id}/{i}.png",filename="temp.png",spoiler=False)
                    await ctx.guild.create_sticker(name = f"{id}_{i}", description = re.findall('data-test="sticker-name-title">.+</p>', data.text)[0].replace('data-test="sticker-name-title">', "").replace("</p>", ""), emoji = "🐔", file = file, reason = f"Linestampを取得(Id:{id})")
                await interaction.followup.send("finish")
            embed = discord.Embed(title = re.findall('data-test="sticker-name-title">.+</p>', data.text)[0].replace('data-test="sticker-name-title">', "").replace("</p>", ""), color = 0x00ff00, description = re.findall('Item01Txt">.+</p>', data.text)[0].replace('Item01Txt">', "").replace("</p>", ""))
            embed.add_field(name = "制作者", value = re.sub('data-test="sticker-author" href="/stickershop/author/\d+/ja">', "", re.findall('data-test="sticker-author" href="/stickershop/author/\d+/ja">.+</a>', data.text)[0]).replace("</a>", ""))
            embed.add_field(name = "値段", value = re.findall('data-test="sticker-price">￥\d+</p>', data.text)[0].replace('data-test="sticker-price">', "").replace("</p>", ""))
            print(re.findall('src="https://stickershop.line-scdn.net/stickershop/v1/product/\d+/LINEStorePC/main.png\?v=1" alt="', data.text)[0].replace('src="', "").replace('" alt="', ""))
            #embed.set_image(url = re.findall('src="https://stickershop.line-scdn.net/stickershop/v1/product/\d+/LINEStorePC/main.png\?v=1" alt="', data.text)[0].replace('src="', "").replace('" alt="', ""))
            os.makedirs(f"temp/{id}", exist_ok=True)
            with open(f"temp/{id}/main.png", "wb") as f:
                f.write(requests.get(re.findall('src="https://stickershop.line-scdn.net/stickershop/v1/product/\d+/LINEStorePC/main.png\?v=1" alt="', data.text)[0].replace('src="', "").replace('" alt="', "")).content)
            file = discord.File(fp=f"temp/{id}/main.png",filename="temp.png",spoiler=False)
            embed.set_image(url=f"attachment://temp.png")
            func.callback = callback_function
            k = await ctx.send(file = file, embed = embed, view=View().add_item(func))

bot.run(Token)