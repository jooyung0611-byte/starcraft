import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Terran RTS",
    layout="wide",
    initial_sidebar_state="collapsed"
)

html = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
* {
    box-sizing: border-box;
}

html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #07100b;
    font-family: Arial, sans-serif;
}

canvas {
    display: block;
}

#game {
    position: fixed;
    inset: 0;
}

#factionScreen {
    position: fixed;
    inset: 0;
    z-index: 1000;
    display: flex;
    justify-content: center;
    align-items: center;
    background:
        radial-gradient(circle at center, #304c38 0%, #111c15 45%, #050905 100%);
}

.factionBox {
    width: 430px;
    padding: 35px;
    text-align: center;
    color: white;
    background: rgba(12,20,16,.94);
    border: 1px solid #708477;
    border-radius: 15px;
    box-shadow: 0 20px 80px rgba(0,0,0,.8);
}

.factionBox h1 {
    margin: 0 0 10px;
    font-size: 38px;
}

.factionBox p {
    color: #bdc8c1;
}

.terranButton {
    width: 100%;
    margin-top: 20px;
    padding: 18px;
    border: 1px solid #879b8e;
    border-radius: 8px;
    background: #26392e;
    color: white;
    font-size: 21px;
    cursor: pointer;
}

.terranButton:hover {
    background: #3a5543;
}

#hud {
    display: none;
}

#topResources {
    position: fixed;
    top: 12px;
    left: 12px;
    z-index: 50;
    display: flex;
    gap: 8px;
}

.resource {
    padding: 9px 14px;
    color: white;
    background: rgba(7,14,11,.92);
    border: 1px solid #62736a;
    border-radius: 7px;
}

#sidePanel {
    position: fixed;
    top: 12px;
    right: 12px;
    width: 290px;
    min-height: 200px;
    padding: 16px;
    z-index: 50;
    color: white;
    background: rgba(7,14,11,.95);
    border: 1px solid #65766c;
    border-radius: 9px;
}

#sidePanel h3 {
    margin-top: 0;
}

.stat {
    margin: 8px 0;
    color: #d5ded9;
}

.uiButton {
    width: 100%;
    margin-top: 8px;
    padding: 10px;
    color: white;
    background: #293d31;
    border: 1px solid #687b70;
    border-radius: 6px;
    cursor: pointer;
}

.uiButton:hover {
    background: #3b5846;
}

.uiButton:disabled {
    opacity: .4;
    cursor: default;
}

#miniMap {
    position: fixed;
    bottom: 12px;
    left: 12px;
    width: 270px;
    height: 175px;
    z-index: 60;
    background: #1d2c20;
    border: 2px solid #85968c;
    border-radius: 5px;
    cursor: pointer;
}

#dragBox {
    display: none;
    position: fixed;
    z-index: 100;
    pointer-events: none;
    border: 1px solid #69ff7d;
    background: rgba(70,255,100,.15);
}

#buildMessage {
    display: none;
    position: fixed;
    top: 75px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 90;
    padding: 10px 18px;
    color: white;
    background: rgba(100,50,15,.92);
    border: 1px solid #ffb26d;
    border-radius: 7px;
    text-align: center;
}

#message {
    position: fixed;
    left: 50%;
    bottom: 25px;
    transform: translateX(-50%);
    z-index: 200;
    padding: 10px 18px;
    color: white;
    background: rgba(0,0,0,.85);
    border-radius: 7px;
    opacity: 0;
    transition: opacity .2s;
    pointer-events: none;
}
</style>
</head>

<body>

<div id="factionScreen">
    <div class="factionBox">
        <h1>STARCRAFT RTS</h1>
        <p>종족을 선택하세요.</p>
        <button class="terranButton" onclick="startTerran()">
            🚀 테란
        </button>
    </div>
</div>

<div id="hud">

    <div id="game"></div>

    <div id="topResources">
        <div class="resource">
            💎 미네랄 <b id="minerals">500</b>
        </div>

        <div class="resource">
            🟢 가스 <b id="gas">0</b>
        </div>

        <div class="resource">
            👨‍🚀 SCV <b id="scvCount">5</b>
        </div>

        <div class="resource">
            🏭 생산 <b id="production">0/5</b>
        </div>
    </div>

    <div id="sidePanel">
        <h3>선택 없음</h3>
        <div>유닛이나 건물을 선택하세요.</div>
    </div>

    <canvas id="miniMap"></canvas>

    <div id="dragBox"></div>

    <div id="buildMessage">
        🏗️ 가스 채취 시설 건설 모드<br>
        <small>가스 지역을 클릭하세요.</small>
    </div>

    <div id="message"></div>

</div>

<script type="module">

import * as THREE from
"https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.module.js";


