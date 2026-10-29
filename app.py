import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="추억의 한국식 라면가게 🍜",
    page_icon="🍜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 게임 HTML/CSS/JS 코드 정의
game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>슈의 한국식 라면가게</title>
    <style>
        * {
            box-sizing: border-box;
            user-select: none;
            -webkit-user-select: none;
            font-family: 'Comic Sans MS', 'Gothic A1', sans-serif, cursive;
        }
        body {
            margin: 0;
            padding: 10px;
            background-color: #ffeff5;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        #game-container {
            position: relative;
            width: 900px;
            height: 680px;
            background: linear-gradient(135deg, #ffd1dc 0%, #ffe4e1 100%);
            border: 8px solid #ff69b4;
            border-radius: 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        /* 헤더 영역 */
        #header {
            position: absolute;
            top: 10px;
            left: 20px;
            right: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 10;
        }
        .title-banner {
            background: #ff3366;
            color: white;
            padding: 8px 20px;
            border-radius: 25px;
            font-size: 22px;
            font-weight: bold;
            box-shadow: 3px 3px 0px #b3003b;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }
        .timer-box, .score-box {
            background: #fff;
            border: 3px solid #ff69b4;
            padding: 6px 15px;
            border-radius: 15px;
            font-size: 18px;
            font-weight: bold;
            color: #d8004e;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        }

        /* 한국식 분식집 배경 decoration */
        .korean-deco {
            position: absolute;
            top: 70px;
            left: 20px;
            background: rgba(255, 255, 255, 0.85);
            border: 2px dashed #ff69b4;
            border-radius: 10px;
            padding: 8px 12px;
            font-size: 14px;
            color: #444;
            font-weight: bold;
        }
        
        /* 라면 모양 말랑이 장식 */
        .squishy-ramen {
            position: absolute;
            top: 75px;
            right: 25px;
            width: 75px;
            height: 75px;
            background: #ffe066;
            border: 4px solid #fcc419;
            border-radius: 50%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            box-shadow: 0 5px 15px rgba(0,0,0,0.15);
            transition: transform 0.1s ease;
            z-index: 12;
        }
        .squishy-ramen:active {
            transform: scale(0.85) rotate(-5deg);
        }
        .squishy-tag {
            position: absolute;
            top: 155px;
            right: 20px;
            font-size: 11px;
            background: #ff69b4;
            color: white;
            padding: 2px 6px;
            border-radius: 8px;
        }

        /* 주방 테이블 & 조리대 */
        #kitchen-table {
            position: absolute;
            bottom: 0;
            width: 100%;
            height: 510px;
            background: #f7d6b5;
            border-top: 10px solid #e0a96d;
        }

        /* 수도꼭지 & 밸브 */
        #faucet-zone {
            position: absolute;
            top: 40px;
            left: 120px;
            width: 100px;
            height: 120px;
        }
        #faucet-pipe {
            position: absolute;
            top: 0;
            left: 35px;
            width: 20px;
            height: 70px;
            background: #b0bec5;
            border: 3px solid #607d8b;
            border-radius: 10px 10px 0 0;
        }
        #faucet-head {
            position: absolute;
            top: 60px;
            left: 25px;
            width: 40px;
            height: 20px;
            background: #78909c;
            border: 3px solid #455a64;
            border-radius: 5px;
        }
        #valve-btn {
            position: absolute;
            top: 20px;
            left: 60px;
            width: 42px;
            height: 42px;
            background: #ff4757;
            border: 3px solid #b21f2d;
            border-radius: 50%;
            cursor: pointer;
            box-shadow: 0 4px 0 #b21f2d;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
            font-size: 11px;
            font-weight: bold;
            transition: all 0.1s;
        }
        #valve-btn:active {
            transform: translateY(3px);
            box-shadow: 0 1px 0 #b21f2d;
        }
        .water-stream {
            position: absolute;
            top: 80px;
            left: 40px;
            width: 10px;
            height: 0px;
            background: rgba(64, 196, 255, 0.7);
            border-radius: 0 0 5px 5px;
            transition: height 0.3s;
        }

        /* 양은냄비 및 가스레인지 */
        #stove-area {
            position: absolute;
            top: 150px;
            left: 280px;
            width: 340px;
            height: 280px;
            background: #cfd8dc;
            border: 5px solid #90a4ae;
            border-radius: 15px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        #pot {
            position: relative;
            width: 240px;
            height: 150px;
            background: linear-gradient(135deg, #ffd700 0%, #e6b800 100%);
            border: 6px solid #b8860b;
            border-radius: 0 0 80px 80px;
            box-shadow: inset 0 5px 15px rgba(0,0,0,0.2), 0 8px 15px rgba(0,0,0,0.15);
            overflow: hidden;
            transition: transform 0.2s;
        }
        /* 냄비 손잡이 */
        .pot-handle-left, .pot-handle-right {
            position: absolute;
            top: 180px;
            width: 35px;
            height: 25px;
            background: #ffd700;
            border: 5px solid #b8860b;
            border-radius: 8px;
        }
        .pot-handle-left { left: 250px; }
        .pot-handle-right { left: 615px; }

        /* 냄비 내부 물 & 기포 생성 */
        #pot-water {
            position: absolute;
            bottom: 0;
            width: 100%;
            height: 0%;
            background: rgba(64, 196, 255, 0.5);
            transition: height 0.5s, background-color 0.5s;
        }
        .boiling {
            animation: boil 0.5s infinite alternate;
        }
        @keyframes boil {
            0% { transform: translateY(0px); }
            100% { transform: translateY(-3px); }
        }

        /* 냄비 내부 추가된 재료 레이어 */
        #pot-contents {
            position: absolute;
            bottom: 10px;
            left: 10px;
            right: 10px;
            top: 20px;
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            align-items: center;
            pointer-events: none;
        }
        .added-item {
            font-size: 26px;
            margin: 2px;
            animation: popIn 0.3s ease-out;
        }
        @keyframes popIn {
            0% { transform: scale(0); }
            80% { transform: scale(1.2); }
            100% { transform: scale(1); }
        }

        /* 불 효과 */
        #fire {
            position: absolute;
            bottom: -20px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 30px;
            display: none;
            animation: flame 0.3s infinite alternate;
        }
        @keyframes flame {
            0% { opacity: 0.7; transform: translateX(-50%) scale(0.9); }
            100% { opacity: 1; transform: translateX(-50%) scale(1.1); }
        }

        /* 재료 선반 (드래그 대상) */
        #ingredient-shelf {
            position: absolute;
            bottom: 15px;
            left: 20px;
            right: 20px;
            height: 150px;
            background: #fff;
            border: 4px solid #ff80ab;
            border-radius: 15px;
            display: flex;
            justify-content: space-around;
            align-items: center;
            padding: 10px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        .ingredient {
            width: 95px;
            height: 110px;
            background: #fff0f5;
            border: 3px solid #ffb6c1;
            border-radius: 12px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            cursor: grab;
            transition: transform 0.2s, background-color 0.2s;
            box-shadow: 0 3px 6px rgba(0,0,0,0.1);
        }
        .ingredient:hover {
            transform: translateY(-5px);
            background: #ffe4e1;
        }
        .ingredient:active {
            cursor: grabbing;
        }
        .ingredient-icon {
            font-size: 42px;
        }
        .ingredient-name {
            font-size: 13px;
            font-weight: bold;
            color: #333;
            margin-top: 5px;
        }

        /* 버튼 영역 */
        #action-btn-group {
            position: absolute;
            top: 360px;
            right: 40px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .action-btn {
            padding: 12px 24px;
            font-size: 16px;
            font-weight: bold;
            color: white;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            box-shadow: 0 4px 0 rgba(0,0,0,0.2);
            transition: all 0.1s;
        }
        .action-btn:active {
            transform: translateY(2px);
            box-shadow: 0 2px 0 rgba(0,0,0,0.2);
        }
        #serve-btn { background: #2ed573; }
        #reset-btn { background: #ff4757; }

        /* 결과 모달 레이어 */
        #modal-overlay {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.6);
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 100;
        }
        .modal-content {
            background: white;
            padding: 30px 40px;
            border-radius: 20px;
            border: 5px solid #ff69b4;
            text-align: center;
            max-width: 450px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        .modal-title {
            font-size: 28px;
            color: #d8004e;
            margin-bottom: 15px;
            font-weight: bold;
        }
        .modal-desc {
            font-size: 18px;
            color: #333;
            margin-bottom: 25px;
            line-height: 1.5;
        }
        .restart-btn {
            background: #ff3366;
            color: white;
            border: none;
            padding: 12px 30px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 25px;
            cursor: pointer;
            box-shadow: 0 4px 0 #b3003b;
        }
        .restart-btn:hover { background: #e6004c; }

        /* 상태 말풍선 */
        #status-bubble {
            position: absolute;
            top: 100px;
            left: 310px;
            background: white;
            border: 3px solid #ff69b4;
            padding: 8px 16px;
            border-radius: 15px;
            font-size: 14px;
            font-weight: bold;
            color: #333;
            box-shadow: 0 3px 8px rgba(0,0,0,0.1);
            z-index: 15;
        }
    </style>
</head>
<body>

<div id="game-container">
    <!-- 헤더 -->
    <div id="header">
        <div class="title-banner">🍜 슈의 분식집 라면가게</div>
        <div class="score-box">💰 매출: <span id="score">0</span>원</div>
        <div class="timer-box">⏱️ 남은시간: <span id="timer">03:00</span></div>
    </div>

    <!-- 한국 분식집 간판 장식 -->
    <div class="korean-deco">🏮 원조 냄비라면 전문점</div>

    <!-- 라면 모양 말랑이 장식 -->
    <div class="squishy-ramen" id="squishy" onclick="popSquishy()">
        <span style="font-size: 32px;">🍜</span>
        <span style="font-size: 10px; color: #d8004e; font-weight: bold;">말랑이</span>
    </div>
    <div class="squishy-tag">눌러보세요!</div>

    <!-- 상태 말풍선 -->
    <div id="status-bubble">1. 밸브를 눌러 냄비에 물을 받으세요!</div>

    <!-- 주방 배경 -->
    <div id="kitchen-table"></div>

    <!-- 수도꼭지 및 밸브 -->
    <div id="faucet-zone">
        <div id="faucet-pipe"></div>
        <div id="faucet-head"></div>
        <div id="valve-btn" onclick="toggleValve()">밸브</div>
        <div class="water-stream" id="water-stream"></div>
    </div>

    <!-- 냄비 손잡이 -->
    <div class="pot-handle-left"></div>
    <div class="pot-handle-right"></div>

    <!-- 스토브 및 양은냄비 -->
    <div id="stove-area">
        <div id="pot" ondragover="allowDrop(event)" ondrop="dropIngredient(event)">
            <div id="pot-water"></div>
            <div id="pot-contents"></div>
        </div>
        <div id="fire">🔥 🔥 🔥</div>
    </div>

    <!-- 완성 제출 / 다시하기 버튼 -->
    <div id="action-btn-group">
        <button class="action-btn" id="serve-btn" onclick="serveRamen()">🍜 제출하기</button>
        <button class="action-btn" id="reset-btn" onclick="resetPot()">🗑️ 냄비 비우기</button>
    </div>

    <!-- 재료 선반 (7가지 요구 재료) -->
    <div id="ingredient-shelf">
        <div class="ingredient" draggable="true" ondragstart="drag(event)" id="ing-noodle" data-name="면" data-icon="🍜">
            <div class="ingredient-icon">🍜</div>
            <div class="ingredient-name">면</div>
        </div>
        <div class="ingredient" draggable="true" ondragstart="drag(event)" id="ing-soup" data-name="라면스프" data-icon="🧂">
            <div class="ingredient-icon">🧂</div>
            <div class="ingredient-name">라면스프</div>
        </div>
        <div class="ingredient" draggable="true" ondragstart="drag(event)" id="ing-scullion" data-name="파" data-icon="🥬">
            <div class="ingredient-icon">🥬</div>
            <div class="ingredient-name">파</div>
        </div>
        <div class="ingredient" draggable="true" ondragstart="drag(event)" id="ing-egg" data-name="계란" data-icon="🥚">
            <div class="ingredient-icon">🥚</div>
            <div class="ingredient-name">계란</div>
        </div>
        <div class="ingredient" draggable="true" ondragstart="drag(event)" id="ing-pepper" data-name="고추" data-icon="🌶️">
            <div class="ingredient-icon">🌶️</div>
            <div class="ingredient-name">고추</div>
        </div>
        <div class="ingredient" draggable="true" ondragstart="drag(event)" id="ing-meat" data-name="고기" data-icon="🥩">
            <div class="ingredient-icon">🥩</div>
            <div class="ingredient-name">고기</div>
        </div>
        <div class="ingredient" draggable="true" ondragstart="drag(event)" id="ing-ricecake" data-name="떡" data-icon="🍡">
            <div class="ingredient-icon">🍡</div>
            <div class="ingredient-name">떡</div>
        </div>
    </div>

    <!-- 종료 모달 -->
    <div id="modal-overlay">
        <div class="modal-content">
            <div class="modal-title" id="modal-title">게임 종료!</div>
            <div class="modal-desc" id="modal-desc">결과 설명이 들어갑니다.</div>
            <button class="restart-btn" onclick="restartGame()">다시 도전하기</button>
        </div>
    </div>
</div>

<script>
    // 상태 변수
    let waterLevel = 0; // 0 ~ 100
    let isWaterFilling = false;
    let isWaterBoiling = false;
    let timerSeconds = 180; // 3분 = 180초
    let timerInterval = null;
    let isTimerStarted = false;
    let score = 0;
    
    // 냄비에 담긴 재료 세트
    let potContents = [];
    
    // 3분 제한시간 카운트다운
    function startTimer() {
        if (isTimerStarted) return;
        isTimerStarted = true;
        
        timerInterval = setInterval(() => {
            timerSeconds--;
            updateTimerDisplay();
            
            if (timerSeconds <= 0) {
                clearInterval(timerInterval);
                gameOver(false, "⏰ 3분 제한시간이 지났습니다! 손님이 기다리다 떠났습니다.");
            }
        }, 1000);
    }

    function updateTimerDisplay() {
        const mins = Math.floor(timerSeconds / 60);
        const secs = timerSeconds % 60;
        document.getElementById('timer').innerText = 
            `${mins < 10 ? '0' : ''}${mins}:${secs < 10 ? '0' : ''}${secs}`;
    }

    // 말랑이 장식 터치 이벤트
    function popSquishy() {
        const squishy = document.getElementById('squishy');
        squishy.style.transform = 'scale(0.8) rotate(-10deg)';
        setTimeout(() => {
            squishy.style.transform = 'scale(1) rotate(0deg)';
        }, 150);
    }

    // 수도 밸브 토글
    function toggleValve() {
        if (waterLevel >= 100) {
            updateStatus("물이 이미 가득 찼습니다!");
            return;
        }

        const stream = document.getElementById('water-stream');
        if (!isWaterFilling) {
            isWaterFilling = true;
            stream.style.height = "100px";
            
            let fillInterval = setInterval(() => {
                if (waterLevel < 100 && isWaterFilling) {
                    waterLevel += 10;
                    document.getElementById('pot-water').style.height = waterLevel + '%';
                    if (waterLevel >= 100) {
                        clearInterval(fillInterval);
                        isWaterFilling = false;
                        stream.style.height = "0px";
                        startBoiling();
                    }
                } else {
                    clearInterval(fillInterval);
                }
            }, 200);
        }
    }

    // 물 끓이기 시작
    function startBoiling() {
        updateStatus("물이 끓기 시작합니다! 3분 안에 재료를 넣으세요.");
        document.getElementById('fire').style.display = 'block';
        document.getElementById('pot').classList.add('boiling');
        
        setTimeout(() => {
            isWaterBoiling = true;
            document.getElementById('pot-water').style.backgroundColor = 'rgba(255, 152, 0, 0.6)';
            startTimer(); // 물이 끓으면 3분 타이머 작동 시작!
        }, 1500);
    }

    // Drag & Drop
    function allowDrop(ev) {
        ev.preventDefault();
    }

    function drag(ev) {
        ev.dataTransfer.setData("text", ev.target.id);
    }

    function dropIngredient(ev) {
        ev.preventDefault();
        
        if (waterLevel < 50) {
            updateStatus("⚠️ 물을 먼저 충분히 받아주세요!");
            return;
        }
        if (!isWaterBoiling) {
            updateStatus("⚠️ 물이 아직 팔팔 끓지 않고 있습니다!");
            return;
        }

        const data = ev.dataTransfer.getData("text");
        const draggedElem = document.getElementById(data);
        const name = draggedElem.getAttribute('data-name');
        const icon = draggedElem.getAttribute('data-icon');

        // 재료 중복 체크
        if (potContents.includes(name)) {
            updateStatus(`⚠️ 이미 '${name}' 재료를 넣었습니다!`);
            return;
        }

        potContents.push(name);
        
        // 냄비 화면 연출
        const itemElem = document.createElement('span');
        itemElem.className = 'added-item';
        itemElem.innerText = icon;
        document.getElementById('pot-contents').appendChild(itemElem);

        // 국물 색상 변경 (스프 추가 시)
        if (name === '라면스프') {
            document.getElementById('pot-water').style.backgroundColor = 'rgba(211, 47, 47, 0.85)';
        }

        updateStatus(`'${name}'(을)를 넣었습니다! (현재 ${potContents.length}/7개)`);
    }

    // 상태 안내 업데이트
    function updateStatus(msg) {
        document.getElementById('status-bubble').innerText = msg;
    }

    // 냄비 비우기
    function resetPot() {
        waterLevel = 0;
        isWaterFilling = false;
        isWaterBoiling = false;
        potContents = [];
        
        document.getElementById('pot-water').style.height = '0%';
        document.getElementById('pot-water').style.backgroundColor = 'rgba(64, 196, 255, 0.5)';
        document.getElementById('pot-contents').innerHTML = '';
        document.getElementById('fire').style.display = 'none';
        document.getElementById('pot').classList.remove('boiling');
        
        updateStatus("냄비를 비웠습니다. 다시 밸브를 열어 물을 받으세요.");
    }

    // 라면 제출 및 점수 계산
    function serveRamen() {
        if (!isWaterBoiling) {
            updateStatus("⚠️ 아직 끓지도 않은 라면을 제출할 수 없습니다!");
            return;
        }
        if (potContents.length === 0) {
            updateStatus("⚠️ 맹물만 제출할 수 없습니다!");
            return;
        }

        // 필수 7가지 재료: 면, 라면스프, 파, 계란, 고추, 고기, 떡
        const required = ["면", "라면스프", "파", "계란", "고추", "고기", "떡"];
        let matched = potContents.filter(item => required.includes(item)).length;

        let earnings = matched * 1000;
        
        if (matched === 7) {
            score += earnings + 3000; // 보너스
            gameOver(true, `🎉 대성공! 7가지 모든 재료가 들어간 최고의 명품 라면!\n매출: +${earnings + 3000}원!`);
        } else if (matched >= 4) {
            score += earnings;
            gameOver(true, `👍 맛있네요! (재료 ${matched}/7개 완비)\n매출: +${earnings}원`);
        } else {
            gameOver(false, `😭 재료가 부족하여 손님이 불만을 표시했습니다. (재료 ${matched}/7개)`);
        }
        
        document.getElementById('score').innerText = score;
    }

    // 게임 종료 모달 처리
    function gameOver(isSuccess, message) {
        clearInterval(timerInterval);
        const modal = document.getElementById('modal-overlay');
        const titleElem = document.getElementById('modal-title');
        const descElem = document.getElementById('modal-desc');

        titleElem.innerText = isSuccess ? "✨ 조리 완료! ✨" : "❌ 조리 실패!";
        titleElem.style.color = isSuccess ? "#2ed573" : "#ff4757";
        descElem.innerText = message;
        
        modal.style.display = 'flex';
    }

    // 다시 시작
    function restartGame() {
        document.getElementById('modal-overlay').style.display = 'none';
        timerSeconds = 180;
        isTimerStarted = false;
        updateTimerDisplay();
        resetPot();
    }
</script>
</body>
</html>
"""

# Streamlit 앱 UI 구성
st.markdown("<h2 style='text-align: center; color: #ff3366;'>🍜 슈의 추억의 라면가게 🍜</h2>", unsafe_allow_html=True)
st.caption("🎮 게임 방법: 1) 밸브를 클릭해 물을 채운다 -> 2) 물이 끓으면 3분 이내에 7가지 재료를 냄비로 드래그 앤 드롭한다 -> 3) [제출하기]를 누른다!")

# HTML Canvas 및 JS 삽입
components.html(game_html, height=720, scrolling=False)
