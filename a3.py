import networkx as nx
import folium
from geopy.distance import geodesic
from datetime import datetime, timedelta

# Cadastro das cidades
cidades = {
    'Curitiba': {'latitude': -25.4296, 'longitude': -49.2719},
    'Londrina': {'latitude': -23.3045, 'longitude': -51.1696},
    'Foz do Iguaçu': {'latitude': -25.5478, 'longitude': -54.5882},
    'União da Vitória': {'latitude': -26.2273, 'longitude': -51.0870},
    'Joinville': {'latitude': -26.3032, 'longitude': -48.8411},
    'Chapecó': {'latitude': -27.1007, 'longitude': -52.6157},
    'Porto Alegre': {'latitude': -30.0346, 'longitude': -51.2177},
    'Uruguaiana': {'latitude': -29.7627, 'longitude': -57.0886},
    'Pelotas': {'latitude': -31.7615, 'longitude': -52.3435},
}

# Verifica se todas as cidades têm a chave 'pos'
for cidade in cidades:
    if 'pos' not in cidades[cidade]:
        cidades[cidade]['pos'] = (0, 0)  # Define uma posição padrão para cidades sem 'pos'

# Criando o grafo ponderado
grafo = nx.Graph()
for cidade, info in cidades.items():
    grafo.add_node(cidade, pos=info['pos'])
    

def condicao(grafo,origem,destino):
    print(grafo.nodes)
    # Condição para Foz do Iguaçu/União da Vitória
    if 'Foz do Iguaçu' in grafo.nodes and 'União da Vitória' in grafo.nodes:
        grafo.add_edge('Foz do Iguaçu', 'União da Vitória', weight=547)
        print("AD Foz")
    # Condição para Joinville/Chapecó
    if 'Joinville' in grafo.nodes:
        grafo.add_edge('Joinville', 'Chapecó', weight=515)
        print('ADD joimn')

# Adicionando arestas com distâncias entre as cidades
grafo.add_edge('Curitiba', 'Londrina', weight=385)
grafo.add_edge('Curitiba', 'Joinville',  weight=140)
grafo.add_edge('Londrina', 'Chapecó', weight=631)
grafo.add_edge('Londrina', 'Joinville', weight=513)
grafo.add_edge('Foz do Iguaçu', 'União da Vitória', weight=546)
grafo.add_edge('União da Vitória', 'Joinville', weight=273)
grafo.add_edge('União da Vitória', 'Chapecó', weight=243)
grafo.add_edge('Joinville ', 'Porto Alegre', weight=515)
grafo.add_edge('Chapecó', 'Pelotas', weight=658)
grafo.add_edge('Chapecó', 'Uruguaiana', weight=670)
grafo.add_edge('Porto Alegre', 'Pelotas', weight=262)

origem = input("Digite a cidade de origem: ")
destino = input("Digite a cidade de destino: ")

# Chamando a função condicao
condicao(grafo, origem, destino)

# Exemplo de uso
menor_caminho = nx.shortest_path(grafo, origem, destino, weight='weight')

# Exibindo informações do menor caminho
distancia_total = sum(grafo[menor_caminho[i]][menor_caminho[i + 1]]['weight'] for i in range(len(menor_caminho) - 1))
custo_total = distancia_total * 20  # Custo por quilômetro

velocidade_media = float(input("Digite a estimativa de velocidade média (em km/h): "))

tempo_total = distancia_total / velocidade_media  # Assumindo uma velocidade média de 80 km/h
horario_atual = datetime.now()
horario_chegada = horario_atual + timedelta(hours=tempo_total)

print(f'Menor caminho: {menor_caminho}')
print(f'Distância total: {distancia_total} km')
print(f'Custo total: R${custo_total:.2f}')
print(f'Tempo: {tempo_total:.3f} horas')
print(f'Horário de partida: {horario_atual.strftime("%H:%M:%S")}')
print(f'Horário estimado de chegada: {horario_chegada.strftime("%H:%M:%S")}')



# Exibindo o mapa
mapa = folium.Map(location=cidades[origem]['pos'], zoom_start=7)
for cidade, info in cidades.items():
    folium.Marker(location=info['pos'], popup=cidade).add_to(mapa)
folium.PolyLine([cidades[cidade]['pos'] for cidade in menor_caminho], color='blue').add_to(mapa)
mapa.save('mapa.html')





