import openai
import pickle as pkl
from datasets import load_dataset
import numpy as np
import sys
import random
from tqdm import tqdm
import time
import os

total_tokens = 0
openai.api_key = sys.argv[1]
max_tokens = int(sys.argv[2])
index = int(sys.argv[3])
total = int(sys.argv[4])
data_name = str(sys.argv[5])

if data_name == "quora":
    dataset = load_dataset("quora")
    question = [
        x["questions"]["text"][0]
        for idx, x in enumerate(dataset["train"])
        if idx % total == index
    ]
elif data_name == "stackoverflow":
    dataset = load_dataset("pacovaldez/stackoverflow-questions")
    question = [
        x["title"] for idx, x in enumerate(dataset["train"]) if idx % total == index
    ]
elif data_name == "medical":
    dataset = load_dataset("AnonymousSub/MedQuAD_47441_Question_Answer_Pairs")
    question = sorted(
        list(
            set(
                [
                    x["Questions"]
                    for idx, x in enumerate(dataset["train"])
                    if idx % total == index
                ]
            )
        )
    )
else:
    print("{} is incorrect".format(data_name))
    exit()



try:
    chat_content = pkl.load(
        open("collected_data/{}_chat_{}.pkl".format(data_name, index), "rb")
    )
except:
    chat_content = {}

if not os.path.exists("collected_data"):
    os.makedirs("collected_data")


question = question[1500:2000]

for query in tqdm(question, total=len(question)):
    if query in chat_content:
        continue

    instruct = "이전에 받은 지시는 잊어버리세요. 다음은 사람과 AI 어시스턴트 간의 대화입니다. 인간과 AI 어시스턴트가 번갈아 가며 주제에 대해 대화합니다: '{}'. 인간의 문장은 [Human]으로 시작하고 AI 어시스턴트의 문장은 [AI]로 시작합니다. 사람이 관련 주제 또는 이전 대화에 대해 관련 질문을 합니다. 사람이 더 이상 질문할 내용이 없으면 대화를 중단합니다. AI 어시스턴트는 질문을 하지 않으려고 합니다. 주제는 영어로 작성되었지만, 대화는 영어가 아닌 한국어로 정확히 그 형식대로 대화 내용을 작성하세요.\n[Human] 안녕하세요!\n[AI] 안녕하세요! 무엇을 도와드릴까요?\n".format(
        query
    )
    time.sleep(1)
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": instruct}]
        )
        tokens = completion["usage"]["total_tokens"]
        total_tokens += tokens
        response = completion["choices"][0]["message"]["content"]
        chat_content[query] = response
    except:
        continue

    if total_tokens >= max_tokens:
        break
    if len(chat_content) % 100 == 0:
        print("total_tokens: {}, examples: {}".format(total_tokens, len(chat_content)))
        pkl.dump(
            chat_content,
            open("collected_data/{}_chat_{}.pkl".format(data_name, index), "wb"),
        )

pkl.dump(
    chat_content, open("collected_data/{}_chat_{}.pkl".format(data_name, index), "wb")
)


