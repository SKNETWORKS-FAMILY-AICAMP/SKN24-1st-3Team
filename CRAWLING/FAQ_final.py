import requests
from bs4 import BeautifulSoup
import json
import time

page = 1

faq_list = []

file_name = "aea_faq_final.json"

while True:
    # 현재 페이지 URL (category=27 고정, pageIndex만 증가)
    url = f"https://www.aea.or.kr/help/faq.do?pageIndex={page}&category=27"

    response = requests.get(url)

    html = response.text

    bs = BeautifulSoup(html, "html.parser")

    text = bs.get_text("\n", strip=True)

    lines = [line for line in text.split("\n") if line.strip()]

    found = 0

    q = None
    a = []

    for line in lines:
        line = " ".join(line.split())

        # AEA 사이트 질문이 [OO 관련] ... 형태라서[ / 관련 / ] 전부 포함되었을 경우로 함
        ev_question = False
        if "[" in line:
            if "관련" in line:
                if "]" in line:
                    ev_question = True


        if ev_question == True:
            # 이전 질문(q)과 답변(a)이 있으면 먼저 저장하고 마무리
            if q is not None:
                if len(a) > 0:
                    faq_list.append({
                        "question": q,
                        "answer": "\n".join(a).strip(),
                    })
                    found += 1  

            q = line

            a = []
            continue


        # AEA 답변은 보통 '▶' 기호 뒤에 답변 문장이 나오는 형태가 많아서 '▶'가 있으면 그 뒤를 답변으로 저장
        if "▶" in line:
            if q is not None:
                # "▶" 기준으로 한 번만 나눠서 뒤쪽만 답변에 추가
                a.append(line.split("▶", 1)[1].strip())
        else:
            # '▶'가 없어도 답변 본문이 이어지는 경우가 있어서 추가로 붙여줌
            if q is not None:
                # (답변을 한 줄도 못 모은 상태면) 무의미한 줄이 섞일 수 있어서
                # 답변이 이미 시작된 경우(len(a)>0)만 계속 붙이도록 제한
                if len(a) > 0:
                    a.append(line)


    if q is not None:
        if len(a) > 0:
            faq_list.append({
                "question": q,
                "answer": "\n".join(a).strip(),
            })
            found += 1


    if found == 0:
        break

    # 다음 페이지로 이동
    page += 1

    time.sleep(1)

with open(file_name, "w", encoding="utf-8") as f:
    json.dump(faq_list, f, ensure_ascii=False, indent=2)

print("총 수집 개수:", len(faq_list))
print("저장 완료:", file_name)
