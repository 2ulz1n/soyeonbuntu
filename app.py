import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="슈의 4구 라면가게 타이쿤 🍜",
    page_icon="🍜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 파이썬 문법 에러를 방지하는 완전 안전 Raw String HTML/JS
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
        .title-banner { background: #ff3366; color: white; padding: 6px 18px; border-radius: 25px; font-size: 20px; font-weight: bold; box-shadow: 3px 3px 0px #b3003b; }
        .score-box { background: #fff; border: 3px solid #ff69b4; padding: 5px 15px; border-radius: 15px; font-size: 18px; font-weight: bold; color: #d8004e; }
        
        #customer-bar { position: absolute; top: 65px; left: 20px; right: 20px; height: 115px; display: flex; justify-content: space-between; gap: 15px; z-index: 15; }
        .customer-card { flex: 1; background: white; border: 4px solid #ff80ab; border-radius: 15px; padding: 6px; display: flex; flex-direction: column; align-items: center; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .customer-timer { width: 100%; height: 8px; background: #eee; border-radius: 4px; margin: 3px 0; overflow: hidden; }
        .customer-timer-bar { width: 100%; height: 100%; background: #2ed573; transition: width 0.3s linear; }
        .order-tag { display: inline-block; background: #ffebee; color: #c62828; padding: 1px 5px; border-radius: 4px; margin: 1px; font-size: 11px; font-weight: bold; border: 1px solid #ffcdd2; }

        #kitchen-table { position: absolute; bottom: 0; width: 100%; height: 550px; background: #f7d6b5; border-top: 10px solid #e0a96d; }
        
        /* 왼쪽 도구 존 (정수기 & 쓰레기통) */
        #utility-zone { position: absolute; top: 195px; left: 20px; width: 100px; display: flex; flex-direction: column; gap: 15px; }
        #water-dispenser { width: 100%; height: 110px; background: #eceff1; border: 4px solid #90a4ae; border-radius: 12px; display: flex; flex-direction: column; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        #trash-can { width: 100%; height: 100px; background: #ffcdd2; border: 4px solid #e57373; border-radius: 12px; display: flex; flex-direction: column; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        
        /* 확대된 4구 가스레인지 */
        #stoves-container { position: absolute; top: 190px; left: 135px; width: 440px; height: 230px; display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; padding: 12px; background: #cfd8dc; border: 5px solid #78909c; border-radius: 15px; }
        .stove-slot { position: relative; width: 195px; height: 95px; background: #b0bec5; border: 3px dashed #546e7a; border-radius: 10px; display: flex; justify-content: center; align-items: center; }

        /* 확대된 냄비 스타일 */
        .pot { position: relative; width: 165px; height: 80px; background: linear-gradient(135deg, #ffd700 0%, #e6b800 100%); border: 5px solid #b8860b; border-radius: 0 0 50px 50px; cursor: grab; overflow: hidden; display: flex; justify-content: center; align-items: flex-end; box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
        .pot:active { cursor: grabbing; }
        .pot-water { position: absolute; bottom: 0; width: 100%; height: 0%; background: rgba(64, 196, 255, 0.6); transition: height 0.3s; }
        .ramen-noodle-layer { position: absolute; bottom: 5px; width: 120px; height: 35px; background: #fbc02d; border-radius: 15px; display: none; box-shadow: inset 0 2px 4px rgba(0,0,0,0.2); }
        .pot-toppings { position: absolute; bottom: 20px; display: flex; gap: 3px; z-index: 5; justify-content: center; max-width: 130px; flex-wrap: wrap; }
        .topping-item { font-size: 20px; }

        /* 서빙 버튼 */
        #serve-buttons-container { position: absolute; top: 430px; left: 135px; width: 440px; display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; }
        .serve-btn { background: #2ed573; color: white; border: none; padding: 10px; font-size: 14px; font-weight: bold; border-radius: 10px; cursor: pointer; box-shadow: 0 3px 0 #1b9e54; }
        .serve-btn:active { transform: translateY(2px); box-shadow: 0 1px 0 #1b9e54; }

        /* 재료 선반 */
        #ingredient-shelf { position: absolute; bottom: 15px; left: 20px; right: 20px; height: 110px; background: #fff; border: 4px solid #ff80ab; border-radius: 15px; display: flex; justify-content: space-around; align-items: center; padding: 5px; }
        .ingredient { width: 75px; height: 90px; background: #fff0f5; border: 3px solid #ffb6c1; border-radius: 10px; display: flex; flex-direction: column; justify-content: center; align-items: center; cursor: grab; transition: transform 0.1s; }
        .ingredient:hover { transform: translateY(-3px); background: #ffe4e1; }
        .ingredient:active { cursor: grabbing; }

        /* 우측 메시지 안내창 */
        #status-bubble { position: absolute; top: 190px; right: 20px; width: 400px; height: 230px; background: white; border: 4px solid #ff69b4; border-radius: 15px; padding: 14px; font-size: 13px; font-weight: bold; overflow-y: auto; box-shadow: 0 4px 10px rgba(0,0,0,0.1); color: #333; line-height: 1.5; }
    </style>
</head>
<body>
<div id="game-container">
    <div id="header">
        <div class="title-banner">🍜 슈의 4구 라면가게 (확대 화구 & 쓰레기통)</div>
        <div class="score-box">💰 매출: <span id="score">0</span>원</div>
    </div>

    <div id="customer-bar">
        <div class="customer-card"><div style="font-size:24px;">👧</div><div style="font-size:11px; color:#d8004e; font-weight:bold;" id="c-text-0">01:30</div><div class="customer-timer"><div class="customer-timer-bar" id="c-timer-0" style="width:100%;"></div></div><div id="c-order-0">주문 대기중</div></div>
        <div class="customer-card"><div style="font-size:24px;">👦</div><div style="font-size:11px; color:#d8004e; font-weight:bold;" id="c-text-1">01:30</div><div class="customer-timer"><div class="customer-timer-bar" id="c-timer-1" style="width:100%;"></div></div><div id="c-order-1">주문 대기중</div></div>
        <div class="customer-card"><div style="font-size:24px;">👨</div><div style="font-size:11px; color:#d8004e; font-weight:bold;" id="c-text-2">01:30</div><div class="customer-timer"><div class="customer-timer-bar" id="c-timer-2" style="width:100%;"></div></div><div id="c-order-2">주문 대기중</div></div>
        <div class="customer-card"><div style="font-size:24px;">👵</div><div style="font-size:11px; color:#d8004e; font-weight:bold;" id="c-text-3">01:30</div><div class="customer-timer"><div class="customer-timer-bar" id="c-timer-3" style="width:100%;"></div></div><div id="c-order-3">주문 대기중</div></div>
    </div>

    <div id="kitchen-table"></div>

    <!-- 유틸리티 존 (정수기 & 쓰레기통) -->
    <div id="utility-zone">
        <div id="water-dispenser" ondragover="event.preventDefault()" ondrop="fillWater(event)" title="냄비를 올려 물을 받으세요">
            <div style="font-size: 11px; font-weight: bold; color: #546e7a;">💧 정수기</div>
            <div style="font-size: 26px;">🚰</div>
        </div>
        <div id="trash-can" ondragover="event.preventDefault()" ondrop="trashPot(event)" title="잘못 만든 냄비를 버려 비우세요">
            <div style="font-size: 11px; font-weight: bold; color: #c62828;">🗑️ 쓰레기통</div>
            <div style="font-size: 26px;">🗑️</div>
            <div style="font-size: 9px; color: #d32f2f; font-weight: bold;">(드롭하여 폐기)</div>
        </div>
    </div>

    <!-- 커진 4구 가스레인지 -->
    <div id="stoves-container">
        <div class="stove-slot" ondragover="event.preventDefault()" ondrop="dropStove(event, 0)"><div class="pot" id="pot-0" draggable="true" ondragstart="dragPot(event, 0)"><div class="pot-water" id="pw-0"></div><div class="ramen-noodle-layer" id="nd-0"></div><div class="pot-toppings" id="tp-0"></div></div></div>
        <div class="stove-slot" ondragover="event.preventDefault()" ondrop="dropStove(event, 1)"><div class="pot" id="pot-1" draggable="true" ondragstart="dragPot(event, 1)"><div class="pot-water" id="pw-1"></div><div class="ramen-noodle-layer" id="nd-1"></div><div class="pot-toppings" id="tp-1"></div></div></div>
        <div class="stove-slot" ondragover="event.preventDefault()" ondrop="dropStove(event, 2)"><div class="pot" id="pot-2" draggable="true" ondragstart="dragPot(event, 2)"><div class="pot-water" id="pw-2"></div><div class="ramen-noodle-layer" id="nd-2"></div><div class="pot-toppings" id="tp-2"></div></div></div>
        <div class="stove-slot" ondragover="event.preventDefault()" ondrop="dropStove(event, 3)"><div class="pot" id="pot-3" draggable="true" ondragstart="dragPot(event, 3)"><div class="pot-water" id="pw-3"></div><div class="ramen-noodle-layer" id="nd-3"></div><div class="pot-toppings" id="tp-3"></div></div></div>
    </div>

    <!-- 제출 버튼 -->
    <div id="serve-buttons-container">
        <button class="serve-btn" onclick="serve(0)">👧 1번 손님 제출</button>
        <button class="serve-btn" onclick="serve(1)">👦 2번 손님 제출</button>
        <button class="serve-btn" onclick="serve(2)">👨 3번 손님 제출</button>
        <button class="serve-btn" onclick="serve(3)">👵 4번 손님 제출</button>
    </div>

    <!-- 상태 가이드 로그 -->
    <div id="status-bubble">
        🎮 <b>게임 플레이 가이드:</b><br>
        1. 냄비를 <b>정수기(🚰)</b>로 끌어가 물을 받으세요.<br>
        2. 물을 채운 냄비를 <b>확대된 가스레인지 화구</b>로 올리면 끓기 시작합니다.<br>
        3. 손님별 주문에 맞게 재료를 넣고 <b>[제출]</b>하세요. (제한시간 1분 30초)<br>
        4. <b>잘못 만든 경우:</b> 냄비를 <b>쓰레기통(🗑️)</b>으로 드래그하면 깔끔하게 비워집니다!
    </div>

    <!-- 재료 선반 -->
    <div id="ingredient-shelf">
        <div class="ingredient" draggable="true" ondragstart="dragIng(event, '면')"><div style="font-size:32px;">🍜</div><div style="font-size:11px;font-weight:bold;">면</div></div>
        <div class="ingredient" draggable="true" ondragstart="dragIng(event, '라면스프')"><div style="font-size:32px;">🧂</div><div style="font-size:11px;font-weight:bold;">스프</div></div>
        <div class="ingredient" draggable="true" ondragstart="dragIng(event, '파')"><div style="font-size:32px;">🥬</div><div style="font-size:11px;font-weight:bold;">파</div></div>
        <div class="ingredient" draggable="true" ondragstart="dragIng(event, '계란')"><div style="font-size:32px;">🥚</div><div style="font-size:11px;font-weight:bold;">계란</div></div>
        <div class="ingredient" draggable="true" ondragstart="dragIng(event, '고추')"><div style="font-size:32px;">🌶️</div><div style="font-size:11px;font-weight:bold;">고추</div></div>
        <div class="ingredient" draggable="true" ondragstart="dragIng(event, '고기')"><div style="font-size:32px;">🥩</div><div style="font-size:11px;font-weight:bold;">고기</div></div>
        <div class="ingredient" draggable="true" ondragstart="dragIng(event, '떡')"><div style="font-size:32px;">🍡</div><div style="font-size:11px;font-weight:bold;">떡</div></div>
    </div>
</div>

<script>
    const TIME_LIMIT = 90; // 손님별 정확히 1분 30초
    const ICONS = {"면": "🟡", "라면스프": "🔴", "파": "🥬", "계란": "🍳", "고추": "🌶️", "고기": "🥩", "떡": "🍡"};
    
    let score = 0;
    let pots = [
        {water: 0, boiling: false, contents: []},
        {water: 0, boiling: false, contents: []},
        {water: 0, boiling: false, contents: []},
        {water: 0, boiling: false, contents: []}
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

    function init() {
        for(let i=0; i<4; i++) {
            pots[i] = {water: 0, boiling: false, contents: []};
            updatePot(i);
            genCust(i);
        }
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
            timeLE[i]--;
            document.getElementById(`c-text-${i}`).innerText = fmt(timeLE[i]);
            document.getElementById(`c-timer-${i}`).style.width = (timeLE[i] / TIME_LIMIT * 100) + '%';
            
            if(timeLE[i] <= 0) {
                score = Math.max(0, score - 500);
                document.getElementById('score').innerText = score;
                logMsg(`⏰ ${i+1}번 손님이 기다리다 지쳐 떠났습니다! (-500원)`);
                genCust(i);
            }
        }, 1000);
    }

    function dragPot(e, idx) { dragPotIdx = idx; }

    // 정수기 물 받아오기
    function fillWater(e) {
        e.preventDefault();
        if(dragPotIdx !== null) {
            pots[dragPotIdx].water = 100;
            pots[dragPotIdx].boiling = false;
            updatePot(dragPotIdx);
            logMsg(`💧 ${dragPotIdx+1}번 냄비에 물을 채웠습니다! 가스레인지로 옮기세요.`);
            dragPotIdx = null;
        }
    }

    // 쓰레기통에 냄비 버려 비우기
    function trashPot(e) {
        e.preventDefault();
        if(dragPotIdx !== null) {
            pots[dragPotIdx] = {water: 0, boiling: false, contents: []};
            updatePot(dragPotIdx);
            logMsg(`🗑️ ${dragPotIdx+1}번 냄비를 쓰레기통에 비웠습니다.`);
            dragPotIdx = null;
        }
    }

    // 화구 위치 변경 / 조리 시작
    function dropStove(e, idx) {
        e.preventDefault();
        if(dragPotIdx !== null) {
            let t = pots[dragPotIdx];
            pots[dragPotIdx] = pots[idx];
            pots[idx] = t;
            updatePot(dragPotIdx);
            updatePot(idx);
            if(pots[idx].water >= 100 && !pots[idx].boiling) {
                pots[idx].boiling = true;
                document.getElementById(`pw-${idx}`).style.backgroundColor = 'rgba(255, 152, 0, 0.7)';
                logMsg(`🔥 ${idx+1}번 화구 냄비가 끓기 시작합니다!`);
            }
            dragPotIdx = null;
        }
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
                        logMsg("⚠️ 물이 아직 끓지 않았습니다!");
                        dragIngName = null;
                        return;
                    }
                    if(!pots[i].contents.includes(dragIngName)) {
                        pots[i].contents.push(dragIngName);
                        updatePot(i);
                        logMsg(`✨ ${i+1}번 냄비에 '${dragIngName}' 넣음!`);
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
            if(p.contents.includes("라면스프")) document.getElementById(`pw-${i}`).style.backgroundColor = 'rgba(211, 47, 47, 0.85)';
        } else {
            nd.style.display = 'none';
        }
        p.contents.forEach(item => {
            if(item !== "면" && item !== "라면스프") {
                let s = document.createElement('span');
                s.className = 'topping-item';
                s.innerText = ICONS[item];
                tp.appendChild(s);
            }
        });
    }

    function serve(i) {
        let p = pots[i];
        if(!p.boiling || p.contents.length === 0) {
            logMsg(`⚠️ ${i+1}번 화구에 제출할 라면이 없습니다!`);
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
            logMsg(`🎉 ${i+1}번 손님 대만족! 최고급 맞춤 라면! (+${2000+earned}원)`);
        } else {
            score += earned;
            logMsg(`👍 ${i+1}번 손님 서빙 완료 (+${earned}원)`);
        }

        document.getElementById('score').innerText = score;
        pots[i] = {water: 0, boiling: false, contents: []};
        updatePot(i);
        genCust(i);
    }
</script>
</body>
</html>
"""

st.markdown("<h2 style='text-align: center; color: #ff3366;'>🍜 슈의 4구 라면가게 (확대 화구 & 쓰레기통) 🍜</h2>", unsafe_allow_html=True)
components.html(GAME_HTML, height=780, scrolling=False)
