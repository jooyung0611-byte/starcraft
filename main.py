import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# STREAMLIT 설정
# ============================================================

st.set_page_config(
    page_title="Terran RTS",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# 게임 전체 HTML
# ============================================================

GAME_HTML = r"""

<!DOCTYPE html>

<html lang="ko">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width,
               initial-scale=1.0">

<title>Terran RTS</title>


<!-- THREE.JS -->

<script src="
https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js
"></script>


<style>

/* ============================================================
   기본
============================================================ */

* {

    box-sizing: border-box;

    user-select: none;

}


html,
body {

    margin: 0;

    padding: 0;

    width: 100%;

    height: 100%;

    overflow: hidden;

    background: #050809;

    font-family:
        Arial,
        "Malgun Gothic",
        sans-serif;

}


body {

    cursor: default;

}


#game {

    position: fixed;

    left: 0;

    top: 0;

    right: 0;

    bottom: 0;

}


canvas {

    display: block;

}


/* ============================================================
   종족 선택 화면
============================================================ */

#raceScreen {

    position: fixed;

    left: 0;

    top: 0;

    right: 0;

    bottom: 0;

    z-index: 1000;

    display: flex;

    align-items: center;

    justify-content: center;

    background:

        radial-gradient(
            circle at center,
            #39484e 0%,
            #172024 35%,
            #070a0c 75%,
            #020303 100%
        );

}


.raceBox {

    width: 480px;

    padding: 45px;

    text-align: center;

    background:

        linear-gradient(
            145deg,
            rgba(60,72,77,.98),
            rgba(9,13,15,.99)
        );

    border: 2px solid #879398;

    border-radius: 8px;

    box-shadow:

        0 0 100px
        rgba(0,0,0,.95),

        inset
        0 0 30px
        rgba(255,255,255,.03);

}


.raceTitle {

    color: #edf3f4;

    font-size: 46px;

    font-weight: bold;

    letter-spacing: 9px;

    margin-bottom: 15px;

    text-shadow:

        0 2px 5px #000;

}


.raceSub {

    color: #aebbc0;

    font-size: 15px;

    margin-bottom: 32px;

}


.raceButton {

    width: 100%;

    padding: 18px;

    color: white;

    font-size: 22px;

    font-weight: bold;

    background:

        linear-gradient(
            #75848a,
            #303b40
        );

    border:

        2px solid
        #a8b3b7;

    border-radius: 5px;

    cursor: pointer;

    transition: .15s;

}


.raceButton:hover {

    background:

        linear-gradient(
            #8d9da2,
            #3c494e
        );

    transform: scale(1.02);

}


/* ============================================================
   顶쪽 자원 UI
============================================================ */

#topUI {

    position: fixed;

    top: 10px;

    left: 50%;

    transform:
        translateX(-50%);

    z-index: 100;

    display: flex;

    gap: 9px;

}


.resource {

    min-width: 125px;

    padding:
        9px 14px;

    text-align: center;

    color: #eef3f4;

    font-size: 15px;

    background:

        linear-gradient(
            rgba(12,18,21,.96),
            rgba(5,9,11,.96)
        );

    border:
        1px solid #68767b;

    border-radius: 5px;

    box-shadow:
        0 2px 8px
        rgba(0,0,0,.5);

}


.resource span {

    font-weight: bold;

    margin-left: 5px;

}


/* ============================================================
   오른쪽 상태창
============================================================ */

#sidePanel {

    position: fixed;

    top: 70px;

    right: 12px;

    width: 305px;

    min-height: 150px;

    z-index: 100;

    display: none;

    padding: 15px;

    color: #edf2f3;

    background:

        linear-gradient(
            145deg,
            rgba(29,38,42,.98),
            rgba(7,10,12,.98)
        );

    border:
        1px solid #78858a;

    border-radius: 6px;

    box-shadow:
        0 4px 18px
        rgba(0,0,0,.7);

}


.panelTitle {

    font-size: 22px;

    font-weight: bold;

    padding-bottom: 10px;

    margin-bottom: 10px;

    border-bottom:
        1px solid #465257;

}


.stat {

    padding: 6px 0;

    color: #cbd4d7;

    font-size: 14px;

}


.stat strong {

    color: #ffffff;

}


.actionButton {

    width: 100%;

    padding: 11px;

    margin-top: 7px;

    color: white;

    font-size: 14px;

    background:

        linear-gradient(
            #606f75,
            #303a3e
        );

    border:
        1px solid #859298;

    border-radius: 4px;

    cursor: pointer;

}


.actionButton:hover {

    background:

        linear-gradient(
            #78888e,
            #3b474c
        );

}


/* ============================================================
   메시지
============================================================ */

#buildMessage {

    position: fixed;

    left: 50%;

    bottom: 105px;

    transform:
        translateX(-50%);

    z-index: 150;

    display: none;

    padding:
        11px 22px;

    min-width: 240px;

    text-align: center;

    color: white;

    background:
        rgba(0,0,0,.86);

    border:
        1px solid #758187;

    border-radius: 5px;

    box-shadow:
        0 3px 15px
        rgba(0,0,0,.7);

}


/* ============================================================
   드래그 선택 박스
============================================================ */

#selectionBox {

    position: fixed;

    z-index: 140;

    display: none;

    border:
        1px solid #6ebcff;

    background:
        rgba(50,150,255,.14);

    pointer-events: none;

}


/* ============================================================
   미니맵
============================================================ */

#miniMap {

    position: fixed;

    left: 15px;

    bottom: 15px;

    width: 260px;

    height: 175px;

    z-index: 110;

    overflow: hidden;

    background: #142318;

    border:
        2px solid #69777b;

    border-radius: 5px;

    box-shadow:
        0 4px 15px
        rgba(0,0,0,.7);

    cursor: crosshair;

}


#miniCanvas {

    width: 100%;

    height: 100%;

    display: block;

}


/* ============================================================
   조작 안내
============================================================ */

#help {

    position: fixed;

    left: 50%;

    bottom: 15px;

    transform:
        translateX(-50%);

    z-index: 110;

    padding:
        8px 14px;

    color: #c1cacc;

    background:
        rgba(0,0,0,.68);

    border-radius: 4px;

    font-size: 12px;

    white-space: nowrap;

}


/* ============================================================
   카메라 방향 표시
============================================================ */

#cameraHint {

    position: fixed;

    left: 50%;

    top: 62px;

    transform:
        translateX(-50%);

    z-index: 90;

    color: rgba(255,255,255,.45);

    font-size: 11px;

    pointer-events: none;

}


/* ============================================================
   모바일/작은 화면
============================================================ */

@media(max-width:900px) {

    #sidePanel {

        width: 260px;

    }

    #miniMap {

        width: 210px;

        height: 140px;

    }

    #help {

        display: none;

    }

}

</style>

</head>


<body>


<!-- =========================================================
     게임
========================================================= -->

<div id="game"></div>


<!-- =========================================================
     종족 선택
========================================================= -->

<div id="raceScreen">

    <div class="raceBox">

        <div class="raceTitle">
            TERRAN
        </div>

        <div class="raceSub">
            테란을 선택하면 사령부와 SCV 5기가 배치됩니다.
        </div>

        <button
            id="startButton"
            class="raceButton"
        >
            테란으로 시작
        </button>

    </div>

</div>


<!-- =========================================================
     자원 UI
========================================================= -->

<div id="topUI">

    <div class="resource">

        💎 미네랄

        <span id="minerals">
            500
        </span>

    </div>


    <div class="resource">

        🟢 가스

        <span id="gas">
            0
        </span>

    </div>


    <div class="resource">

        👷 SCV

        <span id="scvCount">
            5
        </span>

    </div>


    <div class="resource">

        👥 인구수

        <span id="supply">
            5 / 20
        </span>

    </div>

</div>


<!-- =========================================================
     상태창
========================================================= -->

<div id="sidePanel">

    <div
        id="panelTitle"
        class="panelTitle"
    >
        상태
    </div>

    <div id="panelContent"></div>

</div>


<!-- =========================================================
     건설 메시지
========================================================= -->

<div id="buildMessage"></div>


<!-- =========================================================
     선택 박스
========================================================= -->

<div id="selectionBox"></div>


<!-- =========================================================
     미니맵
========================================================= -->

<div id="miniMap">

    <canvas
        id="miniCanvas"
        width="260"
        height="175"
    ></canvas>

</div>


<!-- =========================================================
     도움말
========================================================= -->

<div id="help">

    좌클릭: 선택 / 자원 채취 / 건설
    │
    좌클릭 드래그: 여러 SCV 선택
    │
    우클릭: 이동
    │
    화면 끝: 카메라 이동

</div>


<div id="cameraHint">

    마우스를 화면 가장자리로 이동하면 카메라가 움직입니다.

</div>


<script>


// ============================================================
// THREE 기본 설정
// ============================================================

const scene =
    new THREE.Scene();


scene.background =
    new THREE.Color(
        0x07100b
    );


const camera =
    new THREE.PerspectiveCamera(

        55,

        window.innerWidth /
        window.innerHeight,

        0.1,

        500

    );


camera.position.set(

    0,

    42,

    28

);


const renderer =
    new THREE.WebGLRenderer({

        antialias: true

    });


renderer.setSize(

    window.innerWidth,

    window.innerHeight

);


renderer.setPixelRatio(

    Math.min(
        window.devicePixelRatio,
        2
    )

);


renderer.shadowMap.enabled =
    true;


renderer.shadowMap.type =
    THREE.PCFSoftShadowMap;


document
    .getElementById("game")
    .appendChild(renderer.domElement);


// ============================================================
// 조명
// ============================================================

const ambientLight =
    new THREE.AmbientLight(

        0x89959a,

        0.75

    );


scene.add(
    ambientLight
);


const sun =
    new THREE.DirectionalLight(

        0xffffff,

        1.55

    );


sun.position.set(

    20,

    45,

    20

);


sun.castShadow =
    true;


sun.shadow.mapSize.width =
    2048;


sun.shadow.mapSize.height =
    2048;


scene.add(
    sun
);


// ============================================================
// 게임 변수
// ============================================================

let gameStarted =
    false;


let minerals =
    500;


let gas =
    0;


// ============================================================
// 인구수
// ============================================================

let supplyUsed =
    5;


let supplyMax =
    20;


// ============================================================
// SCV 설정
// ============================================================

const SCV_COST =
    50;


const SCV_BUILD_TIME =
    10;


const MAX_SCV_QUEUE =
    5;


const SCV_MINERAL_AMOUNT =
    50;


const SCV_GAS_AMOUNT =
    25;


const MINERAL_TIME =
    3;


const GAS_TIME =
    3;


// ============================================================
// 건물 설정
// ============================================================

const GAS_BUILD_TIME =
    15;


// ★ 서플라이 디포 건설 시간
// ★ 기존 15초 → 20초
const DEPOT_BUILD_TIME =
    20;


const DEPOT_COST =
    100;


const DEPOT_SUPPLY =
    10;


// ============================================================
// 맵
// ============================================================

const WORLD_SIZE =
    90;


const HALF_WORLD =
    WORLD_SIZE / 2;


// ============================================================
// 배열
// ============================================================

const scvs =
    [];


const mineralNodes =
    [];


const geysers =
    [];


const gasFacilities =
    [];


const supplyDepots =
    [];


const buildings =
    [];


// ============================================================
// 생산 대기열
// ============================================================

let scvQueue =
    0;


// ============================================================
// 선택
// ============================================================

let selectedUnits =
    [];


let selectedObject =
    null;


// ============================================================
// 건설 모드
// ============================================================

let buildMode =
    false;


let buildType =
    null;


let buildPreview =
    null;


let buildPreviewValid =
    false;


let currentBuilder =
    null;


// ============================================================
// 마우스
// ============================================================

const mouse =
    new THREE.Vector2();


const raycaster =
    new THREE.Raycaster();


let mouseDown =
    false;


let dragging =
    false;


let dragStartX =
    0;


let dragStartY =
    0;


let mouseX =
    window.innerWidth / 2;


let mouseY =
    window.innerHeight / 2;


// ============================================================
// 카메라
// ============================================================

let cameraX =
    0;


let cameraZ =
    0;


const CAMERA_EDGE =
    45;


const CAMERA_SPEED =
    0.55;


// ============================================================
// 바닥
// ============================================================

const ground =
    new THREE.Mesh(

        new THREE.PlaneGeometry(

            WORLD_SIZE,

            WORLD_SIZE,

            30,

            30

        ),

        new THREE.MeshStandardMaterial({

            color: 0x17251a,

            roughness: 0.95,

            metalness: 0.02

        })

    );


ground.rotation.x =
    -Math.PI / 2;


ground.receiveShadow =
    true;


ground.userData.type =
    "ground";


scene.add(
    ground
);


// ============================================================
// 맵 장식
// ============================================================

for(
    let i = 0;
    i < 180;
    i++
){

    const rock =
        new THREE.Mesh(

            new THREE.DodecahedronGeometry(

                0.15 +
                Math.random() * 0.45,

                0

            ),

            new THREE.MeshStandardMaterial({

                color: 0x2b3530,

                roughness: 0.9

            })

        );


    rock.position.set(

        (
            Math.random() -
            0.5
        ) * 82,

        0.15,

        (
            Math.random() -
            0.5
        ) * 82

    );


    rock.rotation.set(

        Math.random(),

        Math.random(),

        Math.random()

    );


    rock.castShadow =
        true;


    scene.add(
        rock
    );

}


// ============================================================
// 미네랄 위치
// 사령부에 너무 붙지 않도록 적당히 떨어진 위치
// ============================================================

const mineralPositions = [

    [-24,-12],
    [-22,-9],
    [-20,-13],
    [-18,-10],
    [-16,-13],

    [-24,-6],
    [-22,-3],
    [-20,-7],
    [-18,-4],
    [-16,-8],

    [-23,0],
    [-21,3],
    [-19,-1],
    [-17,2],
    [-15,-2],

    [-22,7],
    [-20,10],
    [-18,6],
    [-16,9]

];


// ============================================================
// 미네랄 생성
// ============================================================

function createMineral(
    x,
    z
){

    const group =
        new THREE.Group();


    for(
        let i = 0;
        i < 4;
        i++
    ){

        const crystal =
            new THREE.Mesh(

                new THREE.DodecahedronGeometry(

                    0.65 +
                    Math.random() * 0.45,

                    0

                ),

                new THREE.MeshStandardMaterial({

                    color: 0x2196ff,

                    emissive: 0x064c85,

                    emissiveIntensity: 0.65,

                    metalness: 0.45,

                    roughness: 0.25

                })

            );


        crystal.position.set(

            (
                Math.random() -
                0.5
            ) * 1.3,

            0.7 +
            Math.random() * 0.4,

            (
                Math.random() -
                0.5
            ) * 1.3

        );


        crystal.scale.y =

            1.4 +
            Math.random();


        crystal.rotation.set(

            Math.random(),

            Math.random(),

            Math.random()

        );


        crystal.castShadow =
            true;


        group.add(
            crystal
        );

    }


    group.position.set(

        x,

        0,

        z

    );


    group.userData = {

        type: "mineral",

        amount: 1500

    };


    mineralNodes.push(
        group
    );


    scene.add(
        group
    );

}


mineralPositions.forEach(

    position => {

        createMineral(

            position[0],

            position[1]

        );

    }

);


// ============================================================
// 가스 분출구 1개
// ============================================================

function createGeyser(
    x,
    z
){

    const group =
        new THREE.Group();


    const outerRock =
        new THREE.Mesh(

            new THREE.CylinderGeometry(

                3,

                3.4,

                0.6,

                24

            ),

            new THREE.MeshStandardMaterial({

                color: 0x303a35,

                roughness: 0.9

            })

        );


    outerRock.position.y =
        0.3;


    outerRock.castShadow =
        true;


    group.add(
        outerRock
    );


    const innerGas =
        new THREE.Mesh(

            new THREE.CylinderGeometry(

                1.8,

                2.2,

                1.2,

                20

            ),

            new THREE.MeshStandardMaterial({

                color: 0x16b765,

                emissive: 0x075d30,

                emissiveIntensity: 1.5,

                transparent: true,

                opacity: 0.72

            })

        );


    innerGas.position.y =
        1;


    group.add(
        innerGas
    );


    group.position.set(

        x,

        0,

        z

    );


    group.userData = {

        type: "geyser",

        hasFacility: false

    };


    geysers.push(
        group
    );


    scene.add(
        group
    );

}


createGeyser(

    14,

    7

);


// ============================================================
// 사령부
// ============================================================

function createCommandCenter(){

    const group =
        new THREE.Group();


    // 메인 몸체

    const base =
        new THREE.Mesh(

            new THREE.BoxGeometry(

                8,

                4,

                7

            ),

            new THREE.MeshStandardMaterial({

                color: 0x555f63,

                metalness: 0.75,

                roughness: 0.35

            })

        );


    base.position.y =
        2;


    base.castShadow =
        true;


    group.add(
        base
    );


    // 상부

    const upper =
        new THREE.Mesh(

            new THREE.BoxGeometry(

                5.5,

                1.6,

                4.7

            ),

            new THREE.MeshStandardMaterial({

                color: 0x3b4549,

                metalness: 0.8,

                roughness: 0.3

            })

        );


    upper.position.y =
        4.7;


    upper.castShadow =
        true;


    group.add(
        upper
    );


    // 유리

    const glass =
        new THREE.Mesh(

            new THREE.BoxGeometry(

                3.3,

                1.5,

                3

            ),

            new THREE.MeshStandardMaterial({

                color: 0x17445a,

                metalness: 0.6,

                roughness: 0.15,

                transparent: true,

                opacity: 0.85

            })

        );


    glass.position.y =
        5.5;


    group.add(
        glass
    );


    // 안테나

    const antenna =
        new THREE.Mesh(

            new THREE.CylinderGeometry(

                0.12,

                0.12,

                4,

                10

            ),

            new THREE.MeshStandardMaterial({

                color: 0x202628,

                metalness: 0.8

            })

        );


    antenna.position.y =
        8;


    group.add(
        antenna
    );


    // 안테나 빛

    const beacon =
        new THREE.Mesh(

            new THREE.SphereGeometry(

                0.25,

                12,

                12

            ),

            new THREE.MeshBasicMaterial({

                color: 0x3caeff

            })

        );


    beacon.position.y =
        10;


    group.add(
        beacon
    );


    group.userData = {

        type: "commandCenter",

        hp: 1500,

        maxHp: 1500

    };


    buildings.push(
        group
    );


    scene.add(
        group
    );


    return group;

}


const commandCenter =
    createCommandCenter();


// ============================================================
// SCV 생성
// ============================================================

function createSCV(
    x,
    z
){

    const group =
        new THREE.Group();


    // 본체

    const body =
        new THREE.Mesh(

            new THREE.BoxGeometry(

                1.7,

                0.8,

                2

            ),

            new THREE.MeshStandardMaterial({

                color: 0xc3a53b,

                metalness: 0.6,

                roughness: 0.4

            })

        );


    body.position.y =
        0.8;


    body.castShadow =
        true;


    group.add(
        body
    );


    // 운전석

    const cabin =
        new THREE.Mesh(

            new THREE.BoxGeometry(

                1.2,

                0.7,

                1

            ),

            new THREE.MeshStandardMaterial({

                color: 0x59666b,

                metalness: 0.65,

                roughness: 0.25

            })

        );


    cabin.position.set(

        0,

        1.35,

        -0.2

    );


    group.add(
        cabin
    );


    // 전면 작업 장치

    const drill =
        new THREE.Mesh(

            new THREE.BoxGeometry(

                1.9,

                0.25,

                0.55

            ),

            new THREE.MeshStandardMaterial({

                color: 0x8e7628,

                metalness: 0.7,

                roughness: 0.35

            })

        );


    drill.position.set(

        0,

        0.75,

        -1.3

    );


    group.add(
        drill
    );


    // 바퀴

    for(
        const side of [-1,1]
    ){

        for(
            const zpos of [-0.7,0.7]
        ){

            const wheel =
                new THREE.Mesh(

                    new THREE.CylinderGeometry(

                        0.38,

                        0.38,

                        0.35,

                        12

                    ),

                    new THREE.MeshStandardMaterial({

                        color: 0x171a1b,

                        metalness: 0.8,

                        roughness: 0.35

                    })

                );


            wheel.rotation.z =
                Math.PI / 2;


            wheel.position.set(

                side * 0.95,

                0.4,

                zpos

            );


            wheel.castShadow =
                true;


            group.add(
                wheel
            );

        }

    }


    group.position.set(

        x,

        0,

        z

    );


    group.userData = {

        type: "scv",

        hp: 50,

        maxHp: 50,

        state: "대기",

        speed: 7,

        moveTarget: null,

        moveCallback: null,

        target: null,

        carryingMineral: 0,

        carryingGas: 0,

        selected: false,

        ignoreObstacles: false

    };


    scvs.push(
        group
    );


    scene.add(
        group
    );


    return group;

}


// ============================================================
// 시작 SCV 5기
// ============================================================

for(
    let i = 0;
    i < 5;
    i++
){

    createSCV(

        6 +
        i * 1.7,

        5

    );

}


// ============================================================
// 가스 채취 시설
// ============================================================

function createGasFacility(
    geyser
){

    const group =
        new THREE.Group();


    // 바닥 플랫폼

    const platform =
        new THREE.Mesh(

            new THREE.CylinderGeometry(

                3.2,

                3.5,

                0.7,

                24

            ),

            new THREE.MeshStandardMaterial({

                color: 0x30383b,

                metalness: 0.8,

                roughness: 0.35

            })

        );


    platform.position.y =
        0.35;


    platform.castShadow =
        true;


    group.add(
        platform
    );


    // 저장 탱크

    const tank =
        new THREE.Mesh(

            new THREE.CylinderGeometry(

                1.55,

                1.85,

                3.8,

                20

            ),

            new THREE.MeshStandardMaterial({

                color: 0x4b5558,

                metalness: 0.8,

                roughness: 0.35

            })

        );


    tank.position.y =
        2.7;


    tank.castShadow =
        true;


    group.add(
        tank
    );


    // 중앙 가스 코어

    const core =
        new THREE.Mesh(

            new THREE.SphereGeometry(

                0.85,

                20,

                20

            ),

            new THREE.MeshStandardMaterial({

                color: 0x35ff91,

                emissive: 0x0fae54,

                emissiveIntensity: 2,

                transparent: true,

                opacity: 0.9

            })

        );


    core.position.y =
        5.2;


    group.add(
        core
    );


    // 가스 파티클

    const particles =
        new THREE.Group();


    for(
        let i = 0;
        i < 55;
        i++
    ){

        const particle =
            new THREE.Mesh(

                new THREE.SphereGeometry(

                    0.07 +
                    Math.random() * 0.12,

                    6,

                    6

                ),

                new THREE.MeshBasicMaterial({

                    color: 0x45ff91,

                    transparent: true,

                    opacity:
                        0.3 +
                        Math.random() * 0.4

                })

            );


        particle.position.set(

            (
                Math.random() -
                0.5
            ) * 1.7,

            5.3 +
            Math.random() * 4,

            (
                Math.random() -
                0.5
            ) * 1.7

        );


        particle.userData.speed =

            0.5 +
            Math.random() * 0.8;


        particles.add(
            particle
        );

    }


    group.add(
        particles
    );


    group.position.copy(
        geyser.position
    );


    group.userData = {

        type: "gasFacility",

        hp: 500,

        maxHp: 500,

        particles: particles,

        core: core

    };


    gasFacilities.push(
        group
    );


    scene.add(
        group
    );


    return group;

}


// ============================================================
// 서플라이 디포
// ============================================================

function createSupplyDepot(
    position
){

    const group =
        new THREE.Group();


    // 메인 몸체

    const base =
        new THREE.Mesh(

            new THREE.BoxGeometry(

                3.5,

                2.5,

                3.5

            ),

            new THREE.MeshStandardMaterial({

                color: 0x555f62,

                metalness: 0.7,

                roughness: 0.4

            })

        );


    base.position.y =
        1.25;


    base.castShadow =
        true;


    group.add(
        base
    );


    // 지붕

    const roof =
        new THREE.Mesh(

            new THREE.BoxGeometry(

                2.8,

                0.7,

                2.8

            ),

            new THREE.MeshStandardMaterial({

                color: 0x353e42,

                metalness: 0.8,

                roughness: 0.35

            })

        );


    roof.position.y =
        2.85;


    group.add(
        roof
    );


    // 표시등

    const light =
        new THREE.Mesh(

            new THREE.BoxGeometry(

                0.35,

                0.35,

                0.35

            ),

            new THREE.MeshBasicMaterial({

                color: 0xffaa22

            })

        );


    light.position.set(

        0,

        3.3,

        -1.3

    );


    group.add(
        light
    );


    group.position.copy(
        position
    );


    group.userData = {

        type: "supplyDepot",

        hp: 500,

        maxHp: 500

    };


    supplyDepots.push(
        group
    );


    buildings.push(
        group
    );


    scene.add(
        group
    );


    return group;

}


// ============================================================
// 건설 미리보기
// ============================================================

function createPreview(
    type
){

    const group =
        new THREE.Group();


    let geometry;


    if(
        type === "gas"
    ){

        geometry =
            new THREE.CylinderGeometry(

                3.2,

                3.5,

                4,

                24

            );

    }

    else{

        geometry =
            new THREE.BoxGeometry(

                3.5,

                3,

                3.5

            );

    }


    const mesh =
        new THREE.Mesh(

            geometry,

            new THREE.MeshStandardMaterial({

                color: 0x55ff88,

                emissive: 0x227744,

                emissiveIntensity: 0.7,

                transparent: true,

                opacity: 0.4

            })

        );


    if(
        type === "gas"
    ){

        mesh.position.y =
            2;

    }

    else{

        mesh.position.y =
            1.5;

    }


    group.add(
        mesh
    );


    group.visible =
        false;


    scene.add(
        group
    );


    return group;

}


const gasPreview =
    createPreview(
        "gas"
    );


const depotPreview =
    createPreview(
        "depot"
    );


// ============================================================
// 메시지
// ============================================================

function showMessage(
    text
){

    const box =
        document.getElementById(
            "buildMessage"
        );


    box.innerHTML =
        text;


    box.style.display =
        "block";


    clearTimeout(
        box.timer
    );


    box.timer =
        setTimeout(

            () => {

                box.style.display =
                    "none";

            },

            2000

        );

}


// ============================================================
// 선택 초기화
// ============================================================

function clearSelection(){

    selectedUnits.forEach(

        unit => {

            unit.userData.selected =
                false;

        }

    );


    selectedUnits =
        [];


    selectedObject =
        null;

}


// ============================================================
// 상태창
// ============================================================

function showPanel(
    obj
){

    const panel =
        document.getElementById(
            "sidePanel"
        );


    const title =
        document.getElementById(
            "panelTitle"
        );


    const content =
        document.getElementById(
            "panelContent"
        );


    panel.style.display =
        "block";


    // ========================================================
    // SCV
    // ========================================================

    if(
        obj.userData.type ===
        "scv"
    ){

        title.innerHTML =
            "👷 SCV";


        content.innerHTML = `

            <div class="stat">
                <strong>체력</strong>
                :
                ${obj.userData.hp}
                /
                ${obj.userData.maxHp}
            </div>

            <div class="stat">
                <strong>상태</strong>
                :
                ${obj.userData.state}
            </div>

            <div class="stat">
                <strong>미네랄 운반량</strong>
                :
                ${obj.userData.carryingMineral}
            </div>

            <div class="stat">
                <strong>가스 운반량</strong>
                :
                ${obj.userData.carryingGas}
            </div>

            <div class="stat">
                <strong>건설 가능한 건물</strong>
            </div>

            <button
                class="actionButton"
                onclick="startGasBuild()"
            >
                🟢 가스 채취 시설
                <br>
                건설 시간 15초
            </button>

            <button
                class="actionButton"
                onclick="startDepotBuild()"
            >
                🏢 서플라이 디포
                <br>
                💎 100 미네랄
                <br>
                👥 인구수 +10
                <br>
                ⏱️ 건설 시간 20초
            </button>

        `;

    }


    // ========================================================
    // 사령부
    // ========================================================

    else if(
        obj.userData.type ===
        "commandCenter"
    ){

        title.innerHTML =
            "🏢 사령부";


        content.innerHTML = `

            <div class="stat">
                <strong>체력</strong>
                :
                ${obj.userData.hp}
                /
                ${obj.userData.maxHp}
            </div>

            <div class="stat">
                <strong>현재 미네랄</strong>
                :
                ${minerals}
            </div>

            <div class="stat">
                <strong>현재 가스</strong>
                :
                ${gas}
            </div>

            <div class="stat">
                <strong>인구수</strong>
                :
                ${supplyUsed}
                /
                ${supplyMax}
            </div>

            <button
                class="actionButton"
                onclick="produceSCV()"
            >
                👷 SCV 만들기
                <br>
                💎 50 미네랄
                <br>
                ⏱️ 10초
            </button>

            <div class="stat">
                <strong>SCV 생산 대기열</strong>
                :
                ${scvQueue}
                /
                ${MAX_SCV_QUEUE}
            </div>

        `;

    }


    // ========================================================
    // 가스 시설
    // ========================================================

    else if(
        obj.userData.type ===
        "gasFacility"
    ){

        title.innerHTML =
            "🟢 가스 채취 시설";


        content.innerHTML = `

            <div class="stat">
                <strong>체력</strong>
                :
                ${obj.userData.hp}
                /
                ${obj.userData.maxHp}
            </div>

            <div class="stat">
                <strong>가스</strong>
                :
                무한
            </div>

            <div class="stat">
                <strong>SCV 채취량</strong>
                :
                ${SCV_GAS_AMOUNT}
            </div>

            <div class="stat">
                <strong>채취 시간</strong>
                :
                ${GAS_TIME}초
            </div>

        `;

    }


    // ========================================================
    // 서플라이 디포
    // ========================================================

    else if(
        obj.userData.type ===
        "supplyDepot"
    ){

        title.innerHTML =
            "🏢 서플라이 디포";


        content.innerHTML = `

            <div class="stat">
                <strong>체력</strong>
                :
                ${obj.userData.hp}
                /
                ${obj.userData.maxHp}
            </div>

            <div class="stat">
                <strong>인구수 증가</strong>
                :
                +10
            </div>

            <div class="stat">
                <strong>건설 비용</strong>
                :
                100 미네랄
            </div>

            <div class="stat">
                <strong>건설 시간</strong>
                :
                20초
            </div>

        `;

    }

}


// ============================================================
// SCV 생산
// ============================================================

function produceSCV(){

    // 대기열 확인

    if(
        scvQueue >=
        MAX_SCV_QUEUE
    ){

        showMessage(

            "🔴 SCV 생산 대기열이 가득 찼습니다."

        );

        return;

    }


    // 인구수 확인

    if(
        supplyUsed >=
        supplyMax
    ){

        showMessage(

            "🔴 인구수가 부족합니다.<br>" +
            "서플라이 디포를 건설하세요."

        );

        return;

    }


    // 미네랄 확인

    if(
        minerals <
        SCV_COST
    ){

        showMessage(

            "🔴 미네랄이 부족합니다."

        );

        return;

    }


    minerals -=
        SCV_COST;


    scvQueue++;


    updateResources();


    showMessage(

        "👷 SCV 생산 시작!<br>" +
        "10초 후 완성됩니다."

    );


    setTimeout(

        () => {

            // 생산 완료 시 인구수 확인

            if(
                supplyUsed >=
                supplyMax
            ){

                minerals +=
                    SCV_COST;


                scvQueue--;


                updateResources();


                showMessage(

                    "🔴 인구수가 부족하여<br>" +
                    "SCV 생산이 취소되었습니다."

                );


                return;

            }


            // 사령부 옆에 생성

            const angle =
                Math.random() *
                Math.PI *
                2;


            const distance =
                7;


            const newSCV =
                createSCV(

                    commandCenter.position.x +
                    Math.cos(angle) *
                    distance,

                    commandCenter.position.z +
                    Math.sin(angle) *
                    distance

                );


            supplyUsed++;


            scvQueue--;


            updateResources();


            showMessage(

                "👷 SCV 생산 완료!"

            );

        },

        SCV_BUILD_TIME *
        1000

    );

}


// ============================================================
// 가스 건설 시작
// ============================================================

function startGasBuild(){

    if(
        selectedUnits.length === 0
    ){

        showMessage(
            "SCV를 선택하세요."
        );

        return;

    }


    const builder =
        selectedUnits.find(

            unit =>
                unit.userData.type ===
                "scv"

        );


    if(
        !builder
    ){

        showMessage(
            "SCV를 선택하세요."
        );

        return;

    }


    cancelBuild();


    buildMode =
        true;


    buildType =
        "gas";


    currentBuilder =
        builder;


    gasPreview.visible =
        true;


    showMessage(

        "🟢 가스 채취 시설의 위치를 선택하세요."

    );

}


// ============================================================
// 서플라이 디포 건설 시작
// ============================================================

function startDepotBuild(){

    if(
        selectedUnits.length === 0
    ){

        showMessage(
            "SCV를 선택하세요."
        );

        return;

    }


    const builder =
        selectedUnits.find(

            unit =>
                unit.userData.type ===
                "scv"

        );


    if(
        !builder
    ){

        showMessage(
            "SCV를 선택하세요."
        );

        return;

    }


    if(
        minerals <
        DEPOT_COST
    ){

        showMessage(

            "🔴 미네랄이 부족합니다.<br>" +
            "서플라이 디포는 100 미네랄이 필요합니다."

        );

        return;

    }


    cancelBuild();


    buildMode =
        true;


    buildType =
        "depot";


    currentBuilder =
        builder;


    depotPreview.visible =
        true;


    showMessage(

        "🏢 서플라이 디포를 설치할 위치를 선택하세요."

    );

}


// ============================================================
// 건설 취소
// ============================================================

function cancelBuild(){

    buildMode =
        false;


    buildType =
        null;


    buildPreviewValid =
        false;


    currentBuilder =
        null;


    gasPreview.visible =
        false;


    depotPreview.visible =
        false;

}


// ============================================================
// 건설 미리보기 위치
// ============================================================

function updateBuildPreview(){

    if(
        !buildMode
    )
        return;


    raycaster.setFromCamera(

        mouse,

        camera

    );


    const hits =
        raycaster.intersectObject(

            ground

        );


    if(
        hits.length === 0
    )
        return;


    const point =
        hits[0].point;


    // ========================================================
    // 가스 시설
    // ========================================================

    if(
        buildType ===
        "gas"
    ){

        let nearest =
            null;


        let nearestDistance =
            Infinity;


        geysers.forEach(

            geyser => {

                const dx =
                    point.x -
                    geyser.position.x;


                const dz =
                    point.z -
                    geyser.position.z;


                const distance =
                    Math.sqrt(

                        dx * dx +
                        dz * dz

                    );


                if(
                    distance <
                    nearestDistance
                ){

                    nearestDistance =
                        distance;


                    nearest =
                        geyser;

                }

            }

        );


        if(

            nearest &&
            nearestDistance < 5 &&
            !nearest.userData.hasFacility

        ){

            buildPreviewValid =
                true;


            gasPreview.position.copy(

                nearest.position

            );


            setPreviewColor(

                gasPreview,

                0x55ff88

            );


            showBuildPreviewMessage(

                "🟢 건설 가능<br>" +
                "좌클릭하여 건설"

            );

        }

        else{

            buildPreviewValid =
                false;


            gasPreview.position.set(

                point.x,

                0,

                point.z

            );


            setPreviewColor(

                gasPreview,

                0xff3333

            );


            showBuildPreviewMessage(

                "🔴 건설할 수 없음<br>" +
                "가스 분출구 위에 설치하세요."

            );

        }

    }


    // ========================================================
    // 서플라이 디포
    // ========================================================

    else if(
        buildType ===
        "depot"
    ){

        buildPreviewValid =
            true;


        depotPreview.position.set(

            point.x,

            0,

            point.z

        );


        setPreviewColor(

            depotPreview,

            0x55ff88

        );


        showBuildPreviewMessage(

            "🟢 건설 가능<br>" +
            "좌클릭하여 건설<br>" +
            "건설 시간 20초"

        );

    }

}


// ============================================================
// 건설 미리보기 메시지
// ============================================================

function showBuildPreviewMessage(
    text
){

    const box =
        document.getElementById(
            "buildMessage"
        );


    box.innerHTML =
        text;


    box.style.display =
        "block";

}


// ============================================================
// 미리보기 색 변경
// ============================================================

function setPreviewColor(
    obj,
    color
){

    obj.traverse(

        child => {

            if(
                child.material
            ){

                child.material.color
                    .setHex(
                        color
                    );


                child.material.emissive
                    .setHex(
                        color
                    );

            }

        }

    );

}


// ============================================================
// 건설 확정
// ============================================================

function confirmBuild(){

    if(
        !buildMode ||
        !currentBuilder
    ){

        return;

    }


    if(
        !buildPreviewValid
    ){

        showMessage(

            "🔴 이 위치에는 건설할 수 없습니다."

        );

        return;

    }


    const builder =
        currentBuilder;


    // ========================================================
    // 가스 시설 건설
    // ========================================================

    if(
        buildType ===
        "gas"
    ){

        let target =
            null;


        geysers.forEach(

            geyser => {

                if(

                    geyser.position.distanceTo(
                        gasPreview.position
                    ) < 0.1

                ){

                    target =
                        geyser;

                }

            }

        );


        if(
            !target
        ){

            showMessage(

                "🔴 가스 분출구가 아닙니다."

            );

            return;

        }


        buildMode =
            false;


        gasPreview.visible =
            false;


        currentBuilder =
            null;


        builder.userData.state =
            "가스 시설 건설 위치로 이동";


        moveUnitTo(

            builder,

            target.position,

            () => {

                builder.userData.state =
                    "가스 시설 건설 중";


                showMessage(

                    "🏗️ 가스 채취 시설 건설 중...<br>" +
                    "15초"

                );


                setTimeout(

                    () => {

                        if(
                            target.userData.hasFacility
                        )
                            return;


                        target.userData.hasFacility =
                            true;


                        createGasFacility(
                            target
                        );


                        builder.userData.state =
                            "대기";


                        showMessage(

                            "🟢 가스 채취 시설 건설 완료!"

                        );

                    },

                    GAS_BUILD_TIME *
                    1000

                );

            },

            false

        );

    }


    // ========================================================
    // 서플라이 디포 건설
    // ========================================================

    else if(
        buildType ===
        "depot"
    ){

        if(
            minerals <
            DEPOT_COST
        ){

            showMessage(

                "🔴 미네랄이 부족합니다."

            );


            cancelBuild();


            return;

        }


        // 비용 지불

        minerals -=
            DEPOT_COST;


        updateResources();


        const position =
            depotPreview
                .position
                .clone();


        buildMode =
            false;


        depotPreview.visible =
            false;


        currentBuilder =
            null;


        builder.userData.state =
            "서플라이 디포 건설 위치로 이동";


        moveUnitTo(

            builder,

            position,

            () => {

                builder.userData.state =
                    "서플라이 디포 건설 중";


                showMessage(

                    "🏢 서플라이 디포 건설 중...<br>" +
                    "20초"

                );


                // ★ 20초

                setTimeout(

                    () => {

                        createSupplyDepot(
                            position
                        );


                        // 인구수 +10

                        supplyMax +=
                            DEPOT_SUPPLY;


                        builder.userData.state =
                            "대기";


                        updateResources();


                        showMessage(

                            "🟢 서플라이 디포 건설 완료!<br>" +
                            "인구수 +10"

                        );

                    },

                    DEPOT_BUILD_TIME *
                    1000

                );

            },

            false

        );

    }

}


// ============================================================
// 자원 채취 중인지 확인
// ============================================================

function isResourceMovement(
    unit
){

    const state =
        unit.userData.state;


    return (

        state ===
            "미네랄로 이동" ||

        state ===
            "미네랄 채취 중" ||

        state ===
            "사령부로 복귀" ||

        state ===
            "가스 시설로 이동" ||

        state ===
            "가스 채취 중"

    );

}


// ============================================================
// 장애물 회피
// ============================================================

function getAvoidance(
    unit
){

    const avoidance =
        new THREE.Vector3();


    // 자원 채취 중에는 장애물을 무시

    if(
        isResourceMovement(
            unit
        )
    ){

        return avoidance;

    }


    // SCV끼리 회피

    scvs.forEach(

        other => {

            if(
                other === unit
            )
                return;


            const offset =
                new THREE.Vector3()
                    .subVectors(

                        unit.position,

                        other.position

                    );


            offset.y =
                0;


            const distance =
                offset.length();


            if(

                distance > 0 &&
                distance < 2

            ){

                offset.normalize();


                avoidance.add(

                    offset.multiplyScalar(

                        (
                            2 -
                            distance
                        ) * 2.5

                    )

                );

            }

        }

    );


    // 건물 회피

    buildings.forEach(

        building => {

            const offset =
                new THREE.Vector3()
                    .subVectors(

                        unit.position,

                        building.position

                    );


            offset.y =
                0;


            const distance =
                offset.length();


            if(

                distance > 0 &&
                distance < 5

            ){

                offset.normalize();


                avoidance.add(

                    offset.multiplyScalar(

                        (
                            5 -
                            distance
                        ) * 1.8

                    )

                );

            }

        }

    );


    return avoidance;

}


// ============================================================
// 이동 명령
// ============================================================

function moveUnitTo(

    unit,

    target,

    callback = null,

    ignoreObstacles = false

){

    unit.userData.moveTarget =
        target.clone();


    unit.userData.moveCallback =
        callback;


    unit.userData.ignoreObstacles =
        ignoreObstacles;


    if(
        !isResourceMovement(
            unit
        )
    ){

        unit.userData.state =
            "이동 중";

    }

}


// ============================================================
// 이동 업데이트
// ============================================================

function updateUnitMovement(

    unit,

    delta

){

    const data =
        unit.userData;


    if(
        !data.moveTarget
    )
        return;


    const direction =
        new THREE.Vector3()
            .subVectors(

                data.moveTarget,

                unit.position

            );


    direction.y =
        0;


    const distance =
        direction.length();


    if(
        distance < 0.45
    ){

        data.moveTarget =
            null;


        const callback =
            data.moveCallback;


        data.moveCallback =
            null;


        if(
            callback
        ){

            callback();

        }


        return;

    }


    direction.normalize();


    let finalDirection =
        direction.clone();


    if(

        !data.ignoreObstacles &&
        !isResourceMovement(
            unit
        )

    ){

        finalDirection.add(

            getAvoidance(
                unit
            )

        );


        if(
            finalDirection.length() >
            0.01
        ){

            finalDirection.normalize();

        }

    }


    unit.position.add(

        finalDirection.multiplyScalar(

            data.speed *
            delta

        )

    );


    unit.rotation.y =

        Math.atan2(

            finalDirection.x,

            finalDirection.z

        );

}


// ============================================================
// 미네랄 채취
// ============================================================

function orderMineMineral(

    scv,

    mineral

){

    if(
        mineral.userData.amount <=
        0
    ){

        scv.userData.state =
            "대기";


        return;

    }


    scv.userData.target =
        mineral;


    scv.userData.state =
        "미네랄로 이동";


    moveUnitTo(

        scv,

        mineral.position,

        () => {

            scv.userData.state =
                "미네랄 채취 중";


            showMessage(

                "⛏️ SCV가 미네랄을 채취합니다.<br>" +
                "3초"

            );


            setTimeout(

                () => {

                    if(
                        mineral.userData.amount <=
                        0
                    ){

                        scv.userData.state =
                            "대기";


                        return;

                    }


                    const amount =
                        Math.min(

                            SCV_MINERAL_AMOUNT,

                            mineral.userData.amount

                        );


                    mineral.userData.amount -=
                        amount;


                    scv.userData.carryingMineral =
                        amount;


                    scv.userData.state =
                        "사령부로 복귀";


                    moveUnitTo(

                        scv,

                        commandCenter.position,

                        () => {

                            minerals +=

                                scv.userData
                                    .carryingMineral;


                            scv.userData
                                .carryingMineral =
                                0;


                            updateResources();


                            // 무한 반복

                            orderMineMineral(

                                scv,

                                mineral

                            );

                        },

                        true

                    );

                },

                MINERAL_TIME *
                1000

            );

        },

        true

    );

}


// ============================================================
// 가스 채취
// ============================================================

function orderMineGas(

    scv,

    facility

){

    if(
        !facility
    )
        return;


    scv.userData.target =
        facility;


    scv.userData.state =
        "가스 시설로 이동";


    moveUnitTo(

        scv,

        facility.position,

        () => {

            scv.userData.state =
                "가스 채취 중";


            showMessage(

                "🟢 SCV가 가스를 채취합니다.<br>" +
                "3초"

            );


            setTimeout(

                () => {

                    // 가스는 무한

                    scv.userData.carryingGas =
                        SCV_GAS_AMOUNT;


                    scv.userData.state =
                        "사령부로 복귀";


                    moveUnitTo(

                        scv,

                        commandCenter.position,

                        () => {

                            gas +=

                                scv.userData
                                    .carryingGas;


                            scv.userData
                                .carryingGas =
                                0;


                            updateResources();


                            // 무한 반복

                            orderMineGas(

                                scv,

                                facility

                            );

                        },

                        true

                    );

                },

                GAS_TIME *
                1000

            );

        },

        true

    );

}


// ============================================================
// 마우스 이동
// ============================================================

renderer.domElement.addEventListener(

    "mousemove",

    event => {

        mouseX =
            event.clientX;


        mouseY =
            event.clientY;


        mouse.x =

            event.clientX /
            window.innerWidth *
            2 -
            1;


        mouse.y =

            -(
                event.clientY /
                window.innerHeight *
                2 -
                1
            );


        if(
            mouseDown
        ){

            const dx =
                event.clientX -
                dragStartX;


            const dy =
                event.clientY -
                dragStartY;


            if(

                Math.abs(dx) > 5 ||
                Math.abs(dy) > 5

            ){

                dragging =
                    true;


                updateSelectionBox(

                    dragStartX,

                    dragStartY,

                    event.clientX,

                    event.clientY

                );

            }

        }


        updateBuildPreview();

    }

);


// ============================================================
// 좌클릭 누르기
// ============================================================

renderer.domElement.addEventListener(

    "mousedown",

    event => {

        if(
            event.button !== 0
        )
            return;


        mouseDown =
            true;


        dragging =
            false;


        dragStartX =
            event.clientX;


        dragStartY =
            event.clientY;

    }

);


// ============================================================
// 좌클릭 떼기
// ============================================================

renderer.domElement.addEventListener(

    "mouseup",

    event => {

        if(
            event.button !== 0
        )
            return;


        mouseDown =
            false;


        // 건설 모드

        if(
            buildMode
        ){

            if(
                !dragging
            ){

                confirmBuild();

            }


            hideSelectionBox();


            dragging =
                false;


            return;

        }


        // 드래그 선택

        if(
            dragging
        ){

            selectUnitsInBox(

                dragStartX,

                dragStartY,

                event.clientX,

                event.clientY

            );

        }

        else{

            clickSelect(

                event.clientX,

                event.clientY

            );

        }


        hideSelectionBox();


        dragging =
            false;

    }

);


// ============================================================
// 우클릭
// ============================================================

renderer.domElement.addEventListener(

    "contextmenu",

    event => {

        event.preventDefault();


        // 건설 중 우클릭 = 건설 취소

        if(
            buildMode
        ){

            cancelBuild();


            showMessage(

                "건설을 취소했습니다."

            );


            return;

        }


        if(
            selectedUnits.length ===
            0
        )
            return;


        mouse.x =

            event.clientX /
            window.innerWidth *
            2 -
            1;


        mouse.y =

            -(
                event.clientY /
                window.innerHeight *
                2 -
                1
            );


        raycaster.setFromCamera(

            mouse,

            camera

        );


        const hits =
            raycaster.intersectObject(

                ground

            );


        if(
            hits.length ===
            0
        )
            return;


        const point =
            hits[0].point;


        selectedUnits.forEach(

            unit => {

                if(
                    unit.userData.type ===
                    "scv"
                ){

                    unit.userData.target =
                        null;


                    unit.userData.state =
                        "이동 중";


                    moveUnitTo(

                        unit,

                        point,

                        null,

                        false

                    );

                }

            }

        );

    }

);


// ============================================================
// 클릭 선택
// ============================================================

function clickSelect(

    x,

    y

){

    mouse.x =

        x /
        window.innerWidth *
        2 -
        1;


    mouse.y =

        -(
            y /
            window.innerHeight *
            2 -
            1
        );


    raycaster.setFromCamera(

        mouse,

        camera

    );


    const objects =
        [];


    scvs.forEach(

        object =>
            objects.push(
                object
            )

    );


    buildings.forEach(

        object =>
            objects.push(
                object
            )

    );


    gasFacilities.forEach(

        object =>
            objects.push(
                object
            )

    );


    mineralNodes.forEach(

        object =>
            objects.push(
                object
            )

    );


    geysers.forEach(

        object =>
            objects.push(
                object
            )

    );


    const hits =
        raycaster.intersectObjects(

            objects,

            true

        );


    if(
        hits.length ===
        0
    ){

        clearSelection();


        document
            .getElementById(
                "sidePanel"
            )
            .style.display =
            "none";


        return;

    }


    let object =
        hits[0].object;


    while(

        object.parent &&
        !object.userData.type

    ){

        object =
            object.parent;

    }


    if(
        !object.userData.type
    )
        return;


    // ========================================================
    // 미네랄
    // ========================================================

    if(
        object.userData.type ===
        "mineral"
    ){

        if(
            selectedUnits.length > 0
        ){

            selectedUnits.forEach(

                unit => {

                    if(
                        unit.userData.type ===
                        "scv"
                    ){

                        orderMineMineral(

                            unit,

                            object

                        );

                    }

                }

            );

        }


        return;

    }


    // ========================================================
    // 가스 시설
    // ========================================================

    if(
        object.userData.type ===
        "gasFacility"
    ){

        if(
            selectedUnits.length > 0
        ){

            selectedUnits.forEach(

                unit => {

                    if(
                        unit.userData.type ===
                        "scv"
                    ){

                        orderMineGas(

                            unit,

                            object

                        );

                    }

                }

            );


            return;

        }


        selectObject(
            object
        );


        return;

    }


    // ========================================================
    // SCV
    // ========================================================

    if(
        object.userData.type ===
        "scv"
    ){

        selectUnit(
            object
        );


        return;

    }


    // ========================================================
    // 사령부
    // ========================================================

    if(
        object.userData.type ===
        "commandCenter"
    ){

        clearSelection();


        selectedObject =
            object;


        showPanel(
            object
        );


        return;

    }


    // ========================================================
    // 서플라이 디포
    // ========================================================

    if(
        object.userData.type ===
        "supplyDepot"
    ){

        selectObject(
            object
        );


        return;

    }

}


// ============================================================
// SCV 선택
// ============================================================

function selectUnit(
    unit
){

    clearSelection();


    unit.userData.selected =
        true;


    selectedUnits.push(
        unit
    );


    selectedObject =
        unit;


    showPanel(
        unit
    );

}


// ============================================================
// 건물 선택
// ============================================================

function selectObject(
    object
){

    clearSelection();


    selectedObject =
        object;


    showPanel(
        object
    );

}


// ============================================================
// 선택 박스 업데이트
// ============================================================

function updateSelectionBox(

    x1,

    y1,

    x2,

    y2

){

    const box =
        document.getElementById(
            "selectionBox"
        );


    box.style.display =
        "block";


    box.style.left =

        Math.min(
            x1,
            x2
        ) + "px";


    box.style.top =

        Math.min(
            y1,
            y2
        ) + "px";


    box.style.width =

        Math.abs(
            x2 -
            x1
        ) + "px";


    box.style.height =

        Math.abs(
            y2 -
            y1
        ) + "px";

}


// ============================================================
// 선택 박스 숨김
// ============================================================

function hideSelectionBox(){

    document
        .getElementById(
            "selectionBox"
        )
        .style.display =
        "none";

}


// ============================================================
// 화면 좌표로 변환
// ============================================================

function worldToScreen(
    position
){

    const vector =
        position.clone();


    vector.project(
        camera
    );


    return {

        x:
            (
                vector.x +
                1
            ) /
            2 *
            window.innerWidth,

        y:
            (
                -vector.y +
                1
            ) /
            2 *
            window.innerHeight

    };

}


// ============================================================
// 드래그 선택
// ============================================================

function selectUnitsInBox(

    x1,

    y1,

    x2,

    y2

){

    clearSelection();


    const left =
        Math.min(
            x1,
            x2
        );


    const right =
        Math.max(
            x1,
            x2
        );


    const top =
        Math.min(
            y1,
            y2
        );


    const bottom =
        Math.max(
            y1,
            y2
        );


    scvs.forEach(

        scv => {

            const screen =
                worldToScreen(

                    scv.position

                );


            if(

                screen.x >= left &&
                screen.x <= right &&
                screen.y >= top &&
                screen.y <= bottom

            ){

                scv.userData.selected =
                    true;


                selectedUnits.push(
                    scv
                );

            }

        }

    );


    if(
        selectedUnits.length > 0
    ){

        selectedObject =
            selectedUnits[0];


        showPanel(
            selectedUnits[0]
        );

    }

}


// ============================================================
// 카메라 이동
// ============================================================

function updateCamera(){

    // 왼쪽 끝

    if(
        mouseX <
        CAMERA_EDGE
    ){

        cameraX -=
            CAMERA_SPEED;

    }


    // 오른쪽 끝

    if(
        mouseX >
        window.innerWidth -
        CAMERA_EDGE
    ){

        cameraX +=
            CAMERA_SPEED;

    }


    // 위쪽 끝

    if(
        mouseY <
        CAMERA_EDGE
    ){

        cameraZ -=
            CAMERA_SPEED;

    }


    // 아래쪽 끝

    if(
        mouseY >
        window.innerHeight -
        CAMERA_EDGE
    ){

        cameraZ +=
            CAMERA_SPEED;

    }


    cameraX =
        THREE.MathUtils.clamp(

            cameraX,

            -38,

            38

        );


    cameraZ =
        THREE.MathUtils.clamp(

            cameraZ,

            -38,

            38

        );


    camera.position.set(

        cameraX,

        42,

        cameraZ + 28

    );


    camera.lookAt(

        cameraX,

        0,

        cameraZ

    );

}


// ============================================================
// 미니맵
// ============================================================

const miniCanvas =
    document.getElementById(
        "miniCanvas"
    );


const miniCtx =
    miniCanvas.getContext(
        "2d"
    );


// ============================================================
// 미니맵 클릭
// ============================================================

document
    .getElementById(
        "miniMap"
    )
    .addEventListener(

        "click",

        event => {

            const rect =
                miniCanvas
                    .getBoundingClientRect();


            const x =

                (
                    event.clientX -
                    rect.left
                ) /
                rect.width;


            const y =

                (
                    event.clientY -
                    rect.top
                ) /
                rect.height;


            cameraX =

                (
                    x -
                    0.5
                ) * 78;


            cameraZ =

                (
                    y -
                    0.5
                ) * 78;

        }

    );


// ============================================================
// 미니맵 그리기
// ============================================================

function drawMiniMap(){

    const width =
        miniCanvas.width;


    const height =
        miniCanvas.height;


    miniCtx.fillStyle =
        "#15251a";


    miniCtx.fillRect(

        0,

        0,

        width,

        height

    );


    // ========================================================
    // 맵 테두리
    // ========================================================

    miniCtx.strokeStyle =
        "#46594b";


    miniCtx.strokeRect(

        1,

        1,

        width - 2,

        height - 2

    );


    // ========================================================
    // 미네랄
    // ========================================================

    mineralNodes.forEach(

        mineral => {

            const x =

                (
                    mineral.position.x +
                    45
                ) /
                90 *
                width;


            const y =

                (
                    mineral.position.z +
                    45
                ) /
                90 *
                height;


            miniCtx.fillStyle =
                "#29a9ff";


            miniCtx.fillRect(

                x - 2,

                y - 2,

                4,

                4

            );

        }

    );


    // ========================================================
    // 가스 분출구
    // ========================================================

    geysers.forEach(

        geyser => {

            const x =

                (
                    geyser.position.x +
                    45
                ) /
                90 *
                width;


            const y =

                (
                    geyser.position.z +
                    45
                ) /
                90 *
                height;


            miniCtx.fillStyle =
                "#32ff77";


            miniCtx.beginPath();


            miniCtx.arc(

                x,

                y,

                5,

                0,

                Math.PI * 2

            );


            miniCtx.fill();

        }

    );


    // ========================================================
    // 사령부
    // ========================================================

    const cx =

        (
            commandCenter.position.x +
            45
        ) /
        90 *
        width;


    const cy =

        (
            commandCenter.position.z +
            45
        ) /
        90 *
        height;


    miniCtx.fillStyle =
        "#eeeeee";


    miniCtx.fillRect(

        cx - 7,

        cy - 7,

        14,

        14

    );


    // ========================================================
    // SCV
    // ========================================================

    scvs.forEach(

        scv => {

            const x =

                (
                    scv.position.x +
                    45
                ) /
                90 *
                width;


            const y =

                (
                    scv.position.z +
                    45
                ) /
                90 *
                height;


            miniCtx.fillStyle =
                "#e7bd42";


            miniCtx.fillRect(

                x - 2,

                y - 2,

                4,

                4

            );

        }

    );


    // ========================================================
    // 가스 시설
    // ========================================================

    gasFacilities.forEach(

        facility => {

            const x =

                (
                    facility.position.x +
                    45
                ) /
                90 *
                width;


            const y =

                (
                    facility.position.z +
                    45
                ) /
                90 *
                height;


            miniCtx.fillStyle =
                "#52ff99";


            miniCtx.fillRect(

                x - 5,

                y - 5,

                10,

                10

            );

        }

    );


    // ========================================================
    // 서플라이 디포
    // ========================================================

    supplyDepots.forEach(

        depot => {

            const x =

                (
                    depot.position.x +
                    45
                ) /
                90 *
                width;


            const y =

                (
                    depot.position.z +
                    45
                ) /
                90 *
                height;


            miniCtx.fillStyle =
                "#aaaaaa";


            miniCtx.fillRect(

                x - 4,

                y - 4,

                8,

                8

            );

        }

    );


    // ========================================================
    // 현재 카메라 위치
    // ========================================================

    const vx =

        (
            cameraX +
            45
        ) /
        90 *
        width;


    const vy =

        (
            cameraZ +
            45
        ) /
        90 *
        height;


    miniCtx.strokeStyle =
        "#ffffff";


    miniCtx.lineWidth =
        1;


    miniCtx.strokeRect(

        vx - 22,

        vy - 15,

        44,

        30

    );

}


// ============================================================
// 가스 파티클 애니메이션
// ============================================================

function animateGas(
    delta
){

    gasFacilities.forEach(

        facility => {

            const particles =
                facility
                    .userData
                    .particles
                    .children;


            particles.forEach(

                particle => {

                    particle.position.y +=

                        particle
                            .userData
                            .speed *
                        delta;


                    if(
                        particle.position.y >
                        9.5
                    ){

                        particle.position.y =
                            5.3;


                        particle.position.x =

                            (
                                Math.random() -
                                0.5
                            ) * 1.7;


                        particle.position.z =

                            (
                                Math.random() -
                                0.5
                            ) * 1.7;

                    }

                }

            );


            const core =
                facility
                    .userData
                    .core;


            core.scale.setScalar(

                1 +

                Math.sin(

                    performance.now() *
                    0.004

                ) * 0.08

            );

        }

    );

}


// ============================================================
// 선택 링
// ============================================================

function updateSelectionVisual(){

    scvs.forEach(

        scv => {

            let ring =
                scv.getObjectByName(
                    "selectionRing"
                );


            if(
                scv.userData.selected
            ){

                if(
                    !ring
                ){

                    ring =
                        new THREE.Mesh(

                            new THREE.RingGeometry(

                                1.1,

                                1.3,

                                24

                            ),

                            new THREE.MeshBasicMaterial({

                                color: 0x66bbff,

                                side:
                                    THREE.DoubleSide

                            })

                        );


                    ring.name =
                        "selectionRing";


                    ring.rotation.x =
                        -Math.PI / 2;


                    ring.position.y =
                        0.05;


                    scv.add(
                        ring
                    );

                }

            }

            else{

                if(
                    ring
                ){

                    scv.remove(
                        ring
                    );

                }

            }

        }

    );

}


// ============================================================
// 자원 UI
// ============================================================

function updateResources(){

    document
        .getElementById(
            "minerals"
        )
        .innerHTML =
        Math.floor(
            minerals
        );


    document
        .getElementById(
            "gas"
        )
        .innerHTML =
        Math.floor(
            gas
        );


    document
        .getElementById(
            "scvCount"
        )
        .innerHTML =
        scvs.length;


    document
        .getElementById(
            "supply"
        )
        .innerHTML =

        supplyUsed +
        " / " +
        supplyMax;


    // 상태창이 열려 있으면 갱신

    if(
        selectedObject
    ){

        if(
            selectedObject.userData.type ===
            "commandCenter"
        ){

            showPanel(
                selectedObject
            );

        }

    }

}


// ============================================================
// 게임 시작
// ============================================================

document
    .getElementById(
        "startButton"
    )
    .addEventListener(

        "click",

        () => {

            gameStarted =
                true;


            document
                .getElementById(
                    "raceScreen"
                )
                .style.display =
                "none";


            updateResources();


            showMessage(

                "⚔️ 테란 기지가 건설되었습니다.<br>" +
                "SCV 5기가 준비되었습니다."

            );

        }

    );


// ============================================================
// 키보드 ESC
// 건설 취소
// ============================================================

window.addEventListener(

    "keydown",

    event => {

        if(
            event.key ===
            "Escape"
        ){

            if(
                buildMode
            ){

                cancelBuild();


                showMessage(

                    "건설을 취소했습니다."

                );

            }

        }

    }

);


// ============================================================
// 메인 게임 루프
// ============================================================

let lastTime =
    performance.now();


function animate(){

    requestAnimationFrame(
        animate
    );


    const now =
        performance.now();


    const delta =
        Math.min(

            (
                now -
                lastTime
            ) / 1000,

            0.05

        );


    lastTime =
        now;


    if(
        gameStarted
    ){

        // 카메라

        updateCamera();


        // SCV

        scvs.forEach(

            scv => {

                updateUnitMovement(

                    scv,

                    delta

                );

            }

        );


        // 가스

        animateGas(
            delta
        );


        // 건설 미리보기

        updateBuildPreview();


        // 선택 표시

        updateSelectionVisual();


        // 미니맵

        drawMiniMap();

    }


    renderer.render(

        scene,

        camera

    );

}


animate();


// ============================================================
// 창 크기 변경
// ============================================================

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


// ============================================================
// 최초 UI
// ============================================================

updateResources();


</script>

</body>

</html>

"""


# ============================================================
# Streamlit에 게임 표시
# ============================================================

components.html(

    GAME_HTML,

    height=900,

    scrolling=False

)
