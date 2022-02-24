#!/usr/bin/env python3

import discord
from discord.utils import get
import time
from random import *
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.utils import find
from discord.ext.commands import Bot
import os

bot = commands.Bot(command_prefix="/", description="Le jeu du Motus adapté à discord !")

emoji_jaune = {'A': 945780457595895838, 'B': 945780460175364187., 'C': 945780459760148553, 'D': 945780460036968458,
               'E': 945780459189698580, 'F': 945780458971611147, 'G': 945780460112474172, 'H': 945780459273613402,
               'I': 945780459403608114, 'J': 945780459382661190, 'K': 945780460183760916, 'L': 945780461425295370,
               'M': 945780460397662298, 'N': 945780460238295071, 'O': 945780459860803596, 'P': 945780459940487169,
               'Q': 945780460590604289, 'R': 945780460313784330, 'S': 945780459948892241, 'T': 945780459932110878,
               'U': 945780460255059988, 'V': 945780460544491591, 'W': 945780460481560626, 'X': 945780460594810880,
               'Y': 945780841370492949, 'Z': 945780841328562246}

emoji_vert = {'A': 945778515150766110, 'B': 945778515243044904, 'C': 945778513393377280, 'D': 945778515205296129,
               'E': 945778513426931742, 'F': 945778513674399814, 'G': 945778515486339102, 'H': 945778513988976650,
               'I': 945778513733095544, 'J': 945778513691172949, 'K': 945778515184336948, 'L': 945778514039291924,
               'M': 945778515134021643, 'N': 945778515461169192, 'O': 945778515704442970, 'P': 945778514450321429,
               'Q': 945778515574423572, 'R': 945778515796705280, 'S': 945778515926745158, 'T': 945778514269974529,
               'U': 945778515956097065, 'V': 945778515805081631, 'W': 945778515956097065, 'X': 945778515574415381,
               'Y': 945778516157415434, 'Z': 945778515670868059}

stats_init = {'money': 10, 'diamonds': 0, 'games': [0, 0, 0, 0, 0, 0, 0], 'notifs': False}


def full_of_zeros(list):
    ''' Détermine si une liste est pleine de zéros '''
    for elem in list:
        if elem != 0:
            return False
    return True


def sauvegarder(data, nom):
    ''' Stocke des données dans un fichier local dont le nom est passé en paramètre '''
    fichier = open(nom, "w")
    fichier.write(str(data))
    fichier.close()


def lire_data(nom):
    ''' Lit les données stockées dans un fichier ligne par ligne et les renvoie sous forme de liste '''
    data_txt = open(nom)
    data = data_txt.readlines()
    return data


def get_data(nom):
    ''' Lit le contenu d'un fichier et l'évalue '''
    data = ''
    data_list = lire_data(nom)
    for elem in data_list:
        data += elem
    data = eval(data)
    return data


@bot.command()
async def stats(ctx):
    '''Affiche les stats d'un joueur'''
    id = ctx.message.author.id
    stats = get_data("stats.txt")

    if id not in stats:
        stats[id] = stats_init
        sauvegarder(stats, "stats.txt")

    embed = discord.Embed(title=":sparkles: Sutom :sparkles:", description="**Inventaire**\n" + str(stats[id]['money']) +
                                                                           'x:coin:\n')
    txt = ''
    for i in range(1, 7):
        txt += '`' + str(i) + "/6:` " + str(stats[id]['games'][i]) + "\n"
    txt += '`Perdues`: ' + str(stats[id]['games'][0])
    embed.add_field(name='**Statistiques**', value=txt, inline=False)

    txt = '*Désactivées* :x:'
    if str(stats[id]['notifs']):
        txt = '*Activées* :white_check_mark:'
    embed.add_field(name='**Notifications**', value=txt, inline=False)

    await ctx.send(embed=embed)


@bot.command()
async def notif(ctx, arg):
    '''Permet d'activer ou de désactiver ses notifications.'''
    stats = get_data('stats.txt')
    id = ctx.message.author.id

    if id not in stats:
        stats[id] = stats_init
        sauvegarder(stats, "stats.txt")

    if arg.lower() == 'on':
        stats[id]['notifs'] = True
        await ctx.send(":white_check_mark: Les notifications sont maintenant activées !", delete_after=4)

    elif arg.lower() == 'off':
        stats[id]['notifs'] = False
        await ctx.send(":x: Les notifications sont maintenant désactivées !", delete_after=4)
    else:
        await ctx.send(":x:`Usage:` /notif [on/off]", delete_after=4)
    sauvegarder(stats, "stats.txt")


