from base64 import decodestring
from itertools import count
from logging import warning
from re import X
import re
from discord import embeds
from discord.embeds import Embed
from discord.ext.commands.core import has_permissions
import pymongo
import discord
from discord import role
from discord import mentions
from discord import channel
from discord import member
from discord.colour import Color
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from pymongo import MongoClient, message
import random
import datetime
import time
import math
import asyncio
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config


import requests
from discord import utils

PREFIX = '!'

owm = OWM('477a0b8e8eaf4d6e906a24fab25ade18' )
mgr = owm.weather_manager()
config_dict = get_default_config()
config_dict['language'] = 'ru'



intents = discord.Intents.default()
intents.guilds = True  # Сервера
intents.members = True  # Мемберы
intents.bans = True  # Баны
intents.emojis = True  # Эмодзи

intents.integrations = True  # Ивент - Интеграции Сервера
intents.webhooks = True  # Ивент - Вебхуки
intents.invites = True  # Ивент - Создание Удаление Приглашений
intents.voice_states = True  # Ивент - Проверка обновлений войса
intents.presences = True  # Ивент - Обновление пользователя

intents.messages = True  # Ивент - Сообщения | Действие - Добавление Реакций
intents.guild_messages = True  # На сервере
intents.dm_messages = True  # ЛС

intents.reactions = True  # Ивент - Реакции
intents.guild_reactions = True  # На сервере
intents.dm_reactions = True  # В лс
intents.reactions = True

intents.typing = True  # Ивент - Кто-то вводит текст
intents.guild_typing = True  # На сервере
intents.dm_typing = True  # В лс

intents = discord.Intents.all()


client = commands.Bot( command_prefix = '!', intents = intents )




cluster = MongoClient('mongodb+srv://strozza:89kola5618zona@cluster0.lhnhg.mongodb.net/Economy?retryWrites=true&w=majority')
users1 = cluster.Economy.users
capture = cluster.Economy.capture
warndb= cluster.Economy.warndb
shop1 = cluster.Economy.shop
buy_role = cluster.Economy.buy_roles
casino1 = cluster.Economy.casino
timely1 = cluster.Economy.timely
roles = cluster.Economy.roles
bio = cluster.Economy.bio





@client.event

async def on_ready():
    print( '\nБот успешно подключен!' )
    guild = client.get_guild( 709144637020831774 )
    # for row in users1.find():
    #     if "chips" not in row:
    #         users1.update_one({"id": row["id"]}, {"$set": {"chips": 0}})
    for member in guild.members:
        post = {
            "id": member.id,
            "balance": 500,
            "lvl": 0,
            "lvlch": 50,
            "exp": 0,
            "rep": 0,
            "warns": 0,
            "chips": 0
        }
        if users1.count_documents( { 'id': member.id } ) == 0:
            users1.insert_one( post )          
    await client.change_presence( status = discord.Status.online, activity = discord.Game( 'Bot By Wallace\n!help - помощь' ) )
    await checker.start()


@client.remove_command( 'help' )





@client.event
async def on_message( message ):
    if not message.author.bot:
        author = message.author
        levs = client.get_emoji(868112129910272060)
        if len(message.content) > 2:
            for row in users1.find( { "id": author.id } ):

                expi = row["exp"] + random.randint(5, 15)

                print(f"Отправлено сообщение в канал.")
                users1.update_one( { "id": author.id }, { "$set": { "exp": expi } } )
                if expi >= row["lvlch"]:
                    lvch = expi * 2
                    lv = row["lvl"]
                    lv += 1
                    avatar = message.author.avatar_url
                    username = message.author.name
                    embed = discord.Embed(
                        title=f"Новый уровень!",
                        description=f"{author.mention}, вы достигли __{lv} уровня {levs}! Поздравляем\n**Вы получили `1500 💶` за новый уровень!**", color=0xbfff70)
                    embed.set_thumbnail(url=avatar)
                    print(f"{avatar}")
                    # embed.add_field(name="undefined", value="undefined", inline=False)
                    channel = client.get_channel(735472856527536208)
                    bal = 1500
                    bal += row["balance"]
                    users1.update_one({"id": author.id}, { "$set": { "balance": bal, "lvl": lv, "lvlch": lvch } })

                    return await message.channel.send( embed=embed )
        await client.process_commands(message)





#leave
@client.event

async def on_member_remove(member):
    channelleave = client.get_channel( 796917006691336263 )
    emb = discord.Embed( description = f'❌  Пользователь { member.mention } был исключен из сервера', color = 0xe74c3c )
    await channelleave.send( embed = emb )



#join
@client.event

async def on_member_join(member):
    channel = client.get_channel( 796917006691336263 )
    role = discord.utils.get( member.guild.roles, id = 772834055565606923 )
    emb = discord.Embed( description = f"**Добро пожаловать, { member.mention }, ты попал в канал виртуальной семьи Wallace\nТебе автоматически была выдана роль <@&772834055565606923>, если требуется информация по ролям - перейди в канал <#863754922552983552>\nТакже не помешало бы ознакомиться с правилами сервера - <#709155076555669504>.\nПриятного тебе общения, не скучай!**", color = 0xe74c3c )
    emb.set_thumbnail( url = member.avatar_url )
    emb.set_footer( text = 'Welcome to Wallace Dynasty Discord server!', icon_url = 'https://cdn.discordapp.com/avatars/797171215285747772/a1f598f82f2ece5fc7f1a9f8ce247efa.webp?size=1024' )
    await member.add_roles( role )
    await channel.send( embed = emb )
    post = {
        "id": member.id,
        "balance": 500,
        "lvl": 0,
        "exp": 0,
        "rep": 0,
        "warns": 0,
        "chips": 0
    }
    if users1.count_documents({'id': member.id}) == 0:
        users1.insert_one(post)

    
@client.command()
async def cub(ctx, arg: int = None, amount: int = None):
    author = ctx.message.author
    cash = amount
    if amount:
        if 'chips' in users1.find_one( { "id": author.id } ):
            if( casino1.count_documents( { "author_id": author.id } ) == 0 ):
                if( casino1.count_documents( { "member_id": author.id } ) == 0 ):
                    if amount > users1.find_one( { "id": author.id } )['chips']: return await ctx.send(embed = discord.Embed(description = "У Вас недостаточно фишек для начала игры!"))
                    if amount <= 0: return await ctx.send(embed = discord.Embed(description = "**Нельзя сыграть на такую ставку!**"))
                    randoms = random.randint(1,6)
                    if arg > randoms:    
                        balance = users1.find_one( { "id": author.id } )['chips']
                        balance -= amount*2
                        users1.update_one( { "id": author.id }, { "$set": { "chips": balance } } )
                        return await ctx.send(embed = discord.Embed(title = 'Вы бросили кубик!', description = f'Вам выпало число { randoms } 🎲\n**__Вы проиграли {(amount*2)} фишек так как загадывали число { arg }__**.', color = 0xF5C85B ))
                    if arg < randoms:
                        balance = users1.find_one( { "id": author.id } )['chips']
                        balance -= amount*2
                        users1.update_one( { "id": author.id }, { "$set": { "chips": balance } } )
                        return await ctx.send(embed = discord.Embed(title = 'Вы бросили кубик!', description = f'Вам выпало число { randoms } 🎲\n**__Вы проиграли {(amount*2)} фишек так как загадывали число { arg }__**.', color = 0xF5C85B ))
                    if arg == randoms:
                        balance = users1.find_one( { "id": author.id } )['chips']
                        balance += amount*2
                        users1.update_one( { "id": author.id }, { "$set": { "chips": balance } } )
                        return await ctx.send(embed = discord.Embed(title = 'Вы бросили кубик!', description = f'Вам выпало число { randoms } 🎲\n**__Вы угадали число и выиграли {(amount*2)} фишек__**.', color = 0xF5C85B ))
    else:
        await ctx.send(embed = discord.Embed(description = "**__Подсказка:__**\n**!cub [число от 1 до 6] [ставка]**\n\n**__Учтите, что при поражении будет списана Ваша ставка в двойном размере!__**"))





#give_role
@client.command(pass_context = True)
async def create_role(ctx):
    name_role = ' '.join(ctx.message.content.split( ' ' )[1:])
    server = ctx.message.server
    new_role = await client.create_role( server )
    await client.edit_role( server, new_role, name = new_role )
    



#GIVE ROLE COMMAND'S

@client.command()
@commands.has_permissions(view_audit_log = True)
async def miss(ctx, member: discord.Member):
    await ctx.channel.purge(limit = 1);
    role_1 = member.guild.get_role(800515204340645918)# ади роли которую будет получать юзер
    emb = discord.Embed(description = f'Модератор { ctx.message.author.mention } выдал роль **Miss Wallace** пользователю { member.mention }', color = 0xff53BB)
    emb.set_footer( text = f'Вызвано: { ctx.message.author }', icon_url = ctx.message.author.avatar_url )
    await member.add_roles(role_1)
    await ctx.send(embed = emb)

