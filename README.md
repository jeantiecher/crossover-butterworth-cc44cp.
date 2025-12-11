# crossover-butterworth-cc44cp.

# Projeto de Crossover Passivo com Filtros Butterworth de 2ª Ordem

## Autor
**Jean de Carvalho**  
Departamento Acadêmico de Engenharia da Computação  
Circuitos de Corrente Alternada - CC44CP  
Prof. Dionatan Cieslak, Dr. Eng.  
Universidade Tecnológica Federal do Paraná (UTFPR)

---

## 1. Apresentação do Problema

Em sistemas de áudio de alta fidelidade, é fundamental distribuir adequadamente as diferentes faixas de frequência para os alto-falantes apropriados. Um **crossover passivo** é um circuito eletrônico composto por indutores e capacitores que divide o sinal de áudio em bandas de frequência distintas:

- **Woofer**: Reproduz frequências baixas (graves) - necessita de um filtro passa-baixas
- **Tweeter**: Reproduz frequências altas (agudos) - necessita de um filtro passa-altas

### Desafios do Projeto:

1. **Separação espectral eficiente**: Garantir que apenas baixas frequências cheguem ao woofer e apenas altas frequências cheguem ao tweeter
2. **Transição suave**: Evitar descontinuidades na resposta em frequência na região de crossover
3. **Componentes comerciais**: Trabalhar com valores discretos disponíveis no mercado, diferentes dos valores ideais calculados
4. **Mínima distorção**: Manter a fidelidade do sinal de áudio

---

## 2. Objetivos e Especificações de Projeto

### Objetivos:

- Projetar um filtro **Passa-Baixas (LPF)** de 2ª ordem Butterworth para o woofer
- Projetar um filtro **Passa-Altas (HPF)** de 2ª ordem Butterworth para o tweeter
- Implementar ferramenta computacional para cálculo automático dos componentes
- Selecionar componentes comerciais mais próximos dos valores ideais
- Analisar quantitativamente o impacto do uso de componentes comerciais

### Especificações Técnicas:

| Parâmetro | Valor |
|-----------|-------|
| **Impedância da carga (R<sub>L</sub>)** | 4 Ω |
| **Frequência de corte (f<sub>c</sub>)** | 3.4 kHz |
| **Tipo de filtro** | Butterworth 2ª ordem |
| **Atenuação em f<sub>c</sub>** | -3 dB |
| **Taxa de atenuação** | 40 dB/década |
| **Topologia** | Filtro em L (série-paralelo) |

### Justificativa da Escolha do Butterworth:

O filtro Butterworth foi escolhido por apresentar:
- **Resposta maximamente plana** na banda passante (sem ripple)
- **Transição suave** entre banda passante e banda de rejeição
- **Facilidade de implementação** com componentes passivos
- **Boa relação custo-benefício** para aplicações de áudio

---

## 3. Funções de Transferência e Fórmulas de Projeto

### 3.1. Filtro Butterworth de 2ª Ordem - Características

O filtro Butterworth de 2ª ordem possui função de transferência normalizada:

```
H(s) = ωc² / (s² + √2·ωc·s + ωc²)
```

Onde:
- `ωc = 2πfc` é a frequência angular de corte
- `√2 ≈ 1.414` é o coeficiente que garante resposta maximamente plana

### 3.2. Filtro Passa-Baixas (LPF)

#### Topologia:
```
Vin ----[L]----+---- Vout
               |
              [C]  [RL]
               |    |
              GND  GND
```

**Indutor em série** + **Capacitor em paralelo com a carga**

#### Fórmulas de Projeto:

```
L = RL / (π · fc)

C = 1 / (2π · fc · RL)
```

#### Função de Transferência:

```
H(jω) = ZC||RL / (ZL + ZC||RL)
```

Onde:
- `ZL = jωL` (impedância do indutor)
- `ZC = 1/(jωC)` (impedância do capacitor)
- `ZC||RL` representa o capacitor em paralelo com a carga

### 3.3. Filtro Passa-Altas (HPF)

#### Topologia:
```
Vin ----[C]----+---- Vout
               |
              [L]  [RL]
               |    |
              GND  GND
```

**Capacitor em série** + **Indutor em paralelo com a carga**

#### Fórmulas de Projeto:

```
C = 1 / (π · fc · RL)

L = RL / (2π · fc)
```

#### Função de Transferência:

```
H(jω) = ZL||RL / (ZC + ZL||RL)
```

### 3.4. Dedução das Fórmulas

As fórmulas acima derivam da normalização do filtro Butterworth para impedância específica:

1. Parte-se do protótipo normalizado (RL = 1Ω, fc = 1 rad/s)
2. Aplica-se desnormalização em frequência: `ωc = 2πfc`
3. Aplica-se desnormalização em impedância: `RL`
4. Para o HPF, aplica-se transformação lowpass→highpass: `L → C` e `C → L`

