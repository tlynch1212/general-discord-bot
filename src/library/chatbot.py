from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.conversation import Statement
import threading
import asyncio
import concurrent.futures
import spacy
import logging

# Configure logging to the console
logging.basicConfig(level=logging.INFO)

nlp = spacy.load("en_core_web_sm")
chatBot = ChatBot(
    'Odin',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        'chatterbot.logic.MathematicalEvaluation'
    ])

def trainChatBot():
    trainer = ChatterBotCorpusTrainer(chatBot)

    trainer.train("chatterbot.corpus.english")

trainingThread = threading.Thread(target=trainChatBot, name="Trainer")
trainingThread.daemon = True

def startTraining():
    trainingThread.start()

def addResponse(input, response):
    input_statement = Statement(text=input)
    response_statement = Statement(text=response)
    chatBot.learn_response(response_statement, input_statement)

def getResponse(message):
    response = chatBot.get_response(str.lower(message.content))
    return response

async def talkToOdin(message):
    if trainingThread.isAlive():
        await message.channel.send('Sorry, I am currently in training. It takes a while to learn over 100 million conversations.')
    else:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            response = await asyncio.get_event_loop().run_in_executor(executor, lambda: getResponse(message))
            await message.channel.send(response)

async def isTrainingDone(channel):
    if not trainingThread.isAlive():
        await channel.send('Training is done!')
        return True
    else:
        return False
