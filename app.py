import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="추억의 슈의 라면가게 3.0 🍜",
    page_icon="🍜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 게임 전체 HTML/CSS/JS 코드 (4인 손님 동시 등장, 4구 화구, 개별 30초 타이머, 리얼 라면 비주얼)
game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>슈의 라면가게 3.0</title>
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
            width: 960px;
            height: 720px;
            background: linear-gradient(135deg, #ffc0cb 0%, #ffdbed 100%);
            border: 8px solid #ff1493;
            border-radius: 25px;
            box-shadow: 0 12px 30px rgba(0,0,0,0.25);
            overflow: hidden;
        }
        /* 헤더 */
        #header {
            position: absolute;
            top: 10px;
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
            padding: 6px 20px;
            border-radius: 25px;
            font-size: 20px;
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

        /* 라면 모양 말랑이 장식 */
        .squishy-ramen {
            position: absolute;
            top: 60px;
            right: 20px;
            width: 65px;
            height: 65px;
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
            top: 130px;
            right: 15px;
            font-size: 10px;
            background: #ff1493;
            color: white;
            padding: 2px 6px;
            border-radius: 10px;
            font-weight: bold;
            z-index: 25;
        }

        /* 4명 손님 영역 */
        #customers-container {
            position: absolute;
            top: 55px;
            left: 20px;
            width: 840px;
            height: 160px;
            display: flex;
            justify-content: space-between;
            z-index: 15;
        }
        .customer-card {
            position: relative;
            width: 195px;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .customer-avatar {
            width: 75px;
            height: 75px;
            background: radial-gradient(circle, #fff 60%, #ffd1dc 100%);
            border: 3px solid #ff69b4;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 42px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .customer-timer-badge {
            position: absolute;
            top: -5px;
            right: 20px;
            background: #ff1493;
            color: white;
            font-size: 12px;
            font-weight: bold;
            padding: 2px 8px;
            border-radius: 12px;
            border: 2px solid white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        .customer-timer-badge.warning {
            background: #ff0000;
            animation: blink 0.5s infinite alternate;
        }
        @keyframes blink {
            from { transform: scale(1); }
            to { transform: scale(1.15); }
        }
        .speech-bubble {
            position: relative;
            margin-top: 5px;
            background: white;
            border: 3px solid #ff1493;
            border-radius: 12px;
            padding: 6px 8px;
            width: 100%;
            text-align: center;
            font-size: 11px;
            font-weight: bold;
            color: #333;
            box-shadow: 0 3px 6px rgba(0,0,0,0.1);
        }

        /* 주방 테이블 배경 */
        #kitchen-table {
            position: absolute;
            bottom: 0;
            width: 100%;
            height: 500px;
            background: #fce4ec;
            border-top: 8px solid #f48fb1;
        }

        /* 정수기 영역 */
        #water-dispenser {
            position: absolute;
            top: 230px;
            left: 20px;
            width: 120px;
            height: 220px;
            background: linear-gradient(180deg, #ffffff 0%, #e1f5fe 100%);
            border: 4px solid #81d4fa;
            border-radius: 15px;
            box-shadow: 0 6px 12px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            align-items: center;
            padding-top: 10px;
            z-index: 10;
        }
        .dispenser-brand {
            font-size: 11px;
            font-weight: bold;
            color: #0288d1;
            background: #b3e5fc;
            padding: 2px 8px;
            border-radius: 8px;
        }
        .dispenser-spout {
            position: absolute;
            bottom: 75px;
            width: 20px;
            height: 22px;
            background: #b0bec5;
            border-radius: 4px;
            border: 2px solid #607d8b;
        }
        .dispenser-tray {
            position: absolute;
            bottom: 12px;
            width: 90px;
            height: 45px;
            background: #e0e0e0;
            border: 2px dashed #9e9e9e;
            border-radius: 8px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 10px;
            color: #555;
            text-align: center;
            font-weight: bold;
        }
        .water-stream-anim {
            position: absolute;
            bottom: 25px;
            width: 10px;
            height: 0px;
            background: rgba(3, 169, 244, 0.7);
            border-radius: 0 0 5px 5px;
            transition: height 0.3s;
            z-index: 11;
        }

        /* 4구 가스레인지 영역 */
        #stove-grid {
            position: absolute;
            top: 230px;
            left: 160px;
            width: 780px;
            height: 220px;
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
        }
        .burner-slot {
            position: relative;
            background: #cfd8dc;
            border: 4px solid #78909c;
            border-radius: 15px;
            box-shadow: 0 6px 12px rgba(0,0,0,0.12);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-end;
            padding-bottom: 10px;
        }
        .burner-ring {
            width: 130px;
            height: 85px;
            border: 5px solid #455a64;
            border-radius: 50%;
            background: #37474f;
            position: relative;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .fire-anim {
            position: absolute;
            font-size: 28px;
            display: none;
            animation: flame 0.25s infinite alternate;
            z-index: 5;
        }
        @keyframes flame {
            0% { opacity: 0.8; transform: scale(0.9); }
            100% { opacity: 1; transform: scale(1.1); }
        }

        /* 냄비 (4개 개별 존재 & 드래그) */
        .pot-container {
            position: absolute;
            width: 135px;
            height: 95px;
            cursor: grab;
            z-index: 30;
            transition: transform 0.1s;
        }
        .pot-container:active { cursor: grabbing; }
        
        .pot-body {
            position: relative;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #ffd700 0%, #f5b041 100%);
            border: 4px solid #b8860b;
            border-radius: 8px 8px 45px 45px;
            box-shadow: inset 0 4px 8px rgba(0,0,0,0.25), 0 6px 10px rgba(0,0,0,0.15);
            overflow: hidden;
        }
        .pot-handle-l, .pot-handle-r {
            position: absolute;
            top: 15px;
            width: 15px;
            height: 25px;
            background: #ffd700;
            border: 3px solid #b8860b;
            border-radius: 6px;
        }
        .pot-handle-l { left: -12px; }
        .pot-handle-r { right: -12px; }

        /* 냄비 내부 리얼 라면 비주얼 레이어 */
        .pot-water-layer {
            position: absolute;
            bottom: 0;
            width: 100%;
            height: 0%;
            background: rgba(64, 196, 255, 0.6);
            transition: height 0.3s, background-color 0.4s;
        }
        .pot-ingredients-layer {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none;
        }

        /* 리얼 그래픽 재료 요소들 */
        .visual-noodle {
            position: absolute;
            top: 15px; left: 10px; right: 10px; bottom: 10px;
            background: radial-gradient(circle, #fff3a0 40%, #f7d070 80%);
            border-radius: 40%;
            border: 3px repeating-linear-gradient(45deg, #f4c430, #f4c430 5px, #ffe87c 5px, #ffe87c 10px);
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);
        }
        .visual-soup-color {
            background-color: rgba(220, 38, 38, 0.85) !important;
        }
        .visual-scullion {
            position: absolute;
            width: 12px; height: 6px;
            background: #2e7d32;
            border: 1px solid #1b5e20;
            border-radius: 3px;
        }
        .visual-egg {
            position: absolute;
            top: 22px; left: 42px;
            width: 36px; height: 28px;
            background: #f8f9fa;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .visual-egg-yolk {
            width: 16px; height: 16px;
            background: #ff9800;
            border-radius: 50%;
        }
        .visual-pepper {
            position: absolute;
            width: 12px; height: 12px;
            border: 2px solid #c62828;
            border-radius: 50%;
        }
        .visual-meat {
            position: absolute;
            width: 26px; height: 10px;
            background: #8d6e63;
            border: 1px solid #4e342e;
            border-radius: 4px;
        }
        .visual-ricecake {
            position: absolute;
            width: 22px; height: 11px;
            background: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
        }

        .boiling-pot {
            animation: boilAnim 0.3초 infinite alternate;
        }
        @keyframes boilAnim {
            0% { transform: translateY(0px); }
            100% { transform: translateY(-2px); }
        }

        /* 하단 재료 선반 */
        #ingredient-shelf {
            position: absolute;
            bottom: 12px;
            left: 20px;
            right: 20px;
            height: 125px;
            background: #ffffff;
            border: 4px solid #ff69b4;
            border-radius: 20px;
            display: flex;
            justify-content: space-around;
            align-items: center;
            padding: 6px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .ingredient-card {
            width: 95px;
            height: 100px;
            background: #fff0f5;
            border: 3px solid #ffb6c1;
            border-radius: 12px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            cursor: grab;
            transition: all 0.2s;
        }
        .ingredient-card:hover {
            transform: translateY(-4px);
            background: #ffe4e1;
            border-color: #ff1493;
        }
        .ingredient-card:active { cursor: grabbing; }
        .ing-icon { font-size: 36px; }
        .ing-name { font-size: 12px; font-weight: bold; color: #333; margin-top: 2px; }

        /* 결과/안내 모달 */
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
            padding: 25px 35px;
            border-radius: 25px;
            border: 6px solid #ff1493;
            text-align: center;
            max-width: 420px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        .modal-title { font-size: 26px; color: #d8004e; font-weight: bold; margin-bottom: 12px; }
        .modal-desc { font-size: 16px; color: #333; margin-bottom: 20px; line-height: 1.4; white-space: pre-line; }
        .btn-restart {
            background: #ff1493; color: white; border: none; padding: 10px 28px;
            font-size: 16px; font-weight: bold; border-radius: 20px; cursor: pointer;
            box-shadow: 0 4px 0 #b3006b;
        }
        .btn-restart:hover { background: #e6006b; }
    </style>
</head>
<body>

<div id="game-container">
    <!-- 헤더 -->
    <div id="header">
        <div class="title-banner">🍜 슈의 라면가게 3.0 (4구 멀티 타이쿤)</div>
        <div class="info-box">💰 매출: <span id="score-text">0</span>원</div>
    </div>

    <!-- 라면 모양 말랑이 -->
    <div class="squishy-ramen" onclick="clickSquishy()">
        <span style="font-size: 28px;">🍜</span>
        <span style="font-size: 9px; color: #d8004e; font-weight: bold;">말랑이</span>
    </div>
    <div class="squishy-tag">말랑이 터치!</div>

    <!-- 손님 4명 동시 상주 영역 -->
    <div id="customers-container">
        <!-- JS로 4명 생성 -->
    </div>

    <!-- 주방 배경 -->
    <div id="kitchen-table"></div>

    <!-- 정수기 -->
    <div id="water-dispenser" ondragover="allowDrop(event)" ondrop="dropPotToDispenser(event)">
        <div class="dispenser-brand">PURE WATER</div>
        <div class="dispenser-spout"></div>
        <div class="water-stream-anim" id="water-stream"></div>
        <div class="dispenser-tray">💧 냄비를 여기로<br>끌어오세요!</div>
    </div>

    <!-- 4구 가스레인지 그리드 -->
    <div id="stove-grid">
        <div class="burner-slot" id="burner-0" ondragover="allowDrop(event)" ondrop="dropPotToStove(event, 0)">
            <div class="burner-ring"><div class="fire-anim" id="fire-0">🔥 🔥</div></div>
            <span style="font-size:11px; font-weight:bold; color:#555;">화구 1번</span>
        </div>
        <div class="burner-slot" id="burner-1" ondragover="allowDrop(event)" ondrop="dropPotToStove(event, 1)">
            <div class="burner-ring"><div class="fire-anim" id="fire-1">🔥 🔥</div></div>
            <span style="font-size:11px; font-weight:bold; color:#555;">화구 2번</span>
        </div>
        <div class="burner-slot" id="burner-2" ondragover="allowDrop(event)" ondrop="dropPotToStove(event, 2)">
            <div class="burner-ring"><div class="fire-anim" id="fire-2">🔥 🔥</div></div>
            <span style="font-size:11px; font-weight:bold; color:#555;">화구 3번</span>
        </div>
        <div class="burner-slot" id="burner-3" ondragover="allowDrop(event)" ondrop="dropPotToStove(event, 3)">
            <div class="burner-ring"><div class="fire-anim" id="fire-3">🔥 🔥</div></div>
            <span style="font-size:11px; font-weight:bold; color:#555;">화구 4번</span>
        </div>
    </div>

    <!-- 냄비 4개 (각 화구 전용) -->
    <div id="pots-layer">
        <!-- JS로 생성 -->
    </div>

    <!-- 하단 재료 선반 -->
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

    <!-- 안내 모달 -->
    <div id="modal-overlay">
        <div class="modal-box">
            <div class="modal-title" id="modal-title">알림</div>
            <div class="modal-desc" id="modal-desc">내용</div>
            <button class="btn-restart" onclick="closeModal()">확인</button>
        </div>
    </div>
</div>

<script>
    let score = 0;
    const avatars = ["👧", "👦", "👨", "👩", "👵", "👴"];
    const optionalIngredients = ["파", "계란", "고추", "고기", "떡"];

    // 4명 손님 데이터 배열 (각각 30초 개별 타이머 관리)
    let customersData = [
        { id: 0, avatar: "👧", order: [], timer: 30, interval: null },
        { id: 1, avatar: "👦", order: [], timer: 30, interval: null },
        { id: 2, avatar: "👨", order: [], timer: 30, interval: null },
        { id: 3, avatar: "👩", order: [], timer: 30, interval: null }
    ];

    // 4개 냄비 상태 관리
    let potsData = [
        { id: 0, isWaterFilled: false, burnerIdx: 0, isBoiling: false, ingredients: [] },
        { id: 1, isWaterFilled: false, burnerIdx: 1, isBoiling: false, ingredients: [] },
        { id: 2, isWaterFilled: false, burnerIdx: 2, isBoiling: false, ingredients: [] },
        { id: 3, isWaterFilled: false, burnerIdx: 3, isBoiling: false, ingredients: [] }
    ];

    window.onload = () => {
        initGame();
    };

    function initGame() {
        renderCustomerCards();
        renderPots();

        // 게임 시작 즉시 4명 손님 주문 부여 및 개별 타이머 시작
        for (let i = 0; i < 4; i++) {
            spawnCustomer(i);
        }
    }

    // 손님 카드 HTML 생성
    function renderCustomerCards() {
        const container = document.getElementById('customers-container');
        container.innerHTML = '';

        for (let i = 0; i < 4; i++) {
            container.innerHTML += `
                <div class="customer-card" id="customer-card-${i}" ondragover="allowDrop(event)" ondrop="dropPotToCustomer(event, ${i})">
                    <div class="customer-timer-badge" id="timer-badge-${i}">⏱️ 30s</div>
                    <div class="customer-avatar" id="avatar-${i}">👧</div>
                    <div class="speech-bubble" id="order-bubble-${i}">주문 생성 중...</div>
                </div>
            `;
        }
    }

    // 냄비 4개 생성 및 초기 위치 설정 (각 화구 위치)
    function renderPots() {
        const potsLayer = document.getElementById('pots-layer');
        potsLayer.innerHTML = '';

        for (let i = 0; i < 4; i++) {
            const potElem = document.createElement('div');
            potElem.className = 'pot-container';
            potElem.id = `pot-${i}`;
            potElem.draggable = true;
            potElem.setAttribute('ondragstart', `dragPot(event, ${i})`);
            potElem.setAttribute('ondragover', 'allowDrop(event)');
            potElem.setAttribute('ondrop', `dropIngredientToPot(event, ${i})`);

            potElem.innerHTML = `
                <div class="pot-handle-l"></div>
                <div class="pot-handle-r"></div>
                <div class="pot-body" id="pot-body-${i}">
                    <div class="pot-water-layer" id="pot-water-${i}"></div>
                    <div class="pot-ingredients-layer" id="pot-ing-layer-${i}"></div>
                </div>
            `;
            potsLayer.appendChild(potElem);
            positionPotToBurner(i, i);
        }
    }

    // 특정 손님 신규 주문 할당 & 30초 개별 타이머 가동
    function spawnCustomer(idx) {
        if (customersData[idx].interval) {
            clearInterval(customersData[idx].interval);
        }

        const randAvatar = avatars[Math.floor(Math.random() * avatars.length)];
        const shuffled = [...optionalIngredients].sort(() => 0.5 - Math.random());
        const selectedOpts = shuffled.slice(0, Math.floor(Math.random() * 3) + 1);
        const order = ["면", "라면스프", ...selectedOpts];

        customersData[idx].avatar = randAvatar;
        customersData[idx].order = order;
        customersData[idx].timer = 30;

        document.getElementById(`avatar-${idx}`).innerText = randAvatar;
        document.getElementById(`order-bubble-${idx}`).innerHTML = `<b>${order.join(', ')}</b> 주세요!`;
        
        updateTimerBadge(idx);

        // 30초 타이머
        customersData[idx].interval = setInterval(() => {
            customersData[idx].timer--;
            updateTimerBadge(idx);

            if (customersData[idx].timer <= 0) {
                clearInterval(customersData[idx].interval);
                showModal("❌ 손님 이탈!", `${idx + 1}번 자리에 앉은 손님이 30초 동안 라면이 안 나와 화를 내며 떠났습니다!`);
                spawnCustomer(idx); // 새 손님 교체
            }
        }, 1000);
    }

    function updateTimerBadge(idx) {
        const badge = document.getElementById(`timer-badge-${idx}`);
        if (!badge) return;
        badge.innerText = `⏱️ ${customersData[idx].timer}s`;
        if (customersData[idx].timer <= 7) {
            badge.classList.add('warning');
        } else {
            badge.classList.remove('warning');
        }
    }

    // 냄비 위치를 지정 화구 위치로 이동
    function positionPotToBurner(potIdx, burnerIdx) {
        const pot = document.getElementById(`pot-${potIdx}`);
        const leftPos = 175 + (burnerIdx * 195);
        pot.style.left = leftPos + "px";
        pot.style.top = "240px";
        potsData[potIdx].burnerIdx = burnerIdx;
    }

    // 말랑이 터치
    function clickSquishy() {
        const sq = document.querySelector('.squishy-ramen');
        sq.style.transform = 'scale(0.8) rotate(-10deg)';
        setTimeout(() => sq.style.transform = 'scale(1) rotate(0deg)', 150);
    }

    // Drag & Drop
    function allowDrop(ev) { ev.preventDefault(); }

    function dragPot(ev, potIdx) {
        ev.dataTransfer.setData("type", "pot");
        ev.dataTransfer.setData("potIdx", potIdx);
    }

    function dragIngredient(ev) {
        ev.dataTransfer.setData("type", "ingredient");
        ev.dataTransfer.setData("id", ev.target.id);
    }

    // 냄비를 정수기에 드롭
    function dropPotToDispenser(ev) {
        ev.preventDefault();
        const type = ev.dataTransfer.getData("type");
        if (type !== "pot") return;

        const potIdx = parseInt(ev.dataTransfer.getData("potIdx"));
        const pot = document.getElementById(`pot-${potIdx}`);
        pot.style.left = "12px";
        pot.style.top = "280px";

        if (!potsData[potIdx].isWaterFilled) {
            const stream = document.getElementById('water-stream');
            stream.style.height = "60px";
            setTimeout(() => {
                potsData[potIdx].isWaterFilled = true;
                document.getElementById(`pot-water-${potIdx}`).style.height = "60%";
                stream.style.height = "0px";
            }, 500);
        }
    }

    // 냄비를 특정 가스레인지 화구에 드롭
    function dropPotToStove(ev, burnerIdx) {
        ev.preventDefault();
        const type = ev.dataTransfer.getData("type");
        if (type !== "pot") return;

        const potIdx = parseInt(ev.dataTransfer.getData("potIdx"));
        positionPotToBurner(potIdx, burnerIdx);

        if (potsData[potIdx].isWaterFilled && !potsData[potIdx].isBoiling) {
            document.getElementById(`fire-${burnerIdx}`).style.display = 'block';
            setTimeout(() => {
                potsData[potIdx].isBoiling = true;
                document.getElementById(`pot-body-${potIdx}`).classList.add('boiling-pot');
            }, 800);
        }
    }

    // 냄비를 특정 손님에게 드롭 (제출)
    function dropPotToCustomer(ev, customerIdx) {
        ev.preventDefault();
        const type = ev.dataTransfer.getData("type");
        if (type !== "pot") return;

        const potIdx = parseInt(ev.dataTransfer.getData("potIdx"));
        const pData = potsData[potIdx];
        const cData = customersData[customerIdx];

        if (!pData.isWaterFilled || !pData.isBoiling) {
            alert("⚠️ 다 끓지 않은 라면을 줄 수 없습니다!");
            return;
        }

        // 주문 검증
        const hasAll = cData.order.every(item => pData.ingredients.includes(item));
        const hasExtra = pData.ingredients.some(item => !cData.order.includes(item));

        if (hasAll && !hasExtra) {
            const earned = 4000;
            score += earned;
            document.getElementById('score-text').innerText = score;
            showModal("🎉 제출 성공!", `${customerIdx + 1}번 손님이 주문하신 완벽한 라면입니다!\n매출 +${earned}원!`);
        } else if (hasAll && hasExtra) {
            const earned = 2000;
            score += earned;
            document.getElementById('score-text').innerText = score;
            showModal("🙂 부분 성공", `원치 않는 재료가 섞였지만 맛있게 먹습니다!\n매출 +${earned}원`);
        } else {
            showModal("😭 조리 실패!", `손님이 요구한 재료가 부족합니다!\n요청: [${cData.order.join(', ')}]`);
        }

        // 해당 손님 및 냄비 리셋
        resetPot(potIdx);
        spawnCustomer(customerIdx);
    }

    // 냄비에 재료 드롭
    function dropIngredientToPot(ev, potIdx) {
        ev.preventDefault();
        const type = ev.dataTransfer.getData("type");
        if (type !== "ingredient") return;

        const pData = potsData[potIdx];
        if (!pData.isWaterFilled) {
            alert("⚠️ 정수기에서 물을 먼저 받아주세요!");
            return;
        }
        if (!pData.isBoiling) {
            alert("⚠️ 냄비를 화구에 올려 물을 먼저 끓여주세요!");
            return;
        }

        const id = ev.dataTransfer.getData("id");
        const ingName = document.getElementById(id).getAttribute('data-name');

        if (pData.ingredients.includes(ingName)) {
            alert(`⚠️ '${ingName}'은(는) 이미 넣었습니다!`);
            return;
        }

        pData.ingredients.push(ingName);
        renderVisualIngredient(potIdx, ingName);
    }

    // 리얼 그래픽 재료 요소 렌더링
    function renderVisualIngredient(potIdx, name) {
        const layer = document.getElementById(`pot-ing-layer-${potIdx}`);

        if (name === "면") {
            const noodle = document.createElement('div');
            noodle.className = 'visual-noodle';
            layer.appendChild(noodle);
        } else if (name === "라면스프") {
            document.getElementById(`pot-water-${potIdx}`).classList.add('visual-soup-color');
        } else if (name === "파") {
            for (let i = 0; i < 4; i++) {
                const sc = document.createElement('div');
                sc.className = 'visual-scullion';
                sc.style.top = (20 + Math.random() * 30) + 'px';
                sc.style.left = (20 + Math.random() * 70) + 'px';
                sc.style.transform = `rotate(${Math.random()*180}deg)`;
                layer.appendChild(sc);
            }
        } else if (name === "계란") {
            const egg = document.createElement('div');
            egg.className = 'visual-egg';
            egg.innerHTML = '<div class="visual-egg-yolk"></div>';
            layer.appendChild(egg);
        } else if (name === "고추") {
            for (let i = 0; i < 3; i++) {
                const pep = document.createElement('div');
                pep.className = 'visual-pepper';
                pep.style.top = (25 + Math.random() * 25) + 'px';
                pep.style.left = (20 + Math.random() * 80) + 'px';
                layer.appendChild(pep);
            }
        } else if (name === "고기") {
            for (let i = 0; i < 2; i++) {
                const meat = document.createElement('div');
                meat.className = 'visual-meat';
                meat.style.top = (30 + Math.random() * 20) + 'px';
                meat.style.left = (30 + Math.random() * 60) + 'px';
                layer.appendChild(meat);
            }
        } else if (name === "떡") {
            for (let i = 0; i < 3; i++) {
                const rc = document.createElement('div');
                rc.className = 'visual-ricecake';
                rc.style.top = (25 + Math.random() * 25) + 'px';
                rc.style.left = (20 + Math.random() * 70) + 'px';
                layer.appendChild(rc);
            }
        }
    }

    // 냄비 리셋
    function resetPot(potIdx) {
        potsData[potIdx].isWaterFilled = false;
        potsData[potIdx].isBoiling = false;
        potsData[potIdx].ingredients = [];

        document.getElementById(`pot-water-${potIdx}`).style.height = "0%";
        document.getElementById(`pot-water-${potIdx}`).classList.remove('visual-soup-color');
        document.getElementById(`pot-ing-layer-${potIdx}`).innerHTML = '';
        document.getElementById(`fire-${potsData[potIdx].burnerIdx}`).style.display = 'none';
        document.getElementById(`pot-body-${potIdx}`).classList.remove('boiling-pot');

        positionPotToBurner(potIdx, potIdx);
    }

    // 모달창
    function showModal(title, msg) {
        document.getElementById('modal-title').innerText = title;
        document.getElementById('modal-desc').innerText = msg;
        document.getElementById('modal-overlay').style.display = 'flex';
    }

    function closeModal() {
        document.getElementById('modal-overlay').style.display = 'none';
    }
</script>
</body>
</html>
"""

st.markdown("<h2 style='text-align: center; color: #ff1493;'>🍜 슈의 라면가게 3.0 (4구 멀티 타이쿤) 🍜</h2>", unsafe_allow_html=True)

# Streamlit Canvas 컴포넌트 출력
components.html(game_html, height=750, scrolling=False)
```
