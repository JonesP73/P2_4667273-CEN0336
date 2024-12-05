def contar_nos(arvore, nivel=0):
    """
    Conta os nós de uma árvore e imprime a árvore à medida que processa.
    
    Args:
    arvore (dict): A árvore representada como dicionário aninhado.
    nivel (int): Nível de profundidade atual na árvore, usado para formatação.
    
    Returns:
    int: Total de nós na árvore.
    """
    if not arvore:
        return 0  # Caso base: árvore vazia tem 0 nós
    
    # Mostra a árvore atual no nível correspondente
    for chave in arvore.keys():
        print(" " * (nivel * 4) + f"- {chave}")  # Indenta de acordo com o nível
    
    total = 1  # Conta o nó atual
    for subarvore in arvore.values():
        total += contar_nos(subarvore, nivel + 1)  # Soma os nós das subárvores
    
    return total

# Exemplo de uso
arvore = {
    "Filo1": {
        "Classe1": {
            "Ordem1": {
                "Familia1": {},
                "Familia2": {}
            },
            "Ordem2": {
                "Familia3": {
                    "Genero3": {},
                    "Genero4": {}
                }
            }
        },
        "Classe2": {
            "Ordem3": {},
            "Ordem4": {
                "Familia4": {},
                "Familia5": {
                    "Genero1": {},
                    "Genero2": {
                        "Especie1": {},
                        "Especie2": {}
                    }
                }
            }
        }
    }
}

# Chamando a função
print("Estrutura da árvore:")
total_nos = contar_nos(arvore)
print(f"\nTotal de nós na árvore: {total_nos}")