@client.command()
@commands.has_permissions(view_audit_log = True)
async def major(ctx, member: discord.Member):
    await ctx.channel.purge(limit = 1);
    role_1 = member.guild.get_role(722952451602251799)# ади роли которую будет получать юзер
    emb = discord.Embed(description = f'*Модератор { ctx.message.author.mention } выдал роль <@&722952451602251799> пользователю { member.mention }*', color = 0xB4050D)
    emb.set_footer( text = f'Вызвано: { ctx.message.author }', icon_url = ctx.message.author.avatar_url )
    await member.add_roles(role_1)
    await ctx.send(embed = emb)

@client.command()
@commands.has_permissions(view_audit_log = True)
async def removemajor(ctx, member: discord.Member):
    await ctx.channel.purge(limit = 1);
    role_1 = member.guild.get_role(722952451602251799)# ади роли которую будет получать юзер
    emb = discord.Embed(description = f'*Модератор { ctx.message.author.mention } **забрал роль** <@&722952451602251799> у { member.mention }*', color = 0xB4050D)
    emb.set_footer( text = f'Вызвано: { ctx.message.author }', icon_url = ctx.message.author.avatar_url )
    await member.remove_roles(role_1)
    await ctx.send(embed = emb)

@client.command()
@commands.has_permissions(view_audit_log = True)
async def capt(ctx, member: discord.Member):
    await ctx.channel.purge(limit = 1);
    role_1 = member.guild.get_role(861944441527205918)# ади роли которую будет получать юзер
    emb = discord.Embed(description = f'*Модератор { ctx.message.author.mention } добавил { member.mention } в капт состав\n\nВыдана роль: <@&861944441527205918>*', color = 0xCC7B04)
    emb.set_footer( text = f'Вызвано: { ctx.message.author }', icon_url = ctx.message.author.avatar_url )
    await member.add_roles(role_1)
    await ctx.send(embed = emb)

@client.command()
@commands.has_permissions(view_audit_log = True)
async def removecapt(ctx, member: discord.Member):
    await ctx.channel.purge(limit = 1);
    role_1 = member.guild.get_role(861944441527205918)# ади роли которую будет получать юзер
    emb = discord.Embed(description = f'*Модератор { ctx.message.author.mention } удалил роль <@&861944441527205918> у { member.mention }*', color = 0xCC7B04)
    emb.set_footer( text = f'Вызвано: { ctx.message.author }', icon_url = ctx.message.author.avatar_url )
    await member.remove_roles(role_1)
    await ctx.send(embed = emb)
    


@client.command()
async def slots( ctx, amount: int = None ):
	author = ctx.message.author
	if ctx.channel.name == 'test-channel' or ctx.channel.name == '💬family-chat' or ctx.channel.name == '🎰game-channel':
		if amount:
			if 'chips' in users1.find_one( { "id": author.id } ):
				if( casino1.count_documents( { "author_id": author.id } ) == 0 ):
					if( casino1.count_documents( { "member_id": author.id } ) == 0 ):

						if amount > users1.find_one( { "id": author.id } )['chips']: return await ctx.send( embed = discord.Embed(description = "У Вас на балансе недостаточно игровых фишек!", color = 0xF02925) )
						if amount <= 0: return await ctx.send( embed = discord.Embed(description = f"Нельзя сыграть на такую маленькую ставку!", color = 0xF02925) )
						a = random.randint(0,6)
						b = random.randint(0,6)

						if a == b: return await ctx.send( embed = discord.Embed(description = f"{ author.mention } сыграл в слоты с крупье на { amount } фишек.\nПолучилась ничья!\n**__Счет:__ { a }:{ b }**", color = 0xD93516) )
						if a > b:
							balance = users1.find_one( { "id": author.id } )['chips']
							balance += amount
							users1.update_one( { "id": author.id }, { "$set": { "chips": balance } } )
							return await ctx.send( embed = discord.Embed(description = f"{ author.mention } сыграл в слоты с крупье на { amount } фишек.\n\n**__Победитель:__ { author.mention }.**\n**__Счет:__ { a }:{ b }**", color = 0x5CFA34) )

						if a < b:
							balance = users1.find_one( { "id": author.id } )['chips']
							balance -= amount 
							users1.update_one( { "id": author.id }, { "$set": { "chips": balance } } )
							return await ctx.send( embed = discord.Embed(description = f"{ author.mention } сыграл в слоты с крупье на { amount } фишек.\n**__Победитель:__ Крупье.**\n**__Счет:__ { b }:{ a }**", color = 0xF02925) )

					else:
						await ctx.send( embed = discord.Embed(description = f"Нельзя играть с Крупье если Вы/Вам предложили ставку!", color = 0xF02925) )
				else:
					await ctx.send( embed = discord.Embed(description = f"Нельзя играть с Крупье если Вы/Вам предложили ставку!", color = 0xF02925) )

			else:
				await ctx.send(embed = discord.Embed(description = f"{author.mention}, на Вашем балансе недостаточно фишек для начала игры!", color = 0xF02925))

		else:
			await ctx.send( embed = discord.Embed(description = f"**Подсказка:** Используйте !slots <количество фишек>") )


@client.command()
async def bet( ctx, user: discord.Member = None, amount: int = None ):
    if ctx.channel.name == 'test-channel' or ctx.channel.name == '💬family-chat' or ctx.channel.name == '🎰game-channel':
        if user and amount:
            if user.id != 797171215285747772:
                author = ctx.message.author
                emoji = client.get_emoji(867177297659822100)
                if author.id != user.id:
                    if( casino1.count_documents( { "author_id": author.id } ) == 0 and casino1.count_documents( { "author_id": user.id } ) == 0 ):
                        if( casino1.count_documents( { "author_id": author.id } ) == 0 and casino1.count_documents( { "author_id": user.id } ) == 0 ):
                            if( 'chips' in users1.find_one( { "id": author.id } ) and 'chips' in users1.find_one( { "id": user.id } ) ):
                                if amount <= 0: return await ctx.send( embed = discord.Embed(description = f"Нельзя кинуть ставку меньше либо равно нулю.", color = 0xF02925) )
                                author_balance = users1.find_one( { "id": author.id } )['chips']
                                member_balance = users1.find_one( { "id": user.id } )['chips']
                                if amount > int( author_balance ): return await ctx.send(embed = discord.Embed(description = f"У вас нету такого кол-ва фишек {emoji}!", color = 0xF02925))
                                if amount > int( member_balance ): return await ctx.send(embed = discord.Embed(description = f"У участника нету такого кол-ва фишек! {emoji}", color = 0xF02925))
                                post = {
									"author_id": author.id,
									"member_id": user.id,
									"bet": amount,
									"type": 0,
								}
                                casino1.insert_one( post )
                                await ctx.send(embed = discord.Embed(title = "Игра в кости 🎲", description = f"**{ author.mention } кинул { user.mention } ставку в размере { amount } фишек. {emoji}**\n\n**Примечание:**\nЧтобы принять ставку введите **!yes**\nЧтобы отклонить ставку введите **!no**\nЧтобы отменить ставку введите **!cancel**", color = 0xD9166C))
                            else:
                                await ctx.send(embed = discord.Embed(description = f"У Вас/Участника нету ни одной фишки. {emoji}", color = 0xD93516))
                        else:
                            await ctx.send(embed = discord.Embed(description = f"Вам/Участнику уже предложили ставку. {emoji}", color = 0xD93516))
                    else:
                        await ctx.send(embed = discord.Embed(description = f"Вы/Участник уже предложил ставку. {emoji}", color = 0xD93516))
                        
                else:
                    await ctx.send(embed = discord.Embed(description = f"Вы не можете играть сами с собой!", color = 0xD93516))
            else:
                await ctx.send(embed = discord.Embed(description = f"Вы не можете кинуть ставку боту!", color = 0xD93516))
                
        else:
            await ctx.send(embed = discord.Embed(description = f"**Используйте:**\n!bet <@участник> <количество {emoji}>", color = 0xD9166C))


