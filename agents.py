from sys import exit
from requests import get, exceptions
from offline import offline

class Agent:
    def __init__(self, API_key: str, query: str):
        self.API_key = API_key
        self.query = query
        self.link = None

        self.url_do_artigo = None
        self.titulo_do_artigo = None
        self.dados = None
    
    def request(self, link: str) -> None:
        """uso o try/except para tentar conectar a api 
        caso nao resulte, o user nao levar com a tela de erro e conseguir perceber o q aconteceu"""
        try:
            resposta = get(link)

            if resposta.status_code == 200:
                #torna o resultado num json para depois poder navegar e filtrar
                self.dados = resposta.json()
            
            else:
                print(f"Algo correu mal. Status code: {resposta.status_code}")
                offline()
        #filtra os erros de coneccao para depois poder entrar no modo offline se o online nao funcionar
        except (exceptions.ConnectionError, exceptions.Timeout):
            offline()
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            offline()
        
    def get_title_and_url(self) -> None:
        #caso tenha os dados (json), vai procurar pelo url e pelo titulo do rpimeiro
        if self.dados:
            try:
                self.url_do_artigo = self.dados ["url"]
                self.titulo_do_artigo = self.dados ["titulo"]
                self.lista_info.append((self.titulo_do_artigo, self.url_do_artigo))

            
            except(KeyError, IndexError):
                #caso deia erro de index ou de falta de itens fecha o programa
                print("Nenhum artigo encontrado ou formato inesperado.")
                exit(1)
        
        else:
            #se falhar o request mostra a mensagem de erro e fecha o programa
            print(f"Erro, nenhum artigo encontrado.")
            exit(1)

class NyTimes(Agent):
    def __init__(self, API_key: str, query: str):
        super().__init__(API_key, query)
        self.link = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q={self.query}&api-key={self.API_key}"
        self.lista_info = []

    def get_title_and_url(self) -> None:
        if self.dados:
            try:
                #adapta esta funcao a api do nytimes
                self.url_do_artigo = self.dados ["response"] ["docs"] [0] ["web_url"]
                self.titulo_do_artigo = self.dados ["response"] ["docs"] [0] ["headline"] ["main"]
                self.lista_info.append((self.titulo_do_artigo, self.url_do_artigo))

            
            except(KeyError, IndexError):
                print("Nenhum artigo encontrado ou formato inesperado.")
                exit(1)
        
        else:
            print(f"Erro, nenhum artigo encontrado.")
            exit(1)

class Guardian(Agent):
    def __init__(self, API_key: str, query: str):
        super().__init__(API_key, query)
        self.link = f"https://content.guardianapis.com/search?q={query}&page=1&api-key={API_key}"
        self.lista_info = []

    def get_title_and_url(self) -> None:
        #adapta esta funcao a api da guardian
        if self.dados:
            try:
                self.url_do_artigo = self.dados ["response"] ["results"] [0] ["webUrl"]
                self.titulo_do_artigo = self.dados ["response"] ["results"] [0] ["webTitle"] 
                self.lista_info.append((self.titulo_do_artigo, self.url_do_artigo))

            except(KeyError, IndexError):
                print("Nenhum artigo encontrado ou formato inesperado.")
                exit(1)
        else:
            print(f"Erro, nenhum artigo encontrado.")
            exit(1)
