def replace_terms_with_no_spaces(text, terms):
    for term in terms:
        term_without_spaces = term.replace(" ", "")
        text = text.replace(term, term_without_spaces)
    return text


def main():
    # Texto de exemplo
    input_text = "Este é um exemplo de texto com termos compostos. Vamos substituir esses termos."

    # Ler termos compostos de um arquivo
    with open("data/termos.txt", "r") as file:
        compound_terms = [line.strip() for line in file]

    # Ordenar os termos compostos por tamanho de string
    compound_terms.sort(key=len, reverse=True)

    # Substituir os termos compostos no texto
    output_text = replace_terms_with_no_spaces(input_text, compound_terms)

    print("Texto original:")
    print(input_text)

    print("\nTexto após substituição:")
    print(output_text)


if __name__ == "__main__":
    main()