@client.command()
async def yes( ctx ):
    author = ctx.message.author
    
    if ctx.channel.name == 'test-channel' or ctx.channel.name == '💬family-chat' or ctx.channel.name == '🎰game-channel':
        
        if casino1.count_documents( { "member_id": author.id } ) != 0:
            a = random.randint(0,6)
            b = random.randint(0,6)
            member = ctx.guild.get_member( int( casino1.find_one( { "member_id": author.id } )['author_id'] ) )
            if a == b:
                casino1.delete_one( { "member_id": author.id } )
                return await ctx.send(embed = discord.Embed(title = "Игра в кости 🎲", description = f"**{ member.mention } и { author.mention} у Вас получилась __ничья__!**\n**__Счет:__ { a }:{ b }**", color = 0xF85E19))

            if a > b:
                cash = int( users1.find_one( { "id": member.id } )['chips'] )
                amount = int( casino1.find_one( { "author_id": member.id } )['bet'] )
                value = cash + amount
                users1.update_one( { "id": member.id }, { "$set": { "chips": value } } )
                cash = int( users1.find_one( { "id": author.id } )['chips'] )
                amount = int( casino1.find_one( { "member_id": author.id } )['bet'] )
                value = cash - amount
                users1.update_one( { "id": author.id }, { "$set": { "chips": value } } ) 
                casino1.delete_one( { "member_id": author.id } )
                casino1.delete_one( { "member_id": author.id } )
                return await ctx.send(embed = discord.Embed(title = "Игра в кости 🎲", description = f"В игре { author.mention } с { member.mention } выйграл { member.mention }!\n**__Счет:__ { a }:{ b }**\n**Выйгрыш составляет __{ amount }__ фишек!**", color = 0x5CFA34))

            if a < b:
                cash = int( users1.find_one( { "id": author.id } )['chips'] )
                amount = int( casino1.find_one( { "member_id": author.id } )['bet'] )
                value = cash + amount
                users1.update_one( { "id": author.id }, { "$set": { "chips": value } } )
                cash = int( users1.find_one( { "id": member.id } )['chips'] )
                amount = int( casino1.find_one( { "author_id": member.id } )['bet'] )
                value = cash - amount
                users1.update_one( { "id": member.id }, { "$set": { "chips": value } } ) 
                casino1.delete_one( { "member_id": author.id } )
                return await ctx.send(embed = discord.Embed(title = "Игра в кости 🎲", description = f"В игре { member.mention } с { author.mention } выйграл { author.mention }!\n**__Счет:__ { a }:{ b }**\n**Выйгрыш составляет __{ amount }__ фишек!**", color = 0x5CFA34))
        else:
            await ctx.send(embed = discord.Embed(description = "Вам никто не предлагает ставку!", color = 0xF02925))


@client.command()
async def no( ctx ):		
	author = ctx.message.author

	if ctx.channel.name == 'test-channel' or ctx.channel.name == '💬family-chat' or ctx.channel.name == '🎰game-channel':
		if casino1.count_documents( { 'member_id': author.id } ) != 0:
			casino1.delete_one( { "member_id": author.id } )
			return await ctx.send(embed = discord.Embed(description = f"{ author.mention } отклонил ставку!", color = 0xF02925))

		else:
			await ctx.send(embed = discord.Embed(description = "Вам никто не предлагает ставку!", color = 0xF02925))


@client.command()
async def cancel( ctx ):
	author = ctx.message.author
	if ctx.channel.name == 'test-channel' or ctx.channel.name == '💬family-chat' or ctx.channel.name == '🎰game-channel':
		if casino1.count_documents( { "author_id": author.id } ) != 0:
			casino1.delete_one( { "author_id": author.id } )
			await ctx.send(embed = discord.Embed(description = "Вы успешно отменили ставку!", color = 0x5CFA34))

		else:
			await ctx.send(embed = discord.Embed(description = "Вы никому не предлагали ставку!", color = 0xF02925))




@client.command()
async def buychips( ctx, amount: int = None ):
    if ctx.channel.name == '🎰game-channel' or ctx.channel.name == 'test-channel':
        author = ctx.message.author
        cash = users1.find_one({ "id": author.id })['balance']
        if amount:
            if amount <= 0: return await ctx.send( embed =discord.Embed(description = f"**Нельзя купить фишек меньше либо раные нулю.**", color = 0xF02925) )
            try:
                int( amount )
                cost = amount * 100
                print(cash)
                print(cost)
                if float( cost ) > float( cash ): return await ctx.send( embed = discord.Embed(description = f"**У Вас недостаточно средств!**", color = 0xF02925) )
                await ctx.send(embed = discord.Embed(title = "Casino касса", description = f"**__Проведение транзакции пользователем { author.mention }__**\n\n**Покупка { amount } фишек за { cost } :euro:**", color = 0x5CFA34))

                if 'chips' in users1.find_one( { "id": author.id } ):
                    chips = users1.find_one( { "id": author.id } )['chips']
                    ch = int(chips) + amount
                    less = cash - cost
                    users1.update_one( { "id": author.id }, { "$set": { "chips": ch } } )
                    users1.update_one( { "id": author.id }, { "$set": { "balance": less } } )
                    print(1)
                else:
                    users1.update_one( { "id": author.id }, { "$inc": { "chips": amount } } )
                    print(2)
            
            except Exception as e:
                print(e)
        else:
            await ctx.send(embed = discord.Embed(description  = f"**__Используйте:__**\n**!buychips <количество фишек>**\n**__Стоимость покупки 1-ой фишки - 100 :euro:__**", color = 0x5CFA34))

@client.command()
async def chips( ctx, user: discord.Member = None ):
	author = ctx.message.author
	if ctx.channel.name == '🎰game-channel' or ctx.channel.name == 'test-channel':
		if user:
			if 'chips' in users1.find_one( { "id": user.id } ):
				chips = users1.find_one( { "id": user.id } )['chips']
				await ctx.send(embed = discord.Embed(description = f"**На данный момент у { user.mention } { chips } фишек.**", color = 0xF02925))

			else:
				await ctx.send(embed = discord.Embed(description = f"**У Вас нету ни одной фишки.**", color = 0x5CFA34))

		else:
			if 'chips' in users1.find_one( { "id": author.id } ):
				chips = users1.find_one( { "id": author.id } )['chips']
				await ctx.send(embed = discord.Embed(description = f"**На данный момент у Вас { chips } фишек.**", color = 0xF02925))

			else:
				await ctx.send(embed = discord.Embed(description = f"**У Вас нету ни одной фишки.**", color = 0x5CFA34))


@client.command()
async def sellchips( ctx, amount: int = None ):
	if ctx.channel.name == '🎰game-channel' or ctx.channel.name == 'test-channel':
		author = ctx.message.author
		cash = users1.find_one({ "id": author.id })['balance']
		if amount:
			if 'chips' in users1.find_one( { "id": author.id } ):
				chips = int( users1.find_one( { "id": author.id } )['chips'] )
				if amount <= 0: return await ctx.send( f"**Нельзя продать фишек меньше либо раные нулю.**" )
				if chips < amount:
					return await ctx.send(f"**У Вас нету такого кол-ва фишек.**")

				rub = amount * 90
				ch = chips - amount
				less = cash + rub
				users1.update_one( { "id": author.id }, { "$set": { "chips": ch } } )
				users1.update_one( { "id": author.id }, { "$set": { "balance": less } } )
				return await ctx.send(embed = discord.Embed(title = "Casino касса", description = f"**__Проведение транзакции пользователем { author.mention }__**\n\n**Продажа { amount } фишек за { rub } :euro:**", color = 0x5CFA34))
			else:
				await ctx.send(f"**У Вас нету ни одной фишки.**")
		else:
			await ctx.send(f"**Используйте:`\n`/sellchips <количество фишек>`\n`Стоимость продажи 1-ой фишки - 90 рублей.**")


@client.command()
async def public(ctx):
    embed = discord.Embed(
        title="Нажмите для перехода в группу семьи",
        description="Ссылка для перехода на группу семьи в VK",
        url='https://vk.com/arzwallace',
    )
    await ctx.send(embed=embed)

#balance
@client.command()

async def balance( ctx, user: discord.Member = None ):
    guild = client.get_guild(709144637020831774)
    author = ctx.message.author
    if user:
        if user in guild.members:
            balance = users1.find_one( { 'id': user.id } )[ "balance" ]
            emb = discord.Embed(description = f'**Баланс пользователя { user.mention } составляет - __{ int(balance) }__** 💶.', color = 0x5CFA34 )
            await ctx.send( embed = emb)
            

    else:
        balance = users1.find_one( { 'id': author.id } )[ "balance" ]
        emb = discord.Embed(description = f'**{ author.mention }, на данный момент на вашем балансе __{ int(balance) }__** 💶.', color = 0x5CFA34)
        await ctx.send( embed = emb)
        




#staff
@client.command()
async def staff(ctx):
    await ctx.send("**Действующее руководство семьи:**\n*Глава семьи - Strozza Wallace*\n\n**Заместители главы:**\n*Melissa Wallace\nFederico Wallace*")


