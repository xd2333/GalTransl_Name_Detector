import os, json,csv
from sudachipy import Dictionary, SplitMode
from caiyun import batch_translate
import thulac


def contains_japanese(text: str) -> bool:
    """
    此函数接受一个字符串作为输入，检查其中是否包含日文字符。

    参数:
    - text: 要检查的字符串。

    返回值:
    - 如果字符串中包含日文字符，则返回 True，否则返回 False。
    """
    # 日文字符范围
    katakana_range = (0x30A0, 0x30FF)

    # 检查字符串中的每个字符
    for char in text:
        # 排除ー
        if char in ["ー", "・"]:
            continue
        # 获取字符的 Unicode 码点
        code_point = ord(char)
        # 检查字符是否在日文字符范围内
        if katakana_range[0] <= code_point <= katakana_range[1]:
            return True
    return False


thu1 = thulac.thulac()  # 默认模式
name_dict_nlp = {}
name_dict = {}  # 存储所有name以及它们出现的次数的字典
zhuan_dict = {}
zhuan_list = []
tokenizer = Dictionary().create()

folder = input("Enter the json_jp folder: ")
threshold = int(input("Enter the threshold: ") or "10")

for filename in os.listdir(folder):
    if not filename.endswith(".json"):
        continue

    with open(os.path.join(folder, filename), "r", encoding="utf-8") as f:
        print(filename)
        data = json.load(f)

    for obj in data:
        # 提取name_dict
        if "name" in obj:
            name = obj["name"]
            if isinstance(name, str):
                if name in name_dict:
                    name_dict[name] += 1
                else:
                    name_dict[name] = 1
        if "names" in obj:
            names = obj["names"]
            if isinstance(names, list):
                for name in names:
                    if isinstance(name, str):
                        if name in name_dict:
                            name_dict[name] += 1
                        else:
                            name_dict[name] = 1

        # nlp技术提取name
        if "name" in obj:
            name = obj["name"]
        else:
            name = ""
        message = obj["message"]
        if name:
            message = name + "：" + message
        tokens = tokenizer.tokenize(message, mode=SplitMode.B)

        for token in tokens:
            # 人名
            if token.part_of_speech()[0] == "名詞" and token.part_of_speech()[2] == "人名":
                name = token.surface()
                if name in name_dict_nlp:
                    name_dict_nlp[name] += 1
                else:
                    name_dict_nlp[name] = 1

            # 假名名词
            if token.part_of_speech()[0] == "名詞" and token.part_of_speech()[2] != "人名":
                name = token.surface()
                # 且是片假名
                if not contains_japanese(name):
                    continue
                if len(name) < 2:
                    continue
                if name in zhuan_dict:
                    zhuan_dict[name] += 1
                else:
                    zhuan_dict[name] = 1

# Remove names with frequency less than threshold
name_dict_nlp = {k: v for k, v in name_dict_nlp.items() if v >= threshold}
zhuan_dict = {k: v for k, v in zhuan_dict.items() if v >= threshold}

# Sort by value
name_dict_nlp = dict(
    sorted(name_dict_nlp.items(), key=lambda item: item[1], reverse=True)
)
zhuan_dict = dict(sorted(zhuan_dict.items(), key=lambda item: item[1], reverse=True))
zhuan_list = [x for x in zhuan_dict.keys()]

with open("计数-人名表-nlp.json", "w", encoding="utf-8") as f:
    json.dump(name_dict_nlp, f, ensure_ascii=False, indent=4)
with open("计数-片假名词表-nlp.json", "w", encoding="utf-8") as f:
    json.dump(zhuan_dict, f, ensure_ascii=False, indent=4)
# 将名字及其出现次数写入CSV文件
with open("人名替换表.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["JP_Name", "CN_Name", "Count"])  # 写入表头
    for name, count in name_dict.items():
        writer.writerow([name, "", count])

han_list = batch_translate(zhuan_list, 50)
result_list = []
for i, text in enumerate(han_list):
    cut_result = thu1.cut(text, text=True)  # 进行一句话分词
    #print(cut_result)
    for flag in ["np", "ns", "nz", "_j", "_i", "_x"]:
        if flag in cut_result:
            result_list.append(f"{zhuan_list[i]}\t{text}")
            break

with open("结果-人名表-nlp.txt", "w", encoding="utf-8") as f:
    f.write("\n".join([x for x in name_dict_nlp.keys()]))

with open("结果-未知片假名表-nlp.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(result_list))


os.system("pause")
