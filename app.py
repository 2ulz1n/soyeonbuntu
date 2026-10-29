import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="슈의 라면가게 4구 멀티 타이쿤 🍜",
    page_icon="🍜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>슈의 라면가게 4구 멀티</title>
    <style>
        * {
            box-sizing: border-box;
            user-select: none;
            font-family: 'Comic Sans MS', 'Gothic A1', sans-serif, cursive;
        }
        body {
            margin: 0;
            padding: 5px;
            background-color: #ffeff5;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        #game-container {
            position: relative;
            width: 1000px;
            height: 720px;
            background: linear-gradient(135deg, #ffd1dc 0%, #ffe4e1 100%);
            border: 8px solid #ff69b4;
            border-radius: 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
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
            z-index: 10;
        }
        .title-banner {
            background: #ff3366;
            color: white;
            padding: 6px 18px;
            border-radius: 25px;
            font-size: 20px;
            font-weight: bold;
            box-shadow: 3px 3px 0px #b3003b;
        }
        .score-box {
            background: #fff;
            border: 3px solid #ff69b4;
            padding: 5px 15px;
            border-radius: 15px;
            font-size: 18px;
            font-weight: bold;
            color: #d8004e;
        }
        
        /* 라면 모양 말랑이 장식 */
        .squishy-ramen {
            position: absolute;
            top: 10px;
            right: 220px;
            width: 50px;
            height: 50px;
            background: #ffe066;
            border: 3px solid #fcc419;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            box-shadow: 0 4px 10px rgba(0,0,0,0.15);
            transition: transform 0.1s;
            z-index: 12;
        }
        .squishy-ramen:active { transform: scale(0.8) rotate(-10deg); }

        /* 상단 손님 4명 대기열 영역 */
        #customer-bar {
            position: absolute;
            top: 70px;
            left: 20px;
            right: 20px;
            height: 120px;
            display: flex;
            justify-content: space-between;
            gap: 15px;
            z-index: 15;
        }
        .customer-card {
            flex: 1;
            background: white;
            border: 4px solid #ff80ab;
            border-radius: 15px;
            padding: 8px;
            display: flex;
            flex-direction: column;
            align-items: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            position: relative;
        }
        .customer-avatar {
            font-size: 28px;
        }
        .customer-timer {
            width: 100%;
            height: 8px;
            background: #eee;
            border-radius: 4px;
            margin: 4px 0;
            overflow: hidden;
        }
        .customer-timer-bar {
            width: 100%;
            height: 100%;
            background: #2ed573;
            transition: width 0.3s linear, background-color 0.3s;
        }
        .order-list {
            font-size: 11px;
            font-weight: bold;
            color: #444;
            text-align: center;
            margin-top: 2px;
        }
        .order-tag {
            display: inline-block;
            background: #ffebee;
            color: #c62828;
            padding: 1px 4px;
            border-radius: 4px;
            margin: 1px;
            font-size: 10px;
            border: 1px solid #ffcdd2;
        }

        /* 메인 조리대 영역 */
        #kitchen-table {
            position: absolute;
            bottom: 0;
            width: 100%;
            height: 510px;
            background: #f7d6b5;
            border-top: 10px solid #e0a96d;
        }

        /* 정수기 존 (냄비를 드래그해서 물 받기) */
        #water-dispenser {
            position: absolute;
            top: 210px;
            left: 20px;
            width: 100px;
            height: 150px;
            background: #eceff1;
            border: 4px solid #90a4ae;
            border-radius: 12px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            padding-top: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            cursor: pointer;
        }
        .dispenser-body {
            width: 60px;
            height: 80px;
            background: #b0bec5;
            border-radius: 8px;
            position: relative;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .dispenser-faucet {
            position: absolute;
            bottom: -10px;
            width: 16px;
            height: 15px;
            background: #78909c;
            border-radius: 0 0 5px 5px;
        }

        /* 4구 가스레인지 & 냄비 존 */
        #stoves-container {
            position: absolute;
            top: 200px;
            left: 140px;
            width: 380px;
            height: 165px;
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            padding: 10px;
            background: #cfd8dc;
            border: 4px solid #78909c;
            border-radius: 15px;
        }
        .stove-slot {
            position: relative;
            width: 165px;
            height: 65px;
            background: #b0bec5;
            border: 3px dashed #546e7a;
            border-radius: 10px;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        /* 냄비 스타일 (드래그 가능) */
        .pot {
            position: relative;
            width: 130px;
            height: 60px;
            background: linear-gradient(135deg, #ffd700 0%, #e6b800 100%);
            border: 4px solid #b8860b;
            border-radius: 0 0 40px 40px;
            cursor: grab;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: flex-end;
        }
        .pot:active { cursor: grabbing; }
        .pot-water {
            position: absolute;
            bottom: 0;
            width: 100%;
            height: 0%;
            background: rgba(64, 196, 255, 0.6);
            transition: height 0.3s, background-color 0.3s;
        }
        
        /* 냄비 속 실제 라면 비주얼 레이어 */
        .ramen-noodle-layer {
            position: absolute;
            bottom: 5px;
            width: 90px;
            height: 25px;
            background: #fbc02d;
            border-radius: 12px;
            display: none;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);
            background-image: radial-gradient(#f57f17 20%, transparent 20%), radial-gradient(#f57f17 20%, transparent 20%);
            background-size: 10px 10px;
            background-position: 0 0, 5px 5px;
        }
        .pot-toppings {
            position: absolute;
            bottom: 15px;
            display: flex;
            gap: 2px;
            z-index: 5;
            flex-wrap: wrap;
            justify-content: center;
            max-width: 100px;
        }
        .topping-item {
            font-size: 16px;
            animation: bounceIn 0.3s;
        }
        @keyframes bounceIn {
            0% { transform: scale(0); }
            70% { transform: scale(1.2); }
            100% { transform: scale(1); }
        }

        /* 손님에게 제출 버튼 그룹 (화구별) */
        #serve-buttons-container {
            position: absolute;
            top: 375px;
            left: 140px;
            width: 380px;
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }
        .serve-btn {
            background: #2ed573;
            color: white;
            border: none;
            padding: 8px;
            font-size: 13px;
            font-weight: bold;
            border-radius: 10px;
            cursor: pointer;
            box-shadow: 0 3px 0 #1b9e54;
            transition: transform 0.1s;
        }
        .serve-btn:active { transform: translateY(2px); box-shadow: 0 1px 0 #1b9e54; }

        /* 재료 선반 (드래그 전용) */
        #ingredient-shelf {
            position: absolute;
            bottom: 15px;
            left: 20px;
            right: 20px;
            height: 110px;
            background: #fff;
            border: 4px solid #ff80ab;
            border-radius: 15px;
            display: flex;
            justify-content: space-around;
            align-items: center;
            padding: 5px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        .ingredient {
            width: 70px;
            height: 90px;
            background: #fff0f5;
            border: 3px solid #ffb6c1;
            border-radius: 10px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            cursor: grab;
            transition: transform 0.2s;
        }
        .ingredient:hover { transform: translateY(-4px); background: #ffe4e1; }
        .ingredient:active { cursor: grabbing; }
        .ing-icon { font-size: 32px; }
        .ing-name { font-size: 11px; font-weight: bold; color: #333; margin-top: 2px; }

        /* 상태 말풍선 */
        #status-bubble {
            position: absolute;
            top: 210px;
            right: 30px;
            width: 420px;
            height: 150px;
            background: white;
            border: 4px solid #ff69b4;
            border-radius: 15px;
            padding: 12px;
            font-size: 14px;
            font-weight: bold;
            color: #333;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            overflow-y: auto;
        }

        /* 게임오버 모달 */
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
            padding: 30px;
            border-radius: 20px;
            border: 5px solid #ff69b4;
            text-align: center;
            max-width: 400px;
        }
        .restart-btn {
            background: #ff3366;
            color: white;
            border: none;
            padding: 10px 25px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 20px;
            cursor: pointer;
            margin-top: 15px;
        }
    </style>
</head>
<body>

<div id="game-container">
    <!-- 헤더 -->
    <div id="header">
        <div class="title-banner">🍜 슈의 4구 라면가게 타이쿤</div>
        <div class="score-box">💰 총 매출: <span id="score">0</span>원</div>
    </div>

    <!-- 라면 말랑이 장식 -->
    <div class="squishy-ramen" onclick="popSquishy()">
        <span style="font-size: 26px;">🍜</span>
    </div>

    <!-- 상단 손님 4명 즉시 대기열 -->
    <div id="customer-bar">
        <div class="customer-card" id="customer-0">
            <div class="customer-avatar">👧 소녀</div>
            <div class="customer-timer"><div class="customer-timer-bar" id="c-timer-0" style="width: 100%;"></div></div>
            <div class="order-list" id="c-order-0">주문 분석중...</div>
        </div>
        <div class="customer-card" id="customer-1">
            <div class="customer-avatar">👦 소년</div>
            <div class="customer-timer"><div class="customer-timer-bar" id="c-timer-1" style="width: 100%;"></div></div>
            <div class="order-list" id="c-order-1">주문 분석중...</div>
        </div>
        <div class="customer-card" id="customer-2">
            <div class="customer-avatar">👨 아저씨</div>
            <div class="customer-timer"><div class="customer-timer-bar" id="c-timer-2" style="width: 100%;"></div></div>
            <div class="order-list" id="c-order-2">주문 분석중...</div>
        </div>
        <div class="customer-card" id="customer-3">
            <div class="customer-avatar">👵 할머니</div>
            <div class="customer-timer"><div class="customer-timer-bar" id="c-timer-3" style="width: 100%;"></div></div>
            <div class="order-list" id="c-order-3">주문 분석중...</div>
        </div>
    </div>

    <!-- 주방 배경 -->
    <div id="kitchen-table"></div>

    <!-- 정수기 (냄비 드래그 시작점) -->
    <div id="water-dispenser" ondragover="allowDrop(event)" ondrop="fillWaterAtDispenser(event)" title="냄비를 여기에 놓으면 물이 채워집니다!">
        <div style="font-size: 11px; font-weight: bold; color: #546e7a;">💧 정수기</div>
        <div class="dispenser-body">
            <span style="font-size: 20px;">🚰</span>
            <div class="dispenser-faucet"></div>
        </div>
        <div style="font-size: 9px; color: #e91e63; margin-top: 4px; font-weight: bold;">물 채우기</div>
    </div>

    <!-- 4구 가스레인지 -->
    <div id="stoves-container">
        <!-- 화구 0 -->
        <div class="stove-slot" ondragover="allowDrop(event)" ondrop="dropOnStove(event, 0)">
            <div class="pot" id="pot-0" draggable="true" ondragstart="dragPot(event, 0)">
                <div class="pot-water" id="pwater-0"></div>
                <div class="ramen-noodle-layer" id="noodle-0"></div>
                <div class="pot-toppings" id="ptopping-0"></div>
            </div>
        </div>
        <!-- 화구 1 -->
        <div class="stove-slot" ondragover="allowDrop(event)" ondrop="dropOnStove(event, 1)">
            <div class="pot" id="pot-1" draggable="true" ondragstart="dragPot(event, 1)">
                <div class="pot-water" id="pwater-1"></div>
                <div class="ramen-noodle-layer" id="noodle-1"></div>
                <div class="pot-toppings" id="ptopping-1"></div>
            </div>
        </div>
        <!-- 화구 2 -->
        <div class="stove-slot" ondragover="allowDrop(event)" ondrop="dropOnStove(event, 2)">
            <div class="pot" id="pot-2" draggable="true" ondragstart="dragPot(event, 2)">
                <div class="pot-water" id="pwater-2"></div>
                <div class="ramen-noodle-layer" id="noodle-2"></div>
                <div class="pot-toppings" id="ptopping-2"></div>
            </div>
        </div>
        <!-- 화구 3 -->
        <div class="stove-slot" ondragover="allowDrop(event)" ondrop="dropOnStove(event, 3)">
            <div class="pot" id="pot-3" draggable="true" ondragstart="dragPot(event, 3)">
                <div class="pot-water" id="pwater-3"></div>
                <div class="ramen-noodle-layer" id="noodle-3"></div>
                <div class="pot-toppings" id="ptopping-3"></div>
            </div>
        </div>
    </div>

    <!-- 화구별 손님 제출 버튼 -->
    <div id="serve-buttons-container">
        <button class="serve-btn" onclick="serveRamen(0)">👧 1번 손님에게 제출</button>
        <button class="serve-btn" onclick="serveRamen(1)">👦 2번 손님에게 제출</button>
        <button class="serve-btn" onclick="serveRamen(2)">👨 3번 손님에게 제출</button>
        <button class="serve-btn" onclick="serveRamen(3)">👵 4번 손님에게 제출</button>
    </div>

    <!-- 상태 가이드 로그 -->
    <div id="status-bubble">
        🎮 <b>게임 가이드:</b><br>
        1. 냄비를 드래그해 <b>정수기</b>에 올려 물을 채우세요!<br>
        2. 물 채운 냄비를 <b>가스레인지 화구</b>에 올리면 끓기 시작합니다.<br>
        3. 각 손님의 <b>주문(취향)</b>을 확인하고 재료를 드래그해 넣으세요.<br>
        4. 완성되면 해당 화구의 <b>제출 버튼</b>을 누르세요! (손님별 30초 제한)
    </div>

    <!-- 재료 선반 (7가지) -->
    <div id
