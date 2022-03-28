class FontColor:
    """不同的版本可能颜色不一样
    调用方式：颜色/背景色/+下划线标志 + 需要加颜色的文字 + 结束标志
    """
    # 字体颜色
    black = "30"
    red = "31"
    green = "32"
    brown = "33"
    blue = "34"
    violet = "35"
    pink = "36"
    white = "37"

    # 背景色
    black_background = "40"  # default
    red_background = "41"
    green_background = "42"
    brown_background = "43"
    pink_background = "44"
    violet_background = "45"  # 紫色
    blue_background = "46"
    white_background = "47"

    # 模板
    template = '\033[{};{}{} \033[0m'

    # 字体格式
    MODEL_BOLD = '1m'  # 加粗
    MODEL_DEFAULT = '2m'  # 正常
    MODEL_ITALIC = '3m'  # 斜体
    MODEL_UNDERLINE = '4m'  # 下划线

    # 设置字体色方法
    @classmethod
    def set_color(cls, text, color="red", model='default'):
        if hasattr(cls, color):
            return cls.template.format(getattr(cls, color), getattr(cls, 'MODEL_' + model.upper()), text)
        return text

    # 设置背景色
    @classmethod
    def set_backcolor(cls, text, backcolor="red", model='default'):
        color = backcolor + "_background"
        if hasattr(cls, color):
            return cls.template.format(getattr(cls, color), getattr(cls, 'MODEL_' + model.upper()), text)
        return text


if __name__ == '__main__':
    print(FontColor.set_color('Moonlight'))
