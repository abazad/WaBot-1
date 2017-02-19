# -*- coding: utf-8 -*-
import string

from app.bot import bot
from app.utils import helper
from app.yesno.yesno import YesNo
from app.anime.anime import Anime
from app.quote.quote import Quote
from app.passwords import CLEVER_API_KEY

import wolframalpha
from app.clever.clever import Cleverbot

####################################################################################################################


def handle_message(instance, command, predicate, message_entity, who, conversation):
    # Nigga who send the message
    who_name = helper.sender_name(message_entity)

    if command == "hola":
        answer = "Hola *" + who_name + "*"
        bot.send_message(instance, answer, conversation)

    elif command == "ayuda":
        answer = "*Lista de comandos* \n!hola \n!anime \n!anime season \n!quote \n!siono \n!ayuda"
        bot.send_message(instance, answer, conversation)

    elif command == "siono":
        yesno = YesNo(instance, conversation)
        yesno.send_yesno()

    elif command == "anime":
        if predicate:
            if predicate == 'season':
                anime = Anime(instance, conversation, param='season')
            else:
                anime = Anime(instance, conversation, param=predicate)
        else:
            anime = Anime(instance, conversation)

        anime.send_anime()

    elif command == "quote":
        quote = Quote(instance, conversation)
        quote.send_quote()
        
    else:
        #return
        # No command for this so use IA
        answer = cleverbot_answer(command + " " + predicate)
        #answer = wolfram_answer(command + " " + predicate, who_name)
        bot.send_message(instance, answer, conversation)
        
    
def wolfram_answer(message, who=""):
    app_id = "WL543X-974Q523T8P"
    client = wolframalpha.Client(app_id)
    try:
        res = client.query(message)
        if hasattr(res, 'pods'):
            return next(res.results).text
        else:
            return cleverbot_answer(message)
    except:
        return "*?*"


def cleverbot_answer(message):
    cb = Cleverbot(CLEVER_API_KEY)
    answer = cb.ask(message)
    return answer