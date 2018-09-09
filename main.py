import os
from datetime import datetime
import statistics

class Agregador (object):
    def __init__(self):
        self.dic_pessoas = {}

    def teste(self):
        pass


    def agrega_dados(self):
        self.limpa_arquivo('acoes.txt')
        robos = self.obtem_diretorios()

        self.acoes = open('acoes.txt', 'a')

        for robo in robos:
            mencoes = open('dados/' + robo + '/mencoes.txt', 'r')
            respostas = open('dados/' + robo + '/respostas.txt', 'r')

            self.agrupa_dados(mencoes.readlines(), 'mencao', robo)
            self.agrupa_dados(respostas.readlines(), 'resposta', robo)

        self.acoes.close()

        self.monta_dicionario()
        self.adiciona_dados_dicionario()
        self.salva_resultados()


    def salva_resultados(self):
        self.limpa_arquivo('resultados.txt')

        resultados = open('resultados.txt', 'a')

        resultados.write('user_id, qtd_mencoes, qtd_respostas, qtd_retweets, qtd_robos, tempo_longo_prazo, ' +
                         'media_curto_prazo, desvio_curto_prazo\n')

        for pessoa in self.dic_pessoas:
            if self.dic_pessoas[pessoa] is not None:
                p = self.dic_pessoas[pessoa]

                resultados.write(str(pessoa) + ', ' +
                                 str(p['qtd_mencoes']) + ', ' +
                                 str(p['qtd_respostas']) + ', ' +
                                 str(p['qtd_retweets']) + ', ' +
                                 str(p['qtd_robos']) + ', ' +
                                 str(p['tempo_longo_prazo']) + ', ' +
                                 str(p['media_curto_prazo']) + ', ' +
                                 str(p['desvio_curto_prazo']) + '\n')


    def adiciona_dados_dicionario(self):
        self.acoes = open('acoes.txt', 'r')
        dados_acoes = self.acoes.readlines()

        array_acoes = []
        for acao in dados_acoes:
            array_acoes.append(acao.split(","))

        for pessoa in self.dic_pessoas:
            tempos = []
            robos_interacoes = []

            qtd_respostas = 0
            qtd_mencoes = 0
            qtd_retweets = 0

            for acao in array_acoes:
                if int(acao[1]) == int(pessoa):
                    if acao[0] == 'resposta':
                        qtd_respostas += 1
                        tempo = datetime.strptime(acao[3].strip().rstrip(), "%Y-%m-%d %H:%M:%S")
                        tempos.append(tempo)
                        robos_interacoes.append(acao[2].strip().rstrip())
                    elif acao[0] == 'mencao':
                        qtd_mencoes += 1
                        tempo = datetime.strptime(acao[3].strip().rstrip(), "%Y-%m-%d %H:%M:%S")
                        tempos.append(tempo)
                        robos_interacoes.append(acao[2].strip().rstrip())

                    elif acao[0] == 'retweet':
                        qtd_retweets += 1
                        tempo = datetime.strptime(acao[3].strip().rstrip(), "%Y-%m-%d %H:%M:%S")
                        tempos.append(tempo)
                        robos_interacoes.append(acao[2].strip().rstrip())

            # Sair do loop caso haja apenas uma acao
            if len(tempos) <= 1:
                continue

            qtd_robos = len(list(set(robos_interacoes)))  # Remove duplicatas

            media_tempos = self.calcula_media_tempos(tempos)
            desvio_padrao_tempos = self.calcula_desvio_padrao_tempos(tempos)
            tempo_total = self.calcula_tempo_total(tempos)

            self.dic_pessoas[pessoa] = {'qtd_mencoes': qtd_mencoes,
                                        'qtd_respostas': qtd_respostas,
                                        'qtd_retweets': qtd_retweets,
                                        'qtd_robos': qtd_robos,
                                        'tempo_longo_prazo': tempo_total,
                                        'media_curto_prazo': media_tempos,
                                        'desvio_curto_prazo': desvio_padrao_tempos}


    def monta_dicionario(self):
        acoes = open('acoes.txt', 'r')

        dados_acoes = acoes.readlines()
        for acao in dados_acoes:
            dados = acao.split(",")
            self.dic_pessoas[int(dados[1])] = None

        acoes.close()


    def agrupa_dados(self, dados, tipo, robo):
        dados.pop(0) # remove cabeçalho
        for dado in dados:
            dados = dado.split(",")
            registro = tipo + ', ' + dados[0] + ', ' + robo + ', ' + dados[2]
            self.acoes.write(registro)


    @staticmethod
    def limpa_arquivo(caminho):
        arquivo = open(caminho, 'w')
        arquivo.write('')
        arquivo.close()


    @staticmethod
    def obtem_diretorios():
        diretorios = os.listdir ('dados')

        result = []
        for diretorio in diretorios:
            if os.path.isdir(os.path.join(os.path.abspath('dados'), diretorio)):
                result.append(diretorio)
        
        result.sort()
        return result


    @staticmethod
    def calcula_media_tempos(tempos):
        tempos.sort()
        distancia_tempos = []
        for i in range(0, len(tempos) - 1):
            distancia = (tempos[i+1] - tempos[i]).total_seconds()
            distancia_tempos.append(distancia)

        return statistics.mean(distancia_tempos)


    @staticmethod
    def calcula_desvio_padrao_tempos(tempos):
        tempos.sort()
        distancia_tempos = []
        for i in range(0, len(tempos) - 1):
            distancia = (tempos[i + 1] - tempos[i]).total_seconds()
            distancia_tempos.append(distancia)

        return statistics.pstdev(distancia_tempos)


    @staticmethod
    def calcula_tempo_total(tempos):
        tempos.sort()
        return (tempos[len(tempos) - 1] - tempos[0]).total_seconds()

agregador = Agregador()
agregador.agrega_dados()
    