@client.command()
async def buy( ctx, id = None ):
    if ctx.channel.name == '💬family-chat' or ctx.channel.name == 'test-channel' or ctx.channel.name == '🎰game-channel':
        if id:
            author = ctx.message.author
            i = 0
            i1 = 0
            for row in shop1.find():
                i += 1
                print( 'f' ) 
                if int( i ) == int( id ):
                    print('ff') 
                    i1 = 1
                    role_id = row['_id']
                    cost = float( row['cost'] )
                    type = row['value']
                    print('mn')
                    break
                print('lll')
            if i1 == 1:
                for row in users1.find( { "id": author.id } ):
                    a = row['balance']
                    if cost > a: return await ctx.send(f"**__Покупка невозможна!__**\nУ Вас недостаточно средств.")
                    role = ctx.guild.get_role( int( role_id ) )
                    if role in author.roles: return await ctx.send(f"**__Покупка невозможна!__**\nУ Вас уже куплена эта роль.")
                    times = time.time()
                    print('g')
                    times += 1209600
                    post = {
                        "id": author.id,
                        "role_id": role.id,
                        "time": times,
                    }
                    buy_role.insert_one(post)
                    print('jj')
                    await author.add_roles( role )
                    cash = a - cost
                    print('ffs')
                    await ctx.send(f"**Вы успешно приобрели данную роль. Роль действительна 14 дней.**")
                    print('ss')
            else: return await ctx.send( f"**Укажите верный id!**" )
    else:
        await ctx.send(f"**`Используйте:`\n`!buy <номер> - Для приобретения какой-либо роли.`**") 

@client.command()
async def shop( ctx, player: discord.Member = None ):
	if ctx.channel.name == '💬family-chat' or ctx.channel.name == 'test-channel' or ctx.channel.name == '🎰game-channel':
		
		i = 0
		i1 = 0
		message = ''
		emoji = ':euro:'
		for row in shop1.find():
			if row['value'] == 'balance': emoji = ':euro:'
			i += 1
			if ( i == 2 or i == 4 or i == 6 or i == 8 or i == 10 or i == 12 or i == 14 or i == 16 or i == 18 ): i1 = 1
			role = ctx.guild.get_role( int( row['_id'] ) )
			message += f'**№{ str(i) } { str(role.mention) }: { row["cost"] } { emoji }**\n\n' 
			# if i1 == 1: 
			# 	message += '\n\n'
			# 	i1 = 0

		embed = discord.Embed(title=f"__Магазин__:", description = message, color=0x9A3FD5)
		embed.set_footer( text = '!buy <номер> - Для приобретения какой-либо роли.\nСрок роли с момента её приобретения - 14 дней.' )

		await ctx.channel.send(embed = embed)


@client.command()
async def add_product( ctx, role_id, cost, value1 ):
    await ctx.channel.purge(limit = 1)
    author = ctx.message.author
    if( role_id and cost and value1 ):
        if( value1 == 'вирт'):
            role = ctx.guild.get_role( int( role_id ) )
            if role in ctx.guild.roles:
                post = {
                    "_id": role_id,
                    "cost": cost,
                    "value": f'{ value1 }',
                }
                shop1.insert_one( post )
                
                await ctx.send( embed = discord.Embed(description = f"**{ author.mention } добавил роль { role.mention } в магазин!**\n**__Заданная стоимость: {cost} :euro:__**", color = 0x70D934) )


@add_product.error
async def add_product_error(ctx,error):
    if isinstance (error, commands.MissingRequiredArgument):
        author = ctx.message.author
        emb = discord.Embed( description = f"{ author.mention }, Данной роли не существует!", color = 0xff0000)
        await ctx.send( embed = emb )

@client.command()
async def dell_product( ctx, role_id ):
	await ctx.channel.purge(limit = 1)
	author = ctx.message.author
	if role_id:
		if shop1.count_documents( { "_id": role_id } ) != 0:
			shop1.delete_one( { "_id": role_id } )
			role = ctx.guild.get_role( int( role_id ) )
			await ctx.send( embed = discord.Embed(description = f"**__{author.mention} удалил роль {role.mention} из магазина.__**", color = 0x4DD941))

		else:
			await ctx.send(embed = discord.Embed(description = f"{ author.mention }, Ошибка! Роль не найдена", color = 0xF02F24))

	else:
		await ctx.send( embed = discord.Embed(description = f"{ author.mention }, Ошибка, введите команду по форме: /dell_product <id роли>", color = 0xF02F24), delete_after = 5 )


# #edit event
# @client.event
# async def on_message_edit(ctx, before, after):
#     channel = client.get_channel( 725338050946924564 )
#     author = ctx.message.author
#     if before.content == after.content:
#         return
#     await channel.send(embed = discord.Embed(description = f'Сообщение было изменено пользователем - { author.mention }'))

#user
@client.command()

async def user( ctx, user: discord.Member = None ):
    guild = client.get_guild( 709133637020831774 )
    author = ctx.message.author
    emoji = client.get_emoji(867177297659822100)
    erep = client.get_emoji(868109639676489768)
    wark = client.get_emoji(868111109712932926)
    levs = client.get_emoji(868112129910272060)
    ops = client.get_emoji(868112072905461760)
    i = 0
    if user:
        rep = users1.find_one( { 'id': user.id } )[ "rep" ]
        balance = users1.find_one( { 'id': user.id } )[ "balance" ]
        lvl = users1.find_one( { 'id': user.id } )[ "lvl" ]
        exp = users1.find_one( { 'id': user.id } )[ "exp" ]
        idi = users1.find_one( { 'id': user.id } )[ "id" ]
        war = users1.find_one( { 'id': user.id } )[ "warns" ]
        lvlch = users1.find_one({'id': user.id})["lvlch"]
        chips = users1.find_one({'id': user.id})["chips"]
        emb = discord.Embed(description = f"**Профиль участника { user.mention }**\n\n\n**__Личная информация:__**\n**{levs} Уровень: { lvl }**\n**{erep} Репутация: { rep }**\n**{ops} Опыт: { exp } из { lvlch }**\n**{wark} Предупреждений: {war} из 3**\n\n**__Кошелек:__**\n**💶 Баланс: __{ int(balance) }__\n{emoji} Фишки: __{ chips }__**", color=0x9A3FD5)
        emb.set_thumbnail( url = user.avatar_url )
        emb.set_footer(text= f'ID участника { author.name } - { idi }')
        await ctx.send(embed=emb)
    else:
        rep = users1.find_one( { 'id': author.id } )[ "rep" ]
        balance = users1.find_one( { 'id': author.id } )[ "balance" ]
        lvl = users1.find_one( { 'id': author.id } )[ "lvl" ]
        exp = users1.find_one( { 'id': author.id } )[ "exp" ]
        idi = users1.find_one( { 'id': author.id } )[ "id" ]
        war = users1.find_one( { 'id': author.id } )[ "warns" ]
        lvlch = users1.find_one({'id': author.id})["lvlch"]
        chips = users1.find_one({'id': author.id})["chips"]
        emb = discord.Embed(description = f"**Профиль участника { author.mention }**\n\n\n**__Личная информация:__**\n**{levs} Уровень: { lvl }**\n**{erep} Репутация: { rep }**\n**{ops} Опыт: { exp } из { lvlch }**\n**{wark} Предупреждений: {war} из 3**\n\n**__Кошелек:__**\n**💶 Баланс: __{ int(balance) }__\n{emoji} Фишки: __{ chips }__**", color=0x9A3FD5)
        emb.set_thumbnail( url = author.avatar_url )
        emb.set_footer(text= f'ID участника { author.name } - { idi }')
        await ctx.send(embed=emb)
        
@client.command()
async def leadersmoney( ctx ):
        counter = 0
        embed = discord.Embed(title='**`Топ-10` Участников по валюте:**', color = 0x9A3FD5)
        for row in users1.find().sort( 'balance', pymongo.DESCENDING ):
            if counter == 10: break
            usr = ctx.guild.get_member( row['id'] )
            if usr is not None:
                if not usr.bot:
                    counter += 1
                    embed.add_field(name=f'**№ { counter }.** { usr.display_name }', value = f'**Деньги: __{ round( row["balance"], 2 ) }__ :euro:**', inline = False)
                    embed.set_footer(text = f'Вызвано: {ctx.message.author}', icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed = embed)

@client.command()
async def leaderboard( ctx ):
        counter = 0
        embed = discord.Embed(title='**`Топ-10` Участников по уровню:**', color = 0x9A3FD5)
        for row in users1.find().sort( 'lvl', pymongo.DESCENDING ):
            if counter == 10: break
            usr = ctx.guild.get_member( row['id'] )
            if usr is not None:
                if not usr.bot:
                    counter += 1
                    embed.add_field(name=f'**№ { counter }.** { usr.display_name }', value = f'**Уровень: __{ round( row["lvl"], 2 ) }__ ⭐️**', inline = False)
                    embed.set_footer(text = f'Вызвано: {ctx.message.author}', icon_url = ctx.message.author.avatar_url)

        await ctx.send(embed = embed)



