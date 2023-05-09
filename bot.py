import discord
from discord.ext import tasks, commands
from discord import utils
import datetime
import asyncio
import re

#import unicodedata

import config



intents = discord.Intents.default()
intents.members = True
intents.invites = True
intents.guilds = True
intents.bans = True
intents.emojis = True

bot = commands.Bot(command_prefix = config.settings['prefix'], intents = intents)
bot.remove_command( 'help' )


@bot.event
async def on_ready():
	#print(f'[Log] Bot {bot.user.name} has been started.')
	channel = bot.get_channel(config.tech_channel)
	await channel.send('Start')


@bot.event
async def on_command_error(ctx, error):
	emb = discord.Embed(title = f'Ошибка!', description = f'{ctx.author.name}, у вас нет прав для выполнения данной команды.', colour = discord.Color.red())
	await ctx.send(embed = emb)


@bot.event
async def on_member_remove(member):
	emb=discord.Embed(title = 'Участник отсоединился', description = f'{member.mention} покинул сервер.', colour = discord.Color.orange())
	emb.set_thumbnail(url = member.avatar_url)
	emb.set_footer(text = f'user ID: {member.id}')

	channel = bot.get_channel(config.tech_channel)
	await channel.send(embed = emb)


@bot.event
async def on_member_join(member):
	emb=discord.Embed(title = 'Участник присоединился', description = f'{member.mention} зашел на сервер.', colour = discord.Color.orange())
	emb.set_thumbnail(url = member.avatar_url)
	emb.set_footer(text = f'user ID: {member.id}')

	channel = bot.get_channel(config.tech_channel)
	await channel.send(embed = emb)


@bot.event
async def on_message_delete(message):
	if message.author.id != config.settings['id']:
		emb = discord.Embed(title = 'Удалили сообщение', description = f'{message.author.mention} удалил сообщение.', colour = discord.Color.red())
		emb.set_thumbnail(url = message.author.avatar_url)
		emb.add_field(name = 'Сообщение:', value = F'```{message.content}```', inline = False)
		emb.add_field(name = 'Канал:', value = f'{message.channel.mention}', inline = True)
		emb.set_footer(text = f'user ID: {message.author.id}')

		channel = bot.get_channel(config.tech_channel)
		await channel.send(embed = emb)


@bot.event
async def on_message_edit(message_before, message_after):
	if message_before.author.id != config.settings['id']:
		emb = discord.Embed(title = 'Отредактировали сообщение', description = f'{message_before.author.mention} отредактировал сообщение.', colour = discord.Color.blue())
		emb.set_thumbnail(url = message_before.author.avatar_url)
		emb.add_field(name = 'Старое сообщение:', value = f'```{message_before.content}```', inline = False)
		emb.add_field(name = 'Новое сообщение:', value = f'```{message_after.content}```', inline = False)
		emb.add_field(name = 'Канал:', value = f'{message_before.channel.mention}', inline = True)
		emb.set_footer(text = f'user ID: {message_after.author.id}')

		channel = bot.get_channel(config.tech_channel)
		await channel.send(embed = emb)


@bot.event
async def on_member_update(before, after):
	if len(before.roles) != len(after.roles):
		channel = bot.get_channel(config.tech_channel)

		if len(before.roles) < len(after.roles):
			role = str(list(set(after.roles) - set(before.roles))).split(' ')
			role = before.guild.get_role(role_id = int(role[1][3:]))

			emb = discord.Embed(title = 'Добавили роль участнику', description = f'{before.mention} получил роль {role.mention}.', colour = discord.Color.green())
			emb.add_field(name = 'Название:', value = f'```{role.name}```', inline = False)
			emb.add_field(name = 'role ID:', value = f'```{role.id}```', inline = False)
		else:
			role = str(list(set(before.roles) - set(after.roles))).split(' ')
			role = before.guild.get_role(role_id = int(role[1][3:]))

			emb = discord.Embed(title = 'Удалили роль участнику', description = f'{before.mention} потерял роль {role.mention}.', colour = discord.Color.red())			
			emb.add_field(name = 'Название:', value = f'```{role.name}```', inline = False)
			emb.add_field(name = 'role ID:', value = f'```{role.id}```', inline = False)

		emb.set_thumbnail(url = before.avatar_url)
		emb.set_footer(text = f'user ID: {before.id}')
		await channel.send(embed = emb)
	if before.display_name != after.display_name:
		emb = discord.Embed(title = 'Изменили ник', description = f'{before.mention} изменил ник.', colour = discord.Color.blue())
		emb.set_thumbnail(url = before.avatar_url)
		emb.add_field(name = 'Старый ник:', value = f'```{before.display_name}```', inline = True)
		emb.add_field(name = 'Новый ник:', value = f'```{after.display_name}```', inline = True)
		emb.set_footer(text = f'user ID: {before.id}')

		channel = bot.get_channel(config.tech_channel)
		await channel.send(embed = emb)


