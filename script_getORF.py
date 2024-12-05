#!/usr/bin/env python3
import sys
import re
import hashlib  # Para calcular o md5sum do script

def carregar_sequencias(caminho_arquivo):
    """
    Lê um arquivo multifasta e retorna as sequências em um dicionário.
    """
    sequencias = {}
    try:
        with open(caminho_arquivo, "r") as arquivo_fasta:
            identificador_atual = ""
            for linha in arquivo_fasta:
                linha = linha.strip()
                if linha.startswith(">"):
                    identificador_atual = linha[1:].split()[0]
                    sequencias[identificador_atual] = ""
                else:
                    sequencias[identificador_atual] += linha.upper()
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
        sys.exit(1)
    return sequencias

def obter_reverso_complementar(sequencia):
    """
    Retorna o reverso complementar de uma sequência de DNA.
    """
    complemento = str.maketrans("ATCG", "TAGC")
    reverso = sequencia[::-1]
    return reverso.translate(complemento)

def identificar_maior_orf(sequencia):
    """
    Encontra o maior ORF (Quadro de Leitura Aberto) em uma sequência de DNA.
    """
    if not sequencia:
        print("Erro: A sequência está vazia.")
        return "", 0, 0, 0

    stop_codons = {'TAA', 'TAG', 'TGA'}
    maior_orf = {
        "sequencia": "",
        "quadro": 0,
        "inicio": 0,
        "fim": 0
    }

    def buscar_orfs(dna, quadro_inicial):
        for quadro in range(quadro_inicial, quadro_inicial + 3):
            codons = re.findall(r".{3}", dna[quadro:])
            orf = []
            for i, codon in enumerate(codons):
                if codon == "ATG" and not orf:
                    orf = [codon]
                elif codon in stop_codons and orf:
                    orf.append(codon)
                    if len("".join(orf)) > len(maior_orf["sequencia"]):
                        maior_orf.update({
                            "sequencia": "".join(orf),
                            "quadro": quadro_inicial // 3 + 1,
                            "inicio": quadro + i * 3 + 1,
                            "fim": quadro + (i + 1) * 3
                        })
                    orf = []
                elif orf:
                    orf.append(codon)

    # Pesquisar nos 3 quadros de leitura e no reverso complementar
    buscar_orfs(sequencia, 0)
    buscar_orfs(obter_reverso_complementar(sequencia), 3)

    return maior_orf["sequencia"], maior_orf["quadro"], maior_orf["inicio"], maior_orf["fim"]

def traduzir_dna_em_proteina(sequencia):
    """
    Traduz uma sequência de DNA em proteína usando a tabela de tradução padrão.
    """
    tabela_traducao = {
        'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
        'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R', 'AGA': 'R', 'AGG': 'R',
        'AAT': 'N', 'AAC': 'N', 'GAT': 'D', 'GAC': 'D',
        'TGT': 'C', 'TGC': 'C', 'CAA': 'Q', 'CAG': 'Q',
        'GAA': 'E', 'GAG': 'E', 'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',
        'CAT': 'H', 'CAC': 'H', 'ATT': 'I', 'ATC': 'I', 'ATA': 'I',
        'TTA': 'L', 'TTG': 'L', 'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
        'AAA': 'K', 'AAG': 'K', 'ATG': 'M', 'TTT': 'F', 'TTC': 'F',
        'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P', 'TCT': 'S', 'TCC': 'S',
        'TCA': 'S', 'TCG': 'S', 'AGT': 'S', 'AGC': 'S', 'ACT': 'T', 'ACC': 'T',
        'ACA': 'T', 'ACG': 'T', 'TGG': 'W', 'TAT': 'Y', 'TAC': 'Y',
        'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V', 'TAA': '*', 'TAG': '*', 'TGA': '*'
    }
    proteina = ""
    for i in range(0, len(sequencia) - 2, 3):
        codon = sequencia[i:i + 3]
        proteina += tabela_traducao.get(codon, 'X')  # 'X' indica códon inválido
    return proteina

# Entry point for the script
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 script_getORF.py <arquivo_fasta>")
        sys.exit(1)

    arquivo_fasta = sys.argv[1]
    sequencias = carregar_sequencias(arquivo_fasta)

    with open("ORF.fna", "w") as arquivo_orf_fna, open("ORF.faa", "w") as arquivo_orf_faa:
        for id_seq, seq in sequencias.items():
            maior_orf, quadro, inicio, fim = identificar_maior_orf(seq)
            identificador = f"{id_seq}_frame{quadro}_{inicio}_{fim}"
            arquivo_orf_fna.write(f">{identificador}\n{maior_orf}\n")
            arquivo_orf_faa.write(f">{identificador}\n{traduzir_dna_em_proteina(maior_orf)}\n")

    # Calcular md5sum do script
    with open(__file__, "rb") as f:
        script_md5sum = hashlib.md5(f.read()).hexdigest()
    print(f"md5sum do script: {script_md5sum}")
