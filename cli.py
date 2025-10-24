from pyfiglet import figlet_format
from sys import exit
from typing import Optional

class Menu:
    @staticmethod
    def menu(title: str, mensagem: str) -> None:
        title_ascii = figlet_format(title)
        print(title_ascii)
        print("\n"+ mensagem)
    
    @staticmethod
    def confirmar_input(mensagem: str) -> bool:
        #filtra se o input e s ou n para reornar true ou false
        while True:
            answer = input(mensagem)
            if answer.lower() == "s":
                return True
            elif answer.lower() == "n":
                return False
            else:
                print("Opcao invalida. Tente outra vez.\n")

    @staticmethod
    def barrier() -> None:
        #para criar uma separacao entre abas
        print("\n" + 40*"-" + "\n")

class OfflineMenu(Menu):
    @staticmethod
    def menu(title: str) -> Optional[bool]:
        #adapta o menu ao menu offline e pergunta se deseja ver noticias arquivadas
        title_ascii = figlet_format(title)
        print(title_ascii)
        print("\n\nEsta offline.")
        answer = Menu.confirmar_input("Deseja ver os ficheiros arquivados (s/n): ")
        if answer == True:
            return True
        elif answer == False:
            print("Obrigado por usar esta app :)")
            exit(1)

class OnlineMenu(Menu):
    @staticmethod
    def menu(title: str) -> None:
        #adapta o menu ao menu online
        title_ascii = figlet_format(title)
        print(title_ascii)
        print("\nBem-vindo!")
        print("Carregando a sua noticia...")