/* =========================================================
   기본 설정
========================================================= */

let gameStarted = false;

window.startTerran = function() {
    document.getElementById("factionScreen").style.display = "none";
    document.getElementById("hud").style.display = "block";
    gameStarted = true;
};


/* =========================================================
   THREE.JS
========================================================= */

const scene = new THREE.Scene();

scene.background = new THREE.Color(0x18251a);

scene.fog = new THREE.Fog(
    0x18251a,
    70,
    190
);


const camera = new THREE.PerspectiveCamera(
    50,
    window.innerWidth / window.innerHeight,
    .1,
    500
);


const renderer = new THREE.WebGLRenderer({
    antialias: true
});

renderer.setSize(
    window.innerWidth,
    window.innerHeight
);

renderer.setPixelRatio(
    Math.min(window.devicePixelRatio, 2)
);

renderer.shadowMap.enabled = true;

document
    .getElementById("game")
    .appendChild(renderer.domElement);


/* =========================================================
   조명
========================================================= */

scene.add(
    new THREE.HemisphereLight(
        0xdcecff,
        0x27351f,
        1.7
    )
);

const sun = new THREE.DirectionalLight(
    0xffffff,
    2.2
);

sun.position.set(30,80,25);
sun.castShadow = true;

scene.add(sun);


/* =========================================================
   맵
========================================================= */

const groundMaterial =
    new THREE.MeshStandardMaterial({
        color: 0x354a30,
        roughness: 1
    });

const ground =
    new THREE.Mesh(
        new THREE.PlaneGeometry(180,180),
        groundMaterial
    );

ground.rotation.x = -Math.PI / 2;

ground.receiveShadow = true;

ground.userData.type = "ground";

scene.add(ground);


/* =========================================================
   데이터
========================================================= */

const minerals = [];
const geysers = [];
const gasFacilities = [];
const scvs = [];

let commandCenter = null;

let selectedUnits = [];
let selectedObject = null;

let mineralAmount = 500;
let gasAmount = 0;

let productionQueue = 0;

let buildMode = false;
let buildSCV = null;


/* =========================================================
   카메라
========================================================= */

let cameraTarget =
    new THREE.Vector3(0,0,0);

let cameraHeight = 55;


/* =========================================================
   마우스
========================================================= */

const raycaster =
    new THREE.Raycaster();

const mouse =
    new THREE.Vector2();

let mouseX = 0;
let mouseY = 0;

let mouseDown = false;

let dragStartX = 0;
let dragStartY = 0;


/* =========================================================
   재질
========================================================= */

function material(
    color,
    roughness=.5,
    metalness=.2,
    emissive=0
) {

    return new THREE.MeshStandardMaterial({
        color,
        roughness,
        metalness,
        emissive,
        emissiveIntensity:
            emissive ? 1 : 0
    });
}


/* =========================================================
   메시지
========================================================= */

function showMessage(text) {

    const element =
        document.getElementById("message");

    element.textContent = text;
    element.style.opacity = "1";

    clearTimeout(showMessage.timer);

    showMessage.timer =
        setTimeout(() => {
            element.style.opacity = "0";
        }, 1700);
}


/* =========================================================
   미네랄
========================================================= */

function createMineral(x,z) {

    const group = new THREE.Group();

    const mat =
        material(
            0x168cff,
            .25,
            .2,
            0x168cff
        );

    for(let i=0;i<7;i++) {

        const height =
            1.5 + Math.random()*1.8;

        const crystal =
            new THREE.Mesh(
                new THREE.CylinderGeometry(
                    .3,
                    .55,
                    height,
                    6
                ),
                mat
            );

        crystal.position.set(
            (Math.random()-.5)*2,
            height/2,
            (Math.random()-.5)*2
        );

        crystal.rotation.z =
            (Math.random()-.5)*.3;

        crystal.rotation.y =
            Math.random()*Math.PI*2;

        crystal.castShadow = true;

        group.add(crystal);
    }

    group.position.set(x,0,z);

    group.userData = {
        type: "mineral",
        amount: 1500
    };

    minerals.push(group);

    scene.add(group);
}


/* =========================================================
   미네랄 배치
========================================================= */

const mineralPositions = [

    [-31,-11],
    [-29,-7],
    [-31,-3],
    [-29,1],
    [-31,5],
    [-28,9],

    [-25,-10],
    [-24,-6],
    [-25,-2],
    [-24,2],
    [-25,6],

    [30,-12],
    [32,-8],
    [30,-4],
    [32,0],
    [30,4],
    [32,8],

    [27,-10],
    [28,-6],
    [28,-2],
    [27,2]

];

mineralPositions.forEach(
    p => createMineral(p[0],p[1])
);


/* =========================================================
   가스 지역
========================================================= */

