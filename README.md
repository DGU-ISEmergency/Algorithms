<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2024-1 동국대 산업시스템공학종합설계 10조</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
        }
        h1, h2, h3, h4 {
            margin-top: 20px;
            margin-bottom: 10px;
        }
        .team-table {
            margin-top: 20px;
        }
        .badge-python {
            margin-top: 10px;
        }
        .img-fluid {
            margin-top: 20px;
        }
    </style>
</head>
<body>

    <div class="container">
        <h1 class="text-center">2024-1 동국대 산업시스템공학종합설계 10조</h1>
        
        <h2>Team Members</h2>
        <table class="table table-bordered team-table">
            <thead>
                <tr>
                    <th>이름</th>
                    <th>학번</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>김태경</td>
                    <td>2021112387</td>
                </tr>
                <tr>
                    <td>류채린</td>
                    <td>2021112385</td>
                </tr>
                <tr>
                    <td>심차현</td>
                    <td>2021112413</td>
                </tr>
                <tr>
                    <td>이상준</td>
                    <td>2019112445</td>
                </tr>
                <tr>
                    <td>주예서</td>
                    <td>2021112443</td>
                </tr>
            </tbody>
        </table>

        <h2>Team Subject</h2>
        <p><strong>교통 혼잡 최소화를 위한 긴급차량 우선신호 시스템 상의 신호 회복주기 최적화 : 강남 테헤란로를 중심으로</strong></p>

        <h2>사용 언어</h2>
        <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge" class="badge-python">

        <h2>사용 기술</h2>
        <ul>
            <li><strong>Optimization</strong>
                <ul>
                    <li>PSO algorithm</li>
                </ul>
            </li>
            <li><strong>Simulation</strong>
                <ul>
                    <li>SUMO</li>
                    <li>TraCI</li>
                </ul>
            </li>
            <li><strong>Data Analysis</strong>
                <ul>
                    <li>Pandas</li>
                    <li>Matplotlib</li>
                    <li>NumPy</li>
                </ul>
            </li>
        </ul>

        <h2>How to Simulate</h2>
        <h3>1. 시뮬레이션 파일이 있는 폴더 이동</h3>
        <pre><code>cd main\ project</code></pre>

        <h3>2. Simulation Configuration</h3>
        <p><code>runner.py</code> 파일에서 <code>run()</code> 함수의 <code>sig_change</code> 변수를 <code>True</code>/ <code>False</code>로 설정.</p>
        <p>기존 신호 체계로 설정하려면 <code>True</code>, 자체 신호 체계로 설정하려면 <code>False</code>로 설정.</p>

        <h3>3. 시뮬레이션 실행</h3>
        <pre><code>python runner.py</code></pre>

        <h2>시뮬레이션 방법론</h2>
        <p>본 연구에서는 교통 신호 제어 시스템의 개선을 위해 긴급차량의 접근을 감지하고, 이에 따른 신호 변경 및 체계 변화를 설명하는 알고리즘을 제안한다. 아래는 본 연구의 절차를 설명하는 플로우 차트이다.</p>

        <ol>
            <li><strong>시작</strong>
                <ul>
                    <li>시스템 초기화, 모든 차량 ID를 확인.</li>
                </ul>
            </li>
            <li><strong>긴급차량 감지</strong>
                <ul>
                    <li>모든 차량 ID를 확인한 후 긴급차량의 존재 여부를 감지.</li>
                    <li>긴급차량이 감지되면 다음 단계로 이동.</li>
                </ul>
            </li>
            <li><strong>요구 녹색시간 계산</strong>
                <ul>
                    <li>긴급차량의 접근을 기반으로 요구되는 녹색 신호 시간을 계산.</li>
                </ul>
            </li>
            <li><strong>초록불 변경 여부 결정</strong>
                <ul>
                    <li>긴급차량의 접근에 따른 신호 변경이 필요한지 판단.</li>
                    <li>신호 변경이 필요하면 다음 단계로 이동.</li>
                </ul>
            </li>
            <li><strong>초록불 변경</strong>
                <ul>
                    <li>요구 녹색시간 동안 초록불을 유지하거나, 기존 신호 체계를 변경.</li>
                </ul>
            </li>
            <li><strong>응급차량 통과 이후, 자체 신호 체계 적용 여부 결정</strong>
                <ul>
                    <li>파일 내 신호체계 변경 여부 설정 값 확인 (True/False).</li>
                    <li>필요시 자체 신호체계를 적용하고, 그렇지 않으면 기존 신호체계를 유지.</li>
                </ul>
            </li>
            <li><strong>종료</strong>
                <ul>
                    <li>모든 과정을 종료하고 초기 상태로 이동.</li>
                </ul>
            </li>
        </ol>

        <h2>분석 방법론</h2>
        <ul>
            <li>기존 신호체계와 자체 신호체계 적용 환경에서 위 시뮬레이션을 각각 100번 반복</li>
            <li>데이터 추출</li>
            <li>데이터 분석 (<code>result.ipynb</code>)</li>
        </ul>

        <h2>시뮬레이션 gui 예시</h2>
        <div class="text-center">
            <img src="https://github.com/DGU-ISEmergency/Algorithms/assets/112681633/7d76442f-1963-483d-8455-09bd3bef6b74" class="img-fluid" alt="Simulation GUI">
        </div>
    </div>

    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
