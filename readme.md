공지사항 알림 (개인용)

서버컴에 설치할 내용
- venv : python3 -m venv venv
- schedule module : pip install schedule
- beautifulsoup4 : pip install beautifulsoup4
- requests : pip install requests
- dotenv : pip install python-dotenv

10분 간격으로 크롤링 후 오늘 날짜 공지 올라오면 메일로 보내기 (해당 게시글 url)

동일 게시글은 제목으로 판단

메일 보낼 주소는 그냥 하드코딩시키기 (연구실 몇 명 안 되니 DB 관리까지는 안 해도 됨)

잠깐 테스트해봤을 때 cpu, ram 크게 안 잡아먹어서 그냥 무한루프 계속 돌려도 됨