function createGeyser(x,z) {

    const group =
        new THREE.Group();

    const rock =
        new THREE.Mesh(
            new THREE.DodecahedronGeometry(3.1,1),
            material(0x4c5550,.95,.1)
        );

    rock.scale.y = .65;

    rock.position.y = 1.1;

    rock.castShadow = true;

    group.add(rock);


    const hole =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                1.35,
                1.55,
                .35,
                32
            ),
            material(
                0x102318,
                .3,
                .1,
                0x102318
            )
        );

    hole.position.y = 2.35;

    group.add(hole);


    const gas =
        new THREE.Mesh(
            new THREE.SphereGeometry(
                1.35,
                16,
                16
            ),
            new THREE.MeshBasicMaterial({
                color: 0x35ff89,
                transparent: true,
                opacity: .4
            })
        );

    gas.position.y = 3.1;

    group.add(gas);


    group.position.set(x,0,z);

    group.userData = {
        type: "geyser",
        hasFacility: false,
        gasMesh: gas
    };

    geysers.push(group);

    scene.add(group);
}

createGeyser(-9,-16);
createGeyser(14,-14);


/* =========================================================
   사령부
========================================================= */

function createCommandCenter(x,z) {

    const group =
        new THREE.Group();


    const base =
        new THREE.Mesh(
            new THREE.BoxGeometry(12,2.2,9),
            material(0x565f63,.4,.8)
        );

    base.position.y = 1.1;

    base.castShadow = true;

    group.add(base);


    const body =
        new THREE.Mesh(
            new THREE.BoxGeometry(8,5,6),
            material(0x747b7d,.45,.65)
        );

    body.position.y = 4;

    body.castShadow = true;

    group.add(body);


    const roof =
        new THREE.Mesh(
            new THREE.BoxGeometry(9,1,7),
            material(0x3b4448,.4,.85)
        );

    roof.position.y = 6.8;

    group.add(roof);


    const core =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                1.2,
                1.2,
                .6,
                24
            ),
            new THREE.MeshStandardMaterial({
                color: 0x55ccff,
                emissive: 0x168cff,
                emissiveIntensity: 1.7
            })
        );

    core.position.y = 7.5;

    group.add(core);


    const tower =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                .12,
                .12,
                4,
                8
            ),
            material(0x24292b,.3,.9)
        );

    tower.position.y = 9.3;

    group.add(tower);


    const lamp =
        new THREE.Mesh(
            new THREE.SphereGeometry(.3,12,12),
            new THREE.MeshBasicMaterial({
                color: 0xff4433
            })
        );

    lamp.position.y = 11.3;

    group.add(lamp);


    for(const side of [-1,1]) {

        const vent =
            new THREE.Mesh(
                new THREE.BoxGeometry(
                    1.2,.7,2.5
                ),
                material(0x30373a,.35,.8)
            );

        vent.position.set(
            side*5.1,
            2.3,
            0
        );

        group.add(vent);
    }


    group.position.set(x,0,z);

    group.userData = {
        type: "command",
        hp: 1500,
        maxHp: 1500
    };

    commandCenter = group;

    scene.add(group);
}

createCommandCenter(0,0);


/* =========================================================
   SCV
========================================================= */

function createSCV(x,z) {

    const group =
        new THREE.Group();


    const body =
        new THREE.Mesh(
            new THREE.BoxGeometry(2.2,.8,2.8),
            material(0x8d9493,.35,.8)
        );

    body.position.y = 1;

    body.castShadow = true;

    group.add(body);


    const cabin =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                1.5,.9,1.3
            ),
            material(0x252c30,.3,.65)
        );

    cabin.position.set(
        0,
        1.7,
        -.25
    );

    cabin.castShadow = true;

    group.add(cabin);


    const front =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                1.5,.35,1.2
            ),
            material(0xb2b6b5,.4,.85)
        );

    front.position.set(
        0,
        .75,
        1.8
    );

    group.add(front);


    for(const side of [-1,1]) {

        for(const zPos of [-.85,.85]) {

            const wheel =
                new THREE.Mesh(
                    new THREE.CylinderGeometry(
                        .45,
                        .45,
                        .3,
                        12
                    ),
                    material(
                        0x151719,
                        .9,
                        .05
                    )
                );

            wheel.rotation.z =
                Math.PI/2;

            wheel.position.set(
                side*1.15,
                .55,
                zPos
            );

            wheel.castShadow = true;

            group.add(wheel);
        }
    }


    for(const side of [-.6,.6]) {

        const light =
            new THREE.Mesh(
                new THREE.SphereGeometry(
                    .13,
                    10,
                    10
                ),
                new THREE.MeshBasicMaterial({
                    color: 0xffe9a3
                })
            );

        light.position.set(
            side,
            1.15,
            1.45
        );

        group.add(light);
    }


    group.position.set(x,0,z);

    group.userData = {

        type: "scv",

        hp: 50,
        maxHp: 50,

        state: "대기",

        target: null,

        carrying: 0,

        carryType: null,

        building: false,

        path: null
    };


    scvs.push(group);

    scene.add(group);

    return group;
}


