import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Mini StarCraft",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

GAME_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">

<style>
* {
    box-sizing: border-box;
    user-select: none;
}

html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #05080b;
    font-family: Arial, sans-serif;
}

#game {
    position: fixed;
    inset: 0;
    background: #071018;
}

canvas {
    position: absolute;
    left: 0;
    top: 0;
    display: block;
}

#hud {
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    height: 58px;
    background:
        linear-gradient(#18232c, #0b1117);
    border-bottom: 2px solid #52606a;
    color: white;
    display: flex;
    align-items: center;
    gap: 24px;
    padding: 0 18px;
    z-index: 20;
    box-shadow: 0 3px 12px #000;
}

.resource {
    min-width: 105px;
    font-size: 17px;
    font-weight: bold;
}

.resource span {
    color: #62d9ff;
}

#gasValue {
    color: #7dff8b;
}

#population {
    color: #ffd45c;
}

#statusText {
    flex: 1;
    color: #c8d2d8;
    font-size: 14px;
}

#minimap {
    position: absolute;
    right: 15px;
    bottom: 15px;
    width: 235px;
    height: 155px;
    background: #111;
    border: 3px solid #737f87;
    z-index: 30;
    box-shadow: 0 0 12px #000;
}

#sidePanel {
    position: absolute;
    right: 15px;
    top: 75px;
    width: 250px;
    min-height: 245px;
    background:
        linear-gradient(145deg, #1a252d, #080d12);
    border: 2px solid #71808a;
    border-radius: 5px;
    color: white;
    z-index: 25;
    padding: 13px;
    box-shadow: 0 4px 20px #000;
    display: none;
}

#sidePanel h2 {
    margin: 0 0 10px 0;
    font-size: 19px;
    color: #e5edf2;
}

.stat {
    margin: 7px 0;
    padding: 7px;
    background: rgba(255,255,255,.04);
    border: 1px solid #34424b;
}

button {
    width: 100%;
    margin-top: 7px;
    padding: 9px;
    border: 1px solid #788892;
    background: linear-gradient(#3c4d57, #182229);
    color: white;
    cursor: pointer;
    font-weight: bold;
}

button:hover {
    background: linear-gradient(#536975, #24343d);
}

button:disabled {
    opacity: .45;
    cursor: not-allowed;
}

#buildMode {
    position: absolute;
    left: 50%;
    top: 70px;
    transform: translateX(-50%);
    background: rgba(10,20,25,.9);
    color: #9deaff;
    padding: 8px 15px;
    border: 1px solid #5c8999;
    z-index: 40;
    display: none;
}

#message {
    position: absolute;
    left: 50%;
    bottom: 180px;
    transform: translateX(-50%);
    padding: 9px 20px;
    background: rgba(0,0,0,.78);
    color: white;
    border: 1px solid #67747c;
    z-index: 50;
    display: none;
}

#raceScreen {
    position: absolute;
    inset: 0;
    background:
        radial-gradient(circle at center, #172832, #020406 70%);
    z-index: 100;
    display: flex;
    justify-content: center;
    align-items: center;
}

.raceBox {
    width: 480px;
    padding: 35px;
    text-align: center;
    color: white;
    background: linear-gradient(#1b2932,#080d12);
    border: 2px solid #788892;
    box-shadow: 0 0 50px #000;
}

.raceBox h1 {
    font-size: 38px;
    margin: 0 0 12px;
}

.raceBox p {
    color: #adb9bf;
}

.raceButton {
    width: 250px;
    margin: 10px auto;
    font-size: 18px;
}

#tips {
    position: absolute;
    left: 15px;
    bottom: 15px;
    color: #d4dde2;
    background: rgba(0,0,0,.65);
    border: 1px solid #46535b;
    padding: 10px;
    z-index: 25;
    font-size: 12px;
    line-height: 1.6;
}
</style>
</head>

<body>

<div id="game">

<canvas id="world"></canvas>
<canvas id="minimap"></canvas>

<div id="hud">
    <div class="resource">💎 미네랄 <span id="minerals">500</span></div>
    <div class="resource">🟢 가스 <span id="gasValue">0</span></div>
    <div class="resource">👥 인구 <span id="population">5 / 20</span></div>
    <div id="statusText">테란 기지를 준비하는 중...</div>
</div>

<div id="sidePanel"></div>

<div id="buildMode">
    건설 위치를 지정하세요 — 가스 위에 클릭
</div>

<div id="message"></div>

<div id="tips">
    좌클릭: 유닛 선택 / 드래그 선택<br>
    우클릭: 이동 / 자원 채취<br>
    가장자리 이동: 카메라 이동<br>
    미니맵 클릭: 해당 위치로 이동
</div>

<div id="raceScreen">
    <div class="raceBox">
        <h1>TERAN COMMAND</h1>
        <p>종족을 선택하세요</p>
        <button class="raceButton" onclick="startTerran()">
            🚀 TERRAN
        </button>
        <button class="raceButton" disabled>
            ZERG — 준비 중
        </button>
        <button class="raceButton" disabled>
            PROTOSS — 준비 중
        </button>
    </div>
</div>

</div>

<script>
"use strict";

/* =========================================================
   기본 설정
========================================================= */

const canvas = document.getElementById("world");
const ctx = canvas.getContext("2d");

const mini = document.getElementById("minimap");
const mctx = mini.getContext("2d");

let W = window.innerWidth;
let H = window.innerHeight;

canvas.width = W;
canvas.height = H;

const MAP_W = 4200;
const MAP_H = 3000;

let camera = {
    x: 0,
    y: 0,
    speed: 12
};

let mouse = {
    x: 0,
    y: 0,
    worldX: 0,
    worldY: 0,
    down: false
};

let gameStarted = false;
let selectedUnits = [];
let selectedObject = null;

let dragging = false;
let dragStart = {x:0,y:0};
let dragEnd = {x:0,y:0};

let buildMode = null;
let buildPreview = null;

let minerals = 500;
let gas = 0;

let supplyUsed = 5;
let supplyMax = 20;

let nextUnitId = 1;
let nextBuildingId = 1;

let units = [];
let buildings = [];
let mineralFields = [];
let geysers = [];

let commandCenter = null;

let messages = [];

/* =========================================================
   사운드
========================================================= */

let audioCtx = null;

