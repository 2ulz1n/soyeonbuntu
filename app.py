import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="추억의 슈의 라면가게 2.0 🍜",
    page_icon="🍜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 게임 전체 HTML/CSS/JS 코드 (정수기, 손님 주문, 30초 타이머, 리얼 라면 비주얼 반영)
game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>슈의 라면가게 2.0</title>
    <style>
        * {
            box-sizing: border-box;
            user-select: none;
            -webkit-user-select: none;
            font-family: 'Comic Sans MS', 'Gothic A1', 'Nanum Gothic', sans-serif, cursive;
        }
        body {
            margin: 0;
            padding: 10px;
            background-color: #ffe6ee;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        #game-container {
            position: relative;
            width: 900px;
            height: 680px;
            background: linear-gradient(135deg, #ffc0cb 0%, #ffdbed 100%);
            border: 8px solid #ff1493;
            border-radius: 25px;
            box-shadow: 0 12px 30px rgba(0,0,0,0.25);
            overflow: hidden;
        }
        /* 헤더 */
        #header {
            position: absolute;
            top: 12px;
            left: 20px;
            right: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 20;
        }
        .title-banner {
            background: #ff1493;
            color: white;
            padding: 8px 22px;
            border-radius: 25px;
            font-size: 22px;
            font-weight: bold;
            box-shadow: 3px 3px 0px #b3006b;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }
        .info-box {
            background: #fff;
            border: 3px solid #ff1493;
            padding: 6px 16px;
            border-radius: 18px;
            font-size: 18px;
            font-weight: bold;
            color: #d8004e;
            box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
        }
        .timer-box.warning {
            color: #ff0000;
            animation: blink 0.5s infinite alternate;
        }
        @keyframes blink {
            from { opacity: 1; transform: scale(1); }
            to { opacity: 0.8; transform: scale(1.05); }
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
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
            transition: transform 0.1s ease;
            z-index: 25;
        }
        .squishy-ramen:active {
            transform: scale(0.82) rotate(-8deg);
        }
        .squishy-tag {
            position: absolute;
            top: 155px;
            right: 20px;
            font-size: 11px;
            background: #ff1493;
            color: white;
            padding: 2px 8px;
            border-radius: 10px;
            font-weight: bold;
            z-index: 25;
        }

        /* 손님 및 주문 대화창 */
        #customer-area {
            position: absolute;
            top: 65px;
            left: 20px;
            display: flex;
            align-items: flex-end;
            gap: 15px;
            z-index: 15;
        }
        #customer-avatar {
            width: 100px;
            height: 100px;
            background: #fff;
            border: 4px solid #ff69b4;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 55px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            background: radial-gradient(circle, #fff 60%, #ffd1dc 100%);
        }
        #speech-bubble {
            position: relative;
            background: white;
            border: 4px solid #ff1493;
            border-radius: 20px;
            padding: 12px 20px;
            max-width: 380px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
            font-size: 15px;
            font-weight: bold;
            color: #333;
        }
        #speech-bubble::after {
            content: '';
            position: absolute;
            left: -15px;
            bottom: 20px;
            border-width: 8px 15px 8px 0;
            border-style: solid;
            border-color: transparent white transparent transparent;
            display: block;
            width: 0;
        }
        #speech-bubble::before {
            content: '';
            position: absolute;
            left: -20px;
            bottom: 18px;
            border-width: 10px 18px 10px 0;
            border-style: solid;
            border-color: transparent #ff1493 transparent transparent;
            display: block;
            width: 0;
        }
        .order-badge {
            display: inline-block;
            background: #fff0f5;
            border: 2px solid #ff69b4;
            color: #d8004e;
            padding: 2px 8px;
            border-radius: 12px;
            margin: 2px;
            font-size: 13px;
        }

        /* 주방 작업대 */
        #kitchen-table {
            position: absolute;
            bottom: 0;
            width: 100%;
            height: 490px;
            background: #fce4ec;
            border-top: 10px solid #f48fb1;
        }

        /* 정수기 영역 */
        #water-dispenser {
            position: absolute;
            top: 190px;
            left: 40px;
            width: 140px;
            height: 250px;
            background: linear-gradient(180deg, #ffffff 0%, #e1f5fe 100%);
            border: 4px solid #81d4fa;
            border-radius: 15px;
            box-shadow: 0 8px 15px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            align-items: center;
            padding-top: 15px;
            z-index: 10;
        }
        .dispenser-brand {
            font-size: 12px;
            font-weight: bold;
            color: #0288d1;
            background: #b3e5fc;
            padding: 2px 10px;
            border-radius: 10px;
        }
        .dispenser-spout {
            position: absolute;
            bottom: 80px;
            width: 24px;
            height: 25px;
            background: #b0bec5;
            border-radius: 4px;
            border: 2px solid #607d8b;
        }
        .dispenser-tray {
            position: absolute;
            bottom: 15px;
            width: 100px;
            height: 50px;
            background: #e0e0e0;
            border: 3px dashed #9e9e9e;
            border-radius: 10px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 11px;
            color: #666;
            text-align: center;
            font-weight: bold;
        }
        .water-stream-anim {
            position: absolute;
            bottom: 30px;
            width: 12px;
            height: 0px;
            background: rgba(3, 169, 244, 0.7);
            border-radius: 0 0 6px 6px;
            transition: height 0.3s;
            z-index: 11;
        }

        /* 가스레인지 & 스토브 */
        #stove-area {
            position: absolute;
            top: 220px;
            left: 320px;
            width: 280px;
            height: 200px;
            background: #cfd8dc;
            border: 5px solid #78909c;
            border-radius: 20px;
            box-shadow: 0 8px 15px rgba(0,0,0,0.15);
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .burner-ring {
            width: 180px;
            height: 120px;
            border: 6px solid #455a64;
            border-radius: 50%;
            background: #37474f;
            position: relative;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        #fire {
            position: absolute;
            font-size: 35px;
            display: none;
            animation: flame 0.25s infinite alternate;
            z-index: 5;
        }
        @keyframes flame {
            0% { opacity: 0.8; transform: scale(0.95); }
            100% { opacity: 1; transform: scale(1.15); }
        }

        /* 드래그 가능한 양은냄비 */
        #pot-container {
            position: absolute;
            top: 240px;
            left: 640px; /* 초기 위치: 대기 조리대 */
            width: 200px;
            height: 140px;
            cursor: grab;
            z-index: 30;
            transition: transform 0.1s;
        }
        #pot-container:active {
            cursor: grabbing;
        }
        .pot-body {
            position: relative;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #ffd700 0%, #f5b041 100%);
            border: 5px solid #b8860b;
            border-radius: 10px 10px 70px 70px;
            box-shadow: inset 0 5px 12px rgba(0,0,0,0.25), 0 8px 15px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .pot-handle-l, .pot-handle-r {
            position: absolute;
            top: 20px;
            width: 22px;
            height: 35px;
            background: #ffd700;
            border: 4px solid #b8860b;
            border-radius: 8px;
        }
        .pot-handle-l { left: -18px; }
        .pot-handle-r { right: -18px; }

        /* 냄비 내부 리얼 라면 비주얼 레이어 */
        #pot-water-layer {
            position: absolute;
            bottom: 0;
            width: 100%;
            height: 0%;
            background: rgba(64, 196, 255, 0.6);
            transition: height 0.4s, background-color 0.5s;
        }
        #pot-ingredients-layer {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none;
        }

        /* 리얼 그래픽 재료 요소들 */
        .visual-noodle {
            position: absolute;
            top: 25px; left: 15px; right: 15px; bottom: 15px;
            background: radial-gradient(circle, #fff3a0 40%, #f7d070 80%);
            border-radius: 40%;
            border: 4px repeating-linear-gradient(45deg, #f4c430, #f4c430 6px, #ffe87c 6px, #ffe87c 12px);
            box-shadow: inset 0 2px 6px rgba(0,0,0,0.2);
            animation: popIn 0.3s ease-out;
        }
        .visual-soup-color {
            background-color: rgba(220, 38, 38, 0.85) !important;
        }
        .visual-scullion {
            position: absolute;
            width: 18px; height: 8px;
            background: #2e7d32;
            border: 1px solid #1b5e20;
            border-radius: 4px;
            transform: rotate(15deg);
        }
        .visual-egg {
            position: absolute;
            top: 35px; left: 65px;
            width: 50px; height: 40px;
            background: #f8f9fa;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.15);
        }
        .visual-egg-yolk {
            width: 22px; height: 22px;
            background: #ff9800;
            border-radius: 50%;
            box-shadow: inset -2px -2px 0px #e65100;
        }
        .visual-pepper {
            position: absolute;
            width: 16px; height: 16px;
            border: 3px solid #c62828;
            border-radius: 50%;
            background: transparent;
        }
        .visual-meat {
            position: absolute;
            width: 38px; height: 14px;
            background: #8d6e63;
            border: 1px solid #4e342e;
            border-radius: 6px;
            transform: rotate(-10deg);
        }
        .visual-ricecake {
            position: absolute;
            width: 32px; height: 16px;
            background: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            transform: rotate(25deg);
            box-shadow: 1px 1px 3px rgba(0,0,0,0.1);
        }

        /* 끓는 애니메이션 */
        .boiling-pot {
            animation: boilAnim 0.3초 infinite alternate;
        }
        @keyframes boilAnim {
            0% { transform: translateY(0px) rotate(0deg); }
            100% { transform: translateY(-3px) rotate(1deg); }
        }

        /* 재료 선반 */
        #ingredient-shelf {
            position: absolute;
            bottom: 12px;
            left: 20px;
            right: 20px;
            height: 140px;
            background: #ffffff;
            border: 4px solid #ff69b4;
            border-radius: 20px;
            display: flex;
            justify-content: space-around;
            align-items: center;
            padding: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .ingredient-card {
            width: 95px;
            height: 110px;
            background: #fff0f5;
            border: 3px solid #ffb6c1;
            border-radius: 15px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            cursor: grab;
            transition: all 0.2s;
            box-shadow: 0 3px 6px rgba(0,0,0,0.08);
        }
        .ingredient-card:hover {
            transform: translateY(-6px);
            background: #ffe4e1;
            border-color: #ff1493;
        }
        .ingredient-card:active { cursor: grabbing; }
        .ing-icon { font-size: 40px; }
        .ing-name { font-size: 13px; font-weight: bold; color: #333; margin-top: 4px; }

        /* 액션 버튼 그룹 */
        #action-group {
            position: absolute;
            top: 240px;
            right: 35px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            z-index: 20;
        }
        .btn-action {
            padding: 12px 20px;
            font-size: 16px;
            font-weight: bold;
            color: white;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            box-shadow: 0 4px 0 rgba(0,0,0,0.2);
            transition: all 0.1s;
        }
        .btn-action:active { transform: translateY(2px); box-shadow: 0 2px 0 rgba(0,0,0,0.2); }
        #btn-serve { background: #2ed573; }
        #btn-reset { background: #ff4757; }

        /* 결과 모달 */
        #modal-overlay {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.65);
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 100;
        }
        .modal-box {
            background: white;
            padding: 30px 40px;
            border-radius: 25px;
            border: 6px solid #ff1493;
            text-align: center;
            max-width: 460px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        .modal-title { font-size: 30px; color: #d8004e; font-weight: bold; margin-bottom: 15px; }
        .modal-desc { font-size: 18px; color: #333; margin-bottom: 25px; line-height: 1.5; white-space: pre-line; }
        .btn-restart {
            background: #ff1493; color: white; border: none; padding: 12px 32px;
            font-size: 18px; font-weight: bold; border-radius: 25px; cursor: pointer;
            box-shadow: 0 4px 0 #b3006b;
        }
        .btn-restart:hover { background: #e6006b; }
    </style>
</head>
<body>

<div id="game-container">
    <!-- 헤더 -->
    <div id="header">
        <div class="title-banner">🍜 슈의 라면가게 2.0</div>
        <div class="info-box">💰 매출: <span id="score-text">0</span>원</div>
        <div class="info-box timer-box" id="timer-box">⏱️ 시간: <span id="timer-text">30</span>초</div>
    </div>

    <!-- 손님 및 주문대화창 -->
    <div id="customer-area">
        <div id="customer-avatar">👧</div>
        <div id="speech-bubble">
            <span id="customer-dialog">손님 주문을 기다리는 중...</span>
        </div>
    </div>

    <!-- 라면 모양 말랑이 -->
    <div class="squishy-ramen" onclick="clickSquishy()">
        <span style="font-size: 32px;">🍜</span>
        <span style="font-size: 10px; color: #d8004e; font-weight: bold;">말랑이</span>
    </div>
    <div class="squishy-tag">말랑이 터치!</div>

    <!-- 주방 배경 -->
    <div id="kitchen-table"></div>

    <!-- 정수기 -->
    <div id="water-dispenser" ondragover="allowDrop(event)" ondrop="dropPotToDispenser(event)">
        <div class="dispenser-brand">PURE WATER</div>
        <div class="dispenser-spout"></div>
        <div class="water-stream-anim" id="water-stream"></div>
        <div class="dispenser-tray">💧 냄비를 여기로<br>끌어오세요!</div>
    </div>

    <!-- 가스레인지 스토브 -->
    <div id="stove-area" ondragover="allowDrop(event)" ondrop="dropPotToStove(event)">
        <div class="burner-ring">
            <div id="fire">🔥 🔥 🔥</div>
            <span style="color:#78909c; font-size:12px; font-weight:bold;">가스레인지 burner</span>
        </div>
    </div>

    <!-- 양은냄비 (드래그 가능) -->
    <div id="pot-container" draggable="true" ondragstart="dragPot(event)" ondragover="allowDrop(event)" ondrop="dropIngredientToPot(event)">
        <div class="pot-handle-l"></div>
        <div class="pot-handle-r"></div>
        <div class="pot-body" id="pot-body">
            <div id="pot-water-layer"></div>
            <div id="pot-ingredients-layer"></div>
        </div>
    </div>

    <!-- 버튼 그룹 -->
    <div id="action-group">
        <button class="btn-action" id="btn-serve" onclick="serveRamen()">🍜 제출하기</button>
        <button class="btn-action" id="btn-reset" onclick="resetPot()">🗑️ 냄비 비우기</button>
    </div>

    <!-- 재료 선반 (드래그 대상) -->
    <div id="ingredient-shelf">
        <div class="ingredient-card" draggable="true" ondragstart="dragIngredient(event)" id="ing-noodle" data-name="면">
            <div class="ing-icon">🍜</div>
            <div class="ing-name">면</div>
        </div>
        <div class="ingredient-card" draggable="true" ondragstart="dragIngredient(event)" id="ing-soup" data-name="라면스프">
            <div class="ing-icon">🧂</div>
            <div class="ing-name">라면스프</div>
        </div>
        <div class="ingredient-card" draggable="true" ondragstart="dragIngredient(event)" id="ing-scullion" data-name="파">
            <div class="ing-icon">🥬</div>
            <div class="ing-name">파</div>
        </div>
        <div class="ingredient-card" draggable="true" ondragstart="dragIngredient(event)" id="ing-egg" data-name="계란">
            <div class="ing-icon">🥚</div>
            <div class="ing-name">계란</div>
        </div>
        <div class="ingredient-card" draggable="true" ondragstart="dragIngredient(event)" id="ing-pepper" data-name="고추">
            <div class="ing-icon">🌶️</div>
            <div class="ing-name">고추</div>
        </div>
        <div class="ingredient-card" draggable="true" ondragstart="dragIngredient(event)" id="ing-meat" data-name="고기">
            <div class="ing-icon">🥩</div>
            <div class="ing-name">고기</div>
        </div>
        <div class="ingredient-card" draggable="true" ondragstart="dragIngredient(event)" id="ing-ricecake" data-name="떡">
            <div class="ing-icon">🍡</div>
            <div class="ing-name">떡</div>
        </div>
    </div>

    <!-- 결과 모달 -->
    <div id="modal-overlay">
        <div class="modal-box">
            <div class="modal-title" id="modal-title">게임 종료!</div>
            <div class="modal-desc" id="modal-desc">결과 요약</div>
            <button class="btn-restart" onclick="nextCustomerOrRestart()">다음 손님 받기</button>
        </div>
    </div>
</div>

<script>
    // 게임 데이터 상태
    let isWaterFilled = false;
    let isOnStove = false;
    let isBoiling = false;
    let timerSeconds = 30; // 30초 제한시간
    let timerInterval = null;
    let score = 0;
    
    // 냄비 속 담긴 재료 목록
    let potIngredients = [];

    // 손님 캐릭터 목록 & 주문 템플릿
    const customers = [
        { avatar: "👧", name: "초등학생 슈" },
        { avatar: "👦", name: "단골 손님 민우" },
        { avatar: "👨", name: "퇴근길 아저씨" },
        { avatar: "👩", name: "얼큰한 맛 마니아 정아" }
    ];

    const allOptionalIngredients = ["파", "계란", "고추", "고기", "떡"];
    let currentCustomer = {};
    let currentOrder = []; // 손님이 요구하는 필수+선택 재료 목록

    window.onload = () => {
        spawnNewCustomer();
    };

    // 새 손님 생성 및 주문 생성
    function spawnNewCustomer() {
        currentCustomer = customers[Math.floor(Math.random() * customers.length)];
        document.getElementById('customer-avatar').innerText = currentCustomer.avatar;

        // 면과 스프는 기본 필수, 옵션 재료 중 1~3개 무작위 요구
        const shuffled = [...allOptionalIngredients].sort(() => 0.5 - Math.random());
        const selectedOptions = shuffled.slice(0, Math.floor(Math.random() * 3) + 1);
        currentOrder = ["면", "라면스프", ...selectedOptions];

        // 대화창 업데이트
        let orderHtml = `안녕하세요! <b>${currentOrder.join(', ')}</b> 들어간 라면으로 30초 안에 부탁해요!`;
        document.getElementById('customer-dialog').innerHTML = orderHtml;

        resetPotPositionAndState();
        start30SecTimer();
    }

    // 30초 타이머
    function start30SecTimer() {
        clearInterval(timerInterval);
        timerSeconds = 30;
        updateTimerDisplay();
        document.getElementById('timer-box').classList.remove('warning');

        timerInterval = setInterval(() => {
            timerSeconds--;
            updateTimerDisplay();

            if (timerSeconds <= 7) {
                document.getElementById('timer-box').classList.add('warning');
            }

            if (timerSeconds <= 0) {
                clearInterval(timerInterval);
                showModal(false, "⏰ 30초 제한시간 초과!\n손님이 너무 오래 기다려서 화내며 떠났습니다!");
            }
        }, 1000);
    }

    function updateTimerDisplay() {
        document.getElementById('timer-text').innerText = timerSeconds;
    }

    // 말랑이 터치 효과
    function clickSquishy() {
        const sq = document.querySelector('.squishy-ramen');
        sq.style.transform = 'scale(0.8) rotate(-10deg)';
        setTimeout(() => sq.style.transform = 'scale(1) rotate(0deg)', 150);
    }

    // Drag & Drop 핸들러들
    function allowDrop(ev) { ev.preventDefault(); }

    function dragPot(ev) {
        ev.dataTransfer.setData("type", "pot");
    }

    function dragIngredient(ev) {
        ev.dataTransfer.setData("type", "ingredient");
        ev.dataTransfer.setData("id", ev.target.id);
    }

    // 냄비를 정수기에 드롭 -> 물 채우기
    function dropPotToDispenser(ev) {
        ev.preventDefault();
        const type = ev.dataTransfer.getData("type");
        if (type !== "pot") return;

        const pot = document.getElementById('pot-container');
        pot.style.left = "20px";
        pot.style.top = "260px";

        if (!isWaterFilled) {
            const stream = document.getElementById('water-stream');
            stream.style.height = "70px";
            setTimeout(() => {
                isWaterFilled = true;
                document.getElementById('pot-water-layer').style.height = "60%";
                stream.style.height = "0px";
            }, 600);
        }
    }

    // 냄비를 가스레인지에 드롭 -> 물 끓이기
    function dropPotToStove(ev) {
        ev.preventDefault();
        const type = ev.dataTransfer.getData("type");
        if (type !== "pot") return;

        const pot = document.getElementById('pot-container');
        pot.style.left = "360px";
        pot.style.top = "210px";
        isOnStove = true;

        if (isWaterFilled && !isBoiling) {
            document.getElementById('fire').style.display = 'block';
            setTimeout(() => {
                isBoiling = true;
                document.getElementById('pot-body').classList.add('boiling-pot');
            }, 1000);
        }
    }

    // 냄비로 재료 드롭 -> 실제 라면 비주얼 추가
    function dropIngredientToPot(ev) {
        ev.preventDefault();
        const type = ev.dataTransfer.getData("type");
        if (type !== "ingredient") return;

        if (!isWaterFilled) {
            alert("⚠️ 정수기에서 먼저 물을 받아주세요!");
            return;
        }
        if (!isOnStove || !isBoiling) {
            alert("⚠️ 냄비를 가스레인지에 올려 물을 먼저 끓여주세요!");
            return;
        }

        const id = ev.dataTransfer.getData("id");
        const name = document.getElementById(id).getAttribute('data-name');

        if (potIngredients.includes(name)) {
            alert(`⚠️ '${name}'은(는) 이미 넣었습니다!`);
            return;
        }

        potIngredients.push(name);
        renderVisualIngredient(name);
    }

    // 실제 라면처럼 비주얼 요소 렌더링
    function renderVisualIngredient(name) {
        const layer = document.getElementById('pot-ingredients-layer');

        if (name === "면") {
            const noodle = document.createElement('div');
            noodle.className = 'visual-noodle';
            layer.appendChild(noodle);
        } else if (name === "라면스프") {
            document.getElementById('pot-water-layer').classList.add('visual-soup-color');
        } else if (name === "파") {
            for (let i = 0; i < 5; i++) {
                const sc = document.createElement('div');
                sc.className = 'visual-scullion';
                sc.style.top = (30 + Math.random() * 40) + 'px';
                sc.style.left = (30 + Math.random() * 100) + 'px';
                sc.style.transform = `rotate(${Math.random()*180}deg)`;
                layer.appendChild(sc);
            }
        } else if (name === "계란") {
            const egg = document.createElement('div');
            egg.className = 'visual-egg';
            egg.innerHTML = '<div class="visual-egg-yolk"></div>';
            layer.appendChild(egg);
        } else if (name === "고추") {
            for (let i = 0; i < 4; i++) {
                const pep = document.createElement('div');
                pep.className = 'visual-pepper';
                pep.style.top = (35 + Math.random() * 35) + 'px';
                pep.style.left = (30 + Math.random() * 110) + 'px';
                layer.appendChild(pep);
            }
        } else if (name === "고기") {
            for (let i = 0; i < 2; i++) {
                const meat = document.createElement('div');
                meat.className = 'visual-meat';
                meat.style.top = (40 + Math.random() * 30) + 'px';
                meat.style.left = (40 + Math.random() * 90) + 'px';
                layer.appendChild(meat);
            }
        } else if (name === "떡") {
            for (let i = 0; i < 3; i++) {
                const rc = document.createElement('div');
                rc.className = 'visual-ricecake';
                rc.style.top = (35 + Math.random() * 35) + 'px';
                rc.style.left = (30 + Math.random() * 100) + 'px';
                layer.appendChild(rc);
            }
        }
    }

    // 제출 평가
    function serveRamen() {
        if (!isWaterFilled || !isBoiling) {
            alert("⚠️ 라면이 아직 다 끓지 않았습니다!");
            return;
        }

        // 손님 취향 검증 (필요한 재료 일치 여부)
        const hasAllRequired = currentOrder.every(ing => potIngredients.includes(ing));
        const hasExtraUnwanted = potIngredients.some(ing => !currentOrder.includes(ing));

        if (hasAllRequired && !hasExtraUnwanted) {
            const earned = 4000;
            score += earned;
            document.getElementById('score-text').innerText = score;
            showModal(true, `🎉 맞춤 완성! 손님이 대만족했습니다!\n매출: +${earned}원`);
        } else if (hasAllRequired && hasExtraUnwanted) {
            const earned = 2000;
            score += earned;
            document.getElementById('score-text').innerText = score;
            showModal(true, `🙂 주문하지 않은 재료가 들어갔지만 먹을만하네요!\n매출: +${earned}원`);
        } else {
            showModal(false, `😭 주문한 재료가 빠져있습니다!\n요청 주문: [${currentOrder.join(', ')}]`);
        }
    }

    // 냄비 초기화
    function resetPot() {
        resetPotPositionAndState();
    }

    function resetPotPositionAndState() {
        isWaterFilled = false;
        isOnStove = false;
        isBoiling = false;
        potIngredients = [];

        const pot = document.getElementById('pot-container');
        pot.style.left = "640px";
        pot.style.top = "240px";

        document.getElementById('pot-water-layer').style.height = "0%";
        document.getElementById('pot-water-layer').classList.remove('visual-soup-color');
        document.getElementById('pot-ingredients-layer').innerHTML = '';
        document.getElementById('fire').style.display = 'none';
        document.getElementById('pot-body').classList.remove('boiling-pot');
    }

    // 결과 모달
    function showModal(isSuccess, msg) {
        clearInterval(timerInterval);
        const modal = document.getElementById('modal-overlay');
        document.getElementById('modal-title').innerText = isSuccess ? "✨ 성공! ✨" : "❌ 실패!";
        document.getElementById('modal-title').style.color = isSuccess ? "#2ed573" : "#ff4757";
        document.getElementById('modal-desc').innerText = msg;
        modal.style.display = 'flex';
    }

    function nextCustomerOrRestart() {
        document.getElementById('modal-overlay').style.display = 'none';
        spawnNewCustomer();
    }
</script>
</body>
</html>
"""

st.markdown("<h2 style='text-align: center; color: #ff1493;'>🍜 슈의 라면가게 2.0 (정수기 & 30초 맞춤 조리) 🍜</h2>", unsafe_allow_html=True)

# Streamlit Canvas 컴포넌트 출력
components.html(game_html, height=720, scrolling=False)