/* 시작 SCV 5기 */

[
    [-5,6],
    [-2,7],
    [1,6],
    [4,7],
    [7,6]

].forEach(
    p => createSCV(p[0],p[1])
);


/* =========================================================
   가스 채취 시설
========================================================= */

function createGasFacility(geyser) {

    const group =
        new THREE.Group();


    const base =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                2.3,
                2.6,
                1.2,
                16
            ),
            material(0x555d60,.4,.8)
        );

    base.position.y = .7;

    base.castShadow = true;

    group.add(base);


    const tank =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                1.7,
                1.7,
                3.5,
                16
            ),
            material(0x4d5558,.35,.75)
        );

    tank.position.y = 2.8;

    tank.castShadow = true;

    group.add(tank);


    const core =
        new THREE.Mesh(
            new THREE.SphereGeometry(1,16,16),
            new THREE.MeshStandardMaterial({
                color: 0x37ff8b,
                emissive: 0x18b85e,
                emissiveIntensity: 1.6
            })
        );

    core.position.y = 4.7;

    group.add(core);


    group.position.copy(
        geyser.position
    );


    group.userData = {

        type: "gasFacility",

        hp: 500,
        maxHp: 500,

        gas: 2500
    };


    geyser.userData.hasFacility = true;

    gasFacilities.push(group);

    scene.add(group);

    return group;
}


/* =========================================================
   선택 표시
========================================================= */

function addSelection(object) {

    if(!object) return;

    if(object.userData.selectionRing)
        return;


    const ring =
        new THREE.Mesh(
            new THREE.RingGeometry(
                1.5,
                1.7,
                32
            ),
            new THREE.MeshBasicMaterial({
                color: 0x55ff55,
                side: THREE.DoubleSide
            })
        );

    ring.rotation.x =
        -Math.PI/2;

    ring.position.y = .06;

    object.add(ring);

    object.userData.selectionRing = ring;
}


function removeSelection(object) {

    if(
        object &&
        object.userData.selectionRing
    ) {

        object.remove(
            object.userData.selectionRing
        );

        object.userData.selectionRing =
            null;
    }
}


function clearSelection() {

    selectedUnits.forEach(
        removeSelection
    );

    if(selectedObject)
        removeSelection(selectedObject);

    selectedUnits = [];

    selectedObject = null;

    showPanel(null);
}


/* =========================================================
   상태창
========================================================= */

function showPanel(object) {

    const panel =
        document.getElementById(
            "sidePanel"
        );


    if(!object) {

        panel.innerHTML = `
            <h3>선택 없음</h3>
            <div>유닛이나 건물을 선택하세요.</div>
        `;

        return;
    }


    const data = object.userData;


    if(data.type === "scv") {

        panel.innerHTML = `

            <h3>👨‍🚀 SCV</h3>

            <div class="stat">
                ❤️ 체력
                ${data.hp}/${data.maxHp}
            </div>

            <div class="stat">
                상태: ${data.state}
            </div>

            <div class="stat">
                운반:
                ${data.carrying}
                ${data.carryType || ""}
            </div>

            <button
                class="uiButton"
                onclick="startBuildMode()"
            >
                🏗️ 가스 채취 시설 건설
            </button>
        `;

    }


    else if(data.type === "command") {

        panel.innerHTML = `

            <h3>🏭 사령부</h3>

            <div class="stat">
                ❤️ 체력
                ${data.hp}/${data.maxHp}
            </div>

            <div class="stat">
                SCV 생산 대기
                ${productionQueue}/5
            </div>

            <button
                class="uiButton"
                onclick="produceSCV()"
                ${productionQueue >= 5 ? "disabled" : ""}
            >
                👨‍🚀 SCV 생산<br>
                💎 50 / ⏱️ 10초
            </button>
        `;

    }


    else if(data.type === "gasFacility") {

        panel.innerHTML = `

            <h3>🟢 가스 채취 시설</h3>

            <div class="stat">
                ❤️ 체력
                ${data.hp}/${data.maxHp}
            </div>

            <div class="stat">
                남은 가스
                ${data.gas}
            </div>

            <div class="stat">
                상태: 채취 가능
            </div>
        `;

    }


    else if(data.type === "geyser") {

        panel.innerHTML = `

            <h3>🟢 가스 지역</h3>

            <div class="stat">
                ${
                    data.hasFacility
                    ? "가스 시설 건설 완료"
                    : "가스 시설 없음"
                }
            </div>
        `;

    }


    else if(data.type === "mineral") {

        panel.innerHTML = `

            <h3>💎 미네랄</h3>

            <div class="stat">
                남은 미네랄
                ${data.amount}
            </div>
        `;
    }
}


