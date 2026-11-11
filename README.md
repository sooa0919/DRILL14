# 새 떼 비행 애니메이션

`python main.py`로 실행합니다. Python과 `pico2d`, `PySDL2`, `transitions`가 필요합니다.
방향키로 소년을 이동하고 Space로 공을 발사하며 Esc로 종료합니다.

## 개발 계획

기존 `game_framework`의 시간 정보와 `game_world`의 갱신·그리기 구조를 사용합니다.
`bird_animation.png`에서 14개의 동작을 읽어 새 10마리의 날갯짓을 표현하고,
화면 경계에서 반사하여 좌우 왕복 비행을 반복하도록 단계적으로 구현합니다.
