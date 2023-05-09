audit.start()
print('[Log] Цикл запущен.')


@tasks.loop(seconds = 2.0)
async def audit():
	before_audit = []
	async for entry in bot.get_guild(config.guild_id).audit_logs():
		before_audit.append(entry)

	if config.before_log != str(before_audit[-1].id):
		config.before_log = str(before_audit[-1].id)
		emb = discord.Embed(title = 'Новая запись в журнале аудита', description = '', colour = discord.Color.purple())
		emb.set_thumbnail(url = before_audit[-1].user.avatar_url)
		emb.add_field(name = 'Исполнитель:', value = f'{before_audit[-1].user.mention}\n```user ID {before_audit[-1].user.id}```', inline = False)
		emb.add_field(name = 'Действие:', value = f'```{str(before_audit[-1].action)[15:]}```', inline = False)
		emb.add_field(name = 'Категория:', value = f'```{str(before_audit[-1].category)[23:]}```', inline = False)
		emb.set_footer(text = f'audit log ID: {before_audit[-1].id}')

		channel = bot.get_channel(config.tech_channel)
		await channel.send(embed = emb)
	else: pass


@bot.event
async def on_invite_create(invite):
	emb = discord.Embed(title = 'Создано приглашение', description = f'{invite}', colour = discord.Color.green())
	emb.add_field(name = 'Создал приглашение:', value = f'{invite.inviter.mention}', inline = False)
	emb.set_footer(text = f'invite ID: {invite.id}')

	channel = bot.get_channel(config.tech_channel)
	await channel.send(embed = emb)


@bot.event
async def on_invite_delete(invite):
	emb = discord.Embed(title = 'Удалено приглашение', description = f'{invite}', colour = discord.Color.red())
	emb.set_footer(text = f'invite ID: {invite.id}')

	channel = bot.get_channel(config.tech_channel)
	await channel.send(embed = emb)


@bot.event
async def on_guild_channel_update(before, after):
	emb = discord.Embed(title = 'Отредактировали канал', description = '', colour = discord.Color.blue())
	emb.add_field(name = 'Старое название категории:', value = f'```{before.category}```', inline = True)
	emb.add_field(name = 'Новое название категории:', value = f'```{after.category}```', inline = True)
	emb.add_field(name = '\u200b', value = '\u200b', inline = True)
	emb.add_field(name = 'Старое название канала:', value = f'```{before.name}```', inline = True)
	emb.add_field(name = 'Новое название канала:', value = f'```{after.name}```', inline = True)
	emb.add_field(name = '\u200b', value = '\u200b', inline = True)
	emb.add_field(name = 'Тип канала:', value = f'```{after.type}```', inline = True)
	emb.add_field(name = '\u200b', value = '\u200b', inline = True)
	emb.add_field(name = '\u200b', value = '\u200b', inline = True)
	emb.add_field(name = 'Ссылка:', value = f'{after.mention}', inline = False)
	emb.set_footer(text = f'channel ID: {after.id}')

	channel = bot.get_channel(config.tech_channel)
	await channel.send(embed = emb)