@bot.command()
async def nouveau_mot(ctx):
    ''' Administrateurs: change le mot du jour '''
    if ctx.message.author.id != 324153640216428548:
        await ctx.send(":x: Seul un `administrateur` peut changer le mot du jour !", delete_after=4)
        return 0
    liste_mots = lire_data("mots_communs.txt")
    new_daily = liste_mots[randrange(len(liste_mots))]

    data = ''
    data_list = lire_data("data_daily.txt")
    for elem in data_list:
        data += elem
    data = eval(data)

    data = {'daily': new_daily[:-1]}

    sauvegarder(data, "data_daily.txt")
    # Il faudra envoyer un message à tous ceux qui ont les notifs activées dans stats.txt pour les prévenir
    stats = get_data("stats.txt")
    for key in stats:
        user = await bot.fetch_user(key)
        await user.send(":sparkles: Un nouveau mot est disponible ! Résous le vite en faisant /daily ! :sparkles:")


@bot.command()
async def sutom(ctx):
    ''' Affiche la liste des commandes possibles '''
    embed = discord.Embed(title=":sparkles: Sutom :sparkles:", description="Le jeu du motus adapté pour discord !")
    embed.add_field(name='Liste des commandes:', value='`/daily`: faire le défi du jour.\n\
`/guess [mot]`: proposer un mot.\n`/stats`: voir ses statistiques.\n\
`/notif [on/off]`: active/désactive les notifications du mot journalier !', inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def daily(ctx):
    ''' Affcihe le mot du jour '''
    data = ''
    data_list = lire_data("data_daily.txt")
    for elem in data_list:
        data += elem
    data = eval(data)

    id = ctx.author.id

    if id not in data:
        data[id] = {'tries': 0, 'words': [], 'found': 0}

    sauvegarder(data, "data_daily.txt")

    await afficher_resultat(ctx, data, id)


async def afficher_resultat(ctx, data, id):
    ''' Fonction d'affichage du résultat d'un sutom '''
    disp = ""
    if data[id]['tries'] == 0:
        disp = (':heavy_minus_sign: ' * len(data['daily']) + '\n') * 6
    else:
        for i in range(len(data[id]['words'])):
            disp += ' ' + data[id]['words'][i] + '\n'
        disp += (':heavy_minus_sign: ' * len(data['daily']) + '\n') * (5-i)

    embed = discord.Embed(title=":sparkles: Sutom :sparkles:", description="Progression: \n" + disp)

    if data[id]['found'] == 0 and data[id]['tries'] == 6:
        embed.add_field(name=':x: Perdu ! :x:', value='Vous avez perdu ! Ré-essayez demain !', inline=False)
    elif data[id]['found'] == 0:
        embed.add_field(name='Partie en cours !', value='`/guess [mot]` pour essayer un nouveau mot !', inline=False)
    else:
        embed.add_field(name=':partying_face: Gagné ! :partying_face:',
                        value=f"Félicitations ! +{(7-data[id]['tries']) * len(data['daily'])}:coin:\nRevenez demain pour un nouveau mot !", inline=False)
    await ctx.send(embed=embed)


def convertir_mot(word):
    ''' convertit un str en minuscules sans accents/cédille '''
    word = word.lower()
    for i in range(len(word)):
        if word[i] in 'éèêë':
            word = word[:i] + 'e' + word[i+1:]
        elif word[i] in 'àâä':
            word = word[:i] + 'a' + word[i+1:]
        elif word[i] in 'ïî':
            word = word[:i] + 'i' + word[i+1:]
        elif word[i] == 'ç':
            word = word[:i] + 'c' + word[i+1:]
        elif word[i] in 'ôö':
            word = word[:i] + 'o' + word[i+1:]
        elif word[i] in 'ùûü':
            word = word[:i] + 'u' + word[i+1:]

    print(word)
    return word


@bot.command()
async def guess(ctx, word=''):
    ''' Permet de deviner un mot '''
    if word == '':
        await ctx.send("Usage: `/guess [mot]` pour deviner un mot !", delete_after=5)
        return 0

    word = convertir_mot(word)
    id = ctx.author.id

    data = get_data("data_daily.txt")

    if id not in data:
        data[id] = {'tries': 0, 'words': [], 'found': 0}

    sauvegarder(data, "data_daily.txt")

    # On teste si le joueur n'a pas déjà fait 6 tentatives ET s'il n'a pas déjà trouvé le mot

    if data[id]['tries'] == 6:
        await ctx.send("Perdu ! Tu n'avais que 6 essais pour trouver le mot ! Ré-essaie demain...", delete_after=4)
        return 0
    if data[id]['found'] != 0:
        await ctx.send("Tu as déjà trouvé le mot ! Reviens demain pour un nouveau défi !", delete_after=4)
        return 0

    # On regarde si le mot existe et si sa taille vaut bien la taille du mot du jour.
    # Note: on a une liste de mots qui se trminent par \n
    liste_mots = lire_data('dictionnaire.txt')

    # S'il n'existe pas (ou que sa taille est incorrecte), on envoie une erreur: "Erreur: ce mot n'existe pas !"

    if (word+'\n') not in liste_mots:
        await ctx.send("Ce mot n'est pas dans nos dictionnaires.", delete_after=4)
        return 0

    if len(word) != len(data['daily']):
        await ctx.send("La taille des mots ne correspond pas !", delete_after=4)
        return 0

    # S'il existe, on incrémente le nombre d'essais, et on stocke l'entrée.
    data[id]['tries'] += 1
    # ------------------------------- TRAITEMENT du mot:

    # On crée une liste contenant toutes les lettres du mot a deviner.
    letters_list = list(data['daily'])
    word_letters = list(word)

    # Pour chaque lettre, on regarde si elle correspond à la vraie lettre, auquel cas on la valide:
    for i in range(len(word_letters)):
        # On ajoute à l'entrée des ` ` autour de la lettre, et on supprime cette instance de la lettre dans la liste.
        if word_letters[i] == letters_list[i]:
            emoji_id = emoji_vert[word_letters[i].upper()]
            word_letters[i] = f"{bot.get_emoji(id=emoji_id)}"
            letters_list[i] = 0

    # On re-parcourt le mot, en indiquant les lettres qui sont mal placées. (on les retire de la liste)
    for i in range(len(word)):
        if word_letters[i] in letters_list:
            letters_list[letters_list.index(word_letters[i])] = 1
            emoji_id = emoji_jaune[word_letters[i].upper()]
            word_letters[i] = f"{bot.get_emoji(id=emoji_id)}"



    # On parcourt une dernière fois le mot en transformant les lettres restantes en emojis.
    for i in range(len(word)):
        if word_letters[i].upper() in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            word_letters[i] = ':regional_indicator_' + word_letters[i].lower() + ':'
            letters_list[i] = 2

    data[id]['words'].append(" ".join(word_letters))

    # Si après avoir parcouru tout le mot, la liste des lettres à deviner n'est pas vide, c'est qu'on n'a pas gagné
    if full_of_zeros(letters_list):
        data[id]['found'] = 1

        stats = get_data("stats.txt")

        if id not in stats:
            stats[id] = stats_init
            sauvegarder(stats, "stats.txt")

        fin_partie(data, stats, id)

    sauvegarder(data, "data_daily.txt")

    await afficher_resultat(ctx, data, id)


def fin_partie(data, stats, id):
    ''' Sauvegarde des statistiques d'un joueur à la fin d'une partie. '''
    if data[id]['tries'] == 6 and data[id]['found'] == 0:
        stats[id]['games'][0] += 1
    elif data[id]['found'] == 1:
        stats[id]['games'][data[id]['tries']] += 1
        stats[id]['money'] += (7-data[id]['tries']) * len(data['daily'])
    sauvegarder(stats, "stats.txt")


bot.run("ODA1NzUwMzA2MjQ3MDE2NDg4.YBfbcw.SLYZxtJqV_L5zlFY2Q12xUlP9GM")