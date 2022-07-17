# historical-figure-questions
Twitter bot that uses a question answering AI from HuggingFace to respond to user mentions.

Example in this repo uses Marcus Aurelius' "Meditations" to respond to questions as if it was the emperor/philosopher himself responding. One could easily repurpose this to respond as any one so long as the AI is fed the appropriate text.

![](Images/example_replies.PNG?raw=true)

*@AureliusRespon1*

The main script is hugginytweepy.py in the Python directory.  The question answering AI is utilized via the transformers library provided by HuggingFace. The exact model used is [deepset/roberta-base-squad2]( https://huggingface.co/deepset/roberta-base-squad2 "Title"). The tweepy library is used to interact with the twitter API.

The mentions timeline is scraped. The Roberta model then generates an answer to the question posed using the context given (here ive used the writings of Marcus Aurelius). The answer is then tweeted back to the user who asked the question.

Anyone could repurpose this script to answer questions in the guise of whoever they desire. Just need to change the context fed to the model. It also would not require much more effort to have the script run autonomously.