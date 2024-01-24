# GalTransl_Name_Detector

这是一个Python脚本，用于处理包含日文文本的JSON文件。它使用自然语言处理（NLP）技术从文本中提取名字和其他名词，计算它们的出现次数，并将它们翻译成中文。

## 如何使用

1. 确保你的Python环境中已经安装了所有必要的库，包括`os`、`json`、`csv`、`sudachipy`、`caiyun`和`thulac`。

2. 运行脚本。当提示输入json_jp文件夹时，输入包含要处理的JSON文件的文件夹的名称。当提示输入阈值时，输入名字出现次数的阈值。如果不输入阈值，将默认为10。

3. 脚本将处理指定文件夹中的每个JSON文件，提取名字和其他名词，计算它们的出现次数，并将它们翻译成中文。

4. 脚本将生成以下输出文件：

   - `计数-人名表-nlp.json`：一个包含名字及其出现次数的JSON文件。
   - `计数-片假名词表-nlp.json`：一个包含其他名词及其出现次数的JSON文件。
   - `人名替换表.csv`：一个包含名字及其出现次数的CSV文件。
   - `结果-人名表-nlp.txt`：一个包含从文本中提取的名字的文本文件。
   - `结果-未知片假名表-nlp.txt`：一个包含翻译后的名字和其他名词的文本文件。

5. 查看生成的输出文件，以获取提取和翻译的结果。