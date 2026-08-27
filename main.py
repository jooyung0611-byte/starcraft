import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="3D RTS",
    layout="wide",
    initial_sidebar_state="collapsed"
)

html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>
html, body {
    margin: 0;
    padding: 0;
    overflow: hidden;
    background: #111;
    font-family: Arial, sans-serif;
}

#game {
    position: fixed;
    left: 0;
    top: 0;
    width: 100vw;
    height: 100vh;
}

canvas {
    display: block;
}

#topUI {
    position: fixed;
    top: 12px;
    left: 15px;
    z-index: 10;

    background: rgba(10,15,20,.85);
    border: 1px solid rgba(255,255,255,.18);
    border-radius: 8px;

    padding: 10px 16px;
    color: white;
    font-size: 15px;

    display: flex;
    gap: 25px;

    box-shadow: 0 5px 20px rgba(0,0,0,.35);
}

.resource {
    min-width: 100px;
}

#sidePanel {
    position: fixed;
    right: 15px;
    top: 15px;

    width: 245px;
    min-height: 180px;

    background: rgba(12,17,22,.92);
    border: 1px solid rgba(255,255,255,.18);
    border-radius: 10px;

    color: white;
    padding: 15px;

    z-index: 20;

    box-shadow: 0 8px 30px rgba(0,0,0,.45);
}

#sidePanel h3 {
    margin-top: 0;
}

.stat {
    margin: 7px 0;
}

button {
    width: 100%;
    padding: 10px;
    margin-top: 8px;

    background: #27343e;
    color: white;

    border: 1px solid #50606b;
    border-radius: 6px;

    cursor: pointer;
}

button:hover {
    background: #3b4d59;
}

button:disabled {
    opacity: .4;
    cursor: default;
}

#miniMap {
    position: fixed;

    left: 15px;
    bottom: 15px;

    width: 230px;
    height: 150px;

    background: #152018;

    border: 2px solid rgba(255,255,255,.35);
    border-radius: 5px;

    z-index: 20;

    overflow: hidden;
}

#miniCanvas {
    width: 100%;
    height: 100%;
}

#selectionBox {
    position: fixed;

    border: 1px solid #65ff65;
    background: rgba(80,255,80,.12);

    pointer-events: none;

    z-index: 50;

    display: none;
}

#message {
    position: fixed;

    left: 50%;
    bottom: 25px;

    transform: translateX(-50%);

    background: rgba(0,0,0,.8);
    color: white;

    padding: 8px 15px;

    border-radius: 6px;

    z-index: 30;

    opacity: 0;

    transition: opacity .2s;
}

#buildMode {
    position: fixed;

    left: 50%;
    top: 70px;

    transform: translateX(-50%);

    background: rgba(110,50,20,.9);

    border: 1px solid #ffb36b;

    padding: 9px 16px;

    color: white;

    border-radius: 6px;

    display: none;

    z-index: 40;
}

</style>
</head>

<body>

<div id="game"></div>

<div id="topUI">

    <div class="resource">
        💎 미네랄:
        <b id="minerals">500</b>
    </div>

    <div class="resource">
        🟢 가스:
        <b id="gas">0</b>
    </div>

    <div class="resource">
        👨‍🚀 SCV:
        <b id="scvCount">5</b>
    </div>

</div>

<div id="sidePanel">

    <h3 id="panelTitle">선택 없음</h3>

    <div id="panelContent">
        유닛이나 건물을 선택하세요.
    </div>

</div>

<div id="miniMap">
    <canvas id="miniCanvas"></canvas>
</div>

<div id="selectionBox"></div>

<div id="buildMode">
    🏗️ 가스 채취 시설 건설 모드
    <br>
    가스 지역을 클릭하세요.
    <br>
    <small>다른 대상을 클릭하면 취소됩니다.</small>
</div>

<div id="message"></div>


<script type="module">

import * as THREE from
'https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.module.js';


// =====================================================
// 기본 설정
// =====================================================

const game = document.getElementById("game");

const scene = new THREE.Scene();

scene.background = new THREE.Color(0x18221a);

scene.fog = new THREE.Fog(
    0x18221a,
    80,
    220
);


// =====================================================
// 카메라
// =====================================================

const camera = new THREE.PerspectiveCamera(
    50,
    window.innerWidth / window.innerHeight,
    0.1,
    500
);

camera.position.set(
    0,
    55,
    48
);

camera.lookAt(0,0,0);


// =====================================================
// 렌더러
// =====================================================

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

game.appendChild(renderer.domElement);


// =====================================================
// 조명
// =====================================================