@bot.event
async def on_guild_channel_create(channel):
	emb = discord.Embed(title = 'Создали канал', description = '', colour = discord.Color.green())
	emb.add_field(name = 'Название категории:', value = f'```{channel.category}```', inline = False)
	emb.add_field(name = 'Название канала:', value = f'```{channel.name}```', inline = False)
	emb.add_field(name = 'Тип канала:', value = f'```{channel.type}```', inline = False)
	emb.add_field(name = 'Ссылка:', value = f'{channel.mention}', inline = False)
	emb.set_footer(text = f'channel ID: {channel.id}')

	channel = bot.get_channel(config.tech_channel)
	await channel.send(embed = emb)


@bot.event
async def on_guild_channel_delete(channel):
	emb = discord.Embed(title = 'Удалили канал', description = '', colour = discord.Color.red())
	emb.add_field(name = 'Название категории:', value = f'```{channel.category}```', inline = False)
	emb.add_field(name = 'Название канала:', value = f'```{channel.name}```', inline = False)
	emb.add_field(name = 'Тип канала:', value = f'```{channel.type}```', inline = False)
	emb.set_footer(text = f'channel ID: {channel.id}')

	channel = bot.get_channel(config.tech_channel)
	await channel.send(embed = emb)


@bot.event
async def on_user_update(before, after):
	urls = [before.avatar_url_as(size = 128), after.avatar_url_as(size = 128)]
	emb = discord.Embed(title = 'Отредактировали свои данные', description = f'{before.mention} изменил фото или имя.', colour = discord.Color.blue())
	emb.set_thumbnail(url = urls[1])
	emb.add_field(name = 'Старое имя:', value = f'```{before.name}```', inline = True)
	emb.add_field(name = 'Новое имя:', value = f'```{after.name}```', inline = True)
	emb.add_field(name = '\u200b', value = '\u200b', inline = True)
	emb.add_field(name = 'Старое фото:', value = '\u200b', inline = True)
	emb.set_image(url = urls[0])
	emb.set_footer(text = f'user ID: {after.id}')

	channel = bot.get_channel(config.tech_channel)
	await channel.send(embed = emb)


@bot.event
async def on_guild_role_create(role):
	emb = discord.Embed(title = 'Создана новая роль', description = f'{role.mention}', colour = discord.Color.green())
	emb.add_field(name = 'Название:', value = f'```{role.name}```', inline = True)
	emb.set_footer(text = f'role ID: {role.id}')

	channel = bot.get_channel(config.tech_channel)
	await channel.send(embed = emb)


@bot.event
async def on_guild_role_delete(role):
	emb = discord.Embed(title = 'Удалена роль', description = '', colour = discord.Color.red())
	emb.add_field(name = 'Название:', value = f'```{role.name}```', inline = True)
	emb.set_footer(text = f'role ID: {role.id}')

	channel = bot.get_channel(config.tech_channel)
	await channel.send(embed = emb)


def true_or_false(emoji):
	if emoji: return '✅'
	else: return '❌'


