from agents import NyTimes
from gemini import Genai
from parser import Parser
from json_app import Json
from email_service import Email
from config import agents, api_nytimes, api_gemini, email, senha_email
from thread import Thread
from cli import OnlineMenu
from offline import offline

def agent_thread_version(parser: object, doc: object, lock: object, url: str, titulo: str, resultados_finais: list) -> None:
    """inicia o gemini, pede a informacao e depois recebe a resposta
    controla a resposta para garantir que esta correta
    adaptado ao thread para quenao ocorra nenhum erro ao tentarem por todos as respostas ao mesmo tempo"""

    gemini = Genai(api_gemini, url, parser.focus, parser.size, parser.context)

    resumo = doc.verificar_se_existe(titulo)

    if resumo:
        with lock:
            resultados_finais.append((titulo, resumo))
    else:
        while True:
            gemini.resumir_noticia()
            if not gemini.controlo_de_resposta():
                break
        
        with lock:
            doc.adicionar_info(titulo, gemini.resposta)
            resultados_finais.append((titulo, gemini.resposta))

def agent(parser: object, doc: object, API_key: str, classe: classmethod) -> str:
    #versao para o modo offline que mostra a noticia e depois retorna as respostas para serem guardadas
    agent = classe(API_key, parser.query)

    agent.request(agent.link)

    agent.get_title_and_url()

    gemini = Genai(api_gemini, agent.url_do_artigo, parser.focus, parser.size, parser.context)

    resumo = doc.verificar_se_existe(agent.titulo_do_artigo)

    if resumo:
        gemini.mostrar_historia(agent.titulo_do_artigo, resumo)
        return agent.titulo_do_artigo, resumo
    else:
        while True:
            gemini.resumir_noticia()
            if not gemini.controlo_de_resposta():
                break
            
        doc.adicionar_info(agent.titulo_do_artigo, gemini.resposta)
        gemini.mostrar_historia(agent.titulo_do_artigo, gemini.resposta)
        return agent.titulo_do_artigo, gemini.resposta



def send_email(parser: object, titulo: str, resumo: str) -> None:
    #controla e envia email, caso seja pedido
    if parser.email:
        email_sender = Email(parser.email, email, senha_email)
        email_sender.enviar_email(titulo, resumo)

def show_new(lista: list) -> None:
    #faz print da noticia
    OnlineMenu.barrier()
    try:
        print(f"\t{lista[0][0]}\n\n")
        print(f"{lista[0][1]}")
    except IndexError:
        print("Noticia nao encontrada.")
        OnlineMenu.barrier()
        offline()
    OnlineMenu.barrier()

def main():
    #prepara todos os objetos e controla o que e feito a partir dos inputs
    parser = Parser()
    doc = Json("info.json", "meu path")

    OnlineMenu.menu("AI_News")

    if parser.thread:
        classe, chave = agents.get(parser.agent, (NyTimes, api_nytimes))
        resultados_finais = []
        thread = Thread(int(parser.thread), agent_thread_version)
        thread.start_multithreading(parser, classe, chave, doc, resultados_finais)
        show_new(resultados_finais)
        send_email(parser, resultados_finais[0][0], resultados_finais[0][1])
    else:
        classe, chave = agents.get(parser.agent, (NyTimes, api_nytimes))
        titulo, resumo = agent(parser, doc, chave, classe)
        send_email(parser, titulo, resumo)

if __name__ == "__main__":
    main()

#proximos passos:
#alterar o path do .json para um caminho relatvo com os.dirname(__file__)                               
#vou ter que alterar a database para poder organizar os itens com baze em topicos                       

#sugestoes:
#interface grafica web com flask ou apk com kivy                                                        #para flask tenho que fazer o conteudo do site com html e css

#publicar:
#criar apk ou ficheiro utilizavel
#fazer backend que lida com requests e api                                                              #se eu fizer o site, o backend e o python
