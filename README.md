# **Detecção de eixos de caminhões para inferência de carga máxima utilizando YOLOv8**

## Problema

Existe uma imprecisão na emissão de alertas automáticos para auditores sobre veículos que poderiam indicar incongruências de carga em relação às notas fiscais emitidas.

---

## Proposta

Os eixos de um caminhão indicam, juntamente com outros fatores, qual é a carga máxima do veículo.

A proposta consiste em detectar essa informação e, com base em regras pré-estabelecidas, inferir uma possível carga máxima para veículos do tipo **caminhão** analisados.

---

## Pipeline

### 1. Detecção de eixos (pneus, para simplificação)

#### 1.1 Análise e pré-processamento da base de dados

* Imagens e informações sobre caminhões registrados pelo sistema de monitoramento de veículos de carga da SEFAZ-PB

#### 1.2 Anotação das imagens

* Total de 821 imagens de caminhões anotadas

#### 1.3 Organização dos dados

* Estruturação das imagens e anotações para treinamento do modelo de *Deep Learning* de *Visão Computacional* (**YOLOv8**)

#### 1.4 Treinamento do modelo

* Utilização de conjuntos de treinamento e teste

#### 1.5 Avaliação do modelo

* Análise de desempenho do modelo de detecção de eixos

#### 1.6 Aplicação prática

* Uso do modelo em cenários reais

---

### 2. Inferência de carga máxima

* A partir da quantidade de eixos detectados, aplicar regras para estimar a carga máxima do veículo

---

## Detecção de Eixos

*(Seção em desenvolvimento)*
