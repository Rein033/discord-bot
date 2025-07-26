# 🚀 Discord Mega Bot

Een alles-in-één Discord bot met **moderatie, muziek, leveling, giveaways, notificaties, tickets, auto-responses en meer!**  
Gebouwd met **Python** en **discord.py v2**.

---

## ✅ Functies & Modules
### 🔹 **Moderation**
Beheer je server met eenvoudige commando's:
- `!kick @user [reden]` → Kick een gebruiker
- `!ban @user [reden]` → Ban een gebruiker
- `!unban Naam#0000` → Unban een gebruiker
- `!mute @user` → Mute een gebruiker
- `!unmute @user` → Unmute een gebruiker
- `!warn @user [reden]` → Geef een waarschuwing
- `!clear [aantal]` → Verwijder berichten

### 🔹 **Music**
Speel muziek in voice kanalen (YouTube via yt-dlp):
- `!join` → Bot joint voice channel
- `!leave` → Bot verlaat voice channel
- `!play <YouTube URL>` → Voeg nummer toe aan queue
- `!skip` → Skip huidig nummer
- `!pause` → Pauzeer muziek
- `!resume` → Hervat muziek
- `!stop` → Stop muziek en leeg queue

### 🔹 **Fun**
Leuke commands voor entertainment:
- `!ping` → Test of de bot online is
- `!joke` → Random grap

### 🔹 **Giveaways**
Organiseer giveaways:
- `!giveaway <tijd_in_sec> <prijs>` → Start giveaway (gebruik 🎉 om mee te doen)

### 🔹 **Leveling**
Laat leden levelen door actief te zijn:
- `!rank` → Bekijk jouw level en XP
- `!leaderboard` → Top 10 spelers

### 🔹 **Notifications**
Automatische meldingen voor streams & uploads:
- `!setnotify #kanaal` → Stel kanaal in voor notificaties
- `!settwitch <username>` → Twitch gebruiker instellen
- `!setyoutube <channel_id>` → YouTube kanaal instellen

### 🔹 **Auto-Responder**
Maak custom reacties voor keywords:
- `!addresponse <trigger> <response>` → Voeg auto-response toe
- `!removeresponse <trigger>` → Verwijder trigger
- `!responses` → Lijst van triggers

### 🔹 **Tickets**
Support systeem voor servers:
- `!ticket` → Maak een ticketkanaal
- `!close` → Sluit ticket

### 🔹 **Stats**
Bekijk serverstatistieken:
- `!serverstats` → Info over leden, kanalen, etc.
- `!userstats [@user]` → Activiteit van gebruiker
- `!topactive` → Top 10 actieve leden

---

## ✅ Installatie
1. **Clone de repository**:
   ```bash
   git clone <jouw-repo>
   cd discord-bot
