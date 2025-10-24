import google.generativeai as genai

class Genai:
    def __init__(self, API_genai: str, url_news: str, focus = None, size = None, context = None):
        #iniciar o requests
        self.API_genai = API_genai
        self.url_news = url_news

        #preparar o modelo e o chat do gemini
        self.modelo = genai.GenerativeModel('gemini-2.0-flash')
        genai.configure(api_key=self.API_genai)
        #prompt base
        self.prompt = f"Vai a este link de uma noticia e resume a historia.Retorna apenas o resumo da historia, sem titulo. Aqui vai o link: {self.url_news}."

        #preparar o prompt completo
        if context == "y":
            self.prompt = """Vai a este link de uma noticia e resume a historia. Depois faz pesquiza sobre o tema e o contexto deste.
                        Retorna apenas dois paragrafos: o primeiro com o contexto e o segundo com o resumo da historia."""
        if focus:
            self.prompt = self.prompt + f"Foca na relacao da historia com o seguinte tema: {focus}"
        if size:
            dict_size = {
                "topics" : "Resposta em 2 a 5 topicos de poucas palavras e simples(de 10 a 30 palavras).",
                "small" : "A resposta deve ter entre 2 e 5 frases com palavras simples(cerca de 50 a 70 palavras).",
                "medium" : "A resposta deve ter entre 5 e 10 frases com carater textual um pouco complexo(cerca de 150 palavras).",
                "extensive" : "A resposta deve ter mais que 12 frases e com carater textual complexo (cerca de 300 palavras)."
            }
            self.prompt = self.prompt + dict_size[size]
        
        self.resposta = None

    def resumir_noticia(self) -> None:
        #tenta conectar ao gemini, enviar a mensagem e depois recebe-la e torna-la legivel, controlando os erros
        try:
            chat = self.modelo.start_chat()
            response = chat.send_message(self.prompt)
            texto = response.candidates[0].content.parts[0].text
            self.resposta = texto.strip()
        except Exception as e:
            print(f"Erro inesperado: {e}")
    
    def controlo_de_resposta(self) -> bool:
        #controla se o gemini retornou uma resposta valida procurando por palavras como web, url e urls, para depois retornar um true ou false
        if not self.resposta:
            print("Resposta nao encontrada. A fechar a aplicacao.")
            return True
        resposta_limpa = self.resposta.replace(",", "").replace(".", "").replace("!", "").replace("?", "")
        if "url" in resposta_limpa.lower().split() or "urls" in resposta_limpa.lower().split() or "web" in resposta_limpa.lower().split():
            print("Ocorreu um erro durante o resumo da historia.")
            print("Tentando outra vez...\n")
            return True
        else:
            return False
    
    def mostrar_historia(self, titulo_historia: str, resumo_da_historia = None) -> None:
        #mostra o titulo e por baixo a historia
        if resumo_da_historia:
            print(f"\t{titulo_historia}\n")
            print(f"{resumo_da_historia}\n")
        else:
            print("Resumo da historia nao encontrado.")

