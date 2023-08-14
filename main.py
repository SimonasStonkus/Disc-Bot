import os
from typing import Optional, Literal

import discord
from discord import app_commands
from dotenv import load_dotenv
from numpy import random
import json

import load_Index
import Siege_record_match
import fetch_CS_Inv



load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()

MY_GUILD = discord.Object(id=1093188291358118011)
# load dictionaries of paints and weapons
paint_dict = load_Index.load_paint()
weapon_dict = load_Index.load_weapon()


# create client
class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

# set intents
intents.members = True
intents.message_content = True
# initialize bot
client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


# defines weapon and paint autocomplete options
async def weapon_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    weapons = list(weapon_dict["Weapon index"].keys())
    return [
        app_commands.Choice(name=weapon, value=weapon)
        for weapon in weapons if current.lower() in weapon.lower()
    ]


async def paint_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    paints = list(paint_dict["Paint index"].keys())
    return [
        app_commands.Choice(name=paint, value=paint)
        for paint in paints if current.lower() in paint.lower()
    ]


@client.tree.command()
@app_commands.autocomplete(weapon=weapon_autocomplete, paint=paint_autocomplete)
@app_commands.rename(skin_float="float")
@app_commands.describe(
    weapon='Weapon name or ID',
    paint='Skin name or ID',
    pattern='Pattern ID',
    skin_float='Float value',
    sticker_1='Sticker ID',
    sticker_1_wear='Sticker wear',
    sticker_2='Sticker ID',
    sticker_2_wear='Sticker wear',
    sticker_3='Sticker ID',
    sticker_3_wear='Sticker wear',
    sticker_4='Sticker ID',
    sticker_4_wear='Sticker wear',
)
# function that accepts the necessary parameters for generating a gencode
async def gencode(interaction: discord.Interaction, weapon: str, paint: str, pattern: int, skin_float: float,
                  sticker_1: int = 0, sticker_1_wear: int = 0, sticker_2: int = 0, sticker_2_wear: int = 0,
                  sticker_3: int = 0, sticker_3_wear: int = 0, sticker_4: int = 0, sticker_4_wear: int = 0):

    # embed attached to the returned gencode
    embed = discord.Embed(title='Selected Weapon', description=f'{weapon} {paint} {pattern} float: {skin_float}')
    await interaction.channel.send(embed=embed)

    # checking if the weapon/paint are in the list, if not, passess the input values into the final response
    if weapon in weapon_dict["Weapon index"]:
        weapon = weapon_dict["Weapon index"][weapon]
    if paint in paint_dict["Paint index"]:
        paint = paint_dict["Paint index"][paint]

    # sends gencode command
    await interaction.response.send_message(
        f'!gen {weapon} {paint} {pattern} {skin_float} {sticker_1} {sticker_1_wear} {sticker_2} {sticker_2_wear} {sticker_3} {sticker_3_wear} {sticker_4} {sticker_4_wear} ')


@client.tree.command()
async def gencode_random(interaction: discord.Interaction, sticker_1: int = 0, sticker_1_wear: int = 0, sticker_2: int = 0, sticker_2_wear: int = 0,
                  sticker_3: int = 0, sticker_3_wear: int = 0, sticker_4: int = 0, sticker_4_wear: int = 0):
    random_weapon = list(weapon_dict["Weapon index"])[round(random.randint(1, len(weapon_dict["Weapon index"])+1))]
    random_paint = list(paint_dict["Paint index"])[round(random.randint(1, len(paint_dict["Paint index"])+1))]
    random_pattern = round(random.rand()*1000)
    random_float = random.rand()

    # embed attached to the returned gencode
    embed = discord.Embed(title='Selected Weapon', description=f'{random_weapon} {random_paint}, pattern: {random_pattern}, float: {random_float}')
    await interaction.channel.send(embed=embed)

    # sends gencode command
    await interaction.response.send_message(
        f'!gen {weapon_dict["Weapon index"][random_weapon]} {paint_dict["Paint index"][random_paint]} {random_pattern} {random_float} {sticker_1} {sticker_1_wear} {sticker_2} {sticker_2_wear} {sticker_3} {sticker_3_wear} {sticker_4} {sticker_4_wear}')


@client.tree.command()
async def update_steam_id(interaction: discord.Interaction, steam_id: str):
    if os.path.isfile("discord_steam_ids.json"):
        user_ids = json.load(open("discord_steam_ids.json", encoding="utf-8"))
        user_ids[str(interaction.user.id)] = steam_id
    else:
        user_ids = {str(interaction.user.id): steam_id}
    with open("discord_steam_ids.json", "w+", encoding="utf8") as file:
        json.dump(user_ids, file)

    await interaction.response.send_message(embed = discord.Embed(title = "Steam ID has been updated."))


@client.tree.command()
async def cs_fetch_inv(interaction: discord.Interaction):
    if os.path.isfile("discord_steam_ids.json") is False:
        await interaction.response.send_message(embed=discord.Embed(title="No steam IDs have been recorded", description="Please use /update_steam_id to record an ID"))
        return
    user_ids = json.load(open("discord_steam_ids.json", encoding="utf-8"))
    if str(interaction.user.id) not in user_ids:
        await interaction.response.send_message(embed=discord.Embed(title="You have not yet recorded a steam ID", description="Please use /update_steam_id to record an ID"))
        return
    await interaction.response.send_message(embed=discord.Embed(title="Loading..."))

    steam_id = user_ids[str(interaction.user.id)]
    total_value = fetch_CS_Inv.get_value_and_save(steam_id)
    image = discord.File("value_plot.png", "value_plot.png")
    embed = discord.Embed(title="The total value of the inventory is: "+str(total_value)+"€")
    embed.set_image(url="attachment://value_plot.png")
    await interaction.edit_original_response(embed=embed, attachments=[image])

    # embed = discord.Embed(title = f"{steam_id} inventory",description = fetch_CS_Inv.return_Inv(descriptions)[0:4000])
    # await interaction.channel.send(embed= embed)
    # await interaction.response.send_message(fetch_CS_Inv.return_Inv(descriptions)[0:1000])
############################################################################################################################################################################################################


async def siege_map_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    maps = Siege_record_match.siege_Maps
    return [
        app_commands.Choice(name=map, value=map)
        for map in maps if current.lower() in map.lower()
    ]


async def siege_outcome_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    outcomes = ["Win","Loss"]
    return [
        app_commands.Choice(name=outcome,value=outcome)
        for outcome in outcomes if current.lower() in outcome.lower()
    ]


@client.tree.command()
@app_commands.autocomplete(map = siege_map_autocomplete, outcome = siege_outcome_autocomplete)
async def siege_record_match(interaction:discord.Interaction, map: str, outcome: str):
    if map not in Siege_record_match.siege_Maps:
        await interaction.response.send_message(
            "Invalid Map"
        )

    elif outcome not in ["Win","Loss"]:
        await interaction.response.send_message(
            "Invalid outcome"
        )
    else:
        Siege_record_match.record_Match(map,outcome)

        await interaction.response.send_message(
            f'Map "{map}" added to data list with outcome "{outcome}"'
    )

client.run(TOKEN)
