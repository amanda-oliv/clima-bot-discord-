import discord
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

intents = discord.Intents.default()
intents.message_content = True  # se o bot precisa ler mensagens
intents.members = True          # se o bot acessa membros do servidor

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')

@bot.command()
async def clima(ctx, *, cidade: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={WEATHER_API_KEY}&units=metric&lang=pt_br"
    resposta = requests.get(url)
    
    if resposta.status_code == 200:
        dados = resposta.json()
        nome = dados['name']
        temp = dados['main']['temp']
        descricao = dados['weather'][0]['description']
        umidade = dados['main']['humidity']
        vento = dados['wind']['speed']

        mensagem = (
            f"🌤️ **Clima em {nome}:**\n"
            f"🌡️ Temperatura: {temp}°C\n"
            f"📝 Condição: {descricao}\n"
            f"💧 Umidade: {umidade}%\n"
            f"💨 Vento: {vento} m/s"
        )
    else:
        mensagem = "❌ Cidade não encontrada! Verifique o nome e tente novamente."

    await ctx.send(mensagem)

bot.run(TOKEN)