/* =========================================================
   SCV 생산
========================================================= */

window.produceSCV = function() {

    if(productionQueue >= 5) {

        showMessage(
            "생산 대기열이 가득 찼습니다."
        );

        return;
    }


    if(mineralAmount < 50) {

        showMessage(
            "미네랄이 부족합니다."
        );

        return;
    }


    mineralAmount -= 50;

    productionQueue++;

    updateResources();

    showPanel(commandCenter);

    showMessage(
        "SCV 생산 시작!"
    );


    setTimeout(() => {

        productionQueue--;

        createSCV(
            7 + Math.random()*2,
            2 + Math.random()*2
        );

        updateResources();

        showPanel(commandCenter);

        showMessage(
            "SCV 생산 완료!"
        );

    },10000);
};


/* =========================================================
   이동
========================================================= */

function moveUnit(
    unit,
    x,
    z,
    callback=null
) {

    unit.userData.path = {
        x,
        z,
        callback
    };

    unit.userData.state = "이동 중";
}


/* =========================================================
   SCV 명령 초기화
========================================================= */

function stopSCV(unit) {

    unit.userData.target = null;

    unit.userData.path = null;

    unit.userData.carrying = 0;

    unit.userData.carryType = null;

    unit.userData.building = false;

    unit.userData.state = "대기";
}


/* =========================================================
   미네랄 채취
========================================================= */

function mineMineral(
    scv,
    mineral
) {

    if(mineral.userData.amount <= 0) {

        showMessage(
            "미네랄이 고갈되었습니다."
        );

        return;
    }


    scv.userData.target =
        mineral;

    scv.userData.state =
        "미네랄 채취 중";


    moveUnit(
        scv,
        mineral.position.x,
        mineral.position.z,

        () => {

            setTimeout(() => {

                if(
                    scv.userData.target !==
                    mineral
                )
                    return;


                if(
                    mineral.userData.amount <= 0
                )
                    return;


                mineral.userData.amount -= 5;


                scv.userData.carrying = 5;

                scv.userData.carryType =
                    "미네랄";


                moveUnit(
                    scv,
                    commandCenter.position.x + 5,
                    commandCenter.position.z + 5,

                    () => {

                        if(
                            scv.userData.target !==
                            mineral
                        )
                            return;


                        mineralAmount +=
                            scv.userData.carrying;


                        scv.userData.carrying = 0;

                        scv.userData.carryType =
                            null;


                        mineMineral(
                            scv,
                            mineral
                        );
                    }
                );

            },3000);
        }
    );
}


/* =========================================================
   가스 채취
========================================================= */

function mineGas(
    scv,
    facility
) {

    if(facility.userData.gas <= 0) {

        showMessage(
            "가스가 고갈되었습니다."
        );

        return;
    }


    scv.userData.target =
        facility;

    scv.userData.state =
        "가스 채취 중";


    moveUnit(
        scv,
        facility.position.x,
        facility.position.z,

        () => {

            setTimeout(() => {

                if(
                    scv.userData.target !==
                    facility
                )
                    return;


                if(
                    facility.userData.gas <= 0
                )
                    return;


                facility.userData.gas -= 5;


                scv.userData.carrying = 5;

                scv.userData.carryType =
                    "가스";


                moveUnit(
                    scv,
                    commandCenter.position.x + 5,
                    commandCenter.position.z + 5,

                    () => {

                        if(
                            scv.userData.target !==
                            facility
                        )
                            return;


                        gasAmount +=
                            scv.userData.carrying;


                        scv.userData.carrying = 0;

                        scv.userData.carryType =
                            null;


                        mineGas(
                            scv,
                            facility
                        );
                    }
                );
            },3000);
        }
    );
}


/* =========================================================
   건설 모드
========================================================= */

window.startBuildMode = function() {

    if(
        selectedUnits.length === 0 ||
        selectedUnits[0].userData.type !== "scv"
    ) {

        showMessage(
            "SCV를 선택하세요."
        );

        return;
    }


    buildMode = true;

    buildSCV =
        selectedUnits[0];


    document
        .getElementById("buildMessage")
        .style.display = "block";


    showMessage(
        "가스 지역을 클릭하세요."
    );
};


/* =========================================================
   건설
========================================================= */

