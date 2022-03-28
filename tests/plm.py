# [汇总表.金额]*[汇总表.本币汇率]-[汇总表.金额]*[汇总表.本币汇率]/1.13*13%


def add(x, y):
    return x * y - (x * y / 1.13 * 0.13)


def add_plus(x, y):
    return x*y*(1-1/1.13)


