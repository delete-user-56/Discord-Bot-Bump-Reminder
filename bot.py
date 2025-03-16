import discord
from discord.ext import commands, tasks
import logging
from datetime import datetime
import asyncio

# Configurer les logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "BOT_TOKEN"
CHANNEL_ID = 1295786617428119664
ROLE_ID = 1345067345911222443

intents = discord.Intents.all()  # Permissions pour l'accès aux événements du bot
bot = commands.Bot(command_prefix="+", intents=intents, help_command=None)

# Rappel pour le bump
@tasks.loop(hours=5)
async def bump_reminder():
    await bot.wait_until_ready()
    logger.info("bump_reminder est en cours d'exécution...")

    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        try:
            # Envoie du message de rappel
            await channel.send(f"<@&{ROLE_ID}> **N'oubliez pas de bump le serveur avec `/bump` !**")
            logger.info(f"Message de rappel envoyé avec succès dans le canal {CHANNEL_ID}.")
        except discord.errors.Forbidden:
            logger.error(f"Erreur : Le bot n'a pas la permission d'envoyer des messages dans le canal {CHANNEL_ID}.")
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi du message dans le canal {CHANNEL_ID}: {e}")
    else:
        logger.error(f"Erreur : Impossible de trouver le canal {CHANNEL_ID}. Vérifie les permissions et l'ID.")

# Commande de bienvenue
@bot.event
async def on_ready():
    logger.info(f"{bot.user} a bien été connecté !")
    await asyncio.sleep(1)

    # Démarrage du rappel de bump si pas déjà en cours
    if not bump_reminder.is_running():
        bump_reminder.start()
        logger.info("La tâche bump_reminder a été démarrée !")
    else:
        logger.warning("La tâche bump_reminder était déjà en cours !")

    logger.info(f"Bot connecté comme {bot.user}")

    # Envoi du message de bienvenue
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        try:
            current_date = datetime.now().strftime("%d-%m-%Y")
            current_time = datetime.now().strftime("%H:%M:%S")
            await channel.send(f"**Bot connecté en tant que** `{bot.user.name}` **le** `{current_date}` **à** `{current_time}` **avec succès ! 🚀**")
            logger.info(f"Message de bienvenue envoyé avec succès dans le canal {CHANNEL_ID}.")
        except discord.errors.Forbidden:
            logger.error(f"Erreur : Le bot n'a pas la permission d'envoyer des messages dans le canal {CHANNEL_ID}.")
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi du message de bienvenue dans le canal {CHANNEL_ID}: {e}")
    else:
        logger.error(f"Erreur : Impossible de trouver le canal {CHANNEL_ID}. Vérifie l'ID et les permissions.")

# Commande de base : Ping
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

# Commande de base : Info
@bot.command()
async def info(ctx):
    current_date = datetime.now().strftime("%d-%m-%Y")
    current_time = datetime.now().strftime("%H:%M:%S")
    
    # Création du message d'info
    embed = discord.Embed(
        title="À propos de moi",
        description=f"Je suis **{bot.user.name}**. Je suis connecté depuis le {current_date} à {current_time}.",
        color=discord.Color.blue()
    )
    
    # Ajout des liens pour soutenir
    embed.add_field(
        name="Pour me soutenir",
        value="- GitHub: [Clique ici](https://github.com/delete-user-56)\n- Discord: [Rejoins ici](https://discord.gg/kkuU6CbQBG)\n- YouTube: [Ma chaîne](https://www.youtube.com/@Vulcain56)",
        inline=False
    )
    
    # Envoi de l'embed
    await ctx.send(embed=embed)

# Commande d'aide avec un embed
@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Commandes du Bot",
        description="Voici une liste des commandes disponibles et leur description.",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="+ping",
        value="Renvoie 'Pong!' pour tester que le bot est actif.",
        inline=False
    )

    embed.add_field(
        name="+info",
        value="Affiche des informations sur le bot, comme son nom et l'heure de connexion.",
        inline=False
    )

    embed.add_field(
        name="+help",
        value="Affiche ce message d'aide avec la liste des commandes.",
        inline=False
    )

    # Ajout des liens pour soutenir en bas
    embed.add_field(
        name="Pour me soutenir",
        value="- GitHub: [Clique ici](https://github.com/delete-user-56)\n- Discord: [Rejoins ici](https://discord.gg/kkuU6CbQBG)\n- YouTube: [Ma chaîne](https://www.youtube.com/@Vulcain56)",
        inline=False
    )

    embed.set_footer(text="Bot développé par deleted_user_562 | Version 1.4")
    await ctx.send(embed=embed)

bot.run(TOKEN)