#info command

@client.command()
async def info( ctx, member: discord.Member ):
    emb = discord.Embed( title = f'Информация о пользователе {member.display_name}', color = 0xff0000)
    emb.add_field( name = "Дата присоединения на сервер: ", value = member.joined_at, inline = False )
    emb.add_field( name = 'Имя: ', value = member.display_name, inline = False )
    emb.add_field( name = 'ID: ', value = f' { member.id } 🔑 ', inline = False )
    emb.add_field( name = 'Аккаунт создан: ', value = member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline = False )
    emb.set_thumbnail( url = member.avatar_url )
    emb.set_footer( text = f'Вызвано: { ctx.message.author }', icon_url = ctx.message.author.avatar_url )
    await ctx.send(embed = emb)

@info.error
async def info_error(ctx,error):
    if isinstance (error, commands.MissingRequiredArgument):
        emb = discord.Embed( title = 'Вы не указали участника!', color = 0xff0000)
        await ctx.send( embed = emb )


#Peresvet Mudak
@client.command()
async def piss( ctx, member: discord.Member ):
    emb = discord.Embed( color = 0xfd8268 )
    emb.add_field( name = f'{ctx.message.author.display_name} обоссал { member.display_name }', value = f'обоссаный { member.display_name } убегает в кустики 😭'  )
    emb.set_thumbnail( url= 'https://live.staticflickr.com/2530/3956896475_8833a3d92a.jpg' )
    await ctx.send( embed = emb)




#give_money
@client.command()
async def give( ctx, user: discord.Member = None, amount: int = None ):
    author = ctx.message.author
    channel = client.get_channel(868125861356908594)
    if user and amount:
        if author == user:
            return await ctx.send( f'Ошибка!' )
        balance = users1.find_one( { 'id': author.id } )[ "balance" ]
        if balance < amount:
            return await ctx.send(f'{ author.mention }, вы ввели неверное значение.')
        balance_user = users1.find_one( { 'id': user.id } )[ "balance" ]
        balance -= amount
        balance_user += amount
        users1.update_one( { "id": author.id }, { "$set": { "balance": balance } } )
        users1.update_one( { "id": user.id }, { "$set": { "balance": balance_user } } )
        await channel.send( embed = discord.Embed(description = f'{author.mention} передал {user.mention} {amount} :euro:'))
        await ctx.send(embed = discord.Embed(description = f'**{ author.mention } успешно перевел пользователю { user.mention } - { amount } 💶.**\n\n**__Баланс пользователя { user.name } составляет - { balance_user } 💶__**'))
        
#give_chips
@client.command()
async def givechips( ctx, user: discord.Member = None, amount: int = None ):
    author = ctx.message.author
    channel = client.get_channel(868125861356908594)
    if user and amount:
        if author == user:
            return await ctx.send( embed = discord.Embed(description = f'Вы не можете передать фишки сами себе!', color = 0x70D934) )
        balance = users1.find_one( { 'id': author.id } )[ "chips" ]
        if balance < amount:
            return await ctx.send(f'{ author.mention }, вы ввели неверное значение.')
        balance_user = users1.find_one( { 'id': user.id } )[ "chips" ]
        balance -= amount
        balance_user += amount
        emoji = client.get_emoji(867177297659822100)
        users1.update_one( { "id": author.id }, { "$set": { "chips": balance } } )
        users1.update_one( { "id": user.id }, { "$set": { "chips": balance_user } } )
        await channel.send( embed = discord.Embed(description = f'{author.mention} передал {user.mention} {amount} {emoji}'))
        await ctx.send(embed = discord.Embed(description = f'**{ author.mention } успешно передал пользователю { user.mention } - { amount } фишек {emoji}.**\n\n**__У { user.name } на данный момент - { balance_user } фишек :coin:__**', color = 0x70D934))

@client.command()
@commands.has_permissions(administrator = True)
async def givemoney(ctx, user: discord.Member = None, amount: int = None):
    author = ctx.message.author
    balance = users1.find_one( { 'id': author.id } )["balance"]
    balance += amount
    users1.update_one( { "id": author.id }, { "$set": { "balance": balance } } )
    users1.update_one( { "id": user.id }, { "$set": { "balance": balance } } )
    if author == user:
        await ctx.send( embed = discord.Embed(description = f'{author.mention} выдал себе - { amount } 💶', color = 0x70D934) )
    else:
        await ctx.send(embed = discord.Embed(description = f'{author.mention} добавил к балансу пользователя { user.mention } - { amount } 💶', color = 0x70D934))
    
@givemoney.error
async def givemoney_error(ctx,error):
    if isinstance (error, commands.MissingRequiredArgument):
        emb = discord.Embed(description = f'{ctx.author.mention}, **введите команду корректно!**\n\n**__Пример:__ !givemoney @Участник [Значение]**', color = 0xF03426)
        emb.set_thumbnail(url='https://aliexpressom.ru/images/aliexpressom/2017/12/oshibka-pri-sintaksicheskom-analize-paketa.jpeg')
        await ctx.send(embed = emb)
    if isinstance(error, commands.MissingPermissions):
        emb = discord.Embed(description = f'{ctx.author.mention}, **у Вас нет доступа к данной команде.**', color = 0xF03426)
        emb.set_thumbnail(url='https://aliexpressom.ru/images/aliexpressom/2017/12/oshibka-pri-sintaksicheskom-analize-paketa.jpeg')
        await ctx.send(embed = emb)



@client.command()
@commands.has_permissions(administrator = True)
async def givechip(ctx, user: discord.Member = None, amount: int = None):
    author = ctx.message.author
    balance = users1.find_one( { 'id': author.id } )["chips"]
    balance += amount
    users1.update_one( { "id": author.id }, { "$set": { "chips": balance } } )
    users1.update_one( { "id": user.id }, { "$set": { "chips": balance } } )
    if author == user:
        await ctx.send( embed = discord.Embed(description = f'**{author.mention} выдал себе - __{ amount } фишек :coin:__**', color = 0x70D934) )
    else:
        await ctx.send(embed = discord.Embed(description = f'**{author.mention} добавил к балансу пользователя { user.mention } - __{ amount } фишек :coin:__**', color = 0x70D934))
    
@givechip.error
async def givechip_error(ctx,error):
    if isinstance (error, commands.MissingRequiredArgument):
        emb = discord.Embed(description = f'{ctx.author.mention}, **введите команду корректно!**\n\n**__Пример:__ !givechips @Участник [Значение]**', color = 0xF03426)
        emb.set_thumbnail(url='https://aliexpressom.ru/images/aliexpressom/2017/12/oshibka-pri-sintaksicheskom-analize-paketa.jpeg')
        await ctx.send(embed = emb)
    if isinstance(error, commands.MissingPermissions):
        emb = discord.Embed(description = f'{ctx.author.mention}, **у Вас нет доступа к данной команде.**', color = 0xF03426)
        emb.set_thumbnail(url='https://aliexpressom.ru/images/aliexpressom/2017/12/oshibka-pri-sintaksicheskom-analize-paketa.jpeg')
        await ctx.send(embed = emb)



@client.command()
@commands.has_permissions(administrator = True)
async def setmoney(ctx, user: discord.Member = None, amount: int = None):
    author = ctx.message.author
    balance = users1.find_one( { 'id': author.id } )["balance"]
    balance = amount
    users1.update_one( { "id": author.id }, { "$set": { "balance": balance } } )
    users1.update_one( { "id": user.id }, { "$set": { "balance": balance } } )
    if author == user:
        await ctx.send( embed = discord.Embed(description = f'{author.mention} изменил своё значение баланса на - **__{ int(amount) } 💶__**', color = 0x70D934) )
    elif balance == 0:
        await ctx.send(embed = discord.Embed(description = f'**Баланс пользователя { user.mention } обнулен.**', color = 0x70D934))
    else:
        await ctx.send(embed = discord.Embed(description = f'{author.mention} изменил значение баланса пользователя { user.mention } на - **__{ int(amount) } 💶__**', color = 0x70D934))

@setmoney.error
async def setmoney_error(ctx,error):
    if isinstance (error, commands.MissingRequiredArgument):
        emb = discord.Embed(description = f'{ctx.author.mention}, **введите команду корректно!**\n\n**__Пример:__ !setmoney @Участник [Значение]**\n**Для того, что бы обнулить баланс - укажите "0"**', color = 0xF03426)
        emb.set_thumbnail(url='https://aliexpressom.ru/images/aliexpressom/2017/12/oshibka-pri-sintaksicheskom-analize-paketa.jpeg')
        await ctx.send(embed = emb)
    if isinstance(error, commands.MissingPermissions):
        emb = discord.Embed(description = f'{ctx.author.mention}, **у Вас нет доступа к данной команде.**', color = 0xF03426)
        emb.set_thumbnail(url='https://aliexpressom.ru/images/aliexpressom/2017/12/oshibka-pri-sintaksicheskom-analize-paketa.jpeg')
        await ctx.send(embed = emb)


