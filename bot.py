import discord
from discord.ext import commands, tasks
import logging
from datetime import datetime
import asyncio

# Configurer les logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "BOT_TOKEN"  # Remplacez par le token de votre bot
CHANNEL_ID = 1234567890123456789  # Remplacez par l'ID du salon pour bump
ROLE_ID = 1234567890123456789  # Remplacez par l'ID du rôle qui va être ping

intents = discord.Intents.all()  # Permissions pour l'accès aux événements du bot
bot = commands.Bot(command_prefix="+", intents=intents, help_command=None)

# Variable pour la fréquence du bump
bump_interval = 5  # Par défaut, toutes les 5 heures

# Fonction pour démarrer la tâche avec la bonne fréquence
def start_bump_task():
    if bump_reminder.is_running():
        bump_reminder.change_interval(hours=bump_interval)
    else:
        bump_reminder.start()

# Tâche de rappel pour le bump
@tasks.loop(hours=bump_interval)
async def bump_reminder():
    await bot.wait_until_ready()
    logger.info("bump_reminder est en cours d'exécution...")

    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        try:
            await channel.send(f"<@&{ROLE_ID}> **N'oubliez pas de bump le serveur avec `/bump` !**")
            logger.info(f"Message de rappel envoyé avec succès dans le canal {CHANNEL_ID}.")
        except discord.errors.Forbidden:
            logger.error(f"Erreur : Le bot n'a pas la permission d'envoyer des messages dans le canal {CHANNEL_ID}.")
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi du message dans le canal {CHANNEL_ID}: {e}")
    else:
        logger.error(f"Erreur : Impossible de trouver le canal {CHANNEL_ID}. Vérifie les permissions et l'ID.")

# Commande pour modifier la fréquence du bump
@bot.command()
async def setbump(ctx, heures: int):
    global bump_interval

    if heures < 1:
        await ctx.send("🚨 La fréquence minimale est de 1 heure !")
        return

    bump_interval = heures
    start_bump_task()
    await ctx.send(f"✅ La fréquence du bump est maintenant réglée à toutes les **{heures} heures**.")

# Commande de bienvenue
@bot.event
async def on_ready():
    logger.info(f"{bot.user} a bien été connecté !")
    await asyncio.sleep(1)

    # Démarrage du rappel de bump
    start_bump_task()
    logger.info("La tâche bump_reminder a été démarrée !")

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
    
    embed = discord.Embed(
        title="À propos de moi",
        description=f"Je suis **{bot.user.name}**. Je suis connecté depuis le {current_date} à {current_time}.",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="Pour me soutenir",
        value="- GitHub: [Clique ici](https://github.com/delete-user-56)\n- Discord: [Rejoins ici](https://discord.gg/kkuU6CbQBG)\n- YouTube: [Ma chaîne](https://www.youtube.com/@Vulcain56)",
        inline=False
    )
    
    await ctx.send(embed=embed)

# Commande d'aide
@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Commandes du Bot",
        description="Voici la liste des commandes disponibles.",
        color=discord.Color.blue()
    )

    embed.add_field(name="+ping", value="Renvoie 'Pong!' pour tester que le bot est actif.", inline=False)
    embed.add_field(name="+info", value="Affiche des informations sur le bot.", inline=False)
    embed.add_field(name="+setbump <heures>", value="Modifie la fréquence du rappel de bump.", inline=False)
    embed.add_field(name="+help", value="Affiche ce message d'aide.", inline=False)

    embed.add_field(
        name="Pour me soutenir",
        value="- GitHub: [Clique ici](https://github.com/delete-user-56)\n- Discord: [Rejoins ici](https://discord.gg/kkuU6CbQBG)\n- YouTube: [Ma chaîne](https://www.youtube.com/@Vulcain56)",
        inline=False
    )

    embed.set_footer(text="Bot développé par deleted_user_562 | Version 1.6")
    await ctx.send(embed=embed)

bot.run(TOKEN)