---

## 4. Lógica do Programa

O programa foi estruturado de forma modular e clara:

### Fluxo de Execução:

```
1. Definição de Parâmetros
   ↓
2. Cálculo de Componentes Ideais
   ↓
3. Seleção de Componentes Comerciais
   ↓
4. Cálculo da Resposta em Frequência
   ↓
5. Geração dos Gráficos de Bode
   ↓
6. Análise Crítica dos Resultados
```

### Módulos Principais:

#### 4.1. Cálculo de Componentes Ideais
- `calcular_lpf_butterworth_2ordem(fc, RL)`: Retorna L e C ideais para o LPF
- `calcular_hpf_butterworth_2ordem(fc, RL)`: Retorna C e L ideais para o HPF

#### 4.2. Seleção de Componentes Comerciais
- `selecionar_componente_comercial(valor_ideal, tabela)`: 
  - Busca o valor comercial mais próximo usando `np.argmin()`
  - Calcula erro percentual: `erro = (comercial - ideal) / ideal × 100%`

#### 4.3. Resposta em Frequência
- `resposta_lpf_2ordem(f, L, C, RL)`: Implementa H(jω) do LPF usando impedâncias complexas
- `resposta_hpf_2ordem(f, C, L, RL)`: Implementa H(jω) do HPF usando impedâncias complexas

**Método de cálculo:**
1. Converte frequência para ω = 2πf
2. Calcula impedâncias complexas: `ZL = jωL` e `ZC = 1/(jωC)`
3. Calcula associação paralela: `Z||RL = (Z·RL)/(Z+RL)`
4. Aplica divisor de tensão
5. Converte magnitude para dB: `20·log₁₀|H(jω)|`

#### 4.4. Visualização
- Gera diagrama de Bode com escala logarítmica em frequência
- Compara curvas ideal vs. comercial
- Marca frequência de corte e nível de -3 dB

---

## 5. Como Executar o Código

### 5.1. Requisitos

**Python 3.x** com as seguintes bibliotecas:

```bash
pip install numpy matplotlib
```

### 5.2. Execução

No terminal, navegue até a pasta do projeto e execute:

```bash
python "trabalho final.py"
```

### 5.3. Saídas Geradas

1. **Saída no terminal**: Todos os valores calculados e análise
2. **Arquivo `bode_comparativo.png`**: Gráficos de Bode dos dois filtros

### 5.4. Personalizando Parâmetros

Para usar outros valores de RL e fc, edite as linhas 4-5 do código:

```python
RL = 4.0  # Impedância da carga (Ohms)
fc = 3.4e3  # Frequência de corte (Hz)
```

---

## 6. Resultados

### 6.1. Filtro Passa-Baixas (LPF) - Woofer

#### Valores Calculados:

| Componente | Valor Ideal | Valor Comercial | Erro |
|------------|-------------|-----------------|------|
| **Indutor (L)** | 0.374482 mH | **0.39 mH** | **+4.14%** |
| **Capacitor (C)** | 11.702569 μF | **12.00 μF** | **+2.54%** |

#### Desvio Médio: **3.34%** ✅

#### Componentes Especificados:
- 🔷 **Indutor:** 0.39 mH (série E12)
- 🔶 **Capacitor:** 12.0 μF (série E12)

---

### 6.2. Filtro Passa-Altas (HPF) - Tweeter

#### Valores Calculados:

| Componente | Valor Ideal | Valor Comercial | Erro |
|------------|-------------|-----------------|------|
| **Capacitor (C)** | 23.405139 μF | **22.00 μF** | **-6.00%** |
| **Indutor (L)** | 0.187241 mH | **0.18 mH** | **-3.87%** |

#### Desvio Médio: **4.94%** ✅

#### Componentes Especificados:
- 🔶 **Capacitor:** 22.0 μF (série E12)
- 🔷 **Indutor:** 0.18 mH (série E12)

---

### 6.3. Gráficos de Bode Comparativos

![Diagrama de Bode - LPF e HPF](bode_comparativo.png)

**Interpretação dos Gráficos:**

- **Linha azul contínua**: Resposta do filtro ideal (componentes calculados exatos)
- **Linha vermelha tracejada**: Resposta do filtro real (componentes comerciais)
- **Linha vertical cinza**: Frequência de corte especificada (3.4 kHz)
- **Linha horizontal verde**: Nível de -3 dB (definição de frequência de corte)

**Observações Visuais:**
- As curvas ideal e real são praticamente sobrepostas na maior parte do espectro
- Pequenas diferenças são visíveis apenas próximo à frequência de corte
- Ambos os filtros apresentam atenuação de 40 dB/década conforme esperado

---

## 7. Análise Crítica

### 7.1. Quantificação das Diferenças

#### Diferenças na Resposta em Frequência:

