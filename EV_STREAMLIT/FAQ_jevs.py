import requests
from bs4 import BeautifulSoup
import json
import time

# 시작 페이지 번호
page = 1

# 수집한 FAQ(질문/답변)를 누적 저장할 리스트
faq_list = []

# 저장할 파일명
file_name = "jevs_faq_final.json"

# 사이트가 1~2페이지만 있으므로 2페이지까지만 반복
while page <= 2:
    # 페이지 번호만 바꿔가며 URL 생성
    url = f"https://jejuevservice.com/echarger/?q=YToxOntzOjEyOiJrZXl3b3JkX3R5cGUiO3M6MzoiYWxsIjt9&page={page}"

    # 해당 페이지 HTML 요청
    response = requests.get(url)

    # HTML 텍스트 가져오기
    html = response.text

    # BeautifulSoup로 HTML 파싱 준비
    bs = BeautifulSoup(html, "html.parser")

    # 페이지의 모든 텍스트를 줄바꿈 기준으로 뽑아냄
    text = bs.get_text("\n", strip=True)

    # 줄 단위로 나누고, 빈 줄은 제거
    lines = [line for line in text.split("\n") if line.strip()]

    # 현재 처리 중인 질문(q)과 답변(a) 초기화
    q = None
    a = []

    # 지금이 "답변을 읽는 중인지" 표시하는 플래그
    # - A:를 만나면 True
    # - 다음 Q:를 만나면 False
    in_answer = False

    # Q: 또는 A: 표시가 다양한 경우를 대비해서 리스트로 준비
    # (사이트에 따라 'Q:' / 'Q :' / 'Q：' 처럼 들어갈 수 있음)
    Q = ["Q:", "Q :", "Q："]
    A = ["A:", "A :", "A："]

    # 줄을 하나씩 읽으면서 Q/A 구조를 찾아냄
    for line in lines:
        # 줄에 공백이 여러 개 있으면 하나로 줄여서 정리
        line = " ".join(line.split())

        # 이 줄이 질문(Q)인지 판단
        is_q = False
        for m in Q:
            # line이 Q마커(m)로 시작하면 질문으로 판단
            if line[:len(m)] == m:
                is_q = True
                break

        # 이 줄이 답변 시작(A)인지 판단
        is_a = False
        for m in A:
            # line이 A마커(m)로 시작하면 답변 시작으로 판단
            if line[:len(m)] == m:
                is_a = True
                break

        # 1) 질문 줄을 만난 경우
        if is_q == True:
            # 기존에 저장 중이던 q/a가 있으면 faq_list에 넣고 마무리
            if q is not None:
                if len(a) > 0:
                    faq_list.append({
                        "question": q,
                        "answer": "\n".join(a).strip(),
                    })

            # 현재 줄에서 Q: 마커를 떼고 실제 질문 문장만 q에 저장
            for m in Q:
                if line[:len(m)] == m:
                    q = line[len(m):].strip()
                    break

            # 새 질문을 시작했으니 답변 리스트 초기화
            a = []

            # 질문을 만났으니 답변 읽기 상태는 False로 초기화
            in_answer = False
            continue

        # 2) 답변 시작 줄(A:)을 만난 경우
        if is_a == True:
            # 이제부터는 답변을 읽는 중
            in_answer = True

            # A: 마커를 떼고 A: 뒤에 텍스트가 바로 있으면 답변 첫 줄로 추가
            for m in A:
                if line[:len(m)] == m:
                    rest = line[len(m):].strip()
                    if rest != "":
                        a.append(rest)
                    break
            continue

        # 3) 답변 영역(in_answer=True)에서 일반 텍스트 줄인 경우
        if in_answer == True:
            # 질문이 존재하는 상태에서만 답변 줄을 추가
            if q is not None:
                a.append(line)

    # 페이지 끝까지 읽었는데 마지막 q/a가 남아있으면 저장
    if q is not None:
        if len(a) > 0:
            faq_list.append({
                "question": q,
                "answer": "\n".join(a).strip(),
            })

    # 다음 페이지로 이동
    page += 1

    # 서버에 부담을 줄이기 위해 잠깐 쉬기(1초)
    time.sleep(1)

# 수집 완료 후 JSON 파일로 저장
with open(file_name, "w", encoding="utf-8") as f:
    json.dump(faq_list, f, ensure_ascii=False, indent=2)

print("저장 완료:", file_name)
