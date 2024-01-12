from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import UbuntuCorpusTrainer
import threading
import spacy

nlp = spacy.load("en_core_web_sm")
gynchChat = ChatBot(
    'Gynch',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'bbw?',
            'output_text': 'Please, I need to know'
        },
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter'
    ])



def trainChatBot():
    # Create a new trainer for the chatbot
    trainer = UbuntuCorpusTrainer(gynchChat)

    # Train the chatbot based on the english corpus
    trainer.train()

trainingThread = threading.Thread(target=trainChatBot, name="Trainer")
trainingThread.start()

async def talkToGynch(message):
    if trainingThread.isAlive():
        await message.channel.send('Sorry, im currently in training, it takes awhile to learn over 100 million conversations.')
    else:
        await message.channel.send(gynchChat.get_response(str.lower(message.content)))