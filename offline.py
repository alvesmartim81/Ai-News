 pathfrom json_app import Json
from cli import OfflineMenu
import sys
import random

#modo offline:
#acede a ficheiros do .json e mostra-os em lista 
#aparece uma tela e pergunta se deseja ver algum, em numeracao
#depois uso o metodo show noticia para o mostrar
#acho q faco uma classe com funcao menu, funcao listar componentes

class Offline:
    def __init__(self, dados: str):
        self.dados = dados
        self.title = "Offline_Mode"
        self.dict_hist = {}
        self.lista = None

    def show_titles(self) -> None:
        #procurar por noticias no ficheiro json e mostrar pelo menos 10 randomizadas, mostrando-os
        todas_as_chaves = list(self.dados["historias"].keys())
        
        num_a_mostrar = min(10, len(todas_as_chaves))
        
        titulos_selecionados = random.sample(todas_as_chaves, num_a_mostrar)
        
        OfflineMenu.barrier()
        
        self.dict_hist = {} 

        for i, titulo in enumerate(titulos_selecionados, 1):
            print(f"{i}. {titulo}")
            self.dict_hist[i] = titulo
            
        OfflineMenu.barrier()

    def ask_to_read(self) -> str:
        #pede ao user para escolher uma historia com controlo de opcoes validas
        while True:
            try:
                answer = int(input("\nDeseja ler alguma destas historias (digite o numero que deseja): "))
                if answer in self.dict_hist:
                    return self.dict_hist[answer]
            except ValueError:
                print("\nOpcao invalida. Por favor tente outra vez\n")

    def show_hist(self, titulo: str):
        #mostra a historia que o user selecionou
        OfflineMenu.barrier()
        print(f"\t{titulo}\n")
        corpo_da_noticia = self.dados["historias"][titulo] 
        print(corpo_da_noticia)
        OfflineMenu.barrier()

def offline() -> None:
    #descreve como o programa se vai comportar no modo offline
    database = Json("info.json", "/home/martim/Secretária/Python/projeto_ai_news")
    database.obter_dados()
    app = Offline(database.dados)
    answer = OfflineMenu.menu(app.title)
    if answer:
        app.show_titles()
        option = app.ask_to_read()
        app.show_hist(option)
        sys.exit(1)
    
