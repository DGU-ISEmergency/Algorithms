# 2024-1 동국대 산업시스템공학종합설계 10조

## 사용 언어
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> 

## 사용 기술
- **Optimization**
  - PSO algorithm
- **Simulation**
  - SUMO
  - TraCI
- **Data Analysis**
  - Pandas
  - Matplotlib
  - NumPy

## How to Optimize

1. **데이터 입력**
   - 최적화하고자 하는 교차로의 데이터 입력
      - 포화 교통류율
      - 도착 교통량
3. **최적화 실행**
    ```bash
    pso_algorithm.ipynb
    ```

   
## How to Simulate

1. **시뮬레이션 파일이 있는 폴더 이동**
    ```bash
    cd main\ project
    ```
2. **Simulation Configuration**
   - `runner.py` 파일에서 `run()` 함수의 `sig_change` 변수를 `True`/`False`로 설정.
   - 기존 신호 체계로 설정하려면 `True`, 자체 신호 체계로 설정하려면 `False`로 설정.

3. **시뮬레이션 실행**
    ```bash
    python runner.py
    ```

## 시뮬레이션 방법론

본 연구에서는 교통 신호 제어 시스템의 개선을 위해 긴급차량의 접근을 감지하고, 이에 따른 신호 변경 및 체계 변화를 설명하는 알고리즘을 제안한다. 아래는 본 연구의 절차를 설명하는 플로우 차트이다.



1. **시작**
   - 시스템 초기화, 모든 차량 ID를 확인.

2. **긴급차량 감지**
   - 모든 차량 ID를 확인한 후 긴급차량의 존재 여부를 감지.
   - 긴급차량이 감지되면 다음 단계로 이동.

3. **요구 녹색시간 계산**
   - 긴급차량의 접근을 기반으로 요구되는 녹색 신호 시간을 계산.

4. **초록불 변경 여부 결정**
   - 긴급차량의 접근에 따른 신호 변경이 필요한지 판단.
   - 신호 변경이 필요하면 다음 단계로 이동.

5. **초록불 변경**
   - 요구 녹색시간 동안 초록불을 유지하거나, 기존 신호 체계를 변경.

6. **응급차량 통과 이후, 자체 신호 체계 적용 여부 결정**
   - 파일 내 신호체계 변경 여부 설정 값 확인 (True/False).
   - 필요시 자체 신호체계를 적용하고, 그렇지 않으면 기존 신호체계를 유지.

7. **종료**
   - 모든 과정을 종료하고 초기 상태로 이동.

## 분석 방법론
- 기존 신호체계와 자체 신호체계 적용 환경에서 위 시뮬레이션을 각각 100번 반복
- 데이터 추출
- 데이터 분석 (`result.ipynb`)

## 시뮬레이션 gui 예시
<div align="center">
  <img src="https://github.com/DGU-ISEmergency/Algorithms/assets/112681633/7d76442f-1963-483d-8455-09bd3bef6b74"  width="600" height="300"/>
</div>


