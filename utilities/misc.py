def obfuscate_word(word):
    """
    Obfuscates a word by replacing each charachter with an *
    """
    return_str = ""
    for char in word:
        return_str += "*"        
    return return_str