function sound(type) {
    try {
        if (!audioCtx)
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();

        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();

        osc.connect(gain);
        gain.connect(audioCtx.destination);

        if(type === "click") {
            osc.frequency.value = 500;
        }
        else if(type === "build") {
            osc.frequency.value = 220;
        }
        else if(type === "mine") {
            osc.frequency.value = 720;
        }
        else if(type === "complete") {
            osc.frequency.value = 900;
        }

        gain.gain.setValueAtTime(.08, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(.001, audioCtx.currentTime + .12);

        osc.start();
        osc.stop(audioCtx.currentTime + .12);
    } catch(e) {}
}

/* =========================================================
   유틸
========================================================= */

function clamp(v,a,b) {
    return Math.max(a, Math.min(b,v));
}

function distance(a,b) {
    return Math.hypot(a.x-b.x,a.y-b.y);
}

function worldMouse() {
    return {
        x: mouse.x + camera.x,
        y: mouse.y + camera.y
    };
}

function showMessage(text) {
    const el = document.getElementById("message");
    el.textContent = text;
    el.style.display = "block";

    clearTimeout(showMessage.timer);

    showMessage.timer = setTimeout(() => {
        el.style.display = "none";
    }, 1800);
}

function updateHUD() {
    document.getElementById("minerals").textContent = Math.floor(minerals);
    document.getElementById("gasValue").textContent = Math.floor(gas);
    document.getElementById("population").textContent =
        supplyUsed + " / " + supplyMax;
}

/* =========================================================
   맵 생성
========================================================= */

function createMap() {

    /*
       사령부
       [미네랄]
       [미네랄]   [가스]
       [미네랄]
       [미네랄]
    */

    commandCenter = {
        id: nextBuildingId++,
        type: "command",
        x: 2050,
        y: 1450,
        w: 220,
        h: 170,
        hp: 1500,
        maxHp: 1500
    };

    buildings.push(commandCenter);

    /*
       미네랄은 사령부 한쪽 옆에 배치
       너무 붙지 않도록 충분한 간격
    */

    const mineralPositions = [
        {x:1660,y:1280},
        {x:1580,y:1360},
        {x:1540,y:1460},
        {x:1580,y:1560},
        {x:1660,y:1640},
        {x:1740,y:1730}
    ];

    mineralPositions.forEach((p,i) => {
        mineralFields.push({
            id:i,
            x:p.x,
            y:p.y,
            amount:999999,
            w:75,
            h:50
        });
    });

    /*
       가스는 하나만
    */

    geysers.push({
        id:1,
        x:2380,
        y:1390,
        w:100,
        h:100,
        amount:Infinity
    });

    /*
       장식용 바위 / 장애물
    */

    for(let i=0;i<25;i++) {

        let x = 250 + Math.random()*(MAP_W-500);
        let y = 250 + Math.random()*(MAP_H-500);

        if(
            Math.abs(x-commandCenter.x)<600 &&
            Math.abs(y-commandCenter.y)<500
        ) continue;

        buildings.push({
            id:nextBuildingId++,
            type:"rock",
            x:x,
            y:y,
            w:70+Math.random()*40,
            h:50+Math.random()*30,
            hp:999999
        });
    }
}

/* =========================================================
   SCV 생성
========================================================= */

function createSCV(x,y) {

    if(supplyUsed >= supplyMax) {
        showMessage("인구수가 부족합니다. 서플라이 디포를 건설하세요.");
        return null;
    }

    const scv = {
        id:nextUnitId++,
        type:"scv",

        x:x,
        y:y,

        radius:24,

        hp:50,
        maxHp:50,

        speed:2.8,

        selected:false,

        state:"idle",

        target:null,

        resourceType:null,

        carrying:0,

        carryingType:null,

        mineTimer:0,

        buildTimer:0,

        buildTarget:null,

        commandTarget:null
    };

    units.push(scv);
    supplyUsed++;

    return scv;
}

/* =========================================================
   초기 SCV 5개
========================================================= */

function spawnStartingSCVs() {

    const positions = [
        {x:1800,y:1260},
        {x:1800,y:1340},
        {x:1800,y:1420},
        {x:1800,y:1500},
        {x:1800,y:1580}
    ];

    positions.forEach(p => createSCV(p.x,p.y));
}

/* =========================================================
   SCV 그리기
========================================================= */

function drawSCV(u) {

    ctx.save();
    ctx.translate(u.x,u.y);

    /*
       그림자
    */
    ctx.fillStyle = "rgba(0,0,0,.35)";
    ctx.beginPath();
    ctx.ellipse(0,18,25,9,0,0,Math.PI*2);
    ctx.fill();

    /*
       바퀴
    */
    ctx.fillStyle = "#171b1d";

    ctx.beginPath();
    ctx.arc(-15,13,8,0,Math.PI*2);
    ctx.fill();

    ctx.beginPath();
    ctx.arc(15,13,8,0,Math.PI*2);
    ctx.fill();

    /*
       몸체
    */
    const bodyGrad = ctx.createLinearGradient(-20,-20,20,20);
    bodyGrad.addColorStop(0,"#d7d8d4");
    bodyGrad.addColorStop(.5,"#888d8c");
    bodyGrad.addColorStop(1,"#353b3d");

    ctx.fillStyle = bodyGrad;

    ctx.beginPath();
    ctx.roundRect(-22,-18,44,34,8);
    ctx.fill();

    ctx.strokeStyle = "#202527";
    ctx.lineWidth = 3;
    ctx.stroke();

    /*
       중앙 장갑
    */
    ctx.fillStyle = "#aeb5b5";
    ctx.fillRect(-12,-11,24,17);

    /*
       전면 유리
    */
    ctx.fillStyle = "#52b9d9";
    ctx.beginPath();
    ctx.roundRect(-10,-22,20,13,4);
    ctx.fill();

    /*
       경고등
    */
    ctx.fillStyle = "#f3c24e";
    ctx.fillRect(-17,-5,5,5);
    ctx.fillRect(12,-5,5,5);

    /*
       선택 링
    */
    if(u.selected) {

        ctx.strokeStyle = "#6cff72";
        ctx.lineWidth = 3;

        ctx.beginPath();
        ctx.ellipse(0,20,29,10,0,0,Math.PI*2);
        ctx.stroke();
    }

    /*
       체력바
    */
    ctx.fillStyle = "#222";
    ctx.fillRect(-25,-39,50,6);

    ctx.fillStyle = "#58e26d";
    ctx.fillRect(-25,-39,50*(u.hp/u.maxHp),6);

    /*
       들고 있는 자원
    */
    if(u.carrying > 0) {

        if(u.carryingType === "mineral") {

            ctx.fillStyle = "#61d7ff";
            ctx.beginPath();
            ctx.moveTo(0,-48);
            ctx.lineTo(10,-35);
            ctx.lineTo(0,-29);
            ctx.lineTo(-10,-35);
            ctx.closePath();
            ctx.fill();

        } else {

            ctx.fillStyle = "#79ff8c";
            ctx.beginPath();
            ctx.arc(0,-38,7,0,Math.PI*2);
            ctx.fill();
        }
    }

    ctx.restore();
}

/* =========================================================
   사령부 그리기
========================================================= */

function drawCommandCenter(b) {

    ctx.save();
    ctx.translate(b.x,b.y);

    /*
       그림자
    */
    ctx.fillStyle = "rgba(0,0,0,.4)";
    ctx.fillRect(-b.w/2+15,-b.h/2+20,b.w,b.h);

    /*
       하부
    */
    ctx.fillStyle = "#323b40";
    ctx.strokeStyle = "#13181b";
    ctx.lineWidth = 6;

    ctx.beginPath();
    ctx.roundRect(-b.w/2,-b.h/2,b.w,b.h,12);
    ctx.fill();
    ctx.stroke();

    /*
       중앙 건물
    */
    const g = ctx.createLinearGradient(0,-80,0,80);
    g.addColorStop(0,"#b8bdbc");
    g.addColorStop(.45,"#686f70");
    g.addColorStop(1,"#2b3032");

    ctx.fillStyle = g;

    ctx.beginPath();
    ctx.roundRect(-70,-70,140,125,10);
    ctx.fill();

    ctx.strokeStyle = "#15191b";
    ctx.stroke();

    /*
       지붕
    */
    ctx.fillStyle = "#4a5357";
    ctx.beginPath();
    ctx.moveTo(-85,-70);
    ctx.lineTo(0,-110);
    ctx.lineTo(85,-70);
    ctx.closePath();
    ctx.fill();

    /*
       창문
    */
    ctx.fillStyle = "#4fd2f2";

    for(let y=-45;y<30;y+=25) {
        ctx.fillRect(-55,y,35,13);
        ctx.fillRect(20,y,35,13);
    }

    /*
       중앙 출입구
    */
    ctx.fillStyle = "#181e21";
    ctx.fillRect(-25,28,50,45);

    /*
       양쪽 구조물
    */
    ctx.fillStyle = "#596265";
    ctx.fillRect(-105,-25,35,80);
    ctx.fillRect(70,-25,35,80);

    /*
       안테나
    */
    ctx.strokeStyle = "#b6c0c3";
    ctx.lineWidth = 4;

    ctx.beginPath();
    ctx.moveTo(0,-105);
    ctx.lineTo(0,-140);
    ctx.stroke();

    ctx.fillStyle = "#e5c34c";
    ctx.beginPath();
    ctx.arc(0,-145,7,0,Math.PI*2);
    ctx.fill();

    /*
       선택 표시
    */
    if(selectedObject === b) {

        ctx.strokeStyle = "#6cff72";
        ctx.lineWidth = 4;

        ctx.strokeRect(
            -b.w/2-8,
            -b.h/2-8,
            b.w+16,
            b.h+16
        );
    }

    /*
       체력
    */
    ctx.fillStyle = "#151515";
    ctx.fillRect(-100,-170,200,9);

    ctx.fillStyle = "#56e36b";
    ctx.fillRect(-100,-170,200*(b.hp/b.maxHp),9);

    ctx.restore();
}

/* =========================================================
   가스 채취 시설
========================================================= */

function drawGasBuilding(b) {

    ctx.save();
    ctx.translate(b.x,b.y);

    ctx.fillStyle = "rgba(0,0,0,.4)";
    ctx.beginPath();
    ctx.ellipse(0,35,55,20,0,0,Math.PI*2);
    ctx.fill();

    /*
       본체
    */
    const g = ctx.createLinearGradient(-40,-50,40,50);
    g.addColorStop(0,"#9ea7a8");
    g.addColorStop(.5,"#505a5d");
    g.addColorStop(1,"#20282b");

    ctx.fillStyle = g;
    ctx.strokeStyle = "#111719";
    ctx.lineWidth = 4;

    ctx.beginPath();
    ctx.roundRect(-48,-50,96,85,10);
    ctx.fill();
    ctx.stroke();

    /*
       상부
    */
    ctx.fillStyle = "#30393c";
    ctx.beginPath();
    ctx.arc(0,-35,30,Math.PI,0);
    ctx.fill();

    /*
       파이프
    */
    ctx.strokeStyle = "#9aa5a8";
    ctx.lineWidth = 8;

    ctx.beginPath();
    ctx.moveTo(-35,0);
    ctx.lineTo(-75,0);
    ctx.lineTo(-75,30);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(35,0);
    ctx.lineTo(75,0);
    ctx.lineTo(75,30);
    ctx.stroke();

    /*
       선택
    */
    if(selectedObject === b) {

        ctx.strokeStyle = "#6cff72";
        ctx.lineWidth = 4;

        ctx.strokeRect(-58,-60,116,105);
    }

    ctx.restore();
}

/* =========================================================
   가스 분출 파티클
========================================================= */

let gasParticles = [];

function updateGasParticles() {

    geysers.forEach(g => {

        for(let i=0;i<2;i++) {

            gasParticles.push({
                x:g.x+(Math.random()-.5)*35,
                y:g.y-35,
                vx:(Math.random()-.5)*.5,
                vy:-Math.random()*1.5-0.5,
                life:1,
                size:Math.random()*5+3
            });
        }
    });

    gasParticles.forEach(p => {
        p.x += p.vx;
        p.y += p.vy;
        p.life -= .015;
    });

    gasParticles = gasParticles.filter(p => p.life>0);
}

function drawGasParticles() {

    gasParticles.forEach(p => {

        ctx.globalAlpha = p.life;

        ctx.fillStyle = "#63e98a";

        ctx.beginPath();
        ctx.arc(p.x,p.y,p.size,0,Math.PI*2);
        ctx.fill();
    });

    ctx.globalAlpha = 1;
}

/* =========================================================
   미네랄
========================================================= */

function drawMineral(m) {

    ctx.save();
    ctx.translate(m.x,m.y);

    /*
       그림자
    */
    ctx.fillStyle = "rgba(0,0,0,.4)";
    ctx.beginPath();
    ctx.ellipse(0,20,45,13,0,0,Math.PI*2);
    ctx.fill();

    /*
       결정
    */
    const grad = ctx.createLinearGradient(-40,-25,40,25);
    grad.addColorStop(0,"#d4f7ff");
    grad.addColorStop(.35,"#5acdf0");
    grad.addColorStop(1,"#175a85");

    ctx.fillStyle = grad;
    ctx.strokeStyle = "#173d54";
    ctx.lineWidth = 3;

    ctx.beginPath();
    ctx.moveTo(-42,12);
    ctx.lineTo(-25,-25);
    ctx.lineTo(-5,-35);
    ctx.lineTo(20,-22);
    ctx.lineTo(42,13);
    ctx.lineTo(20,25);
    ctx.lineTo(-25,25);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();

    ctx.restore();
}

/* =========================================================
   서플라이 디포
========================================================= */

function drawSupplyDepot(b) {

    ctx.save();
    ctx.translate(b.x,b.y);

    ctx.fillStyle = "#555f63";
    ctx.strokeStyle = "#161b1d";
    ctx.lineWidth = 4;

    ctx.beginPath();
    ctx.roundRect(-55,-50,110,100,8);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = "#777f80";

    ctx.fillRect(-42,-38,84,18);
    ctx.fillRect(-42,-12,84,18);
    ctx.fillRect(-42,14,84,18);

    ctx.fillStyle = "#e0bf43";
    ctx.fillRect(-43,-40,84,5);
    ctx.fillRect(-43,-14,84,5);
    ctx.fillRect(-43,12,84,5);

    if(b.building) {

        ctx.strokeStyle = "#62d9ff";
        ctx.lineWidth = 3;

        ctx.strokeRect(-62,-57,124,114);
    }

    ctx.restore();
}

/* =========================================================
   바위
========================================================= */

function drawRock(b) {

    ctx.save();
    ctx.translate(b.x,b.y);

    ctx.fillStyle = "#30383b";

    ctx.beginPath();
    ctx.moveTo(-b.w/2,15);
    ctx.lineTo(-b.w/3,-b.h/2);
    ctx.lineTo(5,-b.h/2-8);
    ctx.lineTo(b.w/2,-5);
    ctx.lineTo(b.w/3,b.h/2);
    ctx.lineTo(-b.w/3,b.h/2);
    ctx.closePath();
    ctx.fill();

    ctx.strokeStyle = "#171c1e";
    ctx.stroke();

    ctx.restore();
}

/* =========================================================
   건설 중 표시
========================================================= */

function drawConstruction(b) {

    ctx.save();
    ctx.translate(b.x,b.y);

    ctx.strokeStyle = "#61d9ff";
    ctx.lineWidth = 3;
    ctx.setLineDash([8,5]);

    ctx.strokeRect(
        -b.w/2,
        -b.h/2,
        b.w,
        b.h
    );

    ctx.setLineDash([]);

    ctx.fillStyle = "rgba(50,150,190,.18)";
    ctx.fillRect(-b.w/2,-b.h/2,b.w,b.h);

    /*
       건설 진행률
    */
    const progress = 1-(b.buildTime/b.totalBuildTime);

    ctx.fillStyle = "#222";
    ctx.fillRect(-60,-b.h/2-20,120,8);

    ctx.fillStyle = "#59e8ff";
    ctx.fillRect(-60,-b.h/2-20,120*progress,8);

    ctx.restore();
}

/* =========================================================
   맵 그리기
========================================================= */

function drawWorld() {

    ctx.clearRect(0,0,W,H);

    ctx.save();
    ctx.translate(-camera.x,-camera.y);

    /*
       바닥
    */
    ctx.fillStyle = "#15241c";
    ctx.fillRect(0,0,MAP_W,MAP_H);

    /*
       타일
    */
    ctx.strokeStyle = "rgba(80,110,90,.12)";
    ctx.lineWidth = 1;

    const grid = 80;

    for(let x=0;x<MAP_W;x+=grid) {

        ctx.beginPath();
        ctx.moveTo(x,0);
        ctx.lineTo(x,MAP_H);
        ctx.stroke();
    }

    for(let y=0;y<MAP_H;y+=grid) {

        ctx.beginPath();
        ctx.moveTo(0,y);
        ctx.lineTo(MAP_W,y);
        ctx.stroke();
    }

    /*
       장식
    */
    for(let i=0;i<60;i++) {

        const x=(i*313)%MAP_W;
        const y=(i*527)%MAP_H;

        ctx.fillStyle="rgba(50,90,55,.35)";

        ctx.beginPath();
        ctx.arc(x,y,25+(i%4)*8,0,Math.PI*2);
        ctx.fill();
    }

    /*
       가스 원천
    */
    geysers.forEach(g => {

        ctx.fillStyle = "#163f2a";

        ctx.beginPath();
        ctx.ellipse(g.x,g.y,70,50,0,0,Math.PI*2);
        ctx.fill();

        ctx.fillStyle = "#39d66b";

        ctx.beginPath();
        ctx.ellipse(g.x,g.y,43,30,0,0,Math.PI*2);
        ctx.fill();

        ctx.fillStyle = "#8affad";

        ctx.beginPath();
        ctx.ellipse(g.x,g.y,23,17,0,0,Math.PI*2);
        ctx.fill();
    });

    /*
       미네랄
    */
    mineralFields.forEach(drawMineral);

    /*
       건물
    */
    buildings.forEach(b => {

        if(b.type === "command")
            drawCommandCenter(b);

        else if(b.type === "gas")
            drawGasBuilding(b);

        else if(b.type === "depot")
            drawSupplyDepot(b);

        else if(b.type === "rock")
            drawRock(b);

        if(b.building)
            drawConstruction(b);
    });

    /*
       SCV
    */
    units.forEach(drawSCV);

    /*
       파티클
    */
    drawGasParticles();

    /*
       선택 박스
    */
    if(dragging) {

        const x=Math.min(dragStart.x,dragEnd.x)+camera.x;
        const y=Math.min(dragStart.y,dragEnd.y)+camera.y;

        const w=Math.abs(dragEnd.x-dragStart.x);
        const h=Math.abs(dragEnd.y-dragStart.y);

        ctx.strokeStyle="#6cff72";
        ctx.fillStyle="rgba(80,255,100,.08)";
        ctx.lineWidth=2;

        ctx.fillRect(x,y,w,h);
        ctx.strokeRect(x,y,w,h);
    }

    /*
       건설 미리보기
    */
    if(buildMode && buildPreview) {

        const p=buildPreview;

        ctx.globalAlpha=.55;

        if(buildMode==="gas") {

            drawGasBuilding({
                x:p.x,
                y:p.y
            });

        } else if(buildMode==="depot") {

            drawSupplyDepot({
                x:p.x,
                y:p.y,
                w:110,
                h:100
            });
        }

        ctx.globalAlpha=1;

        /*
           설치 가능 여부
        */
        ctx.strokeStyle = canBuildAt(p.x,p.y,buildMode)
            ? "#65ff72"
            : "#ff5555";

        ctx.lineWidth=4;

        const size=buildMode==="gas"
            ? 120
            : 125;

        ctx.strokeRect(
            p.x-size/2,
            p.y-size/2,
            size,
            size
        );
    }

    ctx.restore();
}

/* =========================================================
   충돌 / 설치 가능 검사
========================================================= */

function buildingRect(b) {

    return {
        left:b.x-b.w/2,
        right:b.x+b.w/2,
        top:b.y-b.h/2,
        bottom:b.y+b.h/2
    };
}

function overlap(a,b,padding=20) {

    const ar=buildingRect(a);
    const br=buildingRect(b);

    return !(
        ar.right+padding < br.left ||
        ar.left-padding > br.right ||
        ar.bottom+padding < br.top ||
        ar.top-padding > br.bottom
    );
}

function canBuildAt(x,y,type) {

    if(type==="gas") {

        /*
           가스 건물은 반드시 가스 위
        */
        const g=geysers.find(g =>
            Math.hypot(g.x-x,g.y-y)<75
        );

        if(!g)
            return false;

        const existing=buildings.find(b =>
            b.type==="gas" &&
            Math.hypot(b.x-x,b.y-y)<110
        );

        if(existing)
            return false;

        return true;
    }

    if(type==="depot") {

        const test={
            x:x,
            y:y,
            w:110,
            h:100
        };

        for(const b of buildings) {

            if(
                b.type==="rock" ||
                b.type==="command" ||
                b.type==="gas" ||
                b.type==="depot"
            ) {

                if(overlap(test,b,15))
                    return false;
            }
        }

        return true;
    }

    return false;
}

/* =========================================================
   건설
========================================================= */

function startGasBuild() {

    if(minerals<100) {
        showMessage("가스 채취 시설 건설에는 미네랄 100이 필요합니다.");
        return;
    }

    if(!selectedUnits.length) {
        showMessage("SCV를 먼저 선택하세요.");
        return;
    }

    buildMode="gas";
    buildPreview=worldMouse();

    document.getElementById("buildMode").style.display="block";

    showMessage("가스 위에 건설 위치를 클릭하세요.");
}

function startDepotBuild() {

    if(minerals<100) {
        showMessage("서플라이 디포 건설에는 미네랄 100이 필요합니다.");
        return;
    }

    if(!selectedUnits.length) {
        showMessage("SCV를 먼저 선택하세요.");
        return;
    }

    buildMode="depot";
    buildPreview=worldMouse();

    document.getElementById("buildMode").textContent =
        "서플라이 디포 건설 위치를 지정하세요";

    document.getElementById("buildMode").style.display="block";
}

function cancelBuildMode() {

    buildMode=null;
    buildPreview=null;

    document.getElementById("buildMode").style.display="none";
}

function placeBuilding(x,y) {

    if(!buildMode)
        return;

    if(!canBuildAt(x,y,buildMode)) {

        if(buildMode==="gas")
            showMessage("건설할 수 없음 — 가스가 없는 위치입니다.");

        else
            showMessage("건설할 수 없음 — 다른 건물과 겹칩니다.");

        return;
    }

    /*
       가장 가까운 SCV
    */
    let builder=selectedUnits[0];

    if(!builder) {
        cancelBuildMode();
        return;
    }

    /*
       비용
    */
    minerals-=100;

    const type=buildMode;

    const b={
        id:nextBuildingId++,
        type:type,
        x:x,
        y:y,

        w:type==="gas"?96:110,
        h:type==="gas"?90:100,

        hp:1,
        maxHp:type==="gas"?600:400,

        building:true,

        buildTime:type==="gas"?15:20,

        totalBuildTime:type==="gas"?15:20
    };

    buildings.push(b);

    builder.state="building";
    builder.buildTarget=b;
    builder.target=b;

    cancelBuildMode();

    sound("build");

    showMessage(
        type==="gas"
        ? "가스 채취 시설 건설을 시작했습니다."
        : "서플라이 디포 건설을 시작했습니다."
    );
}

/* =========================================================
   건설 완료
========================================================= */

function finishBuilding(b) {

    b.building=false;
    b.hp=b.maxHp;

    if(b.type==="depot") {

        supplyMax+=10;

        showMessage("서플라이 디포 완성! 인구수가 10 증가했습니다.");
    }

    else if(b.type==="gas") {

        showMessage("가스 채취 시설 완성!");
    }

    sound("complete");
}

/* =========================================================
   이동
========================================================= */

function moveUnitTo(u,x,y) {

    u.commandTarget={
        x:x,
        y:y
    };

    u.target=null;
    u.state="moving";
    u.resourceType=null;
}

function moveUnit(u) {

    if(!u.commandTarget)
        return;

    let target=u.commandTarget;

    let dx=target.x-u.x;
    let dy=target.y-u.y;

    let d=Math.hypot(dx,dy);

    if(d<5) {

        u.x=target.x;
        u.y=target.y;
        u.commandTarget=null;
        u.state="idle";

        return;
    }

    let vx=dx/d*u.speed;
    let vy=dy/d*u.speed;

    /*
       건물 회피
    */
    let next={
        x:u.x+vx,
        y:u.y+vy
    };

    for(const b of buildings) {

        if(b.building)
            continue;

        if(b.type==="rock" ||
           b.type==="command" ||
           b.type==="gas" ||
           b.type==="depot") {

            let r=Math.max(b.w,b.h)/2+30;

            if(
                Math.hypot(next.x-b.x,next.y-b.y)<r
            ) {

                /*
                   옆으로 살짝 이동
                */
                const sideX=-dy/d*1.5;
                const sideY=dx/d*1.5;

                vx+=sideX;
                vy+=sideY;
            }
        }
    }

    u.x+=vx;
    u.y+=vy;

    u.x=clamp(u.x,30,MAP_W-30);
    u.y=clamp(u.y,30,MAP_H-30);
}

/* =========================================================
   자원 채취 명령
========================================================= */

function orderMineral(u,m) {

    u.state="toMineral";
    u.target=m;
    u.resourceType="mineral";
    u.commandTarget=null;
}

function orderGas(u,b) {

    if(b.building) {
        showMessage("가스 채취 시설이 아직 건설 중입니다.");
        return;
    }

    u.state="toGas";
    u.target=b;
    u.resourceType="gas";
    u.commandTarget=null;
}

/* =========================================================
   자원 채취 업데이트
========================================================= */

function updateMining(u,dt) {

    if(
        u.state==="toMineral" ||
        u.state==="toGas"
    ) {

        if(!u.target) {
            u.state="idle";
            return;
        }

        let tx=u.target.x;
        let ty=u.target.y;

        /*
           가스 시설 / 미네랄에 접근
        */
        let reach=
            u.state==="toMineral"
            ? 75
            : 80;

        let d=Math.hypot(u.x-tx,u.y-ty);

        if(d>reach) {

            moveUnitTo(u,tx,ty);

            /*
               moveUnitTo가 자원 상태를 덮어쓰지 않도록 복구
            */
            u.state =
                u.resourceType==="mineral"
                ? "toMineral"
                : "toGas";

            u.commandTarget={
                x:tx,
                y:ty
            };

            return;
        }

        u.commandTarget=null;

        /*
           3초 채취
        */
        u.mineTimer+=dt;

        if(u.mineTimer>=3) {

            u.mineTimer=0;

            u.carrying=50;

            u.carryingType=
                u.resourceType==="mineral"
                ? "mineral"
                : "gas";

            if(u.resourceType==="mineral") {

                /*
                   미네랄은 사실상 무한
                */
                sound("mine");

            } else {

                /*
                   가스도 무한
                */
                sound("mine");
            }

            /*
               사령부로 복귀
            */
            u.state="returning";

            u.commandTarget={
                x:commandCenter.x,
                y:commandCenter.y+100
            };
        }
    }
}

/* =========================================================
   자원 반환
========================================================= */

function updateReturning(u) {

    if(u.state!=="returning")
        return;

    let tx=commandCenter.x;
    let ty=commandCenter.y+100;

    let d=Math.hypot(u.x-tx,u.y-ty);

    if(d>100) {

        moveUnitTo(u,tx,ty);

        u.state="returning";

        u.commandTarget={
            x:tx,
            y:ty
        };

        return;
    }

    /*
       자원 반납
    */
    if(u.carrying>0) {

        if(u.carryingType==="mineral")
            minerals+=u.carrying;

        else
            gas+=u.carrying;

        u.carrying=0;
        u.carryingType=null;

        updateHUD();
    }

    /*
       무한 반복
    */
    if(u.resourceType==="mineral") {

        u.state="toMineral";
        u.target=findClosestMineral(u);
        u.mineTimer=0;

    } else if(u.resourceType==="gas") {

        u.state="toGas";

        u.target=buildings.find(
            b=>b.type==="gas"&&!b.building
        );

        u.mineTimer=0;
    }
}

function findClosestMineral(u) {

    let best=null;
    let bestD=Infinity;

    mineralFields.forEach(m => {

        const d=distance(u,m);

        if(d<bestD) {
            bestD=d;
            best=m;
        }
    });

    return best;
}

/* =========================================================
   건설 SCV
========================================================= */

function updateBuilder(u,dt) {

    if(u.state!=="building")
        return;

    const b=u.buildTarget;

    if(!b) {
        u.state="idle";
        return;
    }

    const d=Math.hypot(u.x-b.x,u.y-b.y);

    if(d>100) {

        moveUnitTo(u,b.x,b.y);

        u.state="building";
        u.commandTarget={
            x:b.x,
            y:b.y
        };

        return;
    }

    u.commandTarget=null;

    b.buildTime-=dt;

    if(b.buildTime<=0) {

        finishBuilding(b);

        u.state="idle";
        u.buildTarget=null;
    }
}

/* =========================================================
   SCV 생산
========================================================= */

let productionQueue=[];

function trainSCV() {

    if(!commandCenter)
        return;

    if(minerals<50) {
        showMessage("SCV 생산에는 미네랄 50이 필요합니다.");
        return;
    }

    /*
       최대 5개 생산 대기
    */
    if(productionQueue.length>=5) {

        showMessage("SCV 생산 대기열은 최대 5개입니다.");
        return;
    }

    if(supplyUsed+productionQueue.length>=supplyMax) {

        showMessage("인구수가 부족합니다.");
        return;
    }

    minerals-=50;

    productionQueue.push({
        time:10,
        total:10
    });

    showMessage("SCV 생산을 시작했습니다.");
    updateHUD();
}

function updateProduction(dt) {

    if(productionQueue.length===0)
        return;

    productionQueue[0].time-=dt;

    if(productionQueue[0].time<=0) {

        productionQueue.shift();

        const spawnX=
            commandCenter.x+
            commandCenter.w/2+
            45+
            Math.random()*30;

        const spawnY=
            commandCenter.y+
            (Math.random()-.5)*100;

        createSCV(spawnX,spawnY);

        showMessage("SCV 생산 완료!");
        sound("complete");
    }
}

/* =========================================================
   자동 SCV 상태
========================================================= */

function updateUnit(u,dt) {

    /*
       건설
    */
    if(u.state==="building") {
        updateBuilder(u,dt);
        return;
    }

    /*
       자원 채취
    */
    if(
        u.state==="toMineral" ||
        u.state==="toGas"
    ) {

        updateMining(u,dt);
        return;
    }

    /*
       자원 반납
    */
    if(u.state==="returning") {

        updateReturning(u);
        return;
    }

    /*
       일반 이동
    */
    if(u.state==="moving") {

        moveUnit(u);
        return;
    }
}

/* =========================================================
   선택
========================================================= */

function clearSelection() {

    units.forEach(u=>u.selected=false);

    selectedUnits=[];

    selectedObject=null;

    updateSidePanel();
}

function selectUnit(u,add=false) {

    if(!add)
        clearSelection();

    if(!u.selected) {

        u.selected=true;
        selectedUnits.push(u);
    }

    selectedObject=null;

    updateSidePanel();
}

function selectObject(obj) {

    clearSelection();

    selectedObject=obj;

    updateSidePanel();
}

/* =========================================================
   오브젝트 찾기
========================================================= */

function getUnitAt(x,y) {

    for(let i=units.length-1;i>=0;i--) {

        const u=units[i];

        if(Math.hypot(x-u.x,y-u.y)<35)
            return u;
    }

    return null;
}

function getBuildingAt(x,y) {

    for(let i=buildings.length-1;i>=0;i--) {

        const b=buildings[i];

        if(b.type==="rock")
            continue;

        if(
            Math.abs(x-b.x)<b.w/2 &&
            Math.abs(y-b.y)<b.h/2
        )
            return b;
    }

    return null;
}

function getMineralAt(x,y) {

    for(const m of mineralFields) {

        if(
            Math.abs(x-m.x)<60 &&
            Math.abs(y-m.y)<50
        )
            return m;
    }

    return null;
}

function getGeyserAt(x,y) {

    for(const g of geysers) {

        if(
            Math.hypot(x-g.x,y-g.y)<75
        )
            return g;
    }

    return null;
}

/* =========================================================
   우클릭 명령
========================================================= */

function rightClickCommand(x,y) {

    const m=getMineralAt(x,y);

    if(m) {

        selectedUnits.forEach(u=>{
            orderMineral(u,m);
        });

        showMessage("SCV가 미네랄을 채취합니다.");
        return;
    }

    const b=getBuildingAt(x,y);

    if(b && b.type==="gas") {

        selectedUnits.forEach(u=>{
            orderGas(u,b);
        });

        showMessage("SCV가 가스를 채취합니다.");
        return;
    }

    /*
       일반 이동
    */
    selectedUnits.forEach(u=>{
        moveUnitTo(u,x,y);
    });

    if(selectedUnits.length)
        showMessage("이동 명령");
}

/* =========================================================
   좌클릭
========================================================= */

canvas.addEventListener("mousedown",e=>{

    mouse.x=e.clientX;
    mouse.y=e.clientY;

    if(e.button===0) {

        mouse.down=true;

        dragStart={
            x:mouse.x,
            y:mouse.y
        };

        dragEnd={
            x:mouse.x,
            y:mouse.y
        };

        dragging=false;
    }

    if(e.button===2) {

        e.preventDefault();

        /*
           건설 중이면 우클릭 취소
        */
        if(buildMode) {

            cancelBuildMode();

            showMessage("건설 위치 지정이 취소되었습니다.");
            return;
        }
    }
});

canvas.addEventListener("mousemove",e=>{

    mouse.x=e.clientX;
    mouse.y=e.clientY;

    if(mouse.down) {

        const dx=mouse.x-dragStart.x;
        const dy=mouse.y-dragStart.y;

        if(Math.hypot(dx,dy)>7)
            dragging=true;

        dragEnd={
            x:mouse.x,
            y:mouse.y
        };
    }

    if(buildMode) {

        buildPreview=worldMouse();
    }
});

canvas.addEventListener("mouseup",e=>{

    mouse.x=e.clientX;
    mouse.y=e.clientY;

    if(e.button===0) {

        mouse.down=false;

        /*
           건설 모드
        */
        if(buildMode) {

            const p=worldMouse();

            placeBuilding(p.x,p.y);

            return;
        }

        /*
           드래그 선택
        */
        if(dragging) {

            const left=Math.min(
                dragStart.x,
                dragEnd.x
            );

            const right=Math.max(
                dragStart.x,
                dragEnd.x
            );

            const top=Math.min(
                dragStart.y,
                dragEnd.y
            );

            const bottom=Math.max(
                dragStart.y,
                dragEnd.y
            );

            clearSelection();

            units.forEach(u=>{

                const sx=u.x-camera.x;
                const sy=u.y-camera.y;

                if(
                    sx>=left &&
                    sx<=right &&
                    sy>=top &&
                    sy<=bottom
                ) {

                    u.selected=true;
                    selectedUnits.push(u);
                }
            });

            updateSidePanel();

            dragging=false;

            return;
        }

        /*
           단일 선택
        */
        const p=worldMouse();

        const u=getUnitAt(p.x,p.y);

        if(u) {

            selectUnit(u);
            sound("click");
            return;
        }

        const b=getBuildingAt(p.x,p.y);

        if(b) {

            selectObject(b);
            sound("click");
            return;
        }

        clearSelection();
    }
});

canvas.addEventListener("contextmenu",e=>{
    e.preventDefault();

    if(buildMode) {
        cancelBuildMode();
        return;
    }

    const p={
        x:e.clientX+camera.x,
        y:e.clientY+camera.y
    };

    rightClickCommand(p.x,p.y);
});

/* =========================================================
   상태창
========================================================= */

function updateSidePanel() {

    const panel=document.getElementById("sidePanel");

    if(
        selectedUnits.length===0 &&
        !selectedObject
    ) {

        panel.style.display="none";
        return;
    }

    panel.style.display="block";

    /*
       여러 SCV
    */
    if(selectedUnits.length>0) {

        if(selectedUnits.length===1) {

            const u=selectedUnits[0];

            panel.innerHTML=`
                <h2>🔧 SCV</h2>

                <div class="stat">
                    체력: ${u.hp} / ${u.maxHp}
                </div>

                <div class="stat">
                    상태: ${stateText(u.state)}
                </div>

                <div class="stat">
                    운반: ${u.carryingType || "없음"}
                    ${u.carrying>0 ? " " + u.carrying : ""}
                </div>

                <button onclick="startGasBuild()">
                    🟢 가스 채취 시설 건설
                </button>

                <button onclick="startDepotBuild()">
                    🏗️ 서플라이 디포 건설
                    <br>
                    100 미네랄 / 20초
                </button>
            `;

        } else {

            panel.innerHTML=`
                <h2>SCV 선택</h2>
                <div class="stat">
                    선택된 SCV: ${selectedUnits.length}
                </div>

                <button onclick="startGasBuild()">
                    🟢 가스 채취 시설 건설
                </button>

                <button onclick="startDepotBuild()">
                    🏗️ 서플라이 디포 건설
                </button>
            `;
        }

        return;
    }

    /*
       건물
    */
    if(selectedObject) {

        const b=selectedObject;

        if(b.type==="command") {

            panel.innerHTML=`
                <h2>🏢 사령부</h2>

                <div class="stat">
                    체력:
                    ${Math.floor(b.hp)}
                    / ${b.maxHp}
                </div>

                <div class="stat">
                    SCV 생산 대기:
                    ${productionQueue.length} / 5
                </div>

                <button
                    onclick="trainSCV()"
                    ${productionQueue.length>=5 ? "disabled":""}
                >
                    🔧 SCV 만들기
                    <br>
                    50 미네랄 / 10초
                </button>
            `;

        } else if(b.type==="gas") {

            panel.innerHTML=`
                <h2>🟢 가스 채취 시설</h2>

                <div class="stat">
                    체력: ${b.hp} / ${b.maxHp}
                </div>

                <div class="stat">
                    가스: 무한
                </div>

                <button onclick="commandGasFromPanel()">
                    가스 채취
                </button>
            `;

        } else if(b.type==="depot") {

            panel.innerHTML=`
                <h2>📦 서플라이 디포</h2>

                <div class="stat">
                    체력: ${b.hp} / ${b.maxHp}
                </div>

                <div class="stat">
                    인구수 +10
                </div>
            `;
        }
    }
}

function stateText(s) {

    const map={
        idle:"대기",
        moving:"이동 중",
        toMineral:"미네랄 이동 중",
        toGas:"가스 이동 중",
        returning:"자원 반환 중",
        building:"건설 중"
    };

    return map[s] || s;
}

function commandGasFromPanel() {

    const gasBuilding=buildings.find(
        b=>b.type==="gas"&&!b.building
    );

    if(!gasBuilding)
        return;

    selectedUnits.forEach(u=>{
        orderGas(u,gasBuilding);
    });
}

/* =========================================================
   카메라
========================================================= */

function updateCamera() {

    const edge=45;

    /*
       화면 위
    */
    if(mouse.y<edge)
        camera.y-=camera.speed;

    /*
       화면 아래
    */
    if(mouse.y>H-edge)
        camera.y+=camera.speed;

    /*
       왼쪽
    */
    if(mouse.x<edge)
        camera.x-=camera.speed;

    /*
       오른쪽
    */
    if(mouse.x>W-edge)
        camera.x+=camera.speed;

    camera.x=clamp(
        camera.x,
        0,
        MAP_W-W
    );

    camera.y=clamp(
        camera.y,
        0,
        MAP_H-H
    );
}

/* =========================================================
   미니맵
========================================================= */

function drawMinimap() {

    const mw=mini.width;
    const mh=mini.height;

    mctx.clearRect(0,0,mw,mh);

    mctx.fillStyle="#132219";
    mctx.fillRect(0,0,mw,mh);

    const sx=mw/MAP_W;
    const sy=mh/MAP_H;

    /*
       미네랄
    */
    mineralFields.forEach(m=>{

        mctx.fillStyle="#53d9ff";

        mctx.fillRect(
            m.x*sx-3,
            m.y*sy-3,
            6,
            6
        );
    });

    /*
       가스
    */
    geysers.forEach(g=>{

        mctx.fillStyle="#57f58b";

        mctx.beginPath();
        mctx.arc(
            g.x*sx,
            g.y*sy,
            5,
            0,
            Math.PI*2
        );
        mctx.fill();
    });

    /*
       건물
    */
    buildings.forEach(b=>{

        if(b.type==="rock")
            return;

        if(b.type==="command")
            mctx.fillStyle="#d9d9d9";

        else if(b.type==="gas")
            mctx.fillStyle="#52ff85";

        else if(b.type==="depot")
            mctx.fillStyle="#b7a95a";

        mctx.fillRect(
            b.x*sx-4,
            b.y*sy-4,
            8,
            8
        );
    });

    /*
       SCV
    */
    units.forEach(u=>{

        mctx.fillStyle=u.selected
            ? "#7dff7d"
            : "#e1e1e1";

        mctx.fillRect(
            u.x*sx-2,
            u.y*sy-2,
            4,
            4
        );
    });

    /*
       현재 화면
    */
    mctx.strokeStyle="#ffffff";
    mctx.lineWidth=2;

    mctx.strokeRect(
        camera.x*sx,
        camera.y*sy,
        W*sx,
        H*sy
    );
}

mini.addEventListener("click",e=>{

    const rect=mini.getBoundingClientRect();

    const x=e.clientX-rect.left;
    const y=e.clientY-rect.top;

    camera.x=
        x/MAP_W*MAP_W-
        W/2;

    camera.y=
        y/MAP_H*MAP_H-
        H/2;

    camera.x=clamp(camera.x,0,MAP_W-W);
    camera.y=clamp(camera.y,0,MAP_H-H);
});

/* =========================================================
   키보드
========================================================= */

window.addEventListener("keydown",e=>{

    if(e.key==="Escape") {

        clearSelection();
        cancelBuildMode();
    }
});

/* =========================================================
   게임 루프
========================================================= */

let lastTime=performance.now();

function gameLoop(now) {

    const dt=Math.min(
        (now-lastTime)/1000,
        .1
    );

    lastTime=now;

    if(gameStarted) {

        updateCamera();

        updateProduction(dt);

        units.forEach(u=>{
            updateUnit(u,dt);
        });

        /*
           건설 완료 여부
        */
        buildings.forEach(b=>{

            if(
                b.building &&
                b.buildTime<=0
            ) {
                finishBuilding(b);
            }
        });

        updateGasParticles();

        drawWorld();
        drawMinimap();
        updateHUD();
    }

    requestAnimationFrame(gameLoop);
}

/* =========================================================
   시작
========================================================= */

function startTerran() {

    document.getElementById("raceScreen").style.display="none";

    gameStarted=true;

    createMap();

    spawnStartingSCVs();

    /*
       시작 화면 중심
    */
    camera.x=
        commandCenter.x-W/2;

    camera.y=
        commandCenter.y-H/2;

    camera.x=clamp(camera.x,0,MAP_W-W);
    camera.y=clamp(camera.y,0,MAP_H-H);

    updateHUD();

    document.getElementById("statusText").textContent =
        "테란 기지 — SCV 5기를 선택하여 자원을 채취하세요.";

    showMessage("테란 기지가 건설되었습니다!");
}

/* =========================================================
   창 크기
========================================================= */

window.addEventListener("resize",()=>{

    W=window.innerWidth;
    H=window.innerHeight;

    canvas.width=W;
    canvas.height=H;
});

/* 시작 */
requestAnimationFrame(gameLoop);

</script>

</body>
</html>
"""

components.html(
    GAME_HTML,
    height=900,
    scrolling=False
)
