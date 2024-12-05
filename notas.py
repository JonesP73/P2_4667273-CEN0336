#!/usr/bin/env python3

# Inicialização das variáveis
total = 0
contador_notas = 0

# Loop para inserir 10 notas
while contador_notas < 10:
    nota = float(input("Digite a nota: "))  # Recebe a nota como número decimal
    total += nota  # Soma a nota ao total
    contador_notas += 1  # Incrementa o contador de notas

# Cálculo da média
media = total / 10

# Exibe a média
print(f"A média das notas é: {media:.2f}")
