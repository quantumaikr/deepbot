import pickle
import json
import sys
import os

data_name = str(sys.argv[1])

if not os.path.exists("data"):
    os.makedirs("data")

data = []
for i in range(100):
    try:
        temp = pickle.load(
            open("collected_data/{}_chat_{}.pkl".format(data_name, i), "rb")
        )
    except:
        continue
    for topic in temp:
        x = temp[topic]
        x = x.split("[Human]")[1:-1]
        if len(x) != 0:
            s = ""
            for y in x:
                if "[AI]" in y:
                    y = y.split("[AI]")
                    if len(y) == 2:
                        s += (
                            "[|Human|] "
                            + y[0].strip()
                            + "\n"
                            + "[|AI|] "
                            + y[1].strip()
                            + "\n"
                        )
                    else:
                        break
                else:
                    break
            if s != "":
                prompt = "인간과 AI 어시스턴트 간의 대화입니다.\n"
                s = prompt + s + "[|Human|] "

                data.append({"topic": topic, "input": s})

print('data', len(data))
json.dump(data, open("data/{}_chat_data.json".format(data_name), "w"), ensure_ascii=False)