function constructGasFacility(
    scv,
    geyser
) {

    if(geyser.userData.hasFacility) {

        showMessage(
            "이미 가스 시설이 있습니다."
        );

        return;
    }


    scv.userData.target =
        geyser;

    scv.userData.building =
        true;

    scv.userData.state =
        "건설 중";


    moveUnit(
        scv,
        geyser.position.x,
        geyser.position.z,

        () => {

            showMessage(
                "가스 시설 건설 중... 15초"
            );


            setTimeout(() => {

                if(
                    !scv.userData.building ||
                    scv.userData.target !==
                    geyser
                )
                    return;


                const facility =
                    createGasFacility(
                        geyser
                    );


                scv.userData.building =
                    false;

                scv.userData.target =
                    facility;

                scv.userData.state =
                    "가스 채취 중";


                mineGas(
                    scv,
                    facility
                );


                showMessage(
                    "가스 시설 완성!"
                );

            },15000);
        }
    );
}


/* =========================================================
   건설 취소
========================================================= */

function cancelBuild() {

    if(!buildMode)
        return;


    buildMode = false;


    document
        .getElementById("buildMessage")
        .style.display = "none";


    if(buildSCV) {

        buildSCV.userData.building =
            false;

        buildSCV.userData.target =
            null;

        buildSCV.userData.path =
            null;

        buildSCV.userData.state =
            "대기";
    }


    buildSCV = null;

    showMessage(
        "건설 명령이 취소되었습니다."
    );
}


/* =========================================================
   마우스 좌표
========================================================= */

function updateMouse(event) {

    mouseX = event.clientX;
    mouseY = event.clientY;


    const rect =
        renderer.domElement.getBoundingClientRect();


    mouse.x =
        ((event.clientX - rect.left) /
        rect.width) * 2 - 1;


    mouse.y =
        -((event.clientY - rect.top) /
        rect.height) * 2 + 1;
}


/* =========================================================
   클릭된 오브젝트
========================================================= */

function getObjectAtMouse() {

    raycaster.setFromCamera(
        mouse,
        camera
    );


    const objects = [

        ...scvs,
        commandCenter,
        ...geysers,
        ...gasFacilities,
        ...minerals
    ];


    const hits =
        raycaster.intersectObjects(
            objects,
            true
        );


    if(!hits.length)
        return null;


    let object =
        hits[0].object;


    while(
        object.parent &&
        !object.userData.type
    ) {

        object =
            object.parent;
    }


    return object;
}


/* =========================================================
   선택
========================================================= */

function selectObject(object) {

    clearSelection();


    if(!object)
        return;


    selectedObject =
        object;


    addSelection(object);


    if(
        object.userData.type === "scv"
    ) {

        selectedUnits = [object];
    }


    showPanel(object);
}


/* =========================================================
   드래그 선택
========================================================= */

function selectByDrag() {

    const minX =
        Math.min(
            dragStartX,
            mouseX
        );

    const maxX =
        Math.max(
            dragStartX,
            mouseX
        );

    const minY =
        Math.min(
            dragStartY,
            mouseY
        );

    const maxY =
        Math.max(
            dragStartY,
            mouseY
        );


    clearSelection();


    for(const scv of scvs) {

        const position =
            scv.position.clone();

        position.project(camera);


        const x =
            (position.x + 1) / 2 *
            window.innerWidth;

        const y =
            (-position.y + 1) / 2 *
            window.innerHeight;


        if(
            x >= minX &&
            x <= maxX &&
            y >= minY &&
            y <= maxY
        ) {

            selectedUnits.push(scv);

            addSelection(scv);
        }
    }


    if(selectedUnits.length) {

        selectedObject =
            selectedUnits[0];

        showPanel(
            selectedObject
        );
    }
}


/* =========================================================
   좌클릭
========================================================= */

renderer.domElement.addEventListener(
    "mousedown",
    event => {

        updateMouse(event);


        if(event.button === 0) {

            mouseDown = true;

            dragStartX =
                mouseX;

            dragStartY =
                mouseY;
        }
    }
);


renderer.domElement.addEventListener(
    "mousemove",
    event => {

        updateMouse(event);


        if(mouseDown) {

            const dx =
                Math.abs(
                    mouseX - dragStartX
                );

            const dy =
                Math.abs(
                    mouseY - dragStartY
                );


            if(dx > 5 || dy > 5) {

                const box =
                    document.getElementById(
                        "dragBox"
                    );


                box.style.display =
                    "block";


                box.style.left =
                    Math.min(
                        dragStartX,
                        mouseX
                    ) + "px";


                box.style.top =
                    Math.min(
                        dragStartY,
                        mouseY
                    ) + "px";


                box.style.width =
                    dx + "px";


                box.style.height =
                    dy + "px";
            }
        }
    }
);