const ambient = new THREE.HemisphereLight(
    0xbfd7ff,
    0x26351f,
    1.8
);

scene.add(ambient);


const sun = new THREE.DirectionalLight(
    0xffffff,
    2.2
);

sun.position.set(
    30,
    70,
    20
);

sun.castShadow = true;

scene.add(sun);


// =====================================================
// 바닥
// =====================================================

const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(180,180),
    new THREE.MeshStandardMaterial({
        color: 0x35452e,
        roughness: 1
    })
);

ground.rotation.x = -Math.PI / 2;

ground.receiveShadow = true;

scene.add(ground);


// =====================================================
// 지형 장식
// =====================================================

function createRock(x,z,s=1){

    const rock = new THREE.Mesh(
        new THREE.DodecahedronGeometry(
            s * (0.6 + Math.random()*.5),
            0
        ),
        new THREE.MeshStandardMaterial({
            color: 0x3f4640,
            roughness: .95
        })
    );

    rock.position.set(
        x,
        s*.35,
        z
    );

    rock.rotation.y = Math.random()*6;

    rock.castShadow = true;

    scene.add(rock);
}


for(let i=0;i<100;i++){

    const x =
        (Math.random()-.5)*160;

    const z =
        (Math.random()-.5)*160;

    if(Math.abs(x)<30 && Math.abs(z)<30)
        continue;

    createRock(
        x,
        z,
        .4+Math.random()*.9
    );
}


// =====================================================
// 미네랄
// =====================================================

const minerals = [];


function createMineralCrystal(x,z){

    const group = new THREE.Group();

    const material =
        new THREE.MeshStandardMaterial({
            color: 0x168cff,
            emissive: 0x073f80,
            emissiveIntensity: .5,
            roughness: .3,
            metalness: .15
        });


    const count =
        4 + Math.floor(Math.random()*4);


    for(let i=0;i<count;i++){

        const h =
            1.7 + Math.random()*1.6;

        const crystal = new THREE.Mesh(
            new THREE.CylinderGeometry(
                .35,
                .5,
                h,
                6
            ),
            material
        );

        crystal.position.set(
            (Math.random()-.5)*1.8,
            h/2,
            (Math.random()-.5)*1.8
        );

        crystal.rotation.z =
            (Math.random()-.5)*.3;

        crystal.rotation.y =
            Math.random()*Math.PI;

        crystal.castShadow = true;

        group.add(crystal);
    }


    group.position.set(x,0,z);

    group.userData.type =
        "mineral";

    group.userData.amount =
        1500;

    minerals.push(group);

    scene.add(group);
}


// 사진처럼 왼쪽에 큰 미네랄 덩어리
const leftMinerals = [

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
    [-25,6]
];


