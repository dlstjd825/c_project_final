# 수정내역
엔터치는 방법 : 엔터치고싶은곳에서 공백 두 번 이상 입력하고 엔터치기 또는 `<br>` 태그 사용  
양식 복붙해서 써주세용~ㅎ  
가장 최근 수정 내역 위에다가 작성합시다

***
수정일 : 2024-12-01
수정인 : 정세은
- 프로필 사진 변경 화면 전환되면 반영 안되는 거 오류 해결함. 프로필 사진 변경 기능 구현 끝.

***
수정일 : 2024-11-30 수정인 : 임수빈
- HOBBYHIVE의 핵심 중 하나였던 태그 기능을 잊고 있었음..
- 클래스 생성 부분 수정 -> 태그도 입력받게 함.
- 검색 창에 단어 검색하면 해당 태그를 갖고 있는 클래스 뜨게 구현함 !!

***
수정일 : 2024-11-30
수정인 : 정세은
- 마이페이지 고객센터 전부 끝
- 프로필 변경 버튼 -> 프로필 사진 변경 으로 바꿈
- 현상황: 프로필 사진 변경 버튼 눌러 들어가서 변경하면, 프로필 사진 변경이 되는데, 그 페이지에서만 되고 다시 마이페이지로 돌아가거나 고객센터 들어가면 변경된 프로필 사진이 반영되지 않고, 기본 프로필 사진으로 다시 돌아감. 이 부분만 해결하면 프로필 사진 수정도 끝. 이게 마지막.

***
수정일 : 2024-11-29 수정인 : 임수빈
- 사진 안 뜨는 부분 해결(경로가 너무 꼬여있었음.)!!!!

***
수정일 : 2024-11-29
수정인 : 우재연
- user interface 완료
- community_detail.html

***
수정일 : 2024-11-29
수정인 : 정세은
- (이름)부분에 로그인한 user_id 반영되도록 하는 것 기능 구현 완료

***
수정일 : 2024-11-28
수정인 : 정세은
- 사이드바 마이페이지 누르면 마이페이지html로, 클래스 누르면 클래스html로 넘어가도록 함.
- 아이디 변경, 비밀번호 변경 구현 완료.
- 남은 것: 크게 보면 클래스 마이페이지로 끌어오는 것, (이름)부분에 로그인한 user_id 반영되도록 하는 것(하는중)

- 추가:
- 친절한 코드 빌드 방법 설명
- 
- 위의 코드를 실행하면 실행하고 있는 폴더와 동일한 폴더에 static 파일 하나가 생성됨.
- 새로 생성되는 static파일 속에는 빈 upload랑 user폴더가 있는데, 그 두 개 폴더 안에다가 넣지 말고 그냥 새로 생성된 static 폴더 안에다가 user.csv파일을 복붙해서 넣어야함.
- user.csv는 원래있던 static 파일 속에 넣어놨음. 경로로 설명하면 c_project/static/user.csv

- user.csv 파일을 옮긴 이후엔 sln 파일 빌드해서 파일 경로들 싹 바꿔줘야하는데, vscode에선 실행하는 법 모르겠고, visualstudio들어가서 c_project/C_function/C_fuction.sln 열면 안에 c파일들 있는거 보일거임.
- ctrl shift b 누르면 dll파일 다시 생성되서 경로 본인 컴퓨터로 바뀔거임.

- 다시 vscode로 넘어가서 app.py 실행하면 됨.

- 더해서 c언어 기능 작업하는 사람 있다면, c언어 파일 하나 수정할 때마다 vs가서 빌드 다시 해줘야 바뀐거 적용됨.
- 폴더명 바꾸더라도 다시 빌드해줘서 경로 바꿔줘야함.

***
수정일 : 2024-11-12 수정인 : 임수빈
- 사진이 안 뜸.... 해결 아직 못함.

***
수정일 : 2024-11-12
수정인 : 정인성
- 웹 실행에 불필요한 파일 제거 후 업로드
- 전제 html파일을 html, css, js파일로 분리

***
수정일 : 2024-11-10
수정인 : 정인성
- sign_up.html 파일 html, css, js로 분리
- C_function 파일에서 웹 실행에 불필요한 파일 제거

***
수정일 : 2024-11-09 수정인 : 임수빈
- 클래스 신청할 때 인원 저장해서 마감 되는 부분 구현함(마감되면 버튼 바뀌고 신청 안됨)

***
수정일 : 2024-11-09
수정인 : 정인성
- 웬만한거 다 구현 끗~

***
수정일 : 2024-11-08 수정인 : 임수빈
- 클래스 그리드 화면에 필요한 정보만 보이게 함.
- 구현한 기능 : 클래스 신청
- 신청 기능 자체는 구현 완료, 인원 차서 마감되는 부분 생각해봐야함.

***
수정일 : 2024-11-07 수정인 : 임수빈
- MinGW 설치 성공(비트 크기 문제였음)
- 클래스 UI 코드 받은 것 토대로 기능 구현 시작
- 서버 구현 전 -> csv로 우선 구현
- 구현한 기능 : 클래스 생성, 클래스 기본 화면에 생성된 클래스 그리드로 띄우기
- 멘토일 때만 생성 버튼 실행 가능하게 해야함(로그인 기능과 연결 안 돼서 우선 멘토임을 확인하는 간단한 코드만 만들어 놓음)

***
수정일 : 2024-11-06 수정인 : 임수빈
- 클래스 백엔드 시작 -> 지속적인 MinGW 설치 오류...

***
수정일 : 2024-11-06
수정인 : 정세은
- 마이페이지 UI 완료, 기능 구현 어려운 부분은 수정 필요
  
***
수정일 : 2024-11-04
수정인 : 정인성
- 90% 완료
- 회원가입 신청 버튼 오류 수정완료
- admin페이지에서 거절버튼 만들기
- 웹 다시 실행해도 admin페이지에 정보 남아있게 만들기
- 사람 많아질거 대비해서 로그인 할 때 해시나 이분탐색 쓰면 괜찮을듯,,

***
수정일 : 2024-10-29
수정인 : 우재연
- 70% 완료
- 커뮤니티, 클래스 구현 완료
- 클래스 및 커뮤니티 게시물 추가 관련 수정 필요 백엔드와 논의 후 방향 잡을 듯

***
수정일 : 2024-10-29
수정인 : 정인성
- 80% 완료
- 회원가입 신청 버튼 안 눌리는거 수정해야함 개같은거

***
수정일 : 2024-10-26  
수정인 : 정인성  
- 로그인 c로 구현 완료
- 로그인 <-> 회원가입 전환 다시 구현해야함

***
수정일 : 2024-10-05  
수정인 : 정인성  
- 로그인, 회원가입 ui 구현 완료  
- 로그인에서 회원가입으로, 회원가입에서 로그인으로 넘어가기 구현 완료  
- 회원가입에서 파일 업로드 구현 완료