| Filtro | Diferença Máxima na Banda Passante |
|--------|-------------------------------------|
| **LPF** | **0.514 dB** |
| **HPF** | **0.182 dB** |

#### Desvios dos Componentes:

**Filtro Passa-Baixas (LPF):**
- Indutor: +4.14%
- Capacitor: +2.54%
- **Desvio médio: 3.34%**

**Filtro Passa-Altas (HPF):**
- Capacitor: -6.00%
- Indutor: -3.87%
- **Desvio médio: 4.94%**

### 7.2. Impacto Prático no Sistema de Áudio

#### Percepção Auditiva Humana:

A audição humana possui limitações de resolução em frequência e amplitude:

| Diferença de Magnitude | Percepção |
|------------------------|-----------|
| **< 0.5 dB** | Inaudível para a maioria das pessoas |
| **0.5 - 1.0 dB** | Detectável apenas por ouvintes treinados em testes A/B |
| **1.0 - 3.0 dB** | Perceptível em sistemas high-end |
| **> 3.0 dB** | Claramente audível |

#### Análise do Projeto:

✅ **Diferenças de magnitude < 0.6 dB**: Classificação **EXCELENTE**

✅ **Desvios dos componentes < 5%**: Dentro das tolerâncias típicas de fabricação

✅ **Resposta em frequência mantida**: A transição suave característica do Butterworth foi preservada

#### Fatores Adicionais a Considerar:

1. **Tolerâncias de fabricação**: Componentes reais possuem tolerâncias de ±5% a ±20%, maiores que os desvios calculados

2. **Variação dos alto-falantes**: Woofers e tweeters possuem variações de impedância com a frequência e tolerâncias de ±3 dB, mascarando as diferenças do filtro

3. **Ambiente acústico**: Reflexões e absorções no ambiente causam variações >> 1 dB

4. **Perda de inserção**: Indutores reais possuem resistência série (DCR), capacitores possuem ESR, causando perdas não modeladas

### 7.3. A Diferença Seria Audível?

**RESPOSTA: NÃO, as diferenças são praticamente inaudíveis.**

**Justificativa:**

1. Diferenças de 0.5 dB estão **abaixo do limiar de percepção** (JND - Just Noticeable Difference) para a maioria dos ouvintes

2. Em testes cegos (double-blind), mesmo audiófilos experientes teriam dificuldade em distinguir entre filtros ideal e real

3. Outros fatores do sistema (resposta dos drivers, acústica da sala, qualidade da fonte) têm impacto **muito maior** que estas diferenças

4. As diferenças concentram-se principalmente na **região de transição** (próximo a 3.4 kHz), onde há overlap entre woofer e tweeter

### 7.4. Comparação com Especificações Típicas da Indústria

| Especificação | Projeto | Típico da Indústria | Avaliação |
|---------------|---------|---------------------|-----------|
| Desvio de componentes | < 5% | ±5% a ±10% | ✅ Excelente |
| Diferença de magnitude | < 0.6 dB | < 1 dB | ✅ Excelente |
| Taxa de atenuação | 40 dB/dec | 40 dB/dec | ✅ Atende |

---

## 8. Conclusões

### 8.1. Cumprimento dos Objetivos

✅ **Todos os objetivos foram alcançados com sucesso:**

1. ✅ Filtros Butterworth 2ª ordem projetados corretamente
2. ✅ Ferramenta computacional funcional desenvolvida
3. ✅ Componentes comerciais selecionados otimamente
4. ✅ Análise comparativa quantitativa realizada
5. ✅ Gráficos de Bode gerados e interpretados

### 8.2. Maior Desafio Enfrentado

O principal desafio foi **implementar corretamente as funções de transferência** considerando:

- **Topologia específica** de cada filtro (série-paralelo)
- **Impedâncias complexas** e suas associações em paralelo
- **Divisor de tensão** com cargas complexas
- **Validação dos resultados** através de múltiplas abordagens

A solução envolveu:
1. Estudo detalhado da teoria de circuitos em CA
2. Implementação cuidadosa usando números complexos do NumPy
3. Comparação com resultados de simuladores (MATLAB)
4. Verificação da resposta em frequência nos extremos (baixas e altas frequências)

### 8.3. Lições sobre Componentes Reais

Este projeto evidenciou aspectos fundamentais da **engenharia prática**:

#### 1. Discretização de Valores

Componentes comerciais seguem séries padronizadas (E12, E24, E96):
- **E12**: 12 valores por década (~20% de espaçamento)
- Isso limita a precisão que podemos obter nos valores calculados
- Compromisso inevitável entre ideal teórico e disponibilidade prática

#### 2. Tolerâncias Cumulativas

Em circuitos reais, múltiplas fontes de erro se acumulam:
- Tolerância de fabricação: ±5% (E12), ±10% ou ±20% (eletrólitos)
- Variação com temperatura
- Envelhecimento dos componentes
- Parasitas (DCR em indutores, ESR em capacitores)

