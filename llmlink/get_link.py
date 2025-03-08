from openai import OpenAI
import json
from pathlib import Path
from llmlink import globals
from llmlink.untils import *
import sys
from .globals_set import link_settings_load
client = OpenAI(
    base_url=globals.link_settings['base_url'],
    api_key=globals.link_settings['api_key'],
)


def get_anwser_streamF(context_dict_list,user_input):
    context_dict_list.append({'role':'user','content':user_input})
    response = client.chat.completions.create(
      model=globals.link_settings['model'],
      messages=context_dict_list,
      stream=False,
      temperature=globals.link_settings['temperature'],
      top_p = globals.link_settings['top_p'],
      max_tokens= globals.link_settings['max_tokens'],
      presence_penalty=globals.link_settings['presence_penalty'],
      frequency_penalty=globals.link_settings['frequency_penalty'],
      n= globals.link_settings['n'],
    )

    assistant_message = response.choices[0].message
    # 将对象转换为字典格式，并添加到上下文列表
    context_dict_list.append({
        'role': assistant_message.role,
        'content': assistant_message.content
    })
    return context_dict_list

def get_anwser_streamT(context_dict_list,input_stringvar,scrool_text):
    user_input = input_stringvar.get()
    input_stringvar.set('')
    # 添加用户消息
    context_dict_list.append({'role':'user','content':user_input})

    # 发起流式请求
    response_stream = client.chat.completions.create(
        model=globals.link_settings['model'],
        messages=context_dict_list,
        stream=True,
        temperature=globals.link_settings['temperature'],
        top_p=globals.link_settings['top_p'],
        max_tokens=globals.link_settings['max_tokens'],
        presence_penalty=globals.link_settings['presence_penalty'],
        frequency_penalty=globals.link_settings['frequency_penalty'],
        n=globals.link_settings['n'],

    )

    # 处理流式响应
    full_response = ""
    for chunk in response_stream:
        if chunk.choices[0].delta.content is not None:
            delta = chunk.choices[0].delta.content
            stream_anwser_updata(scrool_text,delta)
            full_response += delta
    scrool_text.insert(END, '\n')
    scrool_text.see(END)
    full_response = full_response
    context_dict_list.append({'role':'assistant','content':full_response})
    return context_dict_list

def translate_segment(segment,glossary,segment_before=''):

    #构造提交字典
    glossary_text = "\n".join([f"{k} : {v}" for k, v in glossary.items()]) #构造对照表文本

    # 构造提示：
    prompt = (
        "【任务指令】\n"
        "1. 请精准识别<JA></JA>标记内的日文内容进行翻译,记住所有内容都不论如何必须要翻译\n"
        "2. 输出格式必须严格遵循：\n"
        "   - 翻译后的中文（保留所有原始格式）\n"
        "   - 标签中的内容，和判断是否翻译的原因\n"
        "   - 分隔符 ===GLOSSARY_UPDATES===\n"
        "   - 新增术语的JSON列表（若无更新则省略该部分）\n\n"

        "【处理规则】\n"
        "• 格式保留：完全保留换行符、空格、标点及特殊符号\n"
        "• 术语处理：\n"
        "   a) 优先使用现有对照表（见下方）\n"
        "   b) 新术语需经上下文验证后添加\n"
        "   c) 请勿输出待翻译文本和术语词典之外的内容\n"
        "   d) 人名/地名需符合官方译名规范\n\n"

        "【术语禁区】\n"
        "以下术语禁止修改（已确认翻译）：\n"
        f"{glossary_text}\n\n"

        "【上下文参考】\n"
        "上文内容（仅辅助理解，无需处理）：\n"
        f"{segment_before}\n\n"

        "【待译内容】\n"
        "<JA>\n"
        f"{segment}\n"
        "</JA>\n\n"

        "【输出示例】\n"
        " Translated text here...\n"
        "保持相同的换行格式\n\n"
        "===GLOSSARY_UPDATES===\n"
        '{"Glossary Updates": [{"original": "東京", "translation": "东京"}]}'
    )
    system_prompt = (
        "你是一个严谨的本地化专家，专门处理中日文档翻译。"
        "你的核心能力：\n"
        "1. 精准识别需要翻译的片段\n"
        "2. 绝对保留原始排版格式\n"
        "3. 专业术语的一致性管理\n"
        "4. 只输出待翻译文本和术语词典\n"
        "5. 严格遵守输出格式要求\n\n"

        "禁止行为：\n"
        "- 添加任何解释性内容\n"
        "- 修改未标记的文本\n"
        "- 自行发明新的翻译格式\n"
        "- <JA></JA>标记内有日语部分没有被翻译,即使它是敬语等需要考虑上下文环境的内容\n"
        "- 翻译任何非<JA></JA>标签内的部分，包括标签本身\n"
        "- 输出非请求的额外信息"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
      model=globals.link_settings['model'],
      messages=messages,
      stream=False,
      temperature=0,
      top_p = 0.8,
      max_tokens= globals.link_settings['max_tokens'],
      presence_penalty=0,
      frequency_penalty=0.1,
      n= globals.link_settings['n'],
    )

    return response.choices[0].message.content

def translate_txt(txt_path,max_chars,glossary_path=None,output_path=None):
    txt_path = Path(txt_path)
    txt_stem = txt_path.stem

    if output_path is None:
        output_path = Path(__file__).parent.parent / (txt_stem + '_translated.txt')
    if glossary_path is None:
        glossary_path = Path(__file__).parent.parent / (txt_stem +'_glossary.txt')
    else:
        glossary_path = Path(glossary_path)

    segments = split_text(txt_path,max_chars)
    glossary = load_translation_glossary(glossary_path)

    # 复制一份对照表用于更新
    updated_glossary = glossary.copy()
    translated_segments = []
    segment_before = ''#参考用的前文

    print('开始翻译')
    for idx, segment in enumerate(segments):
        result = translate_segment(segment, updated_glossary,segment_before)
        translated_result,glossary_result = separate_translation_and_glossary(result)

        translation_text = translated_result  # 此处直接使用返回内容
        updates = parse_glossary_update(glossary_result)

        # 更新本地对照表：新增或修改已有条目
        for entry in updates:
            original = entry.get("original")
            translation = entry.get("translation")
            if original and translation:
                updated_glossary[original] = translation

        translated_segments.append(translation_text)
    # 将最终翻译结果写入文件
    output_path = Path(output_path)
    with output_path.open('w',encoding="utf-8") as f:
        for seg in translated_segments:
            #f.write(seg + "\n\n")
            f.write(seg)
    # 保存更新后的对照表到 glossary.txt 文件中
    with glossary_path.open('w',encoding="utf-8") as f:
        for k, v in updated_glossary.items():
            f.write(f"{k}: {v}\n")
    print("所有翻译完成，对照表已更新。")



