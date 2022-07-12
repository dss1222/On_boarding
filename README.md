# On_boarding
신입 온보딩

신입으로 입사하여 공부하는 레포

# 스팩

- 회원 (중요한 부분은 아니므로 약식으로 구현할것)
    - 회원가입
    - 로그인
    - 내 정보 수정
- 게시판
    - 게시판 목록
    - 게시판 생성
    - 이름 수정
    - 삭제
    - 게시글
        - 글쓰기
        - 수정
        - 읽기
        - 태그
        - 공지
        - 댓글, 대댓글
        - 글, 댓글, 대댓글 좋아요
        - 검색
- 메인페이지
    - 좋아요 많은 글 10개
    - 댓글 많은 글 10개
    - 최신 글 10개
- 마이페이지
    - 내가 쓴 글
    - 내가 쓴 댓글
    - 내가 좋아요한글

# 필수 기술 스택

- Flask
- Flask-classful
- mashmallow
- MongoEngine

# 패키지 매니져

- Poetry

# 소스코드 관리

- 개인 github



<br />
<br />
<br />

---

### 특이사항
- 테스트 코드 미구현 (구현 예정)
- 좋아요, 댓글 갯수를 배열의 size를 가져오는 것이 아닌, 댓글 작성, 좋아요 누를때마다 해당 cnt가 증가or감소하여 해당 컬럼의 갯수를 가지고 정렬을 함
  - 이유 : 쿼리 작성 미숙, 추 후 수정 예정
- 검색 기능 : 태그 검색만 구현, 게시글의 제목이나 내용 게시판의 제목등은 태그 검색과 동일한 기능이기때문에 구현하지 않음
  - 태그 검색 : contains를 사용하여 like %검색어% 와 동일한 기능
- 이해한 내용 간단하게 요약 <정확하지 않습니다. 틀렸다면 알려주세요!> :
  - flask-classful : view를 구현할 때 전체 view를 하나의 class view로 묶어 관리하기 편하게 만들어줌
  - marshmallow : 데이터의 정보를 보기 쉽게 가공하여 사용(spring 의 dto와 비슷)
  - mongoengine : orm처럼 db접근을 쉽게 함 또한 mongodb는 nosql인데 mongoengine을 이용하여 rdbms처럼 비슷하게 사용할 수 있음
  
 
 <br />
 <br />
 
 # API
 
<details>
<summary>펼치기</summary>
작성중 ...
<div>

|종류|분류|uri|비고|
|:-: |:-: |:-: |:- |
|회원 관련|회원가입|/users/signup, POST|{<br />"username" : "아이디",<br />"password" : "비밀번호" <br />}|
|회원 관련|로그인|/users/login, POST|{<br />"username" : "아이디",<br />"password" : "비밀번호" <br />}|
|회원 관련|내가 쓴 글 조회|/users/mypage/posts, GET||
|회원 관련|내가 쓴 댓글 조회|/users/mypage/comments, GET||
|회원 관련|내가 좋아요한 글 조회|/users/mypage/posts/likes, GET||
|회원 관련|정보 수정|/users/update, PATCH|{<br />"username" : "아이디",<br />}|
|||||
|게시판 관련|게시판 작성|/boards, POST|{<br />"name" : "보드 이름",<br />}|
|||||
|게시글 관련|게시글 작성|/boards/<board_id>/posts, POST|{<br />"title" : "게시글 이름",<br />"content" : "게시글 내용",<br />"tag" : "태그 내용"<br />}|
|게시글 관련|게시글 자세히 보기|/boards/<board_id>/posts/<post_id>, GET||   
|게시글 관련|게시글 최신순 10개 보기|/boards/<board_id>/posts/order/created, GET||   
|게시글 관련|게시글 댓글 많은 순 10개 보기|/boards/<board_id>/posts/order/comments, GET||  
|게시글 관련|게시글 좋아요 많은 순 10개 보기|/boards/<board_id>/posts/order/likes, GET||  
|게시글 관련|게시글 좋아요|/boards/<board_id>/posts/<post_id>/likes, POST|| 
|게시글 관련|게시글 태그 검색|/boards/<board_id>/posts/search/검색어, GET||  
|게시글 관련|게시글 수정|/boards/<board_id>/posts/<post_id>, PATCH|{<br />"title" : "게시글 이름",<br />"content" : "게시글 내용",<br />"tag" : "태그 내용"<br />}|
|게시글 관련|게시글 삭제|/boards/<board_id>/posts/<post_id>, DELETE|| 
|||||
</div>
</details>
