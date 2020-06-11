def palabra_valida(palabra):
    """
    Verifica si la palabra formada existe y devuelve true y es un Sustantivo, Adjetivo o Verbo
    """
    from pattern.text.es import verbs, spelling, lexicon , parse
    import string
    if not (palabra.lower() in verbs) and (not palabra.lower() in spelling) and (not(palabra.lower() in lexicon) and not(palabra.upper() in lexicon) and not(palabra.capitalize() in lexicon)):
        pass
    else:
        tipo_palabra = parse(palabra)
        return ("NN" in tipo_palabra) or ("VB" in tipo_palabra) or ("JJ" in tipo_palabra)