renderer.domElement.addEventListener(
    "mouseup",
    event => {

        updateMouse(event);


        if(event.button !== 0)
            return;


        const dx =
            Math.abs(
                mouseX - dragStartX
            );

        const dy =
            Math.abs(
                mouseY - dragStartY
            );


        mouseDown = false;


        document
            .getElementById("dragBox")
            .style.display = "none";


        if(dx > 8 || dy > 8) {

            if(buildMode) {

                cancelBuild();

            } else {

                selectByDrag();
            }

            return;
        }


        if(buildMode) {

            const object =
                getObjectAtMouse();


            if(
                object &&
                object.userData.type ===
                "geyser" &&
                !object.userData.hasFacility
            ) {

                constructGasFacility(
                    buildSCV,
                    object
                );


                buildMode = false;

                document
                    .getElementById(
                        "buildMessage"
                    )
                    .style.display =
                    "none";

                buildSCV = null;

            } else {

                cancelBuild();
            }


            return;
        }


        selectObject(
            getObjectAtMouse()
        );
    }
);


/* =========================================================
   우클릭 명령
========================================================= */

renderer.domElement.addEventListener(
    "contextmenu",
    event => {

        event.preventDefault();

        updateMouse(event);


        if(!selectedUnits.length)
            return;


        const object =
            getObjectAtMouse();


        /* 미네랄 */

        if(
            object &&
            object.userData.type ===
            "mineral"
        ) {

            selectedUnits.forEach(
                scv =>
                    mineMineral(
                        scv,
                        object
                    )
            );

            return;
        }


        /* 가스 시설 */

        if(
            object &&
            object.userData.type ===
            "gasFacility"
        ) {

            selectedUnits.forEach(
                scv =>
                    mineGas(
                        scv,
                        object
                    )
            );

            return;
        }


        /* 가스 지역 */

        if(
            object &&
            object.userData.type ===
            "geyser"
        ) {

            if(
                !object.userData.hasFacility
            ) {

                constructGasFacility(
                    selectedUnits[0],
                    object
                );
            }

            return;
        }


        /* 땅 */

        raycaster.setFromCamera(
            mouse,
            camera
        );


        const hit =
            raycaster.intersectObject(
                ground
            );


        if(!hit.length)
            return;


        const point =
            hit[0].point;


        const count =
            selectedUnits.length;


        selectedUnits.forEach(
            (scv,index) => {

                stopSCV(scv);


                const angle =
                    (index/count) *
                    Math.PI * 2;


                const radius = 2;


                moveUnit(
                    scv,
                    point.x +
                    Math.cos(angle)*radius,

                    point.z +
                    Math.sin(angle)*radius
                );
            }
        );
    }
);


/* =========================================================
   줌
========================================================= */

renderer.domElement.addEventListener(
    "wheel",
    event => {

        event.preventDefault();

        cameraHeight +=
            event.deltaY * .04;


        cameraHeight =
            THREE.MathUtils.clamp(
                cameraHeight,
                25,
                85
            );
    },
    {passive:false}
);


/* =========================================================
   SCV 움직임
========================================================= */

function updateSCVs(delta) {

    for(const scv of scvs) {

        const path =
            scv.userData.path;


        if(!path)
            continue;


        const dx =
            path.x -
            scv.position.x;

        const dz =
            path.z -
            scv.position.z;


        const distance =
            Math.hypot(dx,dz);


        if(distance < .3) {

            scv.position.x =
                path.x;

            scv.position.z =
                path.z;


            scv.userData.path =
                null;


            if(path.callback) {

                path.callback();

            } else {

                scv.userData.state =
                    "대기";
            }


            continue;
        }


        const speed = 6;


        scv.position.x +=
            dx / distance *
            speed *
            delta;


        scv.position.z +=
            dz / distance *
            speed *
            delta;


        const angle =
            Math.atan2(dx,dz);


        let difference =
            angle -
            scv.rotation.y;


        while(
            difference > Math.PI
        )
            difference -=
                Math.PI*2;


        while(
            difference < -Math.PI
        )
            difference +=
                Math.PI*2;


        scv.rotation.y +=
            difference *
            Math.min(
                delta*8,
                1
            );
    }
}


/* =========================================================
   카메라 끝 이동
========================================================= */

function updateCamera() {

    const edge = 45;

    let moveX = 0;
    let moveZ = 0;


    if(mouseX <= edge)
        moveX = -1;

    if(
        mouseX >=
        window.innerWidth-edge
    )
        moveX = 1;


    if(mouseY <= edge)
        moveZ = -1;

    if(
        mouseY >=
        window.innerHeight-edge
    )
        moveZ = 1;


    if(moveX || moveZ) {

        const length =
            Math.hypot(
                moveX,
                moveZ
            );


        cameraTarget.x +=
            moveX / length * .7;

        cameraTarget.z +=
            moveZ / length * .7;
    }


    cameraTarget.x =
        THREE.MathUtils.clamp(
            cameraTarget.x,
            -75,
            75
        );


    cameraTarget.z =
        THREE.MathUtils.clamp(
            cameraTarget.z,
            -75,
            75
        );


    camera.position.set(
        cameraTarget.x,
        cameraHeight,
        cameraTarget.z +
        cameraHeight*.87
    );


    camera.lookAt(
        cameraTarget.x,
        0,
        cameraTarget.z
    );
}