@bot.event
async def on_guild_role_update(before, after):
	if (before.name != after.name) or (before.color != after.color) or (before.permissions != after.permissions):
		emb = discord.Embed(title = 'Отредактировали роль', description = f'{after.mention}', colour = discord.Color.blue())
		emb.add_field(name = 'Старое название:', value = f'```{before.name}```', inline = True)
		emb.add_field(name = 'Новое название:', value = f'```{after.name}```', inline = True)
		emb.add_field(name = '\u200b', value = '\u200b', inline = True)
		emb.add_field(name = 'Старый цвет:', value = f'```{before.color}```', inline = True)
		emb.add_field(name = 'Новый цвет:', value = f'```{after.color}```', inline = True)
		emb.add_field(name = '\u200b', value = '\u200b', inline = True)
		emb.add_field(name = 'Отображается отдельно от всех участников:', value = f'```{true_or_false(after.hoist)}```', inline = False)
		emb.add_field(name = 'Может ли быть упомянута другими участниками:', value = f'```{true_or_false(after.mentionable)}```', inline = False)

		emb.add_field(name = '\u200b', value = '\u200b', inline = False)
		emb.add_field(name = 'Права:', value = '\u200b', inline = False)

		emb.add_field(name = '\u200b', value = f'```Добавлять реакции: {true_or_false(after.permissions.add_reactions)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Администратор: {true_or_false(after.permissions.administrator)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Прикреплять файлы: {true_or_false(after.permissions.attach_files)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Банить участников: {true_or_false(after.permissions.ban_members)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Менять никнейм: {true_or_false(after.permissions.change_nickname)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Создавать приглашение: {true_or_false(after.permissions.create_instant_invite)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Оглушать участников: {true_or_false(after.permissions.deafen_members)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Вставлять ссылки: {true_or_false(after.permissions.embed_links)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Внешние смайлики: {true_or_false(after.permissions.external_emojis)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Выгонять участников: {true_or_false(after.permissions.kick_members)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Управлять каналами: {true_or_false(after.permissions.manage_channels)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Управлять смайликами: {true_or_false(after.permissions.manage_emojis)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Управлять сервером: {true_or_false(after.permissions.manage_guild)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Управлять сообщениями: {true_or_false(after.permissions.manage_messages)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Управлять никнеймами: {true_or_false(after.permissions.manage_nicknames)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Управлять правами: {true_or_false(after.permissions.manage_permissions)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Управлять ролями: {true_or_false(after.permissions.manage_roles)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Управлять вебхуками: {true_or_false(after.permissions.manage_webhooks)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Упомянуть всех: {true_or_false(after.permissions.mention_everyone)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Перемещать участников: {true_or_false(after.permissions.move_members)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Мутить участников: {true_or_false(after.permissions.mute_members)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Приоритетный режим: {true_or_false(after.permissions.priority_speaker)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Читать историю сообщений: {true_or_false(after.permissions.read_message_history)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Читать сообщения: {true_or_false(after.permissions.read_messages)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Просьба выступить: {true_or_false(after.permissions.request_to_speak)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Отправлять сообщения: {true_or_false(after.permissions.send_messages)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Отправлять tts сообщения: {true_or_false(after.permissions.send_tts_messages)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Говорить: {true_or_false(after.permissions.speak)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Стримить: {true_or_false(after.permissions.stream)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Использовать внешние смайлики: {true_or_false(after.permissions.use_external_emojis)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Использовать слеш(/) команды: {true_or_false(after.permissions.use_slash_commands)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Использовать активацию по голосу: {true_or_false(after.permissions.use_voice_activation)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Просматривать журнал аудита: {true_or_false(after.permissions.view_audit_log)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Просматривать канал: {true_or_false(after.permissions.view_channel)}```', inline = True)
		emb.add_field(name = '\u200b', value = f'```Просматривать информацию о сервере: {true_or_false(after.permissions.view_guild_insights)}```', inline = True)

		emb.set_footer(text = f'role ID: {after.id}')

		channel = bot.get_channel(config.tech_channel)
		await channel.send(embed = emb)


@bot.event
async def on_member_ban(guild, user):
	emb = discord.Embed(title = 'Участник забанен', description = f'{user.mention} получил бан.', colour = discord.Color.red())
	emb.set_thumbnail(url = user.avatar_url)
	emb.set_footer(text = f'user ID: {user.id}')

	channel = bot.get_channel(config.tech_channel)
	await channel.send(embed = emb)


@bot.event
async def on_member_unban(guild, user):
	emb = discord.Embed(title = 'Участник разбанен', description = f'{user.mention} получил разбан.', colour = discord.Color.green())
	emb.set_thumbnail(url = user.avatar_url)
	emb.set_footer(text = f'user ID: {user.id}')

	channel = bot.get_channel(config.tech_channel)
	await channel.send(embed = emb)


def connect_or_disconnect(before, after):
	if before.channel == None: return 'подключился к каналу'
	elif (before.channel != after.channel) and (before.channel != None) and (after.channel != None): return 'переместился в другой канал'
	else:  return 'отключился от канала'


@bot.event
async def on_voice_state_update(member, before, after):
	emb = discord.Embed(title = f'Кто-то {connect_or_disconnect(before, after)}', description = f'{member.mention} {connect_or_disconnect(before, after)}.', colour = discord.Color.purple())
	emb.set_thumbnail(url = member.avatar_url)
	if connect_or_disconnect(before, after) == 'отключился от канала': emb.add_field(name = 'Канал:', value = f'{before.channel.mention}', inline = False)
	elif connect_or_disconnect(before, after) == 'переместился в другой канал': 
		emb.add_field(name = 'Старый канал:', value = f'{before.channel.mention}', inline = False)
		emb.add_field(name = 'Новый канал:', value = f'{after.channel.mention}', inline = False)
	elif connect_or_disconnect(before, after) == 'подключился к каналу': emb.add_field(name = 'Канал:', value = f'{after.channel.mention}', inline = False)
	emb.set_footer(text = f'user ID: {member.id}')

	channel = bot.get_channel(config.tech_channel)
	await channel.send(embed = emb)


