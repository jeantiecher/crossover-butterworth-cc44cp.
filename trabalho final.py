import numpy as np
import matplotlib.pyplot as plt

# PARÂMETROS DE PROJETO
# Jean de Carvalho: RL = 4 Ω, fc = 3.4 kHz
RL = 4.0  # Impedância da carga (Ohms)
fc = 3.4e3  # Frequência de corte (Hz)

# VALORES COMERCIAIS DISPONÍVEIS
# Tabela 2: Indutores comerciais (em Henry)
INDUTORES_COMERCIAIS = np.array([
    0.10e-3, 0.12e-3, 0.15e-3, 0.18e-3, 0.22e-3, 0.27e-3,
    0.33e-3, 0.39e-3, 0.47e-3, 0.56e-3, 0.68e-3, 0.82e-3,
    1.0e-3, 1.2e-3, 1.5e-3, 1.8e-3, 2.2e-3, 2.7e-3,
    3.3e-3, 3.9e-3, 4.7e-3, 5.6e-3, 6.8e-3, 8.2e-3,
    10e-3, 12e-3, 15e-3
])

# Tabela 3: Capacitores comerciais (em Farad)
CAPACITORES_COMERCIAIS = np.array([
    1.0e-6, 1.2e-6, 1.5e-6, 1.8e-6, 2.2e-6, 2.7e-6,
    3.3e-6, 3.9e-6, 4.7e-6, 5.6e-6, 6.8e-6, 8.2e-6,
    10e-6, 12e-6, 15e-6, 18e-6, 22e-6, 27e-6,
    33e-6, 39e-6, 47e-6, 56e-6, 68e-6, 82e-6,
    100e-6
])

# FUNÇÕES DE CÁLCULO - FILTRO BUTTERWORTH 2ª ORDEM

def calcular_lpf_butterworth_2ordem(fc, RL):
    """
    Calcula valores ideais de L e C para filtro Passa-Baixas Butterworth 2ª ordem.
    
    Topologia: Indutor em série + Capacitor em paralelo com carga
    
    Fórmulas:
        L = RL / (π * fc)
        C = 1 / (2π * fc * RL)
    """
    L_ideal = RL / (np.pi * fc)
    C_ideal = 1 / (2 * np.pi * fc * RL)
    return L_ideal, C_ideal


def calcular_hpf_butterworth_2ordem(fc, RL):
    """
    Calcula valores ideais de C e L para filtro Passa-Altas Butterworth 2ª ordem.
    
    Topologia: Capacitor em série + Indutor em paralelo com carga
    
    Fórmulas:
        C = 1 / (π * fc * RL)
        L = RL / (2π * fc)
    """
    C_ideal = 1 / (np.pi * fc * RL)
    L_ideal = RL / (2 * np.pi * fc)
    return C_ideal, L_ideal


def selecionar_componente_comercial(valor_ideal, valores_comerciais):
    """
    Seleciona o componente comercial mais próximo do valor ideal.
    
    Retorna: (valor_comercial, erro_percentual)
    """
    idx = np.argmin(np.abs(valores_comerciais - valor_ideal))
    valor_comercial = valores_comerciais[idx]
    erro_percentual = ((valor_comercial - valor_ideal) / valor_ideal) * 100
    return valor_comercial, erro_percentual


# FUNÇÕES PARA RESPOSTA EM FREQUÊNCIA

def resposta_lpf_2ordem(f, L, C, RL):
    """
    Calcula resposta em frequência (dB) do filtro Passa-Baixas.
    
    Usa divisor de tensão: H(jω) = ZC||RL / (ZL + ZC||RL)
    """
    omega = 2 * np.pi * f
    ZL = 1j * omega * L
    ZC = 1 / (1j * omega * C)
    ZC_par_RL = (ZC * RL) / (ZC + RL)
    H = ZC_par_RL / (ZL + ZC_par_RL)
    return 20 * np.log10(np.abs(H))


def resposta_hpf_2ordem(f, C, L, RL):
    """
    Calcula resposta em frequência (dB) do filtro Passa-Altas.
    
    Usa divisor de tensão: H(jω) = ZL||RL / (ZC + ZL||RL)
    """
    omega = 2 * np.pi * f
    ZC = 1 / (1j * omega * C)
    ZL = 1j * omega * L
    ZL_par_RL = (ZL * RL) / (ZL + RL)
    H = ZL_par_RL / (ZC + ZL_par_RL)
    return 20 * np.log10(np.abs(H))


