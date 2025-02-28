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
        "请将下面的文本中的日文部分翻译成中文，要求仅输出翻译后的文本，"
        "严格保留原文格式（包括换行、空格等）。\n"
        "请同时检查文本中的专有名词（如人名、地名），并维护一个翻译对照表。"
        "如果发现新的专有名词翻译，请在翻译完成后，输出一个 JSON 格式的 'Glossary Updates' 部分，"
        "格式为：\n"
        '{"Glossary Updates": [{"original": "原词", "translation": "译词"}, ...]}\n\n'
        "在输出'Glossary Updates' 部分之前，你需要输出'===GLOSSARY_UPDATES==='在翻译文本和它之间，作为分隔符"
        "请不要输出我给你的,除了待翻译文本的翻译之外的内容！"
        "【翻译对照表】\n"
        f"{glossary_text}\n\n"
        '【参考语境用的上文,不需要翻译】\n'
        f"{segment_before}"
        "【待翻译文本】\n"
        f"{segment}"
    )
    messages = [
        {"role": "system", "content": "你是一名专业的翻译专家，请严格按照要求翻译文本，并在翻译完成后提供对照表更新。"},
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
    if output_path is None:
        output_path = Path(__file__).parent.parent / 'translated.txt'
    if glossary_path is None:
        glossary_path = Path(__file__).parent.parent / 'glossary.txt'
    else:
        glossary_path = Path(glossary_path)
    txt_path = Path(txt_path)
    segments = split_text(txt_path,max_chars)
    glossary = load_translation_glossary(glossary_path)

    # 复制一份对照表用于更新
    updated_glossary = glossary.copy()
    translated_segments = []
    segment_before = ''#参考用的前文

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
            f.write(seg + "\n\n")
    # 保存更新后的对照表到 glossary.txt 文件中
    with glossary_path.open('w',encoding="utf-8") as f:
        for k, v in updated_glossary.items():
            f.write(f"{k}: {v}\n")
    print("所有翻译完成，对照表已更新。")



