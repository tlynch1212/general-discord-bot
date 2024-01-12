from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import UbuntuCorpusTrainer
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

# Create a new trainer for the chatbot
trainer = UbuntuCorpusTrainer(gynchChat)

# Train the chatbot based on the english corpus
trainer.train()

async def talkToGynch(message):
    await message.channel.send(gynchChat.get_response(str.lower(message.content)))