def moderation_level(level):
	if str(level) == 'none': return 'Отсутствует'
	elif str(level) == 'low': return 'Низкий'
	elif str(level) == 'medium': return 'Средний'
	elif str(level) == 'high': return 'Высокий'
	elif str(level) == 'extreme': return 'Самый высокий'


@bot.event
async def on_guild_update(before, after):
	if (before.name != after.name) or (before.region != after.region) or (before.verification_level != after.verification_level) or (before.icon_url != after.icon_url):
		emb = discord.Embed(title = f'Изменили настройки сервера', description = f'', colour = discord.Color.purple())

		if before.name != after.name:
			emb.add_field(name = 'Старое название:', value = f'```{before.name}```', inline = True)
			emb.add_field(name = '\u200b', value = '\u200b', inline = True)
			emb.add_field(name = 'Новое название:', value = f'```{after.name}```', inline = True)
		if before.region != after.region:
			emb.add_field(name = 'Старый регион:', value = f'```{before.region}```', inline = True)
			emb.add_field(name = '\u200b', value = '\u200b', inline = True)
			emb.add_field(name = 'Новый регион:', value = f'```{after.region}```', inline = True)
		if before.verification_level != after.verification_level:
			emb.add_field(name = 'Старый уровень проверки:', value = f'```{moderation_level(before.verification_level)}```', inline = True)
			emb.add_field(name = '\u200b', value = '\u200b', inline = True)
			emb.add_field(name = 'Новый уровень проверки:', value = f'```{moderation_level(after.verification_level)}```', inline = True)
		if before.icon_url != after.icon_url:
			emb.add_field(name = 'Сменили иконку', value = '\u200b', inline = True)
			emb.set_thumbnail(url = after.icon_url)

		channel = bot.get_channel(config.tech_channel)
		await channel.send(embed = emb)


@bot.event
async def on_guild_emojis_update(guild, before, after):
	#print(before, '\n', after)
	if (len(before) < len(after)) or (len(before) > len(after)):
		if len(before) < len(after):
			emojis = str(list(set(after) - set(before))).split(' ')
			emoji = bot.get_emoji(int(emojis[1][3:]))
			emb = discord.Embed(title = f'Добавили эмодзи', description = f'', colour = discord.Color.green())
			emb.set_thumbnail(url = emoji.url)
			emb.add_field(name = 'Название:', value = f'```{emoji.name}```', inline = True)
		elif len(before) > len(after):
			print(before)
			emojis = str(list(set(before) - set(after))).split(' ')
			emb = discord.Embed(title = f'Удалили эмодзи', description = f'', colour = discord.Color.red())
			emb.add_field(name = 'Название:', value = f'```{emojis[2][6:-1]}```', inline = True)

		channel = bot.get_channel(config.tech_channel)
		await channel.send(embed = emb)


@bot.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def clear(ctx, amount = 2):
	await ctx.channel.purge(limit = amount)


@bot.event
async def on_message(message):
	await bot.process_commands(message)
	msg = message.content.lower()

	#print("".join(re.findall("\d+", msg)))

	'''print(str(''.join([unicodedata.normalize('NFD', msg)])))

	if str(''.join([unicodedata.normalize('NFD', msg)])) in config.zalgo:
		await message.channel.purge(limit = 1)'''

	if message.channel.id == config.code_channel:
		if config.student_code in msg:
			channel = bot.get_channel(config.code_channel)
			await message.channel.purge(limit = 1)

			member = message.author
			role = member.guild.get_role(config.student_role)
			await member.add_roles(role)

			emb = discord.Embed(title = f'{message.author.name}, Вас повысили!', description = f'Новая роль: {role.mention}', colour = discord.Color.red())
			emb.set_thumbnail(url = message.author.avatar_url)
			emb.add_field(name = '\u200b', value = f'{config.student_message}', inline = True)

			await message.channel.send(embed = emb)

			await asyncio.sleep(60)
			await message.channel.purge(limit = 1)
		else:
			if message.author.id != config.admin_id:
				if message.author.id != config.moder_id:
					if message.author.id != config.settings['id']:
						await message.channel.purge(limit = 1)
	else:
		if config.student_code in msg:
			await message.channel.purge(limit = 1)


bot.run(config.settings['token'])