import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="슈의 4구 라면가게 타이쿤 🍜",
    page_icon="🍜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 파이썬 문법 에러를 완벽히 방지하는 Raw String 단일 코드 블록
GAME_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>슈의 라면가게</title>
    <style>
        * { box-sizing: border-box; user-select: none; font-family: 'Comic Sans MS', sans-serif; }
        body { margin: 0; padding: 5px; background-color: #ffeff5; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        #game-container { position: relative; width: 1020px; height: 750px; background: linear-gradient(135deg, #ffd1dc 0%, #ffe4e1 100%); border: 8px solid #ff69b4; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); overflow: hidden; }
        #header { position: absolute; top: 10px; left: 20px; right: 20px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }
        .title-banner { background: #ff3366; color: white; padding: 6px 18px; border-radius: 25px; font-size: 19px; font-weight: bold; box-shadow: 3px 3px 0px #b3003b; }
        
        .header-right { display: flex; align-items: center; gap: 10px; }
        .score-box { background: #fff; border: 3px solid #ff69b4; padding: 5px 15px; border-radius: 15px; font-size: 18px; font-weight: bold; color: #d8004e; }
        .break-btn { background: #9c27b0; color: white; border: 3px solid #7b1fa2; padding: 6px 14px; border-radius: 15px; font-size: 15px; font-weight: bold; cursor: pointer; box-shadow: 0 3px 0 #6a1b9a; }
        .break-btn:active { transform: translateY(2px); box-shadow: 0 1px 0 #6a1b9a; }
        
        #customer-bar { position: absolute; top: 65px; left: 20px; right: 20px; height: 115px; display: flex; justify-content: space-between; gap: 15px; z-index: 15; }
        .customer-card { flex: 1; background: white; border: 4px solid #ff80ab; border-radius: 15px; padding: 6px; display: flex; flex-direction: column; align-items: center; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .customer-timer { width: 100%; height: 8px; background: #eee; border-radius: 4px; margin: 3px 0; overflow: hidden; }
        .customer-timer-bar { width: 100%; height: 100%; background: #2ed573; transition: width 0.3s linear; }
        .order-tag { display: inline-block; background: #ffebee; color: #c62828; padding: 1px 5px; border-radius: 4px; margin: 1px; font-size: 11px; font-weight: bold; border: 1px solid #ffcdd2; }

        #kitchen-table { position: absolute; bottom: 0; width: 100%; height: 550px; background: #f7d6b5; border-top: 10px solid #e0a96d; }
        
        #utility-zone { position: absolute; top: 190px; left: 20px; width: 100px; display: flex; flex-direction: column; gap: 15px; }
        #water-dispenser { width: 100%; height: 110px; background: #eceff1; border: 4px solid #90a4ae; border-radius: 12px; display: flex; flex-direction: column; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        #trash-can { width: 100%; height: 100px; background: #ffcdd2; border: 4px solid #e57373; border-radius: 12px; display: flex; flex-direction: column; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        
        #stoves-container { position: absolute; top: 190px; left: 135px; width: 440px; height: 230px; display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; padding: 12px; background: #cfd8dc; border: 5px solid #78909c; border-radius: 15px; }
        .stove-slot { position: relative; width: 195px; height: 95px; background: #b0bec5; border: 3px dashed #546e7a; border-radius: 10px; display: flex; justify-content: center; align-items: center; }

        .pot { position: relative; width: 165px; height: 80px; background: linear-gradient(135deg, #ffd700 0%, #e6b800 100%); border: 5px solid #b8860b; border-radius: 0 0 50px 50px; cursor: grab; overflow: hidden; display: flex; justify-content: center; align-items: flex-end; box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
        .pot:active { cursor: grabbing; }
        .pot-water { position: absolute; bottom: 0; width: 100%; height: 0%; background: rgba(64, 196, 255, 0.6); transition: height 0.3s, background-color 0.5s; }
        
        .pot.boiling-anim { animation: potShake 0.3s infinite alternate ease-in-out; }
        @keyframes potShake {
            0% { transform: translateY(0px); }
            100% { transform: translateY(-2px); }
        }
        .bubble {
            position: absolute;
            background: rgba(255, 255, 255, 0.85);
            border-radius: 50%;
            animation: bubbleUp 0.6s infinite ease-in;
        }
        @keyframes bubbleUp {
            0% { bottom: 5px; opacity: 1; transform: scale(0.5); }
            100% { bottom: 45px; opacity: 0; transform: scale(1.3); }
        }

        .boil-timer-tag { position: absolute; top: 5px; background: rgba(0,0,0,0.7); color: #fff; padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: bold; z-index: 10; display: none; }

        .ramen-noodle-layer {
            position: absolute; bottom: 5px; width: 130px; height: 40px;
            background: #fbc02d; border-radius: 20px; display: none;
            box-shadow: inset 0 3px 6px rgba(0,0,0,0.3);
            background-image: radial-gradient(#f57f17 25%, transparent 25%), radial-gradient(#f57f17 25%, transparent 25%);
            background-size: 12px 12px; background-position: 0 0, 6px 6px;
        }
        .pot-toppings { position: absolute; bottom: 12px; display: flex; gap: 4px; z-index: 5; justify-content: center; align-items: center; max-width: 140px; flex-wrap: wrap; }
        
        .vis-scullion { width: 22px; height: 8px; background: #2e7d32; border-radius: 4px; transform: rotate(-15deg); border: 1px solid #1b5e20; display: inline-block; }
        .vis-egg { width: 28px; height: 20px; background: #ffffff; border-radius: 50%; display: flex; justify-content: center; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }
        .vis-egg-yolk { width: 12px; height: 12px; background: #ff9800; border-radius: 50%; }
        .vis-pepper { width: 18px; height: 8px; background: #d32f2f; border-radius: 4px; transform: rotate(20deg); border: 1px solid #b71c1c; display: inline-block; }
        .vis-meat { width: 30px; height: 14px; background: #8d6e63; border-radius: 6px; border: 2px solid #4e342e; display: inline-block; }
        .vis-ricecake { width: 24px; height: 12px; background: #fff8e1; border-radius: 10px; border: 1px solid #d7ccc8; transform: rotate(-5deg); display: inline-block; }

        #serve-buttons-container { position: absolute; top: 430px; left: 135px; width: 440px; display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; }
        .serve-btn { background: #2ed573; color: white; border: none; padding: 10px; font-size: 14px; font-weight: bold; border-radius: 10px; cursor: pointer; box-shadow: 0 3px 0 #1b9e54; }
        .serve-btn:active { transform: translateY(2px); box-shadow: 0 1px 0 #1b9e54; }

        #ingredient-shelf { position: absolute; bottom: 15px; left: 20px; right: 20px; height: 110px; background: #fff; border: 4px solid #ff80ab; border-radius: 15px; display: flex; justify-content: space-around; align-items: center; padding: 5px; }
        .ingredient { width: 75px; height: 90px; background: #fff0f5; border: 3px solid #ffb6c1; border-radius: 10px; display: flex; flex-direction: column; justify-content: center; align-items: center; cursor: grab; transition: transform 0.1s; }
        .ingredient:hover { transform: translateY(-3px); background: #ffe4e1; }
        .ingredient:active { cursor: grabbing; }

        #status-bubble { position: absolute; top: 190px; right: 20px; width: 400px; height: 230px; background: white; border: 4px solid #ff69b4; border-radius: 15px; padding: 14px; font-size: 13px; font-weight: bold; overflow-y: auto; box-shadow: 0 4px 10px rgba(0,0,0,0.1); color: #333; line-height: 1.5; }

        /* 브레이크 타임 (일시정지) 모달창 스타일 */
        #break-modal {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.65);
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 100;
        }
        .break-modal-box {
            background: white;
            padding: 35px 50px;
            border-radius: 25px;
            border: 6px solid #9c27b0;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        .resume-btn {
            background: #9c27b0;
            color: white;
            border: none;
            padding: 12px 30px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 25px;
            cursor: pointer;
            box-shadow: 0 4px 0 #6a1b9a;
            margin-top: 15px;
        }
        .resume-btn:hover { background: #8e24aa; }
    </style>
</head>
<body>
<div id="game-container">
    <div id="header">
        <div class="title-banner">🍜 슈의 4구 라면가게 (브레이크타임 기능)</div>
        <div class="header-right">
            <button class="break-btn" onclick="toggleBreakTime()">☕ 브레이크 타임</button>
            <div class="score-box">💰 매출: <span id="score">0</span>원</div>
        </div>
    </div>

    <div id="customer-bar">
        <div class="customer-card"><div style="font-size:24px;">👧</div><div style="font-size:11px; color:#d8004e; font-weight:bold;" id="c-text-0">01:30</div><div class="customer-timer"><div class="customer-timer-bar" id="c-timer-0" style="width:100%;"></div></div><div id="c-order-0">주문 대기중</div></div>
        <div class="customer-card"><div style="font-size:24px;">👦</div><div style="font-size:11px; color:#d8004e; font-weight:bold;" id="c-text-1">01:30</div><div class="customer-timer"><div class="customer-timer-bar" id="c-timer-1" style="width:100%;"></div></div><div id="c-order-1">주문 대기중</div></div>
        <div class="customer-card"><div style="font-size:24px;">👨</div><div style="font-size:11px; color:#d8004e; font-weight:bold;" id="c-text-2">01:30</div><div class="customer-timer"><div class="customer-timer-bar" id="c-timer-2" style="width:100%;"></div></div><div id="c-order-2">주문 대기중</div></div>
        <div class="customer-card"><div style="font-size:24px;">👵</div><div style="font-size:11px; color:#d8004e; font-weight:bold;" id="c-text-3">01:30</div><div class="customer-timer"><div class="customer-timer-bar" id="c-timer-3" style="width:100%;"></div></div><div id="c-order-3">주문 대기중</div></div>
    </div>

    <div id="kitchen-table"></div>

    <div id="utility-zone">
        <div id="water-dispenser" ondragover="event.preventDefault()" ondrop="fillWater(event)">
            <div style="font-size: 11px; font-weight: bold; color: #546e7a;">💧 정수기</div>
            <div style="font-size: 26px;">🚰</div>
        </div>
        <div id="trash-can" ondragover="event.preventDefault()" ondrop="trashPot(event)">
            <div style="font-size: 11px; font-weight: bold; color: #c62828;">🗑️ 쓰레기통</div>
            <div style="font-size: 26px;">🗑️</div>
            <div style="font-size: 9px; color: #d32f2f; font-weight: bold;">(드롭하여 폐기)</div>
        </div>
    </div>

    <div id="stoves-container">
        <div class="stove-slot" ondragover="event.preventDefault()" ondrop="dropStove(event, 0)">
            <div class="pot" id="pot-0" draggable="true" ondragstart="dragPot(event, 0)">
                <div class="boil-timer-tag" id="btimer-0">🔥 10초</div>
                <div class="pot-water" id="pw-0"></div>
                <div class="ramen-noodle-layer" id="nd-0"></div>
                <div class="pot-toppings" id="tp-0"></div>
            </div>
        </div>
        <div class="stove-slot" ondragover="event.preventDefault()" ondrop="dropStove(event, 1)">
            <div class="pot" id="pot-1" draggable="true" ondragstart="dragPot(event, 1)">
                <div class="boil-timer-tag" id="btimer-1">🔥 10초</div>
                <div class="pot-water" id="pw-1"></div>
                <div class="ramen-noodle-layer" id="nd-1"></div>
                <div class="pot-toppings" id="tp-1"></div>
            </div>
        </div>
        <div class="stove-slot" ondragover="event.preventDefault()" ondrop="dropStove(event, 2)">
            <div class="pot" id="pot-2" draggable="true" ondragstart="dragPot(event, 2)">
                <div class="boil-timer-tag" id="btimer-2">🔥 10초</div>
                <div class="pot-water" id="pw-2"></div>
                <div class="ramen-noodle-layer" id="nd-2"></div>
                <div class="pot-toppings" id="tp-2"></div>
            </div>
        </div>
        <div class="stove-slot" ondragover="event.preventDefault()" ondrop="dropStove(event, 3)">
            <div class="pot" id="pot-3" draggable="true" ondragstart="dragPot(event, 3)">
                <div class="boil-timer-tag" id="btimer-3">🔥 10초</div>
                <div class="pot-water" id="pw-3"></div>
                <div class="ramen-noodle-layer" id="nd-3"></div>
                <div class="pot-toppings" id="tp-3"></div>
            </div>
        </div>
    </div>

    <div id="serve-buttons-container">
        <button class="serve-btn" onclick="serve(0)">👧 1번 손님 제출</button>
        <button class="serve-btn" onclick="serve(1)">👦 2번 손님 제출</button>
        <button class="serve-btn" onclick="serve(2)">👨 3번 손님 제출</button>
        <button class="serve-btn" onclick="serve(3)">👵 4번 손님 제출</button>
    </div>

    <div id="status-bubble">
        🎮 <b>게임 가이드:</b><br>
        1. 상단의 <b>[☕ 브레이크 타임]</b> 버튼을 누르면 시간이 일시정지됩니다!<br>
        2. 정수기 물 받기 ➔ 10초 끓이기 ➔ 재료 투입 후 손님에게 서빙하세요.
    </div>

    <div id="ingredient-shelf">
        <div class="ingredient" draggable="true" ondragstart="dragIng(event, '면')"><div style="font-size:32px;">🍜</div><div style="font-size:11px;font-weight:bold;">면</div></div>
        <div class="ingredient" draggable="true" ondragstart="dragIng(event, '라면스프')"><div style="font-size:32px;">🧂</div><div style="font-size:11px;font-weight:bold;">스프</div></div>
        <div class="ingredient" draggable="true" ondragstart="dragIng(event, '파')"><div style="font-size:32px;">🥬</div><div style="font-size:11px;font-weight:bold;">파</div></div>
        <div class="ingredient" draggable="true" ondragstart="dragIng(event, '계란')"><div style="font-size:32px;">🥚</div><div style="font-size:11px;font-weight:bold;">계란</div></div>
        <div class="ingredient" draggable="true" ondragstart="dragIng(event, '고추')"><div style="font-size:32px;">🌶️</div><div style="font-size:11px;font-weight:bold;">고추</div></div>
        <div class="ingredient" draggable="true" ondragstart="dragIng(event, '고기')"><div style="font-size:32px;">🥩</div><div style="font-size:11px;font-weight:bold;">고기</div></div>
        <div class="ingredient" draggable="true" ondragstart="dragIng(event, '떡')"><div style="font-size:32px;">🍡</div><div style="font-size:11px;font-weight:bold;">떡</div></div>
    </div>

    <!-- 브레이크 타임 (일시정지) 모달창 -->
    <div id="break-modal">
        <div class="break-modal-box">
            <h2 style="color: #9c27b0; margin-top: 0;">☕ 브레이크 타임 (영업 일시정지)</h2>
            <p style="font-size: 16px; color: #444; margin-bottom: 25px;">잠시 숨을 고르는 중입니다.<br>타이머와 손님 대기 시간이 멈춰있습니다.</p>
            <button class="resume-btn" onclick="toggleBreakTime()">☕ 영업 재개하기</button>
        </div>
    </div>
</div>

<script>
    const TIME_LIMIT = 90;
    
    let score = 0;
    let isPaused = false; // 일시정지 상태 플래그

    let pots = [
        {water: 0, boiling: false, boilTimeLeft: 0, boilInterval: null, bubbleInterval: null, contents: []},
        {water: 0, boiling: false, boilTimeLeft: 0, boilInterval: null, bubbleInterval: null, contents: []},
        {water: 0, boiling: false, boilTimeLeft: 0, boilInterval: null, bubbleInterval: null, contents: []},
        {water: 0, boiling: false, boilTimeLeft: 0, boilInterval: null, bubbleInterval: null, contents: []}
    ];
    let customers = [null, null, null, null];
    let timers = [null, null, null, null];
    let timeLE = [TIME_LIMIT, TIME_LIMIT, TIME_LIMIT, TIME_LIMIT];
    let dragPotIdx = null;
    let dragIngName = null;

    function fmt(s) {
        let m = Math.floor(s / 60);
        let sec = s % 60;
        return `${m < 10 ? '0' : ''}${m}:${sec < 10 ? '0' : ''}${sec}`;
    }

    function logMsg(msg) {
        let b = document.getElementById('status-bubble');
        b.innerHTML = msg + "<br>" + b.innerHTML;
    }

    // 브레이크 타임 토글 함수 (일시정지 / 재개)
    function toggleBreakTime() {
        isPaused = !isPaused;
        let modal = document.getElementById('break-modal');
        if (isPaused) {
            modal.style.display = 'flex';
            logMsg("☕ 브레이크 타임 진입: 시간이 일시정지되었습니다.");
        } else {
            modal.style.display = 'none';
            logMsg("🔔 영업이 재개되었습니다!");
        }
    }

    function init() {
        for(let i=0; i<4; i++) {
            resetPotObj(i);
            updatePot(i);
            genCust(i);
        }
    }

    function resetPotObj(i) {
        if(pots[i]) {
            if(pots[i].boilInterval) clearInterval(pots[i].boilInterval);
            if(pots[i].bubbleInterval) clearInterval(pots[i].bubbleInterval);
        }
        pots[i] = {water: 0, boiling: false, boilTimeLeft: 0, boilInterval: null, bubbleInterval: null, contents: []};
        let potElem = document.getElementById(`pot-${i}`);
        if(potElem) potElem.classList.remove('boiling-anim');
        let btag = document.getElementById(`btimer-${i}`);
        if(btag) btag.style.display = 'none';
    }

    function genCust(i) {
        clearInterval(timers[i]);
        timeLE[i] = TIME_LIMIT;
        
        let order = ["면", "라면스프"];
        let optional = ["파", "계란", "고추", "고기", "떡"];
        let count = Math.floor(Math.random() * 3) + 1;
        let shuffled = optional.sort(() => 0.5 - Math.random());
        for(let k=0; k<count; k++) {
            order.push(shuffled[k]);
        }
        
        customers[i] = order;
        
        let html = "";
        order.forEach(o => html += `<span class="order-tag">${o}</span>`);
        document.getElementById(`c-order-${i}`).innerHTML = html;

        timers[i] = setInterval(() => {
            if (isPaused) return; // 일시정지 중이면 손님 타이머도 대기

            timeLE[i]--;
            document.getElementById(`c-text-${i}`).innerText = fmt(timeLE[i]);
            document.getElementById(`c-timer-${i}`).style.width = (timeLE[i] / TIME_LIMIT * 100) + '%';
            
            if(timeLE[i] <= 0) {
                score = Math.max(0, score - 500);
                document.getElementById('score').innerText = score;
                logMsg(`⏰ ${i+1}번 손님이 지쳐 떠났습니다! (-500원)`);
                genCust(i);
            }
        }, 1000);
    }

    function dragPot(e, idx) { dragPotIdx = idx; }

    function fillWater(e) {
        e.preventDefault();
        if(dragPotIdx !== null) {
            let idx = dragPotIdx;
            resetPotObj(idx);
            pots[idx].water = 100;
            updatePot(idx);
            start10SecBoil(idx);
            dragPotIdx = null;
        }
    }

    function trashPot(e) {
        e.preventDefault();
        if(dragPotIdx !== null) {
            resetPotObj(dragPotIdx);
            updatePot(dragPotIdx);
            logMsg(`🗑️ ${dragPotIdx+1}번 냄비를 폐기했습니다.`);
            dragPotIdx = null;
        }
    }

    function dropStove(e, idx) {
        e.preventDefault();
        if(dragPotIdx !== null) {
            let src = dragPotIdx;
            let temp = pots[src];
            pots[src] = pots[idx];
            pots[idx] = temp;
            
            updatePot(src);
            updatePot(idx);
            dragPotIdx = null;
        }
    }

    // 10초 끓이기 타이머 (브레이크 타임 연동)
    function start10SecBoil(idx) {
        pots[idx].boilTimeLeft = 10;
        let btag = document.getElementById(`btimer-${idx}`);
        btag.style.display = 'block';
        btag.innerText = `🔥 10초`;
        logMsg(`💧 ${idx+1}번 냄비 물 투입! 10초 후 보글보글 끓습니다.`);

        pots[idx].boilInterval = setInterval(() => {
            if (isPaused) return; // 일시정지 중이면 끓이기 타이머도 정지

            pots[idx].boilTimeLeft--;
            btag.innerText = `🔥 ${pots[idx].boilTimeLeft}초`;
            
            if(pots[idx].boilTimeLeft <= 0) {
                clearInterval(pots[idx].boilInterval);
                pots[idx].boiling = true;
                btag.style.display = 'none';
                
                document.getElementById(`pw-${idx}`).style.backgroundColor = 'rgba(255, 152, 0, 0.75)';
                document.getElementById(`pot-${idx}`).classList.add('boiling-anim');
                
                startBubbling(idx);
                logMsg(`♨️ ${idx+1}번 냄비 물이 보글보글 끓습니다! 재료 투입 가능!`);
            }
        }, 1000);
    }

    function startBubbling(idx) {
        let pWater = document.getElementById(`pw-${idx}`);
        pots[idx].bubbleInterval = setInterval(() => {
            if(isPaused || !pots[idx].boiling) return;
            let bubble = document.createElement('div');
            bubble.className = 'bubble';
            let size = Math.random() * 8 + 6;
            bubble.style.width = size + 'px';
            bubble.style.height = size + 'px';
            bubble.style.left = (Math.random() * 80 + 10) + '%';
            pWater.appendChild(bubble);

            setTimeout(() => bubble.remove(), 600);
        }, 150);
    }

    function dragIng(e, name) { dragIngName = name; }

    document.addEventListener("DOMContentLoaded", () => {
        for(let i=0; i<4; i++) {
            let slot = document.querySelectorAll('.stove-slot')[i];
            slot.addEventListener('dragover', (e) => e.preventDefault());
            slot.addEventListener('drop', (e) => {
                e.preventDefault();
                if(dragIngName) {
                    if(pots[i].water < 100) {
                        logMsg("⚠️ 정수기에서 물을 먼저 받아주세요!");
                        dragIngName = null;
                        return;
                    }
                    if(!pots[i].boiling) {
                        logMsg("⚠️ 아직 10초가 지나지 않아 물이 끓지 않았습니다!");
                        dragIngName = null;
                        return;
                    }
                    if(!pots[i].contents.includes(dragIngName)) {
                        pots[i].contents.push(dragIngName);
                        updatePot(i);
                        logMsg(`✨ ${i+1}번 냄비에 '${dragIngName}' 투입 완료!`);
                    } else {
                        logMsg(`⚠️ 이미 '${dragIngName}'이(가) 들어있습니다.`);
                    }
                    dragIngName = null;
                }
            });
        }
        init();
    });

    function updatePot(i) {
        let p = pots[i];
        document.getElementById(`pw-${i}`).style.height = p.water + '%';
        let nd = document.getElementById(`nd-${i}`);
        let tp = document.getElementById(`tp-${i}`);
        tp.innerHTML = '';

        if(p.contents.includes("면")) {
            nd.style.display = 'block';
            if(p.contents.includes("라면스프")) {
                document.getElementById(`pw-${i}`).style.backgroundColor = 'rgba(211, 47, 47, 0.85)';
            }
        } else {
            nd.style.display = 'none';
        }

        p.contents.forEach(item => {
            if(item !== "면" && item !== "라면스프") {
                let elem = document.createElement('div');
                if(item === "파") elem.className = 'vis-scullion';
                else if(item === "계란") {
                    elem.className = 'vis-egg';
                    elem.innerHTML = '<div class="vis-egg-yolk"></div>';
                }
                else if(item === "고추") elem.className = 'vis-pepper';
                else if(item === "고기") elem.className = 'vis-meat';
                else if(item === "떡") elem.className = 'vis-ricecake';
                
                tp.appendChild(elem);
            }
        });
    }

    function serve(i) {
        let p = pots[i];
        if(!p.boiling || p.contents.length === 0) {
            logMsg(`⚠️ ${i+1}번 화구에 제출할 완성된 라면이 없습니다!`);
            return;
        }
        
        let order = customers[i];
        let userContents = p.contents;

        let correctCount = 0;
        let penaltyCount = 0;

        userContents.forEach(item => {
            if(order.includes(item)) correctCount++;
            else penaltyCount++;
        });

        let missingCount = order.length - correctCount;
        let earned = (correctCount * 500) - (missingCount * 300) - (penaltyCount * 300);
        earned = Math.max(200, earned);

        if(missingCount === 0 && penaltyCount === 0) {
            score += 2000 + earned;
            logMsg(`🎉 ${i+1}번 손님 대만족! 완벽 맞춤 라면 서빙! (+${2000+earned}원)`);
        } else {
            score += earned;
            logMsg(`👍 ${i+1}번 손님 서빙 완료 (+${earned}원)`);
        }

        document.getElementById('score').innerText = score;
        resetPotObj(i);
        updatePot(i);
        genCust(i);
    }
</script>
</body>
</html>
"""

st.markdown("<h2 style='text-align: center; color: #ff3366;'>🍜 슈의 4구 라면가게 (브레이크타임 일시정지) 🍜</h2>", unsafe_allow_html=True)
components.html(GAME_HTML, height=780, scrolling=False)