@client.command()
@commands.has_permissions(administrator = True)
async def setchips(ctx, user: discord.Member = None, amount: int = None):
    author = ctx.message.author
    balance = users1.find_one( { 'id': author.id } )["chips"]
    balance = amount
    users1.update_one( { "id": author.id }, { "$set": { "chips": balance } } )
    users1.update_one( { "id": user.id }, { "$set": { "chips": balance } } )
    if author == user:
        await ctx.send( embed = discord.Embed(description = f'**{author.mention} изменил себе количество фишек на - __{ int(amount) } :coin:__**', color = 0x70D934) )
    elif balance == 0:
        await ctx.send(embed = discord.Embed(description = f'**Баланс пользователя { user.mention } обнулен.**', color = 0x70D934))
    else:
        await ctx.send(embed = discord.Embed(description = f'**{author.mention} изменил количество фишек пользователю { user.mention } на - __{ int(amount) } :coin:__**', color = 0x70D934))

@setchips.error
async def setchips_error(ctx,error):
    if isinstance (error, commands.MissingRequiredArgument):
        emb = discord.Embed(description = f'{ctx.author.mention}, **введите команду корректно!**\n\n**__Пример:__ !setchips @Участник [Значение]**\n**Для того, что бы обнулить фишки - укажите "0"**', color = 0xF03426)
        emb.set_thumbnail(url='https://aliexpressom.ru/images/aliexpressom/2017/12/oshibka-pri-sintaksicheskom-analize-paketa.jpeg')
        await ctx.send(embed = emb)
    if isinstance(error, commands.MissingPermissions):
        emb = discord.Embed(description = f'{ctx.author.mention}, **у Вас нет доступа к данной команде.**', color = 0xF03426)
        emb.set_thumbnail(url='https://aliexpressom.ru/images/aliexpressom/2017/12/oshibka-pri-sintaksicheskom-analize-paketa.jpeg')
        await ctx.send(embed = emb)

@client.command()
async def timely( ctx ):
    author = ctx.message.author
    if timely1.count_documents({'id': author.id}) == 0:
		
        times = time.time()
        tim1 = 86400
        tim2 = times + tim1
        cash = 1500
        cash += users1.find_one({'id': author.id})['balance']
        users1.update_one({ 'id': author.id }, { '$set': { 'balance': cash } })
        post = {
			"id": author.id,
			"time": tim2,
		}
        timely1.insert_one( post )
        if tim1 == 0:
            await ctx.send(f"**Вы получили ежедневный бонус в виде** **__1500__** **вирт.**")
        else:
            time1 = time.time()
            time2 = float(timely1.find_one({ "id": author.id })['time'])
            time3 = time2 - time1
            tim1 = time.gmtime( time3 )
            times = time.strftime( '`%H:%M`', tim1 )
            await ctx.send(f"**До следующего использования данной команды должно пройти:\n{ times }\n\n**")






@client.command()
async def fwarn( ctx, user: discord.Member = None, member: discord.Member = None, reason  = None):
    author = ctx.message.author
    warning = users1.find_one( { "id": user.id } )["warns"]
    warning += 1
    users1.update_one( { "id": user.id }, { "$set": { "warns": warning } } )
    await ctx.send(embed = discord.Embed(description = f'**{author.mention} выдал { warning } предупреждение из 3 пользователю { user.mention }**', color = 0x70D934))
    if warning >= 3:
        await ctx.send(f'{ user.mention } был заблокирован так как получил 3/3 предупреждений')
        await member.ban(reason='3/3 предупреждений')


@client.command()
async def unfwarn(ctx, user: discord.Member = None, reason  = None):
    author = ctx.message.author
    warning = users1.find_one( { "id": user.id } )["warns"]
    warning = 0
    users1.update_one( { "id": user.id }, { "$set": { "warns": warning } } )
    await ctx.send(embed = discord.Embed(description = f'**{author.mention} аннулировал предупреждения пользователю { user.mention }**', color = 0x70D934))


@client.event
async def on_voice_state_update(member, before, after):
    if before.channel == after.channel:
        return
    if not before.channel:
        channel = client.get_channel(725338050946924564)
        embed = discord.Embed(description = f"Пользователь {member.mention} подключился к голосовому каналу.\nКанал: {after.channel.mention}", color = member.color)
        return await channel.send(embed = embed)
    if not after.channel:
        channel = client.get_channel(725338050946924564)
        embed = discord.Embed(description = f"Пользователь {member.mention} покинул голосовой канал.\nКанал: {before.channel.mention}", color = member.color)
        return await channel.send(embed = embed)
    else:
        channel = client.get_channel(725338050946924564)
        embed = discord.Embed(description = f"Пользователь {member.mention} перешел в другой голосовой канал.\nИз канала: {before.channel.mention} в канал: {after.channel.mention}", color = member.color)
        return await channel.send(embed = embed)





#rep
@client.command()

async def rep( ctx, user: discord.Member = None ):
    guild = client.get_guild(709144637020831774)
    author = ctx.message.author
    if user:
        if user in guild.members:
            rep = users1.find_one( { 'id': user.id } )[ "rep" ]
            emb = discord.Embed(description = f'У пользователя { user.mention } на данный момент **{ rep }** репутации.  🔥', color = 0xFA9900)
            await ctx.send( embed = emb )

    else:
        rep = users1.find_one( { 'id': author.id } )[ "rep" ]
        emb = discord.Embed(description = f'{ author.mention }, на данный момент у Вас **{ rep }** репутации.  🔥', color = 0xFA9900)
        await ctx.send( embed = emb )
        


#.clear command

@client.command()

async def hello( ctx, amount = 1 ):
	await ctx.channel.purge( limit = amount )

	author = ctx.message.author
	await ctx.send( f'**Здарова, __{ author.mention }__, пососи мне член**' )


#CAPTURE COMMAND

@client.command()
@commands.has_permissions(view_audit_log = True)
async def captureinfo( ctx, time1 = None, reason = None, reason1 = None, await_time: int = None ):
    await ctx.message.delete()
    channel = client.get_channel( 867171815049527306 )
    if time and reason and await_time:
        emb = discord.Embed(description = f"{ ctx.message.author.mention } хочет забить капт.\n**__Параметры:__**\nСемья **__{reason}__** против семьи **__{reason1}__**\n**__Время встречи:__**\n**{time1} по МСК.**\n\n**Для одобрения используйте - !yes**\n**Для отказа используйте !no**", color = 0xff0000)
        emb.set_thumbnail( url='https://i.ytimg.com/vi/7XSpZcUEtvw/maxresdefault.jpg')
        await channel.send( embed = emb )
        # for row in capture.find():
        #      if "id" not in row:
        #          capture.update_one({"id": row["id"]}, {"$set": {"id": member.id}})
        post = {
            "await_time": await_time * 60 + time.time(),
            "time": time1,
            "reason": reason,
            "reason1": reason1,
        }
        capture.insert_one(post)
    else:
        emb1 = discord.Embed(description = f"{ctx.message.author.mention} Вы некорректно указали семью, дату и время!", color = 0xff0000)
        emb1.add_field(name="Пример:", value = "!captureinfo [Время] [Семья, которая забила] [Семья которой забили] [Время до оповещения в минутах]")
        await ctx.send( embed = emb1 )



@client.command()
async def cinfo(ctx):
    await ctx.message.delete()
    message = ""
    for row in capture.find():
        message += f'**⚔️ {row["reason"]}** vs **{row["reason1"]}**, сегодня в **{row["time"]}**\n'
        print(message)
    await ctx.send("<@&861944441527205918>")
    emb = discord.Embed(title="Капты на сегодня:", description = message, color = 0xff0000)
    await ctx.send(embed = emb)

# @captureinfo.error
# async def captureinfo_error(ctx,error):
#     if isinstance (error, commands.MissingRequiredArgument):
#         emb = discord.Embed(description = f"{ctx.message.author.mention} Вы некорректно указали семью, дату и время!", color = 0xff0000)
#         emb.add_field(name="Пример:", value = "!captureinfo[Время] [Семья без пробелов]")
#         await ctx.send( embed = emb )
#     if isinstance(error, commands.MissingPermissions):
#         emb = discord.Embed(description = f"{ctx.message.author.mention},у Вас недостаточно прав для данной команды!", color = 0xff0000)
#         await ctx.send( embed = emb )





