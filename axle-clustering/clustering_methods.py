# Clusterização de rodas em conjuntos de eixos
#
# 

'''
Objetivo:
Dado um conjunto de rodas detectadas, clusterizá-las em conjuntos de eixos, 
onde cada eixo é composto por um ou mais rodas.
'''

'''
Entradas:
- Conjunto de rodas detectadas, onde cada roda é representada por um ponto central (x, y), uma largura (w) e uma altura (h).
    - Formato: [(x1, y1, w1, h1), (x2, y2, w2, h2), ..., (xn, yn, wn, hn)]
- Permissividade: 
'''

# Premissas:

# 1. O modelo só detectou rodas de um mesmo caminhão;
# 2. Todas as rodas tem tamanho aproximadamente igual;
# 3. A distância entre pneus de eixos diferentes é, no mínimo, a largura de um pneu;

# Algoritmo elaborado:

'''
1. Ordenar labels de rodas;
2. Inicializar uma lista de eixos, inicialemente vazia e definir uma threshold;
3. Para cada um dos labels, até o penúltimo:
    3.1.

1. Ordenar conjunto de rodas (ponto central, largura, eixo = 0) 
2. Incicializar lista de eixos vazia, definição do treshholdeweas em porcentagem
3. Para cada roda, até a penúltima
3.1 Copie o eixo global para essa roda
3.1 Calcule a distância do ponto central dessa roda para o centro da próxima roda
3.2 Use esse distância como hipotenusa e a largura da roda atual como cateto inferior para
conseguir o ângulo entre hipotenusa e cateto inferior
3.3 Calcule a hipotenusa de um triângulo retângulo com cateto inferior de tamanho de largura
da roda atual + treshholderw * largura da roda atual com o ângulo obtido
3.4 Se a distância entre o centro da roda atual e o centro da próxima roda for menor ou igual que
a última hipotenusa obtida: faça nada
3.5 Se não, incremente o eixo atual em 1 e o eixo global em 1
'''