# CÁLCULOS PRINCIPAIS

print("="*70)
print("PROJETO DE CROSSOVER PASSIVO - FILTROS BUTTERWORTH 2ª ORDEM")
print("="*70)
print(f"\nPARÂMETROS DE PROJETO:")
print(f"  Impedância da carga (RL): {RL} Ω")
print(f"  Frequência de corte (fc): {fc/1000:.1f} kHz")
print("="*70)

# FILTRO PASSA-BAIXAS (LPF)
print("\n[1] FILTRO PASSA-BAIXAS (LPF) - WOOFER")
print("-"*70)

L_lpf_ideal, C_lpf_ideal = calcular_lpf_butterworth_2ordem(fc, RL)
print(f"\nValores Ideais Calculados:")
print(f"  L_ideal = {L_lpf_ideal*1e3:.6f} mH ({L_lpf_ideal:.6e} H)")
print(f"  C_ideal = {C_lpf_ideal*1e6:.6f} μF ({C_lpf_ideal:.6e} F)")

L_lpf_comercial, erro_L_lpf = selecionar_componente_comercial(L_lpf_ideal, INDUTORES_COMERCIAIS)
C_lpf_comercial, erro_C_lpf = selecionar_componente_comercial(C_lpf_ideal, CAPACITORES_COMERCIAIS)

print(f"\nComponentes Comerciais Selecionados:")
print(f"  L_comercial = {L_lpf_comercial*1e3:.2f} mH (erro: {erro_L_lpf:+.2f}%)")
print(f"  C_comercial = {C_lpf_comercial*1e6:.2f} μF (erro: {erro_C_lpf:+.2f}%)")

desvio_medio_lpf = (abs(erro_L_lpf) + abs(erro_C_lpf)) / 2
print(f"\nDesvio Médio dos Componentes: {desvio_medio_lpf:.2f}%")

# FILTRO PASSA-ALTAS (HPF)
print("\n[2] FILTRO PASSA-ALTAS (HPF) - TWEETER")
print("-"*70)

C_hpf_ideal, L_hpf_ideal = calcular_hpf_butterworth_2ordem(fc, RL)
print(f"\nValores Ideais Calculados:")
print(f"  C_ideal = {C_hpf_ideal*1e6:.6f} μF ({C_hpf_ideal:.6e} F)")
print(f"  L_ideal = {L_hpf_ideal*1e3:.6f} mH ({L_hpf_ideal:.6e} H)")

C_hpf_comercial, erro_C_hpf = selecionar_componente_comercial(C_hpf_ideal, CAPACITORES_COMERCIAIS)
L_hpf_comercial, erro_L_hpf = selecionar_componente_comercial(L_hpf_ideal, INDUTORES_COMERCIAIS)

print(f"\nComponentes Comerciais Selecionados:")
print(f"  C_comercial = {C_hpf_comercial*1e6:.2f} μF (erro: {erro_C_hpf:+.2f}%)")
print(f"  L_comercial = {L_hpf_comercial*1e3:.2f} mH (erro: {erro_L_hpf:+.2f}%)")

desvio_medio_hpf = (abs(erro_C_hpf) + abs(erro_L_hpf)) / 2
print(f"\nDesvio Médio dos Componentes: {desvio_medio_hpf:.2f}%")

# GERAÇÃO DOS GRÁFICOS DE BODE

frequencias = np.logspace(1, 5, 1000)  # 10 Hz a 100 kHz

# Respostas em frequência
mag_lpf_ideal = resposta_lpf_2ordem(frequencias, L_lpf_ideal, C_lpf_ideal, RL)
mag_lpf_real = resposta_lpf_2ordem(frequencias, L_lpf_comercial, C_lpf_comercial, RL)
mag_hpf_ideal = resposta_hpf_2ordem(frequencias, C_hpf_ideal, L_hpf_ideal, RL)
mag_hpf_real = resposta_hpf_2ordem(frequencias, C_hpf_comercial, L_hpf_comercial, RL)

