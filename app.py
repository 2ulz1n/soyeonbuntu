import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="슈의 4구 라면가게 타이쿤 🍜",
    page_icon="🍜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 파이썬 문법 오류가 절대 나지 않도록 최적화된 HTML/JS 단일 블록
GAME_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>슈의 라면가게</title>
    <style>
        * { box-sizing: border-box; user-select: none; font-family: 'Comic Sans MS', sans-serif; }
        body { margin: 0; padding: 5px; background-color: #ffeff5; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        #game-container { position: relative; width: 1000px; height: 720px; background: linear-gradient(135deg, #ffd1dc 0%, #ffe4e1 100%); border: 8px solid #ff69b4; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); overflow: hidden; }
        #header { position: absolute; top: 10px; left: 20px; right: 20px; display: flex; justify-content: space-between; align-items: center; z-index: 10; }
        .title-banner { background: #ff3366; color: white; padding: 6px 18px; border-radius: 25px; font-size: 20px; font-weight: bold; box-shadow: 3px 3px 0px #b3003b; }
        .score-box { background: #fff; border: 3px solid #ff69b4; padding: 5px 15px; border-radius: 15px; font-size: 18px; font-weight: bold; color: #d8004e; }
        
        #customer-bar { position: absolute; top: 70px; left: 20px; right: 20px; height: 120px; display: flex; justify-content: space-between; gap: 15px; z-index: 15; }
        .customer-card { flex: 1; background: white; border: 4px solid #ff80ab; border-radius: 15px; padding: 8px; display: flex; flex-direction: column; align-items: center; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .customer-timer { width: 100%; height: 8px; background: #eee; border-radius: 4px; margin: 4px 0; overflow: hidden; }
        .customer-timer-bar { width: 100%; height: 100%; background: #2ed573; transition: width 0.3s linear; }
        .order-tag { display: inline-block; background: #ffebee; color: #c62828; padding: 1px 4px; border-radius: 4px; margin: 1px; font-size: 10px; border: 1px solid #ffcdd2; }

        #kitchen-table { position: absolute; bottom: 0; width: 100%; height: 510px; background: #f7d6b5; border-top: 10px solid #e0a96d; }
        #water-dispenser { position: absolute; top: 210px; left: 20px; width: 100px; height: 150px; background: #eceff1; border: 4px solid #90a4ae; border-radius: 12px; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; padding-top: 10px; cursor: pointer; }
        .dispenser-body { width: 60px; height: 80px; background: #b0bec5; border-radius: 8px; position: relative; display: flex; justify-content: center; align-items: center; }
        
        #stoves-container { position: absolute; top: 200px; left: 140px; width: 380px; height: 165px; display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; padding: 10px; background: #cfd8dc; border: 4px solid #78909c; border-radius: 15px; }
        .stove-slot { position: relative; width: 165px; height: 65px; background: #b0bec5; border: 3px dashed #546e7a; border-radius: 10px; display: flex; justify-content: center; align-items: center; }

        .pot { position: relative; width: 130px; height: 60px; background: linear-gradient(135deg, #ffd700 0%, #e6b800 100%); border: 4px solid #b8860b; border-radius: 0 0 40px 40px; cursor: grab; overflow: hidden; display: flex; justify-content: center; align-items: flex-end; }
        .pot-water { position: absolute; bottom: 0; width: 100%; height: 0%; background: rgba(64, 196, 255, 0.6); transition: height 0.3s; }
        .ramen-noodle-layer { position: absolute; bottom: 5px; width: 90px; height: 25px; background: #fbc02d; border-radius: 12px; display: none; }
        .pot-toppings { position: absolute; bottom: 15px; display: flex; gap: 2px; z-index: 5; justify-content: center; max-width: 100px; }

        #serve-buttons-container { position: absolute; top: 375px; left: 140px; width: 380px; display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; }
        .serve-btn { background: #2ed573; color: white; border: none; padding: 8px; font-size: 13px; font-weight: bold; border-radius: 10px; cursor: pointer; }

        #ingredient-shelf { position: absolute; bottom: 15px; left: 20px; right: 20px; height: 110px; background: #fff; border: 4px solid #ff80ab; border-radius: 15px; display: flex; justify-content: space-around; align-items: center; padding: 5px; }
        .ingredient { width: 70px; height: 90px; background: #fff0f5; border: 3px solid #ffb6c1; border-radius: 10px; display: flex; flex-direction: column; justify-content: center; align-items: center; cursor: grab; }
        
        #status-bubble { position: absolute; top: 210px; right: 30px; width: 420px; height: 150px; background: white; border: 4px solid #ff69b4; border-radius: 15px; padding: 12px; font-size: 13px; font-weight: bold; overflow-y: auto; }
    </style>
</head>
<body>
<div id="game-container">
    <div id="header">
        <div class="title-banner">🍜 슈의 4구 라면가게 (1분30초)</div>
        <div class="score-box">💰 매출: <span id="score">0</span>원</div>
    </div>

    <div id="customer-bar">
        <div class="customer-card"><div style="font-size:24px;">👧</div><div style="font-size:11px; color:#d8004e;" id="c-text-0">01:30</div><div class="customer-timer"><div class="customer-timer-bar" id="c-timer-0" style="width:100%;"></div></div><div id="c-order-0" style="font-size:10px;">주문중</div></div>
        <div class="customer-card"><div style="font-size:24px;">👦</div><div style="font-size:11px; color:#d8004e;" id="c-text-1">01:30</div><div class="customer-timer"><div class="customer-timer-bar" id="c-timer-1" style="width:100%;"></div></div><div id="c-order-1" style="font-size:10px;">주문중</div></div>
        <div class="customer-card"><div style="font-size:24px;">👨</div><div style="font-size:11px; color:#d8004e;" id="c-text-2">01:30</div><div class="customer-timer"><div class="customer-timer-bar" id="c-timer-2" style="width:100%;"></div></div><div id="c-order-2" style="font-size:10px;">주문중</div></div>
        <div class="customer-card"><div style="font-size:24px;">👵</div><div style="font-size:11px; color:#d8004e;" id="c-text-3">01:30</div><div class="customer-timer"><div class="customer-timer-bar" id="c-timer-3" style="width:100%;"></div></div><div id="c-order-3" style="font-size:10px;">주문중</div></div>
    </div>

    <div id="kitchen-table"></div>

    <div id="water-dispenser" ondragover="event.preventDefault()" ondrop="fillWater(event)">
        <div style="font-size: 11px; font-weight: bold; color: #546e7a;">💧 정수기</div>
        <div class="dispenser-body"><span style="font-size: 20px;">🚰</span></div>
    </div>

    <div id="stoves-container">
        <div class="stove-slot" ondragover="event.preventDefault()" ondrop="dropStove(event, 0)"><div class="pot" id="pot-0" draggable="true" ondragstart="dragPot(event, 0)"><div class="pot-water" id="pw-0"></div><div class="ramen-noodle-layer" id="nd-0"></div><div class="pot-toppings" id="tp-0"></div></div></div>
        <div class="stove-slot" ondragover="event.preventDefault()" ondrop="dropStove(event, 1)"><div class="pot" id="pot-1" draggable="true" ondragstart="dragPot(event, 1)"><div class="pot-water" id="pw-1"></div><div class="ramen-noodle-layer" id="nd-1"></div><div class="pot-toppings" id="tp-1"></div></div></div>
        <div class="stove-slot" ondragover="event.preventDefault()" ondrop="dropStove(event, 2)"><div class="pot" id="pot-2" draggable="true" ondragstart="dragPot(event, 2)"><div class="pot-water" id="pw-2"></div><div class="ramen-noodle-layer" id="nd-2"></div><div class="pot-toppings" id="tp-2"></div></div></div>
        <div class="stove-slot" ondragover="event.preventDefault()" ondrop="dropStove(event, 3)"><div class="pot" id="pot-3" draggable="true" ondragstart="dragPot(event, 3)"><div class="pot-water" id="pw-3"></div><div class="ramen-noodle-layer" id="nd-3"></div><div class="pot-toppings" id="tp-3"></div></div></div>
    </div>

    <div id="serve-buttons-container">
        <button class="serve-btn" onclick="serve(0)">1번 손님 제출</button>
        <button class="serve-btn" onclick="serve(1)">2번 손님 제출</button>
        <button class="serve-btn" onclick="serve(2)">3번 손님 제출</button>
        <button class="serve-btn" onclick="serve(3)">4번 손님 제출</button>
    </div>

    <div id="status-bubble">게임 시작! 정수기에 냄비를 드래그해 물을 받고 화구에 끓이세요. (손님별 제한시간 90초)</div>

    <div id="ingredient-shelf">
        <div class="ingredient" draggable="true" ondragstart="dragIng(event, '면')"><div style="font-size:28px;">🍜</div><div style="font-size:11px;font-weight:bold;">면</div></div>
        <div class="ingredient" draggable="true" ondragstart="dragIng(event, '라면스프')"><div style="font-size:28px;">🧂</div><div style="font-size:11px;font-weight:bold;">스프</div></div>
        <div class="ingredient" draggable="true" ondragstart="dragIng(event, '파')"><div style="font-size:28px;">🥬</div><div style="font-size:11px;font-weight:bold;">파</div></div>
        <div class="ingredient" draggable="true" ondragstart="dragIng(event, '계란')"><div style="font-size:28px;">🥚</div><div style="font-size:11px;font-weight:bold;">계란</div></div>
        <div class="ingredient" draggable="true" ondragstart="dragIng(event, '고추')"><div style="font-size:28px;">🌶️</div><div style="font-size:11px;font-weight:bold;">고추</div></div>
        <div class="ingredient" draggable="true" ondragstart="dragIng(event, '고기')"><div style="font-size:28px;">🥩</div><div style="font-size:11px;font-weight:bold;">고기</div></div>
        <div class="ingredient" draggable="true" ondragstart="dragIng(event, '떡')"><div style="font-size:28px;">🍡</div><div style="font-size:11px;font-weight:bold;">떡</div></div>
    </div>
</div>

<script>
    const TIME_LIMIT = 90; // 정확히 1분 30초 (90초)
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
        let order = ["면", "라면ส프", ["파","계란","고추","고기","떡"][Math.floor(Math.random()*5)]];
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
                genCust(i);
            }
        }, 1000);
    }

    function dragPot(e, idx) { dragPotIdx = idx; }
    function fillWater(e) {
        e.preventDefault();
        if(dragPotIdx !== null) {
            pots[dragPotIdx].water = 100;
            pots[dragPotIdx].boiling = false;
            updatePot(dragPotIdx);
            dragPotIdx = null;
        }
    }

    function dropStove(e, idx) {
        e.preventDefault();
        if(dragPotIdx !== null) {
            let t = pots[dragPotIdx];
            pots[dragPotIdx] = pots[idx];
            pots[idx] = t;
            updatePot(dragPotIdx);
            updatePot(idx);
            if(pots[idx].water >= 100) {
                pots[idx].boiling = true;
                document.getElementById(`pw-${idx}`).style.backgroundColor = 'rgba(255, 152, 0, 0.7)';
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
                    if(pots[i].water < 100 || !pots[i].boiling) return;
                    if(!pots[i].contents.includes(dragIngName)) {
                        pots[i].contents.push(dragIngName);
                        updatePot(i);
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
                s.innerText = ICONS[item];
                tp.appendChild(s);
            }
        });
    }

    function serve(i) {
        let p = pots[i];
        if(!p.boiling || p.contents.length === 0) return;
        
        score += 1500;
        document.getElementById('score').innerText = score;
        pots[i] = {water: 0, boiling: false, contents: []};
        updatePot(i);
        genCust(i);
    }
</script>
</body>
</html>
"""

st.markdown("<h2 style='text-align: center; color: #ff3366;'>🍜 슈의 4구 라면가게 (1분 30초) 🍜</h2>", unsafe_allow_html=True)
components.html(GAME_HTML, height=750, scrolling=False)