// 오른쪽에도 작은 필드
const rightMinerals = [

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


[...leftMinerals,...rightMinerals]
.forEach(p=>{
    createMineralCrystal(
        p[0],
        p[1]
    );
});


// =====================================================
// 가스 지역
// =====================================================

const geysers = [];


function createGeyser(x,z){

    const group = new THREE.Group();


    // 바위
    const rock = new THREE.Mesh(
        new THREE.DodecahedronGeometry(
            3.2,
            1
        ),
        new THREE.MeshStandardMaterial({
            color: 0x4a514c,
            roughness: .95
        })
    );

    rock.scale.y = .65;

    rock.position.y = 1.2;

    rock.castShadow = true;

    group.add(rock);


    // 중앙 가스 구멍
    const hole = new THREE.Mesh(
        new THREE.CylinderGeometry(
            1.4,
            1.6,
            .4,
            32
        ),
        new THREE.MeshStandardMaterial({
            color: 0x102318,
            emissive: 0x0b6d35,
            emissiveIntensity: 1.5
        })
    );

    hole.position.y = 2.4;

    group.add(hole);


    // 가스
    const gas = new THREE.Mesh(
        new THREE.SphereGeometry(
            1.4,
            16,
            16
        ),
        new THREE.MeshBasicMaterial({
            color: 0x39ff8a,
            transparent: true,
            opacity: .28
        })
    );

    gas.position.y = 3.1;

    group.add(gas);


    group.position.set(x,0,z);

    group.userData.type =
        "geyser";

    group.userData.hasFacility =
        false;

    geysers.push(group);

    scene.add(group);

    return group;
}


// 사진과 비슷하게 기지 주변 가스
createGeyser(-9,-16);
createGeyser(14,-14);


// =====================================================
// 사령부
// =====================================================

let commandCenter;


function createCommandCenter(x,z){

    const group =
        new THREE.Group();


    // 하부
    const base = new THREE.Mesh(
        new THREE.BoxGeometry(
            12,
            2.2,
            9
        ),
        new THREE.MeshStandardMaterial({
            color: 0x555e63,
            metalness: .75,
            roughness: .4
        })
    );

    base.position.y = 1.1;

    base.castShadow = true;

    group.add(base);


    // 중앙 본체
    const body = new THREE.Mesh(
        new THREE.BoxGeometry(
            8,
            5,
            6
        ),
        new THREE.MeshStandardMaterial({
            color: 0x727a7c,
            metalness: .65,
            roughness: .45
        })
    );

    body.position.y = 4;

    body.castShadow = true;

    group.add(body);


    // 지붕
    const roof = new THREE.Mesh(
        new THREE.BoxGeometry(
            9,
            1,
            7
        ),
        new THREE.MeshStandardMaterial({
            color: 0x3d4548,
            metalness: .8
        })
    );

    roof.position.y = 6.8;

    group.add(roof);


    // 중앙 코어
    const core = new THREE.Mesh(
        new THREE.CylinderGeometry(
            1.2,
            1.2,
            .6,
            24
        ),
        new THREE.MeshStandardMaterial({
            color: 0x55ccff,
            emissive: 0x168cff,
            emissiveIntensity: 1.5
        })
    );

    core.position.y = 7.5;

    group.add(core);


    // 안테나
    const pole = new THREE.Mesh(
        new THREE.CylinderGeometry(
            .12,
            .12,
            4,
            8
        ),
        new THREE.MeshStandardMaterial({
            color: 0x25292b,
            metalness: .9
        })
    );

    pole.position.set(
        0,
        9.3,
        0
    );

    group.add(pole);


    const light = new THREE.Mesh(
        new THREE.SphereGeometry(
            .3,
            12,
            12
        ),
        new THREE.MeshBasicMaterial({
            color: 0xff4433
        })
    );

    light.position.set(
        0,
        11.3,
        0
    );

    group.add(light);


    group.position.set(x,0,z);

    group.userData.type =
        "command";

    group.userData.hp =
        1500;

    group.userData.maxHp =
        1500;

    group.userData.queue = 0;

    scene.add(group);

    commandCenter = group;

    return group;
}


createCommandCenter(0,0);


// =====================================================
// SCV
// =====================================================

const scvs = [];


function createSCV(x,z){

    const group =
        new THREE.Group();


    // 차체
    const body = new THREE.Mesh(
        new THREE.BoxGeometry(
            2.2,
            .8,
            2.8
        ),
        new THREE.MeshStandardMaterial({
            color: 0x8b9292,
            metalness: .8,
            roughness: .35
        })
    );

    body.position.y = 1;

    body.castShadow = true;

    group.add(body);


    // 운전석
    const cabin = new THREE.Mesh(
        new THREE.BoxGeometry(
            1.5,
            .9,
            1.3
        ),
        new THREE.MeshStandardMaterial({
            color: 0x252d31,
            metalness: .6,
            roughness: .3
        })
    );

    cabin.position.set(
        0,
        1.7,
        -.25
    );

    cabin.castShadow = true;

    group.add(cabin);


    // 앞쪽 작업 장치
    const arm = new THREE.Mesh(
        new THREE.BoxGeometry(
            1.5,
            .35,
            1.2
        ),
        new THREE.MeshStandardMaterial({
            color: 0xb1b5b4,
            metalness: .85
        })
    );

    arm.position.set(
        0,
        .75,
        1.8
    );

    group.add(arm);


    // 바퀴
    for(let side of [-1,1]){

        for(let zpos of [-.85,.85]){

            const wheel =
                new THREE.Mesh(
                    new THREE.CylinderGeometry(
                        .45,
                        .45,
                        .3,
                        12
                    ),
                    new THREE.MeshStandardMaterial({
                        color: 0x151719,
                        roughness: .9
                    })
                );

            wheel.rotation.z =
                Math.PI/2;

            wheel.position.set(
                side*1.15,
                .55,
                zpos
            );

            wheel.castShadow = true;

            group.add(wheel);
        }
    }


    // 앞 조명
    for(let side of [-.6,.6]){

        const lamp =
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

        lamp.position.set(
            side,
            1.15,
            1.45
        );

        group.add(lamp);
    }


    group.position.set(
        x,
        0,
        z
    );


    group.userData.type =
        "scv";

    group.userData.hp =
        50;

    group.userData.maxHp =
        50;

    group.userData.state =
        "idle";

    group.userData.target =
        null;

    group.userData.carrying =
        0;

    group.userData.carryType =
        null;

    group.userData.building =
        false;

    group.userData.path =
        null;


    scvs.push(group);

    scene.add(group);

    return group;
}


// 시작 SCV 5기
createSCV(-5,6);
createSCV(-2,7);
createSCV(1,7);
createSCV(4,6);
createSCV(7,5);


// =====================================================
// 가스 시설
// =====================================================

const facilities = [];


function createGasFacility(geyser){

    const group =
        new THREE.Group();


    const base = new THREE.Mesh(
        new THREE.CylinderGeometry(
            2.3,
            2.6,
            1.2,
            16
        ),
        new THREE.MeshStandardMaterial({
            color: 0x555d60,
            metalness: .8,
            roughness: .4
        })
    );

    base.position.y = .7;

    base.castShadow = true;

    group.add(base);


    const tank = new THREE.Mesh(
        new THREE.CylinderGeometry(
            1.7,
            1.7,
            3.5,
            16
        ),
        new THREE.MeshStandardMaterial({
            color: 0x4d5558,
            metalness: .75,
            roughness: .35
        })
    );

    tank.position.y = 2.8;

    tank.castShadow = true;

    group.add(tank);


    // 상단 가스 코어
    const core = new THREE.Mesh(
        new THREE.SphereGeometry(
            1,
            16,
            16
        ),
        new THREE.MeshStandardMaterial({
            color: 0x37ff8b,
            emissive: 0x18b85e,
            emissiveIntensity: 1.5
        })
    );

    core.position.y = 4.7;

    group.add(core);


    // 파이프
    for(let i=0;i<3;i++){

        const pipe =
            new THREE.Mesh(
                new THREE.CylinderGeometry(
                    .13,
                    .13,
                    2.7,
                    8
                ),
                new THREE.MeshStandardMaterial({
                    color: 0x202527,
                    metalness: .9
                })
            );

        pipe.position.set(
            (i-1)*.8,
            2.2,
            1.5
        );

        pipe.rotation.x =
            Math.PI/2;

        group.add(pipe);
    }


    group.position.copy(
        geyser.position
    );


    group.userData.type =
        "gasFacility";

    group.userData.hp =
        500;

    group.userData.maxHp =
        500;

    group.userData.gas =
        2500;


    facilities.push(group);

    geyser.userData.hasFacility =
        true;

    scene.add(group);

    return group;
}


// =====================================================
// 자원
// =====================================================

let mineralsAmount = 500;
let gasAmount = 0;

let selectedUnits = [];

let selectedObject = null;

let buildMode = false;
let buildSCV = null;

let productionQueue = 0;


// =====================================================
// UI
// =====================================================

function updateResources(){

    document.getElementById(
        "minerals"
    ).textContent =
        Math.floor(mineralsAmount);

    document.getElementById(
        "gas"
    ).textContent =
        Math.floor(gasAmount);

    document.getElementById(
        "scvCount"
    ).textContent =
        scvs.length;
}


function showMessage(text){

    const el =
        document.getElementById("message");

    el.textContent = text;

    el.style.opacity = 1;

    clearTimeout(
        showMessage.timer
    );

    showMessage.timer =
        setTimeout(()=>{
            el.style.opacity = 0;
        },1800);
}


// =====================================================
// 선택 표시
// =====================================================

function createSelectionRing(){

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

    ring.position.y =
        .06;

    return ring;
}


function addSelection(object){

    if(object.userData.selectionRing)
        return;

    const ring =
        createSelectionRing();

    object.add(ring);

    object.userData.selectionRing =
        ring;
}


function removeSelection(object){

    if(
        object &&
        object.userData.selectionRing
    ){

        object.remove(
            object.userData.selectionRing
        );

        object.userData.selectionRing =
            null;
    }
}


// =====================================================
// 상태창
// =====================================================

function showPanel(object){

    const title =
        document.getElementById(
            "panelTitle"
        );

    const content =
        document.getElementById(
            "panelContent"
        );


    if(!object){

        title.textContent =
            "선택 없음";

        content.innerHTML =
            "유닛이나 건물을 선택하세요.";

        return;
    }


    const type =
        object.userData.type;


    if(type === "scv"){

        title.textContent =
            "SCV";

        content.innerHTML = `
            <div class="stat">
                ❤️ 체력:
                ${object.userData.hp}/50
            </div>

            <div class="stat">
                상태:
                ${object.userData.state}
            </div>

            <div class="stat">
                운반 자원:
                ${object.userData.carrying}
            </div>

            <button
                onclick="startGasBuild()"
            >
                🏗️ 가스 채취 시설 건설
            </button>
        `;
    }


    else if(type === "command"){

        title.textContent =
            "사령부";

        content.innerHTML = `
            <div class="stat">
                ❤️ 체력:
                ${object.userData.hp}
                / ${object.userData.maxHp}
            </div>

            <div class="stat">
                생산 대기:
                ${productionQueue}/5
            </div>

            <button
                onclick="buildSCV()"
                ${productionQueue>=5 ? "disabled":""}
            >
                👨‍🚀 SCV 생산
                <br>
                💎 50
                / 10초
            </button>
        `;
    }


    else if(type === "gasFacility"){

        title.textContent =
            "가스 채취 시설";

        content.innerHTML = `
            <div class="stat">
                ❤️ 체력:
                ${object.userData.hp}/500
            </div>

            <div class="stat">
                남은 가스:
                ${object.userData.gas}
            </div>

            <div class="stat">
                상태:
                가스 채취 가능
            </div>
        `;
    }


    else if(type === "geyser"){

        title.textContent =
            "가스 지역";

        content.innerHTML = `
            <div class="stat">
                상태:
                ${
                    object.userData.hasFacility
                    ? "시설 건설 완료"
                    : "시설 없음"
                }
            </div>
        `;
    }
}


// =====================================================
// SCV 생산
// =====================================================

window.buildSCV = function(){

    if(productionQueue >= 5){

        showMessage(
            "생산 대기열이 가득 찼습니다."
        );

        return;
    }


    if(mineralsAmount < 50){

        showMessage(
            "미네랄이 부족합니다."
        );

        return;
    }


    mineralsAmount -= 50;

    productionQueue++;

    updateResources();

    showMessage(
        "SCV 생산 시작!"
    );


    const current =
        productionQueue;


    setTimeout(()=>{

        productionQueue--;

        const offset =
            scvs.length * .8;


        const newSCV =
            createSCV(
                7 + offset,
                2
            );


        showMessage(
            "SCV 생산 완료!"
        );

        updateResources();

    },10000);
};


// =====================================================
// 가스 시설 건설
// =====================================================

window.startGasBuild = function(){

    if(
        selectedUnits.length === 0
    ){

        showMessage(
            "먼저 SCV를 선택하세요."
        );

        return;
    }


    const scv =
        selectedUnits[0];


    if(
        scv.userData.type !== "scv"
    ){

        showMessage(
            "SCV를 선택해야 합니다."
        );

        return;
    }


    buildMode = true;

    buildSCV = scv;

    document.getElementById(
        "buildMode"
    ).style.display =
        "block";

    showMessage(
        "가스 지역을 클릭하세요."
    );
};


// =====================================================
// 이동
// =====================================================

function moveUnitTo(
    unit,
    x,
    z,
    callback=null
){

    unit.userData.path = {
        x:x,
        z:z,
        callback:callback
    };

    unit.userData.state =
        "moving";
}


function updateUnits(dt){

    scvs.forEach(scv=>{

        const path =
            scv.userData.path;


        if(!path)
            return;


        const dx =
            path.x - scv.position.x;

        const dz =
            path.z - scv.position.z;

        const distance =
            Math.sqrt(
                dx*dx + dz*dz
            );


        if(distance < .25){

            scv.position.x =
                path.x;

            scv.position.z =
                path.z;

            const callback =
                path.callback;

            scv.userData.path =
                null;

            if(callback)
                callback();

            return;
        }


        const speed = 6;

        scv.position.x +=
            dx/distance * speed * dt;

        scv.position.z +=
            dz/distance * speed * dt;


        scv.rotation.y =
            Math.atan2(
                dx,
                dz
            );
    });
}


// =====================================================
// 미네랄 채취
// =====================================================

function mineMineral(
    scv,
    mineral
){

    if(!mineral)
        return;


    scv.userData.state =
        "mining";

    scv.userData.target =
        mineral;


    moveUnitTo(
        scv,
        mineral.position.x,
        mineral.position.z,
        ()=>{

            setTimeout(()=>{

                if(
                    !scv.userData.target
                )
                    return;


                if(
                    mineral.userData.amount <= 0
                ){

                    scv.userData.state =
                        "idle";

                    return;
                }


                const amount = 5;

                mineral.userData.amount -=
                    amount;

                scv.userData.carrying =
                    amount;

                scv.userData.carryType =
                    "mineral";


                // 사령부로 귀환
                moveUnitTo(
                    scv,
                    commandCenter.position.x + 5,
                    commandCenter.position.z + 5,
                    ()=>{

                        mineralsAmount +=
                            scv.userData.carrying;

                        scv.userData.carrying =
                            0;

                        scv.userData.carryType =
                            null;


                        // 다시 채취
                        if(
                            scv.userData.target
                        ){

                            mineMineral(
                                scv,
                                mineral
                            );
                        }
                    }
                );

            },3000);
        }
    );
}


// =====================================================
// 가스 채취
// =====================================================

function mineGas(
    scv,
    facility
){

    scv.userData.state =
        "gas";

    scv.userData.target =
        facility;


    moveUnitTo(
        scv,
        facility.position.x,
        facility.position.z,
        ()=>{

            setTimeout(()=>{

                if(
                    facility.userData.gas <= 0
                )
                    return;


                facility.userData.gas -= 5;

                scv.userData.carrying =
                    5;

                scv.userData.carryType =
                    "gas";


                moveUnitTo(
                    scv,
                    commandCenter.position.x + 5,
                    commandCenter.position.z + 5,
                    ()=>{

                        gasAmount +=
                            scv.userData.carrying;

                        scv.userData.carrying =
                            0;

                        scv.userData.carryType =
                            null;


                        if(
                            scv.userData.target
                        ){

                            mineGas(
                                scv,
                                facility
                            );
                        }
                    }
                );

            },3000);
        }
    );
}


// =====================================================
// 가스 시설 건설 시작
// =====================================================

function beginConstruction(
    scv,
    geyser
){

    if(
        geyser.userData.hasFacility
    ){

        showMessage(
            "이미 가스 시설이 있습니다."
        );

        return;
    }


    scv.userData.state =
        "building";

    scv.userData.target =
        geyser;

    scv.userData.building =
        true;


    moveUnitTo(
        scv,
        geyser.position.x,
        geyser.position.z,
        ()=>{

            showMessage(
                "가스 시설 건설 중..."
            );


            setTimeout(()=>{

                // 건설이 취소된 경우
                if(
                    !scv.userData.building
                )
                    return;


                createGasFacility(
                    geyser
                );


                scv.userData.building =
                    false;

                scv.userData.state =
                    "gas";

                const facility =
                    facilities[
                        facilities.length-1
                    ];


                mineGas(
                    scv,
                    facility
                );


                showMessage(
                    "가스 채취 시설 완성!"
                );

            },15000);
        }
    );
}


// =====================================================
// 건설 취소
// =====================================================

function cancelBuild(){

    if(
        !buildMode
    )
        return;


    buildMode = false;

    document.getElementById(
        "buildMode"
    ).style.display =
        "none";


    if(buildSCV){

        buildSCV.userData.building =
            false;

        buildSCV.userData.target =
            null;

        buildSCV.userData.path =
            null;

        buildSCV.userData.state =
            "idle";
    }


    buildSCV = null;

    showMessage(
        "건설 명령이 취소되었습니다."
    );
}


// =====================================================
// 마우스 / 선택
// =====================================================

const raycaster =
    new THREE.Raycaster();

const mouse =
    new THREE.Vector2();


let mouseDown =
    false;

let dragStartX = 0;
let dragStartY = 0;

let mouseX = 0;
let mouseY = 0;


function setMouse(event){

    mouseX =
        event.clientX;

    mouseY =
        event.clientY;


    const rect =
        renderer.domElement
        .getBoundingClientRect();


    mouse.x =
        ((event.clientX - rect.left)
        / rect.width) * 2 - 1;

    mouse.y =
        -((event.clientY - rect.top)
        / rect.height) * 2 + 1;
}


// =====================================================
// 클릭 가능한 객체 찾기
// =====================================================

function getObjectUnderMouse(){

    raycaster.setFromCamera(
        mouse,
        camera
    );


    const objects = [
        ...scvs,
        commandCenter,
        ...geyser,
        ...facilities,
        ...minerals
    ];


    const hits =
        raycaster.intersectObjects(
            objects,
            true
        );


    if(hits.length === 0)
        return null;


    let obj =
        hits[0].object;


    while(
        obj.parent &&
        !obj.userData.type
    ){

        obj =
            obj.parent;
    }


    return obj;
}


// =====================================================
// 선택
// =====================================================

function clearSelection(){

    selectedUnits.forEach(
        removeSelection
    );

    selectedUnits = [];

    if(selectedObject)
        removeSelection(
            selectedObject
        );

    selectedObject =
        null;
}


function selectObject(object){

    clearSelection();

    if(!object)
        return;


    selectedObject =
        object;

    addSelection(
        object
    );

    if(
        object.userData.type ===
        "scv"
    ){

        selectedUnits =
            [object];
    }


    showPanel(object);
}


// =====================================================
// SCV 드래그 선택
// =====================================================

function selectBox(){

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


    scvs.forEach(scv=>{

        const pos =
            scv.position.clone();

        pos.project(camera);


        const sx =
            (pos.x+1)/2 *
            window.innerWidth;

        const sy =
            (-pos.y+1)/2 *
            window.innerHeight;


        if(
            sx >= minX &&
            sx <= maxX &&
            sy >= minY &&
            sy <= maxY
        ){

            selectedUnits.push(
                scv
            );

            addSelection(
                scv
            );
        }
    });


    if(
        selectedUnits.length > 0
    ){

        selectedObject =
            selectedUnits[0];

        showPanel(
            selectedObject
        );
    }
}


// =====================================================
// 이벤트
// =====================================================

renderer.domElement.addEventListener(
    "mousedown",
    event=>{

        setMouse(event);

        if(event.button !== 0)
            return;


        mouseDown = true;

        dragStartX =
            mouseX;

        dragStartY =
            mouseY;
    }
);


renderer.domElement.addEventListener(
    "mousemove",
    event=>{

        setMouse(event);


        if(
            mouseDown
        ){

            const dx =
                Math.abs(
                    mouseX-dragStartX
                );

            const dy =
                Math.abs(
                    mouseY-dragStartY
                );


            if(
                dx > 5 ||
                dy > 5
            ){

                const box =
                    document.getElementById(
                        "selectionBox"
                    );

                box.style.display =
                    "block";

                box.style.left =
                    Math.min(
                        dragStartX,
                        mouseX
                    )+"px";

                box.style.top =
                    Math.min(
                        dragStartY,
                        mouseY
                    )+"px";

                box.style.width =
                    dx+"px";

                box.style.height =
                    dy+"px";
            }
        }
    }
);


renderer.domElement.addEventListener(
    "mouseup",
    event=>{

        setMouse(event);

        if(event.button !== 0)
            return;


        const dx =
            Math.abs(
                mouseX-dragStartX
            );

        const dy =
            Math.abs(
                mouseY-dragStartY
            );


        mouseDown = false;


        document.getElementById(
            "selectionBox"
        ).style.display =
            "none";


        // 실제 드래그였을 경우
        if(
            dx > 8 ||
            dy > 8
        ){

            selectBox();

            return;
        }


        // 건설 모드
        if(buildMode){

            const target =
                getObjectUnderMouse();


            if(
                target &&
                target.userData.type ===
                "geyser"
            ){

                beginConstruction(
                    buildSCV,
                    target
                );

                buildMode = false;

                document.getElementById(
                    "buildMode"
                ).style.display =
                    "none";

                return;
            }


            // 다른 것을 클릭하면 취소
            cancelBuild();

            return;
        }


        const target =
            getObjectUnderMouse();


        if(target){

            selectObject(
                target
            );
        }
        else{

            clearSelection();

            showPanel(null);
        }
    }
);


// =====================================================
// 우클릭 이동 / 채취
// =====================================================

renderer.domElement.addEventListener(
    "contextmenu",
    event=>{

        event.preventDefault();

        setMouse(event);


        if(
            selectedUnits.length === 0
        )
            return;


        const target =
            getObjectUnderMouse();


        // 미네랄
        if(
            target &&
            target.userData.type ===
            "mineral"
        ){

            selectedUnits.forEach(
                scv=>{
                    mineMineral(
                        scv,
                        target
                    );
                }
            );

            return;
        }


        // 가스 시설
        if(
            target &&
            target.userData.type ===
            "gasFacility"
        ){

            selectedUnits.forEach(
                scv=>{
                    mineGas(
                        scv,
                        target
                    );
                }
            );

            return;
        }


        // 가스 지역
        if(
            target &&
            target.userData.type ===
            "geyser"
        ){

            if(
                !target.userData.hasFacility
            ){

                beginConstruction(
                    selectedUnits[0],
                    target
                );

                return;
            }
        }


        // 땅 이동
        raycaster.setFromCamera(
            mouse,
            camera
        );


        const hit =
            raycaster.intersectObject(
                ground
            );


        if(hit.length){

            const p =
                hit[0].point;


            selectedUnits.forEach(
                scv=>{
                    moveUnitTo(
                        scv,
                        p.x +
                        (Math.random()-.5)*3,
                        p.z +
                        (Math.random()-.5)*3
                    );

                    scv.userData.target =
                        null;

                    scv.userData.state =
                        "moving";
                }
            );
        }
    }
);


// =====================================================
// 카메라 이동
// =====================================================

let cameraTarget =
    new THREE.Vector3(
        0,0,0
    );

let cameraHeight =
    55;

const CAMERA_SPEED =
    0.7;


function clampCamera(){

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
}


function updateCamera(){

    const EDGE =
        45;


    let dx = 0;
    let dz = 0;


    if(mouseX <= EDGE)
        dx = -1;


    if(
        mouseX >=
        window.innerWidth-EDGE
    )
        dx = 1;


    if(mouseY <= EDGE)
        dz = -1;


    if(
        mouseY >=
        window.innerHeight-EDGE
    )
        dz = 1;


    if(dx || dz){

        const len =
            Math.sqrt(
                dx*dx+dz*dz
            );

        dx /= len;
        dz /= len;


        cameraTarget.x +=
            dx * CAMERA_SPEED;

        cameraTarget.z +=
            dz * CAMERA_SPEED;


        clampCamera();
    }


    camera.position.x =
        cameraTarget.x;

    camera.position.z =
        cameraTarget.z +
        cameraHeight*.87;

    camera.position.y =
        cameraHeight;

    camera.lookAt(
        cameraTarget.x,
        0,
        cameraTarget.z
    );
}


// =====================================================
// 휠 줌
// =====================================================

renderer.domElement.addEventListener(
    "wheel",
    event=>{

        event.preventDefault();

        cameraHeight +=
            event.deltaY*.04;


        cameraHeight =
            THREE.MathUtils.clamp(
                cameraHeight,
                25,
                85
            );
    },
    {passive:false}
);


// =====================================================
// 미니맵
// =====================================================

const miniCanvas =
    document.getElementById(
        "miniCanvas"
    );

const miniCtx =
    miniCanvas.getContext(
        "2d"
    );


function drawMiniMap(){

    const w =
        miniCanvas.width =
        460;

    const h =
        miniCanvas.height =
        300;


    miniCtx.clearRect(
        0,0,w,h
    );


    miniCtx.fillStyle =
        "#263728";

    miniCtx.fillRect(
        0,0,w,h
    );


    function sx(x){

        return (
            (x+90)/180
        )*w;
    }


    function sy(z){

        return (
            (z+90)/180
        )*h;
    }


    // 미네랄
    miniCtx.fillStyle =
        "#168cff";

    minerals.forEach(m=>{

        miniCtx.fillRect(
            sx(m.position.x)-4,
            sy(m.position.z)-4,
            8,
            8
        );
    });


    // 가스
    miniCtx.fillStyle =
        "#39ff8a";

    geysers.forEach(g=>{

        miniCtx.beginPath();

        miniCtx.arc(
            sx(g.position.x),
            sy(g.position.z),
            6,
            0,
            Math.PI*2
        );

        miniCtx.fill();
    });


    // 사령부
    miniCtx.fillStyle =
        "#ffffff";

    miniCtx.fillRect(
        sx(commandCenter.position.x)-7,
        sy(commandCenter.position.z)-7,
        14,
        14
    );


    // SCV
    miniCtx.fillStyle =
        "#ffd34d";

    scvs.forEach(s=>{

        miniCtx.fillRect(
            sx(s.position.x)-2,
            sy(s.position.z)-2,
            4,
            4
        );
    });


    // 카메라
    miniCtx.strokeStyle =
        "#ffffff";

    miniCtx.strokeRect(
        sx(cameraTarget.x)-35,
        sy(cameraTarget.z)-25,
        70,
        50
    );
}


document.getElementById(
    "miniMap"
).addEventListener(
    "click",
    event=>{

        const rect =
            event.currentTarget
            .getBoundingClientRect();


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


        clampCamera();
    }
);


// =====================================================
// 애니메이션
// =====================================================

let lastTime =
    performance.now();


function animate(){

    requestAnimationFrame(
        animate
    );


    const now =
        performance.now();

    const dt =
        Math.min(
            (now-lastTime)/1000,
            .05
        );

    lastTime = now;


    updateCamera();

    updateUnits(dt);

    updateResources();

    drawMiniMap();


    // 가스 효과
    geysers.forEach(g=>{

        const gas =
            g.children.find(
                c =>
                c.material &&
                c.material.color &&
                c.material.color.g > .8
            );


        if(gas){

            gas.scale.y =
                1 +
                Math.sin(
                    now*.003
                )*.12;
        }
    });


    renderer.render(
        scene,
        camera
    );
}


window.addEventListener(
    "resize",
    ()=>{

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
