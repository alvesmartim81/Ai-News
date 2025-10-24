import threading

class Thread:
    def __init__(self, quantity: int, func: function):
        self.quantity = quantity
        self.func = func
        self.lista_dados = None
        self.lock = threading.Lock()
        self.threads = []
        self.shared_list = []
    
    def start_multithreading(self, parser: object, classe: classmethod, API_key: str, doc: object, resultados_finais: list) -> None:
        #quero que cada thread faca a funcao agent e q pegue na info que recebeu e uma de cada vez salve a informacao numa lista,
        #depois quero pegar no primeiro item da lista e mostralo ao user para que se ele depois quiser itens semelhantes eu telos
        #ou ate para ter uma database de noticias maior

        agent = classe(API_key, parser.query)

        agent.request(agent.link)
        
        agent.get_title_and_url()

        self.lista_dados = agent.lista_info

        for i in range(self.quantity):
            t = threading.Thread(target = self.func, args= (parser, doc, self.lock, self.lista_dados[i][1], self.lista_dados[i][0], resultados_finais))
            self.threads.append(t)
            t.start()

        for t in self.threads:
            t.join()
    
    