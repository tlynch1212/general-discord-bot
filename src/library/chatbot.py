from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
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
        }
    ])

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(gynchChat)

# Train the chatbot based on the english corpus
trainer.train("chatterbot.corpus.english")