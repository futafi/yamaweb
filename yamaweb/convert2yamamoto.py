import numpy as np
import zipfile
from io import BytesIO


def jij2str(jij):
    # 384x384に拡張
    jij = np.pad(jij, (0, 384 - jij.shape[0]))

    # 丸め
    jij = np.where(jij >= 31, 31, jij)
    jij = np.where(jij <= -32, -32, jij)

    # 分割
    separated = []
    # tate -> yoko
    for i in np.hsplit(jij, 4):
        separated.extend(np.vsplit(i, 4))
    # # yoko -> tate
    # for i in np.vsplit(jij, 4):
    #     jij_lists.extend(np.hsplit(i, 4))

    def toStr(jij):
        jij = np.vectorize(lambda x: format(x if x >= 0 else (x & 0x3f), '02X'))(jij)
        jij = "".join(np.apply_along_axis(lambda x: "".join(x), 1, jij))
        return jij

    jij = "".join(map(toStr, separated))
    return jij


def hi2str(hi):
    hi = np.pad(hi, (0, 384 - hi.size))
    hi = np.vectorize(lambda x: format(x if x >= 0 else (x & 0xffff), '04x'))(hi)
    hi = "".join(hi)
    return hi


def param2str(temperature=255, eta=0.9995, test0=0, test1=0, test2=0, test3=0, result=0):
    temperature = format(int(format(int(temperature), '016b')[::-1], 2), '04X')
    eta = format(int(format(round(eta * 65536), '016b')[::-1], 2), '04X')
    test0 = format(int(format(int(test0), '016b')[::-1], 2), '04X')
    test1 = format(int(format(int(test1), '016b')[::-1], 2), '04X')
    test2 = format(int(format(int(test2), '016b')[::-1], 2), '04X')
    test3 = format(int(format(int(test3), '016b')[::-1], 2), '04X')
    result = format(int(format(int(result), '08b')[::-1], 2), '02X')
    return temperature + eta + test0 + test1 + test2 + test3 + result


def toYamamotoStr(jij, hi, temperature=255, eta=0.9995, test0=0, test1=0, test2=0, test3=0, result=0):
    str1 = "@" + jij2str(jij)
    str2 = adder_spin_str = "+" + ("01" * (1536 // 2))
    controller_spin_str = "01" * (384 // 2)
    str3 = "*" + controller_spin_str + hi2str(hi) + param2str(temperature, eta, test0, test1, test2, test3, result)
    return str1, str2, str3


def toYamamotoFile(jij, hi, temperature=255, eta=0.9995, test0=0, test1=0, test2=0, test3=0, result=0):
    strs = toYamamotoStr(jij, hi, temperature, eta, test0, test1, test2, test3, result)
    file = BytesIO()
    with zipfile.ZipFile(file, 'w', zipfile.ZIP_STORED) as z:
        for name, text in zip(["01_JIJ.txt", "02_controller_spin.txt", "03_settings_hi.txt"], strs):
            z.writestr(str(name), text.encode("UTF-8"))
    file.seek(0)
    return file