# @capture.error
# async def capture_error(ctx,error):
#     if isinstance (error, commands.MissingRequiredArgument):
#         emb = discord.Embed(description = f"{ctx.message.author.mention} Вы некорректно указали семью, дату и время!", color = 0xff0000)
#         emb.add_field(name="Пример:", value = "!capture [Дата в формате xx/xx/xxxx][Время] [Семья без пробелов]")
#         await ctx.send( embed = emb )
#     if isinstance(error, commands.MissingPermissions):
#         emb = discord.Embed(description = f"{ctx.message.author.mention},у Вас недостаточно прав для данной команды!", color = 0xff0000)
#         await ctx.send( embed = emb )





@client.command()

async def bye( ctx, amount = 1 ):
	await ctx.channel.purge( limit = amount )

	author = ctx.message.author
	await ctx.send( f'**__{ author.mention }__, давай уебывай, перхоть ебаная.**' )



#level
@client.command()

async def level( ctx, user: discord.Member = None ):
    guild = client.get_guild( 709144637020831774 )
    author = ctx.message.author
    if user:
        if user in guild.members:
            lvl = users1.find_one( { 'id': user.id } )[ "lvl" ]
            exp = users1.find_one({'id': user.id})["exp"]
            lvlch = users1.find_one({'id': user.id})["lvlch"]
            await ctx.send( embed = discord.Embed(description = f'**Пользователь { user.mention } имеет { lvl } уровень и `{ exp }` опыта из `{ lvlch }`⭐**') )

    else:
        lvl = users1.find_one( { 'id': author.id } )[ "lvl" ]
        exp = users1.find_one({'id': author.id})["exp"]
        lvlch = users1.find_one({'id': author.id})["lvlch"]
        await ctx.send( embed = discord.Embed(description = f'**{ author.mention }, на данный момент у Вас { lvl } уровень и `{ exp }` опыта из `{ lvlch }`⭐**') )




#.clear

@client.command()

async def clear(ctx, amount = None):
    author = ctx.message.author
    await ctx.channel.purge(limit=int(amount))

    await ctx.send(f'```Пользователь { author.name } удалил { amount } сообщений!```')





@clear.error
async def clear_error(ctx,error):
    if isinstance (error, commands.MissingRequiredArgument):
        await ctx.send(f'**{ctx.author.mention}, обязательно укажите аргумент!**')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'**{ctx.author.mention}, вы не обладаете такими правами!**')





#.ban

@client.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def ban (ctx, member: discord.Member, *, reason = None):
    emb = discord.Embed (title = 'Бан :lock:', colour = discord.Color.dark_red())

    await ctx.channel.purge(limit = 1)

    await member.ban(reason = reason)

    emb.set_author (name = member.name, icon_url = member.avatar_url)
    emb.add_field (name = 'Пользователь заблокирован', value = 'Блокировка пользователя : {}'.format(member.mention))
    emb.set_footer (text = 'Был заблокирован администратором {}'.format (ctx.author.name), icon_url = ctx.author.avatar_url)

    await ctx.send (embed = emb)






#.unban


@client.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member):
    await ctx.channel.purge(limit = 1)
    emb = discord.Embed (title = 'Разблокировка :unlock:', color = discord.Color.purple())
    banned_users = await ctx.guild.bans()

    for ban_entry in banned_users:
        user = ban_entry.user

        await ctx.guild.unban (user)
        emb.set_author (name = member.name, icon_url = member.avatar_url)
        emb.add_field (name = 'Разблокирован пользователь', value = 'Разблокирован пользователь : {}'.format(member.mention))
        emb.set_footer (text = 'Был разблокирован модератором {}'.format (ctx.author.name), icon_url = ctx.author.avatar_url)
        await ctx.send (embed = emb)
        return





@unban.error
async def unban_error(ctx,error):
    if isinstance (error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name}, обязательно укажите аргумент без @!')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'**{ctx.author.mention}, вы не обладаете такими правами!**')



#.help
@client.command()

async def help( ctx ):
    await ctx.channel.purge( limit = 1 )

    
    version = "v2.0"
    emb1 = discord.Embed( title = 'Навигация по командам' )
    emb1.add_field( name = '{}clear'.format( PREFIX ), value = 'Очистить чат 📬' )
    emb1.add_field( name = '{}rep'.format( PREFIX ), value = 'Узнать репутацию (Свою/Участника) 🚩\n' )
    emb1.add_field( name = '{}balance'.format( PREFIX ), value = 'Узнать баланс (Свой/Участника) 💶\n' )
    emb1.add_field( name = '{}level'.format( PREFIX ), value = 'Узнать свой уровень и опыт 📄\n' )
    emb1.add_field( name = '{}mute'.format( PREFIX ), value = 'Заглушить участника 🔇 [Для модераторов]\n' )
    emb1.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f'Mr. Wallace Bot by Strozza | { version }' )
    
    emb2 = discord.Embed( title = 'Навигация по командам' )
    emb2.add_field( name = '{}unmute'.format( PREFIX ), value = 'Снять мут участнику 🔇 [*Для модераторов*]\n' )
    emb2.add_field( name = '{}user'.format( PREFIX ), value = 'Узнать информацию о себе/участнике 📄\n' )
    emb2.add_field( name = '{}kick'.format( PREFIX ), value = 'Выгнать участника 🔒\n' )
    emb2.add_field( name = '{}staff'.format( PREFIX ), value = 'Список действующего руководства семьи 🔒\n' )
    emb2.add_field( name = '{}give'.format( PREFIX ), value = 'Передать деньги участнику 💶\n' )
    emb2.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f'Mr. Wallace Bot by Strozza | { version }' )
    
    emb3 = discord.Embed( title = 'Навигация по командам' )
    emb3.add_field( name = '{}ban'.format( PREFIX ), value = 'Заблокировать участника 🔒 [*Для руководителей*]\n' )
    emb3.add_field( name = '{}bye'.format( PREFIX ), value = 'Попрощаться с ботом 🚩\n' )
    emb3.add_field( name = '{}cub'.format( PREFIX ), value = 'Бросить кубик 🎲\n' )
    emb3.add_field( name = '{}cinfo'.format( PREFIX ), value = 'Проверить забитые капты\n' )
    emb3.add_field( name = '{}captureinfo'.format( PREFIX ), value = 'Забить капт (Только для роли **Manager of Capture** и выше ) 🚩\n' )
    emb3.set_footer( icon_url = ctx.guild.owner.avatar_url, text = f'Mr. Wallace Bot by Strozza | { version }' )

    embeds = [emb1, emb2, emb3]
    reactions = ["⬅️", "➡️"]
    message = await ctx.send(embed = emb1)
    page = pag(client, message, only=ctx.author, use_more=False, reactions=reactions)
    await page.start()










# Ping
@client.command()

async def ping(ctx):
    ping = client.ws.latency # Получаем пинг клиента

    ping_emoji = '🟩🔳🔳🔳🔳' # Эмоция пинга, если он меньше 100ms

    if ping > 0.10000000000000000:
        ping_emoji = '🟧🟩🔳🔳🔳' # Эмоция пинга, если он больше 100ms

    if ping > 0.15000000000000000:
        ping_emoji = '🟥🟧🟩🔳🔳' # Эмоция пинга, если он больше 150ms

    if ping > 0.20000000000000000:
        ping_emoji = '🟥🟥🟧🟩🔳' # Эмоция пинга, если он больше 200ms

    if ping > 0.25000000000000000:
        ping_emoji = '🟥🟥🟥🟧🟩' # Эмоция пинга, если он больше 250ms

    if ping > 0.30000000000000000:
        ping_emoji = '🟥🟥🟥🟥🟧' # Эмоция пинга, если он больше 300ms

    if ping > 0.35000000000000000:
        ping_emoji = '🟥🟥🟥🟥🟥' # Эмоция пинга, если он больше 350ms

    message = await ctx.send('Пожалуйста, подождите. . .') # Переменная message с первоначальным сообщением
    await message.edit(content = f'*Ping Бота!* {ping_emoji} `{ping * 1000:.0f}ms` ⏳') # Редактирование первого сообщения на итоговое (на сам пинг)
    print(f'[Logs:utils] Пинг сервера был выведен | {prefix}ping') # Информация в консоль, что команда "ping" была использована
    print(f'[Logs:utils] На данный момент пинг == {ping * 1000:.0f}ms | {prefix}ping') # Вывод пинга в консоль



