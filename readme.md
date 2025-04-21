# 🗳 대한민국 대선 후보 정보 플랫폼

## 📖 프로젝트 소개
- 이 프로젝트는 대한민국 대선 후보들의 공약 및 논란사항 등 투표 과정에서 필요한 정보를 손쉽게 제공하기 위한 비영리 목적으로 개발되었습니다.
- 사용자의 정치색과 무관하게 중립적인 정보 제공을 목표로 합니다.

## 🛠 기능
- 정당 및 후보에 대한 상세 정보 조회
- 후보별 공약 및 논란사항 확인
- 전체 후보 통합 질의응답 시스템

## ▶️ 실행 방법
### ▶️ 웹사이트 접속
- 공식 링크: [https://대선은지금.com](https://대선은지금.com)
- 대한민국 제21 대통령선거를 위해 한시적으로 운영됩니다. 

### 🖥️ 로컬 실행
```bash
git clone https://github.com/minsuchae/politics-app.git
cd politics-app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### 🖥️ 로컬 실행(docker 기반)
```bash
git clone https://github.com/minsuchae/politics-app.git politics-app
cd politics-app
cp docker.env.sample docker.env
vi docker.env
sudo docker build -t politics_app .
sudo docker create --restart always --name politics_app_container -p 5000:5000 --env-file docker.env politics_app
sudo docker start politics_app_container
```
## 🤝 기여 & 문의
- 한 사람에 의해 해당 프로젝트가 관리하고 있으며, 주업무가 아니기 때문에 요청 사항에 대해 빠른 반응이 어려울 수 있습니다.
- 모든 기여와 문의는 환영하며, 가능한 한 빨리 답변드리도록 하겠습니다.
- 프로젝트 문의 및 기여는 GitHub 이슈 또는 Pull Request를 통해 할 수 있습니다.
- 2025년 대통령 대선까지 주요한 버그 수정 외에 추가기능 PR은 후순위에 밀립니다.
- 인공지능을 활용하여 빠르게 만들다보니 테스트코드가 없으며 수기로 테스트하였습니다.

## 📚 기술 스택
- Flask
- HTML/CSS
- JavaScript

## 📁 프로젝트 구조

```bash
politics_app/
├── app.py                     # Flask 앱의 진입점
├── data/
│   ├── sample_data.json       # 정당 및 후보자 JSON 데이터
│   └── data_loader.py         # 데이터 로딩 및 전역 공유 모듈
├── route/                     # Flask 라우트 정의
│   ├── index.py               # 메인 페이지
│   ├── party_detail.py        # 정당 상세 정보
│   ├── candidate_detail.py    # 후보 상세 정보
│   └── ask_candidate.py       # LLM 기반 질의응답 처리
├── templates/                 # Jinja2 템플릿
│   ├── base.html
│   ├── index.html
│   ├── party_detail.html
│   └── candidate_detail.html
├── static/
│   └── css/
│       └── style.css          # LLM 로딩 애니메이션 CSS
├── requirements.txt
└── README.md
```

## ⚠️ 주의사항
- 정당 및 후보 관련 정보는 중앙선거관리위원회의 제21대 대통령선거 정당 정책을 확인하여 업데이트됩니다.
- 정보 수정 및 삭제 요청은 선거의 공정성을 위해 잘못된 정보에 한해서만 반영됩니다.
- 대통령 후보자 및 선거캠프 관련자분들께서는 보시기 불편하더라도 양해부탁드립니다.
- AI 답변은 LLM 모델의 환각증상으로 인해 잘못된 내용이 나올 수 있습니다.

## 💰 서버 비용 및 지원
- LLM 답변 퀄리티를 우선시할 경우 Google Gemma3-27b-it 모델이 적합하지만, 서버 운영 비용을 고려하여  Gemma3-1b-it 모델로 운영하고 있습니다.
- Gemma3-27b-it 모델로 서버 운영 시 최소 운영 비용은 월 60만원이상입니다. 클라우드 리소스나 크레딧을 지원할 수 있는 기관 및 업체의 협조를 환영합니다.