O desvio calculado (3-5%) é **pequeno comparado** às tolerâncias reais!

#### 3. Validação Experimental é Essencial

Mesmo com cálculos precisos:
- Medições reais são **necessárias** para validar o projeto
- Ajustes finos podem ser feitos empiricamente
- Componentes podem ser testados e selecionados (matching)

#### 4. Sobre-engenharia é Contraproducente

Buscar componentes "perfeitos":
- Aumenta custo exponencialmente
- Não traz benefício prático audível
- Ignora outras fontes de erro do sistema

**O importante é atender especificações com margem de segurança razoável.**

#### 5. Pensamento Sistêmico

O crossover é apenas uma parte do sistema de áudio:
- Alto-falantes têm tolerâncias >> 1 dB
- Acústica da sala domina a resposta final
- Qualidade da fonte é frequentemente o fator limitante

Otimizar excessivamente uma parte não melhora o sistema como um todo.

### 8.4. Aprendizados Aplicáveis a Projetos Futuros

1. **Análise de sensibilidade**: Identificar quais parâmetros têm maior impacto
2. **Trade-offs conscientes**: Balancear precisão, custo, e complexidade
3. **Validação multi-método**: Cálculo analítico + simulação + medição
4. **Documentação rigorosa**: Rastreabilidade de decisões de projeto
5. **Pensamento prático**: Considerar manufatura e manutenção desde o início

### 8.5. Considerações Finais

O projeto demonstrou que **componentes comerciais padrão são perfeitamente adequados** para aplicações de crossover de áudio de alta qualidade. A diferença entre filtros ideal e real é:

- ✅ **Quantificável**: Desvios < 5%, diferenças < 0.6 dB
- ✅ **Previsível**: Modelada matematicamente com precisão
- ✅ **Aceitável**: Dentro de todas as normas da indústria
- ✅ **Inaudível**: Abaixo do limiar de percepção humana

Este resultado valida a abordagem de projeto baseada em componentes da série E12 e reforça que **a perfeição teórica nem sempre é necessária para excelência prática**.

A engenharia real é sobre encontrar o ponto ótimo entre:
- Desempenho técnico
- Custo econômico  
- Viabilidade de fabricação
- Requisitos da aplicação

Este projeto atende todos esses critérios com distinção.

---

## 9. Referências

1. SEDRA, A. S.; SMITH, K. C. **Microeletrônica**. 5ª ed. São Paulo: Pearson, 2007.

2. BOYLESTAD, R. L. **Introdução à Análise de Circuitos**. 12ª ed. São Paulo: Pearson, 2012.

3. WILLIAMS, A. B.; TAYLOR, F. J. **Electronic Filter Design Handbook**. 4ª ed. McGraw-Hill, 2006.

4. BUTTERWORTH, S. "On the Theory of Filter Amplifiers". *Wireless Engineer*, vol. 7, pp. 536-541, 1930.

5. SMALL, R. H. "Direct-Radiator Loudspeaker System Analysis". *IEEE Transactions on Audio and Electroacoustics*, vol. AU-19, no. 4, pp. 269-281, 1971.

6. LIPSHITZ, S. P.; VANDERKOOY, J. "A Family of Linear-Phase Crossover Networks of High Slope Derived by Time Delay". *Journal of the Audio Engineering Society*, vol. 31, no. 1/2, pp. 2-20, 1983.

7. COLLOMS, M. **High Performance Loudspeakers**. 6ª ed. Wiley, 2005.

8. **IEC 60268-5**: Sound system equipment - Part 5: Loudspeakers. International Electrotechnical Commission, 2003.

---

## 10. Apêndice: Lista de Materiais (BOM)

### Bill of Materials - Crossover 3.4 kHz @ 4Ω

| Item | Componente | Valor | Filtro | Quantidade | Tolerância |
|------|------------|-------|--------|------------|------------|
| L1 | Indutor air-core | 0.39 mH | LPF | 1 | ±5% |
| C1 | Capacitor filme/poliéster | 12 μF | LPF | 1 | ±5% |
| L2 | Indutor air-core | 0.18 mH | HPF | 1 | ±5% |
| C2 | Capacitor filme/poliéster | 22 μF | HPF | 1 | ±5% |

**Observações:**
- Usar indutores air-core para minimizar distorção
- Capacitores de filme (poliéster, polipropileno) para baixo ESR
- Respeitar tensão de trabalho adequada (mín. 100V para aplicações de potência)
- Componentes devem suportar correntes adequadas ao sistema

---

**Data de conclusão:** Dezembro/2024  
**Repositório:** [GitHub - Crossover Butterworth CC44CP](https://github.com/jeantiecher/crossover-butterworth-cc44cp)
