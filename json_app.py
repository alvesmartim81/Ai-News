from json import load, dump
from os import path
from typing import Optional

class Json:
    def __init__(self, ficheiro: str, path: str):
        self.ficheiro = ficheiro
        self.path = path
        self.full_path = path.join(self.path, self.ficheiro)

        self.dados = None
        self.obter_dados()
    
    def obter_dados(self) -> None:
        #procura pelo ficheiro json e retira info do ficheiro json
        if path.exists(self.full_path):
            with open(self.full_path, "r", encoding="utf-8") as f:
                self.dados = load(f)
        else:
            self.dados = {"historias":{}}
            self.salvar_dados()
    
    def verificar_se_existe(self, titulo: str) -> Optional[str]:
        #procura por um titulo no ficheiro json para nao ter que criar outro resumo caso ja exista
        try:
            if titulo in self.dados["historias"]:
                resumo = self.dados ["historias"] [titulo]
                return resumo
            else:
                return None
        except KeyError:
            return None
    
    def adicionar_info(self, titulo: str, resumo: str) -> None:
        #cria no ficheiro json um novo item para a historia nova
        self.dados ["historias"] [titulo] = resumo
        self.salvar_dados()
    
    def salvar_dados(self) -> None:
        #salva os dados no ficheiro com adicao dos novos
        with open(self.full_path, "w", encoding = "utf-8") as f:
                dump(self.dados, f, ensure_ascii= False, indent = 2)