# Criação dos gráficos
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Gráfico LPF
ax1.semilogx(frequencias, mag_lpf_ideal, 'b-', linewidth=2, label='Ideal')
ax1.semilogx(frequencias, mag_lpf_real, 'r--', linewidth=2, label='Comercial')
ax1.axvline(fc, color='gray', linestyle=':', linewidth=1, label=f'fc = {fc/1000:.1f} kHz')
ax1.axhline(-3, color='green', linestyle=':', linewidth=1, alpha=0.5, label='-3 dB')
ax1.grid(True, which='both', alpha=0.3)
ax1.set_xlabel('Frequência (Hz)', fontsize=12)
ax1.set_ylabel('Magnitude (dB)', fontsize=12)
ax1.set_title(f'Filtro Passa-Baixas (LPF) - Woofer | RL = {RL}Ω, fc = {fc/1000:.1f} kHz', 
              fontsize=14, fontweight='bold')
ax1.legend(loc='upper right', fontsize=10)
ax1.set_ylim([-60, 5])

# Gráfico HPF
ax2.semilogx(frequencias, mag_hpf_ideal, 'b-', linewidth=2, label='Ideal')
ax2.semilogx(frequencias, mag_hpf_real, 'r--', linewidth=2, label='Comercial')
ax2.axvline(fc, color='gray', linestyle=':', linewidth=1, label=f'fc = {fc/1000:.1f} kHz')
ax2.axhline(-3, color='green', linestyle=':', linewidth=1, alpha=0.5, label='-3 dB')
ax2.grid(True, which='both', alpha=0.3)
ax2.set_xlabel('Frequência (Hz)', fontsize=12)
ax2.set_ylabel('Magnitude (dB)', fontsize=12)
ax2.set_title(f'Filtro Passa-Altas (HPF) - Tweeter | RL = {RL}Ω, fc = {fc/1000:.1f} kHz', 
              fontsize=14, fontweight='bold')
ax2.legend(loc='lower right', fontsize=10)
ax2.set_ylim([-60, 5])

plt.tight_layout()
plt.savefig('bode_comparativo.png', dpi=300, bbox_inches='tight')
print("\n" + "="*70)
print("Gráfico salvo como 'bode_comparativo.png'")
print("="*70)
plt.show()

# ANÁLISE CRÍTICA

print("\n[3] ANÁLISE CRÍTICA")
print("-"*70)

# Diferença máxima de magnitude nas bandas de passagem
idx_baixa = frequencias < fc
idx_alta = frequencias > fc
diff_lpf_passante = np.max(np.abs(mag_lpf_ideal[idx_baixa] - mag_lpf_real[idx_baixa]))
diff_hpf_passante = np.max(np.abs(mag_hpf_ideal[idx_alta] - mag_hpf_real[idx_alta]))

print(f"\nDiferenças entre filtros ideais e comerciais:")
print(f"  LPF - Diferença máxima na banda passante: {diff_lpf_passante:.3f} dB")
print(f"  HPF - Diferença máxima na banda passante: {diff_hpf_passante:.3f} dB")

print(f"\nDesvio dos componentes:")
print(f"  LPF - Desvio médio dos componentes: {desvio_medio_lpf:.2f}%")
print(f"  HPF - Desvio médio dos componentes: {desvio_medio_hpf:.2f}%")

print("\n" + "="*70)
print("CONCLUSÃO DA ANÁLISE")
print("="*70)

# Classificação da qualidade
if diff_lpf_passante < 0.5 and diff_hpf_passante < 0.5:
    qualidade = "EXCELENTE"
    impacto = "praticamente inaudíveis"
elif diff_lpf_passante < 1.0 and diff_hpf_passante < 1.0:
    qualidade = "MUITO BOA"
    impacto = "apenas ouvintes muito críticos detectariam"
else:
    qualidade = "BOA"
    impacto = "podem ser perceptíveis em sistemas high-end"

print(f"""
Qualidade da aproximação: {qualidade}

Diferenças de magnitude na banda passante: {impacto}
- LPF: {diff_lpf_passante:.3f} dB
- HPF: {diff_hpf_passante:.3f} dB

Desvios dos componentes:
- LPF: {desvio_medio_lpf:.2f}% (L: {erro_L_lpf:+.2f}%, C: {erro_C_lpf:+.2f}%)
- HPF: {desvio_medio_hpf:.2f}% (C: {erro_C_hpf:+.2f}%, L: {erro_L_hpf:+.2f}%)

Este projeto atende às especificações típicas de crossovers de áudio.
Para análise detalhada, consulte o README.md
""")