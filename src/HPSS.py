def hpss(wave):
    """Split the wave into harmonic and percussive"""
    return wave, wave


def harmonic_summ(arr):
    arr = abs(arr)
    for i in range(1, len(arr)+1):
        if (i+1)*2 < len(arr):
            arr[i-1] += arr[(i+1)*2]
            if (i+1)*3 < len(arr):
                arr[i-1] += arr[(i+1)*3]
                if (i+1)*4 < len(arr):
                    arr[i-1] += arr[(i+1)*4]
                    if (i+1)*5 < len(arr):
                        arr[i-1] += arr[(i+1)*5]
    return arr