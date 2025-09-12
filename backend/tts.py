from gtts import gTTS
import os

import json
from pypinyin import pinyin, Style


def get_one_hanzi_for_pinyin(syllable, tone):
    target = syllable + str(tone)
    for codepoint in range(0x4E00, 0x9FFF):  # CJK Unified Ideographs
        char = chr(codepoint)
        py = pinyin(char, style=Style.TONE3, strict=False)
        if py and py[0][0] == target:
            return char
    return None

pinyins = [
    "a", "ai", "an", "ang", "ao", "ba", "bai", "ban", "bang", "bao", "bei", "ben", "beng",
    "bi", "bian", "biang", "biao", "bie", "bin", "bing", "bo", "bu", "ca", "cai", "can",
    "cang", "cao", "ce", "cei", "cen", "ceng", "cha", "chai", "chan", "chang", "chao",
    "che", "chen", "cheng", "chi", "chong", "chou", "chu", "chua", "chuai", "chuan",
    "chuang", "chui", "chun", "chuo", "ci", "cong", "cou", "cu", "cuan", "cui", "cun",
    "cuo", "da", "dai", "dan", "dang", "dao", "de", "dei", "den", "deng", "di", "dian",
    "diao", "die", "ding", "diu", "dong", "dou", "du", "duan", "dui", "dun", "duo", "e",
    "ei", "en", "eng", "er", "fa", "fan", "fang", "fei", "fen", "feng", "fo", "fou",
    "fu", "ga", "gai", "gan", "gang", "gao", "ge", "gei", "gen", "geng", "gong", "gou",
    "gu", "gua", "guai", "guan", "guang", "gui", "gun", "guo", "ha", "hai", "han",
    "hang", "hao", "he", "hei", "hen", "heng", "hong", "hou", "hu", "hua", "huai",
    "huan", "huang", "hui", "hun", "huo", "ji", "jia", "jian", "jiang", "jiao", "jie",
    "jin", "jing", "jiong", "jiu", "ju", "juan", "jue", "jun", "ka", "kai", "kan",
    "kang", "kao", "ke", "kei", "ken", "keng", "kong", "kou", "ku", "kua", "kuai",
    "kuan", "kuang", "kui", "kun", "kuo", "la", "lai", "lan", "lang", "lao", "le",
    "lei", "leng", "li", "lia", "lian", "liang", "liao", "lie", "lin", "ling", "liu",
    "lo", "long", "lou", "lu", "luan", "lun", "luo", "lü", "lüe", "ma", "mai", "man",
    "mang", "mao", "me", "mei", "men", "meng", "mi", "mian", "miao", "mie", "min",
    "ming", "miu", "mo", "mou", "mu", "na", "nai", "nan", "nang", "nao", "ne", "nei",
    "nen", "neng", "ni", "nian", "niang", "niao", "nie", "nin", "ning", "niu", "nong",
    "nou", "nu", "nuan", "nuo", "nü", "nüe", "o", "ou", "pa", "pai", "pan", "pang",
    "pao", "pei", "pen", "peng", "pi", "pian", "piao", "pie", "pin", "ping", "po",
    "pou", "pu", "qi", "qia", "qian", "qiang", "qiao", "qie", "qin", "qing", "qiong",
    "qiu", "qu", "quan", "que", "qun", "ran", "rang", "rao", "re", "ren", "reng", "ri",
    "rong", "rou", "ru", "rua", "ruan", "rui", "run", "ruo", "sa", "sai", "san", "sang",
    "sao", "se", "sen", "seng", "sha", "shai", "shan", "shang", "shao", "she", "shei",
    "shen", "sheng", "shi", "shou", "shu", "shua", "shuai", "shuan", "shuang", "shui",
    "shun", "shuo", "si", "song", "sou", "su", "suan", "sui", "sun", "suo", "ta", "tai",
    "tan", "tang", "tao", "te", "teng", "ti", "tian", "tiao", "tie", "ting", "tong",
    "tou", "tu", "tuan", "tui", "tun", "tuo", "wa", "wai", "wan", "wang", "wei", "wen",
    "weng", "wo", "wu", "xi", "xia", "xian", "xiang", "xiao", "xie", "xin", "xing",
    "xiong", "xiu", "xu", "xuan", "xue", "xun", "ya", "yan", "yang", "yao", "ye", "yi",
    "yin", "ying", "yong", "you", "yu", "yuan", "yue", "yun", "za", "zai", "zan",
    "zang", "zao", "ze", "zei", "zen", "zeng", "zha", "zhai", "zhan", "zhang", "zhao",
    "zhe", "zhei", "zhen", "zheng", "zhi", "zhong", "zhou", "zhu", "zhua", "zhuai",
    "zhuan", "zhuang", "zhui", "zhun", "zhuo", "zi", "zong", "zou", "zu", "zuan",
    "zui", "zun", "zuo"
]
dict = {}

for pin in pinyins:

    for t in range(1, 5):
        key = f"{pin}{t}"
        char = get_one_hanzi_for_pinyin(pin, t)
        if char is not None: 
            dict[key] = get_one_hanzi_for_pinyin(pin, t)
            print(key, "->", char)

print(dict)
print(len(dict))

print("Total found:", len(dict))

# Save dictionary to JSON
with open("pinyin_to_hanzi.json", "w", encoding="utf-8") as f:
    json.dump(dict, f, ensure_ascii=False, indent=2)

print("Dictionary saved to pinyin_to_hanzi.json")

# # -----------------------------
# # 1. Define syllables and tones
# # -----------------------------
# syllables = [
#     ("ma1", "妈"),  # Tone 1
#     ("ma2", "麻"),  # Tone 2
#     ("ma3", "马"),  # Tone 3
#     ("ma4", "骂")   # Tone 4
# ]

# OUTPUT_DIR = "tts_audio"
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# # -----------------------------
# # 2. Generate TTS audio
# # -----------------------------
# for label, hanzi in syllables:
#     tts = gTTS(text=hanzi, lang='zh-cn', slow=False)
#     path = os.path.join(OUTPUT_DIR, f"{label}.mp3")
#     tts.save(path)
#     print(f"Saved original {path}")