/* =========================================================
   자원 UI
========================================================= */

function updateResources() {

    document
        .getElementById("minerals")
        .textContent =
        Math.floor(
            mineralAmount
        );


    document
        .getElementById("gas")
        .textContent =
        Math.floor(
            gasAmount
        );


    document
        .getElementById("scvCount")
        .textContent =
        scvs.length;


    document
        .getElementById("production")
        .textContent =
        productionQueue + "/5";
}


/* =========================================================
   미니맵
========================================================= */

const miniMap =
    document.getElementById(
        "miniMap"
    );

const miniCtx =
    miniMap.getContext("2d");


function drawMiniMap() {

    const width = 540;
    const height = 350;


    miniMap.width = width;
    miniMap.height = height;


    miniCtx.clearRect(
        0,
        0,
        width,
        height
    );


    miniCtx.fillStyle =
        "#263728";

    miniCtx.fillRect(
        0,
        0,
        width,
        height
    );


    const mapX =
        x => (x+90)/180*width;

    const mapZ =
        z => (z+90)/180*height;


    /* 미네랄 */

    miniCtx.fillStyle =
        "#168cff";


    minerals.forEach(
        mineral => {

            miniCtx.fillRect(
                mapX(
                    mineral.position.x
                ) - 4,

                mapZ(
                    mineral.position.z
                ) - 4,

                8,
                8
            );
        }
    );


    /* 가스 */

    miniCtx.fillStyle =
        "#39ff8a";


    geysers.forEach(
        geyser => {

            miniCtx.beginPath();

            miniCtx.arc(
                mapX(
                    geyser.position.x
                ),
                mapZ(
                    geyser.position.z
                ),
                6,
                0,
                Math.PI*2
            );

            miniCtx.fill();
        }
    );


    /* 사령부 */

    miniCtx.fillStyle =
        "#ffffff";


    miniCtx.fillRect(
        mapX(0)-7,
        mapZ(0)-7,
        14,
        14
    );


    /* SCV */

    miniCtx.fillStyle =
        "#ffd34d";


    scvs.forEach(
        scv => {

            miniCtx.fillRect(
                mapX(
                    scv.position.x
                )-2,

                mapZ(
                    scv.position.z
                )-2,

                4,
                4
            );
        }
    );


    /* 카메라 영역 */

    miniCtx.strokeStyle =
        "#ffffff";


    miniCtx.strokeRect(
        mapX(
            cameraTarget.x
        )-35,

        mapZ(
            cameraTarget.z
        )-25,

        70,
        50
    );
}


/* =========================================================
   미니맵 클릭 이동
========================================================= */

miniMap.addEventListener(
    "click",
    event => {

        const rect =
            miniMap.getBoundingClientRect();


        const x =
            (event.clientX -
            rect.left) /
            rect.width;


        const z =
            (event.clientY -
            rect.top) /
            rect.height;


        cameraTarget.x =
            x*180-90;


        cameraTarget.z =
            z*180-90;
    }
);


/* =========================================================
   리사이즈
========================================================= */

window.addEventListener(
    "resize",
    () => {

        camera.aspect =
            window.innerWidth /
            window.innerHeight;

        camera.updateProjectionMatrix();

        renderer.setSize(
            window.innerWidth,
            window.innerHeight
        );
    }
);


/* =========================================================
   애니메이션
========================================================= */

let previousTime =
    performance.now();


function animate() {

    requestAnimationFrame(
        animate
    );


    const currentTime =
        performance.now();


    const delta =
        Math.min(
            (currentTime -
            previousTime) / 1000,
            .05
        );


    previousTime =
        currentTime;


    updateCamera();

    updateSCVs(delta);

    updateResources();

    drawMiniMap();


    /* 가스 효과 */

    geysers.forEach(
        geyser => {

            const gas =
                geyser.userData.gasMesh;


            gas.scale.y =
                1 +
                Math.sin(
                    currentTime*.003
                )*.12;
        }
    );


    if(selectedObject)
        showPanel(
            selectedObject
        );


    renderer.render(
        scene,
        camera
    );
}


updateResources();

animate();

</script>

</body>
</html>
"""

components.html(
    html,
    height=900,
    scrolling=False
)
