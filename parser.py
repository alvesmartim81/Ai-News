import argparse

class Parser:
    def __init__(self):
        #criar um parser e depois procura pelos requesitos ao iniciar o programa
        parser = argparse.ArgumentParser(description="Resumo da historia mais relevante de um dado tema")
        #criar um topico query que e requerido
        parser.add_argument("-q", "--query", required= True, help="Give a topic to get the top history related to it.")
        #opcao de escolher entre nytimes e nwesapi
        parser.add_argument("-a", "--agent", required = False, choices = ["nytimes", "guardian"], help = "Choose your agent to request the new.")
        #opcao de enviar email
        parser.add_argument("-e", "--email", required = False, help = "Input an email in order to send to you the content of the answer.")
        #opcao de multithread
        parser.add_argument("-t", "--thread", required = False, choices = ["1", "2", "3"], 
                            help = "Choose the amount of news to take from the api. Though will only show one at the end.")
        #opcao foco
        parser.add_argument("-f", "--focus", required = False, help = "Choose a topic in order for the gemini to focus on it.")
        #tamanho da resposta
        parser.add_argument("-s", "--size", required = False, choices = ["topics","small", "medium", "extensive"], help = "Choose the size of the answer.")
        #contexto
        parser.add_argument("-c", "--context", required = False, choices = ["y", "n"], help = "Ask for context about the story")
        args = parser.parse_args()

        self.query = args.query
        self.agent = args.agent
        self.email = args.email
        self.thread = args.thread
        self.focus = args.focus
        self.size = args.size
        self.context = args.context
