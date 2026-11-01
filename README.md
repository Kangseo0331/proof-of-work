# Blockchain Application assignment1


해시 체인 기반 proof-of-work 채굴 실험 코드와 결과

## 1. 환경 및 하드웨어

| 항목 | 내용 |
|---|---|
| OS | macOS sequoia 15.3.1 |
| CPU | M4 |
| 메모리 | 16GB |
| Python | 3.13.2 |

모든 실험(Part 1, 보정, Part 2)은 위와 동일한 컴퓨터에서 실행했습니다.

## 2. 의존성

- Python 3.13.2
- 표준 라이브러리: `hashlib`, `time`, `csv`, `statistics`, `copy`
- 외부 패키지: `matplotlib` (그래프 출력용)

```bash
pip install matplotlib
```

## 3. 실행 방법

```bash
python part1_1.py      # 목표값 2^252, 2^248, 2^244, 2^240, 2^236 실험 -> part1_1.csv
python part1_2.py      # 목표값 T* 실험 -> part1_1.csv

python part2.py      # 보정된 목표값 T* 실험 (5회) -> part2.csv
python plot.py       # part1.csv로 평균 채굴 시간 그래프 및 r, T* 계산
```

파일 이름은 제출한 zip 안의 실제 이름에 맞춰 수정하세요.

## 4. 블록 인코딩

각 블록의 해시 입력은 다음과 같이 만듭니다.

```python
data = f"{prev_hash}{payload}{nonce}".encode("utf-8")
H = int.from_bytes(hashlib.sha256(data).digest(), "big")
```

- `prev_hash`: 이전 블록의 `sha256(...).digest()` 결과(bytes). f-string으로 문자열화되어 들어갑니다. 제네시스 블록은 정수 `0`.
- `payload`: 블록 번호(정수).
- `nonce`: 0부터 1씩 증가하는 정수.
- 해시 함수: SHA-256 (한 번만 적용, double SHA-256 아님).
- 해시 결과 32바이트를 big-endian 부호 없는 정수로 변환합니다.
- 채굴 성공 조건: `H < T` (T는 목표값).
- 보정과 Part 2에서도 동일한 인코딩을 사용했습니다.

## 5. 실험 설정

- Part 1: 목표값 `T = 2^e`, `e in {252, 248, 244, 240, 236}`. 각 목표값마다 제네시스 블록 뒤로 9개 블록을 채굴하고 블록별 시간을 `time.perf_counter()`로 측정합니다.
- 보정: 총 해시 시도 횟수를 총 실행 시간(초)으로 나눠 해시율 `r`을 추정하고, `T* = 2^256 / (60 r)` (정수)로 목표값을 정했습니다.
- Part 2: `T*`로 5회 새로 채굴합니다. 시행당 최대 5분이며, 초과 시 미완료로 기록하고 제외하지 않습니다.


## 6. 파일 구성


part1_1.py   part1_1.csv
part1_2.py   part1_2.csv
part2.py    part2.csv
drawPlot.py
README.md