@client.command()
async def weather( ctx, arg ):
    observation = mgr.weather_at_place(arg)
    w = observation.weather
    temp = int(w.temperature('celsius')["temp"])
    humidity = w.humidity
    wind = w.wind()['speed']
    sunrise_iso = w.sunrise_time(timeformat='iso')
    sunrset_iso = w.sunset_time(timeformat='iso')
    temp_max = w.temperature('celsius')['temp_max']
    temp_min = w.temperature('celsius')['temp_min']
    temp = w.temperature('celsius')['temp']
    emb = discord.Embed(title = f"Прогноз погоды в городе {arg}", description = f"🏙️ В городе **{arg}** сейчас **{w.detailed_status}**\n\n💨 Ветер: **{str(wind)}** метра(ов) в секунду\n\n🌡 Текущая температура: **{str(temp)}°**\n\n🌡 Максимальная температура сегодня: **{str(temp_max)}°**\n\n🌡 Минимальная температура сегодня: **{str(temp_min)}°**\n\n🌅 Восход солнца: **{ sunrise_iso }**\n\n🌇 Закат солнца: **{ sunrset_iso }**")
    await ctx.send(embed = emb)



#.kick

@client.command(pass_context = True)
@commands.has_permissions(view_audit_log = True)

async def kick (ctx, member: discord.Member, *, reason):
    emb = discord.Embed (title = 'Kick :wave:', colour = discord.Color.red())
    await member.kick(reason = reason)
    emb.set_author (name = member.name, icon_url = member.avatar_url)
    emb.add_field (name = 'Пользователь кикнут', value = 'Выгнан пользователь : {}'.format(member.mention))
    emb.set_footer (text = 'Был выгнан с сервера лидером семьи {}'.format (ctx.author.name), icon_url = ctx.author.avatar_url)
    await member.kick(reason = reason)
    await ctx.send (embed = emb)
    




@kick.error
async def kick_error(ctx,error):
    if isinstance (error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name}, обязательно укажите причину!')
    if isinstance(error, commands.MissingPermissions):
         await ctx.send(f"**У Вас недостаточно прав**")





#mute

@client.command()
@commands.has_permissions(view_audit_log = True)

async def mute (ctx, member: discord.Member, time:int, reason):
    channel = client.get_channel( 725338050946924564 )
    rolemute = discord.utils.get( ctx.guild.roles, id = 794997077142667284 )
    emb = discord.Embed(title=f"🔇 Использована команда Mute", color = 0xff0000)
    emb.add_field(name = 'Модератор', value = ctx.message.author.mention, inline = False)
    emb.add_field(name = 'Нарушитель', value = member.mention)
    emb.add_field(name = 'Причина: ', value = reason, inline = False)
    emb.add_field(name = 'Время: ', value = f"{time} минут", inline = False)
    emb.set_footer (text = '🔇 Мут выдан модератором {}'.format (ctx.author.name), icon_url = ctx.author.avatar_url)
    await member.add_roles( rolemute )
    await ctx.send(embed = emb)
    await channel.send(embed = emb)
    await asyncio.sleep(time * 60)
    await member.remove_roles(rolemute)

@mute.error
async def mute_error(ctx,error):
    if isinstance (error, commands.MissingRequiredArgument):
        emb = discord.Embed(description = f'{ctx.author.mention}, **убедитесь, что вы указали время и причину!**\n\nПример: `!mute @Участник [Время] [Причина]`', color = 0xF03426)
        emb.set_thumbnail(url='https://aliexpressom.ru/images/aliexpressom/2017/12/oshibka-pri-sintaksicheskom-analize-paketa.jpeg')
        await ctx.send(embed = emb)
    if isinstance(error, commands.MissingPermissions):
        emb = discord.Embed(description = f'{ctx.author.mention}, **у Вас нет доступа к данной команде.**', color = 0xF03426)
        emb.set_thumbnail(url='https://aliexpressom.ru/images/aliexpressom/2017/12/oshibka-pri-sintaksicheskom-analize-paketa.jpeg')
        await ctx.send(embed = emb)






#avatar command

@client.command()
async def avatar( ctx, member: discord.Member ):
    emb = discord.Embed( title = f'Аватар пользователя - {member.display_name}', color = 0xff0000)
    emb.set_image( url = member.avatar_url )
    await ctx.send( embed = emb)

@avatar.error
async def avatar_error(ctx,error):
    if isinstance (error, commands.MissingRequiredArgument):
        emb = discord.Embed( title = 'Вы не указали участника!', color = 0xff0000)
        await ctx.send( embed = emb )

@client.command()
@commands.has_permissions(view_audit_log = True)

async def unmute (ctx, member: discord.Member):
    channel = client.get_channel( 725338050946924564 )
    unrolemute = discord.utils.get( ctx.guild.roles, id = 794997077142667284 )
    emb = discord.Embed(title=f"🔇 Использована команда unMute", color = 0xff0000)
    emb.add_field(name = 'Модератор', value = ctx.message.author.mention, inline = False)
    emb.add_field(name = 'Нарушитель', value = member.mention)
    emb.set_footer (text = '🔇 Мут снят пользователем {}'.format (ctx.author.name), icon_url = ctx.author.avatar_url)
    await member.remove_roles( unrolemute )
    await ctx.send(embed = emb)
    await channel.send(embed = emb)
    

    
    #emb.set_author (name = member.name, icon_url = member.avatar_url)
    #emb.add_field (name = 'Чат заблокирован', value = 'Блокировка чата пользователю : {}'.format(member.mention))
    #emb.set_footer (text = 'Был помещён в мут модератором {}'.format (ctx.author.name), icon_url = ctx.author.avatar_url)
    #await ctx.send (embed = emb)






#crash

# @commands.command()
# async def crash(self, ctx, bet: int = None, coef: int = None):
#     if bet is None:
#         await ctx.send(f"{ctx.author.name}, Укажи сумму!")

#     elif coef is None:
#         await ctx.send(f"{ctx.author.name}, Укажи коэффициент!")

#     elif coef <= 1:
#         await ctx.send(f"{ctx.author.name}, Коэффициент должен быть выше 1x!")

#     else:
#         if cash < bet:
#             await ctx.send(f"{ctx.author.name}, У тебя недостаточно денег!")

#         else:
#             # ограничение по беттингу (10/100000)
#             if bet < 10:
#                 await ctx.send("Минимальная ставка 10 монет!")
#             elif bet > 100000:
#                 await ctx.send("Максимальная ставка 100000 монет!")

#             else:
#                 #Для генерации результата в режиме Crash требуется 1 случайное число в интервале (0..1),
#                 #которое затем переводится в коэффициент Crash, имеющий экспоненциальное распределение,
#                 #по следующему алгоритму.
#                 number = random.randint(0, 1)
#                 crashOutcome = 1000000 / (math.floor(number * 1000000) + 1) * (1 - 0.05)

#                 #Иногда может выпасть число по типу 0.99 или меньше, в самой игре такого нет,
#                 #этот IF спасает от таких ситуации.
#                 if crashOutcome <= 1:
#                     crashOutcome = 1.00

#                 #если коэф пользователя выше или равен крашу, то он выиграл
#                 if crashOutcome >= coef:
#                     winCash = bet * coef - bet
#                     roundWinCash = round(winCash)
#                     await ctx.send(content= ctx.author.mention, embed = discord.Embed(title="📈 Сломанный Краш", description=f"{ctx.author.name}, ты выиграл: **+{round(roundWinCash)} :euro:**\n\nКоэф: **{round(crashOutcome, 2)}**\nТы поставил на коэф: **{round(coef,2)}**\nТвоя ставка: **{bet}**"))

#                     #Тут уже входит в силу ваша база данных.
#                     #переменная roundWinCash, это выигрыш пользователя.

#                 #или проиграл :(
#                 else:
#                     await ctx.send(content= ctx.author.mention, embed = discord.Embed(title="📈 Сломанный Краш", description=f"{ctx.author.name}, ты проиграл: **{bet} :euro:**\n\nКоэф: **{round(crashOutcome, 2)}**\nТы поставил на коэф: **{round(coef,2)}**\nТвоя ставка: **{bet}**"))

#                     #Тут уже входит в силу ваша база данных.
#                     #тут вы должны снять с баланса пользователя его ставку




@tasks.loop(seconds=60.0)
async def checker():
    for guild in client.guilds:
        for row in capture.find():
            if row["await_time"] <= time.time():
                channel = guild.get_channel(861942997361229864)
                capture.delete_one({"await_time": row["await_time"] })
                emb = discord.Embed(f'Напоминаем, что в {row["time1"]} назначена встреча семьи {row["reason"]} с семьей {row["reason1"]}. Всем явиться на территорию!')
                emb.set_thumbnail( url='https://i.ytimg.com/vi/7XSpZcUEtvw/maxresdefault.jpg')
                await channel.send(embed = emb)
        
        for row in timely1.find():
            if row['time'] <= time.time():
                print( row['id'] )
                print('Тимели')
                member = guild.get_member( row['id'] )
                print(member)
                if member != None:
                    timely1.delete_one( { "id": member.id } )

token = open( 'token.txt', 'r' ).readline()

client.run( token )



