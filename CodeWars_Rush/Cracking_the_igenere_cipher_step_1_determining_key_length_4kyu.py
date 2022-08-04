# accepted on codewars.com
alphabet = 'abcdefghijklmnopqrstuvwxyz'

# Returns the Index of Coincidence for the part of cipher text
def get_index_of_coincidence(cipher_text_part):
    N = float(len(cipher_text_part))
    freq_sum = 0.0
    # here we use Index of Coincidence formula
    for letter in alphabet:
        freq_sum += cipher_text_part.count(letter) * (cipher_text_part.count(letter) - 1)

    index_of_coincidence = freq_sum / (N * (N - 1))
    return index_of_coincidence


# Returns the key length with the highest average Index of Coincidence
def get_key_length(cipher_text, max_key_length):
    table_of_coincidence = []

    # Splits the initial ciphertext into sequences based on the guessed key length from 0 to max_key_length
    for curr_length in range(max_key_length):
        coincidence_sum = 0.0
        average_coincidence = 0.0
        for i in range(curr_length):
            sequence = ""
            # breaks the ciphertext into sequences
            for j in range(0, len(cipher_text[i:]), curr_length):
                sequence += cipher_text[i + j]
            coincidence_sum += get_index_of_coincidence(sequence)
        # prevents dividing by zero
        if not curr_length == 0:
            average_coincidence = coincidence_sum / curr_length
        table_of_coincidence.append(average_coincidence)

    # The index of the highest Index of Coincidence
    best_guess = table_of_coincidence.index(sorted(table_of_coincidence)[::-1][0])

    return best_guess


cipher_text_given = '''+vzf>=xsIzP/bqDKF/I8BvG\\vrfvi`vDPOy|zCIfD]I8wzG\\x8zSA/GHDJL+CzTfQ|ICIB\x0cU%COzBUrIOCM`boIyi[rHCzK+KwxDy\\bQCvP@vGf\'S|NwyBCUUCyBQ]E8{\'C zGfXy`ICGG UtoGGC.bHCzijzuzIC`v8xDN<vFfPL,IsvFy,CsfDLUywNfp)nmfKG/tsf`<<v8VGN<rpzOi0zDCzPubwIfyUtvDGB`vB`Ni[ruvUG\\v`f$LUinms\rU*qDzL|ztDxi\x0bDsMDA+E8yzQ-IwwzBUKvzf>=xsIzP/bqDKF/I8vNiuzAKJQ{zpGzi]w8OMy\\JzvOG]E?\n/F=J8MzN}KoODM\\bKvNi\\FHfyC{vFQzBBbQCvP@vGfWy,soBzi=J8FIM E8OJi<rJzfz`FyzIi+bJvMG+EHfJDUKvzfA=GvzMi+J8zvP@P8vNi"pjp\x0ci<FKzQC`{8Czi.zrI`RUGIwGG{y8CDQUNCMF\x0c8rGDNI=bsIOG`vzTfz`FyzfR<v8xDN<vFfvL.bDPwJ=Jvzyi|ysfOC-yBDLS/bwIfR<v8muR<bqzIR}IM\nf#~vBfwC:FFzfR<zG fR<FIBC\rUJCHzi{BwGGC.bqMTN|rBvGW{KGfxM}CrfJA-rGDJL+CzTfz`voFfR<v8xDN<vFfDLUKvzfp\'KvfxC\\KIMT~kzyDKC.zo|'''

print(get_key_length(cipher_text_given, 10))
