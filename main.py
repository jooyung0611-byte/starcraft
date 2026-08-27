import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="StarCraft 3D Mini",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# 시작 화면
# =========================================================

if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:

    st.markdown("""
    <style>
    .title {
        text-align:center;
        font-size:72px;
        font-weight:900;
        margin-top:130px;
        letter-spacing:8px;
    }

    .subtitle {
        text-align:center;
        color:#aaa;
        font-size:22px;
        margin-bottom:40px;
    }
    </style>

    <div class="title">STARCRAFT</div>
    <div class="subtitle">TERRAN COMMAND</div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c2:
        if st.button(
            "🔵 TERRAN",
            use_container_width=True
        ):
            st.session_state.started = True
            st.rerun()

    st.info("현재는 테란만 플레이할 수 있습니다.")
    st.stop()


# =========================================================
# 3D GAME
# =========================================================

html = r"""
<!DOCTYPE html>
<html>

<head>

<meta charset="UTF-8">

<style>

html, body {
    margin:0;
    padding:0;
    width:100%;
    height:100%;
    overflow:hidden;
    background:#05080a;
    font-family:Arial, sans-serif;
}

#game {
    width:100%;
    height:100%;
}


/* ================================
   상단 자원 UI
================================ */

#topUI {

    position:absolute;

    top:15px;
    left:15px;

    z-index:30;

    background:rgba(5,10,15,0.94);

    border:1px solid #526575;

    border-radius:8px;

    padding:13px 20px;

    color:white;

    min-width:500px;

    box-shadow:
        0 4px 20px rgba(0,0,0,0.5);
}

.resource {

    display:inline-block;

    margin-right:28px;

    font-size:18px;
}

#message {

    margin-top:10px;

    color:#7fcaff;

    font-size:14px;
}


/* ================================
   선택 / 명령 UI
================================ */

#commandUI {

    position:absolute;

    right:20px;

    bottom:20px;

    z-index:30;

    width:280px;

    background:rgba(5,10,15,0.96);

    border:1px solid #526575;

    border-radius:8px;

    padding:15px;

    color:white;

    display:none;

    box-shadow:
        0 4px 20px rgba(0,0,0,0.6);
}

#commandUI button {

    width:100%;

    margin-top:8px;

    padding:11px;

    background:#172b38;

    border:1px solid #4c7188;

    color:white;

    border-radius:5px;

    cursor:pointer;

    font-size:14px;
}

#commandUI button:hover {

    background:#284b60;
}


/* ================================
   생산 진행바
================================ */

#progressArea {

    margin-top:12px;

    display:none;
}

#progress {

    height:9px;

    background:#222;

    border-radius:5px;

    overflow:hidden;

    margin-top:5px;
}

#progressBar {

    width:0%;

    height:100%;

    background:#28aaff;
}


/* ================================
   선택 박스
================================ */

#selectionBox {

    position:absolute;

    z-index:25;

    display:none;

    border:1px solid #55caff;

    background:rgba(40,180,255,0.12);

    pointer-events:none;
}


/* ================================
   도움말
================================ */

#help {

    position:absolute;

    bottom:18px;

    left:18px;

    z-index:30;

    background:rgba(0,0,0,0.72);

    color:#ddd;

    padding:10px 15px;

    border-radius:6px;

    font-size:13px;

    line-height:1.6;
}

</style>

</head>


<body>

<div id="game"></div>


<div id="topUI">

    <span class="resource">
        💎 미네랄:
        <b id="minerals">500</b>
    </span>

    <span class="resource">
        🟢 가스:
        <b id="gas">0</b>
    </span>

    <span class="resource">
        👨‍🚀 SCV:
        <b id="scvCount">5</b>
    </span>

    <span class="resource">
        📦 생산대기:
        <b id="queue">0</b>/5
    </span>

    <div id="message">
        SCV를 좌클릭해서 선택하세요.
    </div>

</div>


<div id="commandUI">

    <div id="selectedTitle">
        선택된 유닛
    </div>

    <button id="trainSCV">
        👨‍🚀 SCV 생산
        <br>
        💎 미네랄 50 / ⏱️ 10초
    </button>

    <button id="buildGas">
        🟢 가스 채취 시설 건설
        <br>
        ⏱️ 건설시간 15초
    </button>

    <div id="progressArea">

        생산/건설 진행 중

        <div id="progress">
            <div id="progressBar"></div>
        </div>

    </div>

</div>


<div id="selectionBox"></div>


<div id="help">

<b>조작법</b><br>
좌클릭 : 유닛/건물 선택<br>
드래그 : 여러 SCV 선택<br>
우클릭 : 이동 / 자원 채취 명령<br>
SCV 선택 → 가스 지역 클릭 : 가스 시설 건설<br>
사령부 클릭 → SCV 생산

</div>


<script type="importmap">
{
    "imports": {
        "three":
        "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",

        "three/addons/":
        "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
    }
}
</script>


<script type="module">

import * as THREE from "three";

import {
    OrbitControls
}
from
"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/controls/OrbitControls.js";


// =========================================================
// GAME DATA
// =========================================================

let mineralsCount = 500;

let gasCount = 0;

let selectedUnits = [];

let scvs = [];

let minerals = [];

let gasFacility = null;

let gasGeyser = null;

let commandCenter = null;

let scvQueue = 0;

let producingSCV = false;

let buildingGas = false;


// =========================================================
// SCENE
// =========================================================

const scene = new THREE.Scene();

scene.background =
    new THREE.Color(0x101820);

scene.fog =
    new THREE.Fog(
        0x101820,
        100,
        400
    );


// =========================================================
// CAMERA
// =========================================================

const camera =
    new THREE.PerspectiveCamera(
        55,
        window.innerWidth /
        window.innerHeight,
        0.1,
        800
    );

camera.position.set(
    100,
    110,
    110
);


// =========================================================
// RENDERER
// =========================================================

const renderer =
    new THREE.WebGLRenderer({
        antialias:true
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

renderer.shadowMap.enabled = true;

renderer.shadowMap.type =
    THREE.PCFSoftShadowMap;

document
    .getElementById("game")
    .appendChild(renderer.domElement);


// =========================================================
// CAMERA CONTROLS
// =========================================================

const controls =
    new OrbitControls(
        camera,
        renderer.domElement
    );

controls.enableDamping = true;

controls.target.set(
    0,
    0,
    20
);

controls.maxPolarAngle =
    Math.PI / 2.05;

controls.minDistance = 20;

controls.maxDistance = 280;


// =========================================================
// LIGHT
// =========================================================

scene.add(
    new THREE.HemisphereLight(
        0x9fc8ff,
        0x202020,
        2.2
    )
);


const sun =
    new THREE.DirectionalLight(
        0xffffff,
        3
    );

sun.position.set(
    100,
    160,
    70
);

sun.castShadow = true;

sun.shadow.mapSize.width = 2048;
sun.shadow.mapSize.height = 2048;

scene.add(sun);


// =========================================================
// GROUND
// =========================================================

const ground =
    new THREE.Mesh(
        new THREE.PlaneGeometry(
            320,
            320,
            100,
            100
        ),
        new THREE.MeshStandardMaterial({
            color:0x26382e,
            roughness:0.95
        })
    );

ground.rotation.x =
    -Math.PI / 2;

ground.receiveShadow = true;

ground.userData.type =
    "ground";

scene.add(ground);


// =========================================================
// ROCKS
// =========================================================

for(let i=0;i<180;i++){

    const size =
        Math.random()*4+1;

    const rock =
        new THREE.Mesh(
            new THREE.DodecahedronGeometry(
                size
            ),
            new THREE.MeshStandardMaterial({
                color:0x38423e
            })
        );

    rock.position.set(
        Math.random()*280-140,
        size/2,
        Math.random()*280-140
    );

    rock.rotation.y =
        Math.random()*Math.PI;

    rock.castShadow = true;

    scene.add(rock);
}


// =========================================================
// COMMAND CENTER
// =========================================================

function createCommandCenter(){

    const group =
        new THREE.Group();


    // 하부
    const bottom =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                22,
                5,
                18
            ),
            new THREE.MeshStandardMaterial({
                color:0x4f5a62,
                metalness:0.75,
                roughness:0.3
            })
        );

    bottom.position.y=2.5;

    bottom.castShadow=true;

    group.add(bottom);


    // 중앙 건물
    const center =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                12,
                12,
                11
            ),
            new THREE.MeshStandardMaterial({
                color:0x747e85,
                metalness:0.7,
                roughness:0.3
            })
        );

    center.position.y=10;

    center.castShadow=true;

    group.add(center);


    // 앞쪽 출입구
    const entrance =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                6,
                4,
                1
            ),
            new THREE.MeshStandardMaterial({
                color:0x151b1f,
                metalness:0.5
            })
        );

    entrance.position.set(
        0,
        3,
        -6
    );

    group.add(entrance);


    // 좌우 엔진
    for(
        let x of [-8,8]
    ){

        const engine =
            new THREE.Mesh(
                new THREE.CylinderGeometry(
                    3,
                    3,
                    5,
                    16
                ),
                new THREE.MeshStandardMaterial({
                    color:0x343c41,
                    metalness:0.8
                })
            );

        engine.position.set(
            x,
            2.5,
            3
        );

        engine.castShadow=true;

        group.add(engine);


        const engineLight =
            new THREE.PointLight(
                0x168cff,
                3,
                12
            );

        engineLight.position.set(
            x,
            4,
            0
        );

        group.add(engineLight);
    }


    // 상부 지붕
    const roof =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                8,
                8,
                2,
                8
            ),
            new THREE.MeshStandardMaterial({
                color:0x606b72,
                metalness:0.8
            })
        );

    roof.position.y=17;

    roof.rotation.y =
        Math.PI/8;

    group.add(roof);


    // 중앙 푸른 에너지
    const energy =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                2.3,
                2.3,
                4,
                16
            ),
            new THREE.MeshStandardMaterial({
                color:0x159fff,
                emissive:0x0088ff,
                emissiveIntensity:3
            })
        );

    energy.position.y=20;

    group.add(energy);


    // 안테나
    const antenna =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                0.35,
                0.35,
                12
            ),
            new THREE.MeshStandardMaterial({
                color:0x202020
            })
        );

    antenna.position.y=25;

    group.add(antenna);


    // 안테나 빛
    const antennaLight =
        new THREE.PointLight(
            0x00aaff,
            5,
            25
        );

    antennaLight.position.y=30;

    group.add(antennaLight);


    group.position.set(
        0,
        0,
        35
    );

    group.userData.type =
        "command";


    scene.add(group);

    commandCenter=group;
}

createCommandCenter();


// =========================================================
// MINERALS
// =========================================================

const mineralPositions = [

    [-65,0,-60],
    [-55,0,-65],
    [-45,0,-68],
    [-35,0,-65],

    [55,0,-65],
    [65,0,-60],
    [75,0,-52],
    [82,0,-43],

    [-100,0,0],
    [-92,0,10],
    [-84,0,20],
    [-76,0,28],

    [75,0,0],
    [85,0,10],
    [95,0,20],
    [102,0,30],

    [-75,0,85],
    [-65,0,95],
    [-52,0,100],

    [65,0,85],
    [78,0,92],
    [90,0,85]

];


function createMineral(x,y,z){

    const group =
        new THREE.Group();


    const crystal =
        new THREE.Mesh(
            new THREE.OctahedronGeometry(
                3,
                0
            ),
            new THREE.MeshStandardMaterial({
                color:0x10c5ff,
                emissive:0x007799,
                emissiveIntensity:2,
                metalness:0.7,
                roughness:0.15
            })
        );

    crystal.scale.y=1.7;

    crystal.castShadow=true;

    group.add(crystal);


    for(let i=0;i<4;i++){

        const small =
            new THREE.Mesh(
                new THREE.OctahedronGeometry(
                    1.2
                ),
                new THREE.MeshStandardMaterial({
                    color:0x69eaff,
                    emissive:0x0088aa,
                    emissiveIntensity:1.5
                })
            );

        small.position.set(
            Math.random()*5-2.5,
            Math.random()*2,
            Math.random()*5-2.5
        );

        group.add(small);
    }


    group.position.set(
        x,
        3,
        z
    );

    group.userData.type =
        "mineral";

    group.userData.amount =
        999999;

    scene.add(group);

    minerals.push(group);
}


mineralPositions.forEach(
    p =>
        createMineral(
            p[0],
            p[1],
            p[2]
        )
);


// =========================================================
// GAS GEYSER
// =========================================================

function createGasGeyser(){

    const group =
        new THREE.Group();


    const base =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                7,
                8,
                2,
                24
            ),
            new THREE.MeshStandardMaterial({
                color:0x303a35
            })
        );

    base.position.y=1;

    group.add(base);


    const gas =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                4,
                4.5,
                3,
                24
            ),
            new THREE.MeshStandardMaterial({
                color:0x22e866,
                emissive:0x00aa44,
                emissiveIntensity:2
            })
        );

    gas.position.y=3;

    group.add(gas);


    group.position.set(
        30,
        0,
        55
    );

    group.userData.type =
        "geyser";

    scene.add(group);

    gasGeyser=group;
}

createGasGeyser();


// =========================================================
// GAS FACILITY
// =========================================================

function createGasFacility(){

    if(gasFacility)
        return;


    const group =
        new THREE.Group();


    const body =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                6,
                6,
                8,
                20
            ),
            new THREE.MeshStandardMaterial({
                color:0x647078,
                metalness:0.75,
                roughness:0.3
            })
        );

    body.position.y=4;

    body.castShadow=true;

    group.add(body);


    const top =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                3,
                4,
                3,
                20
            ),
            new THREE.MeshStandardMaterial({
                color:0x31e86b,
                emissive:0x00aa44,
                emissiveIntensity:2
            })
        );

    top.position.y=9;

    group.add(top);


    const pipe =
        new THREE.Mesh(
            new THREE.TorusGeometry(
                4,
                0.35,
                8,
                32
            ),
            new THREE.MeshStandardMaterial({
                color:0x30373a,
                metalness:0.8
            })
        );

    pipe.rotation.x =
        Math.PI/2;

    pipe.position.y=6;

    group.add(pipe);


    group.position.copy(
        gasGeyser.position
    );

    group.userData.type =
        "gasFacility";

    scene.add(group);

    gasFacility=group;


    message(
        "🟢 가스 채취 시설 완성!"
    );
}


// =========================================================
// SCV
// =========================================================

function createSCV(index){

    const scv =
        new THREE.Group();


    // 몸체
    const body =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                3.2,
                1.6,
                3.8
            ),
            new THREE.MeshStandardMaterial({
                color:0xbfc1bb,
                metalness:0.65,
                roughness:0.35
            })
        );

    body.position.y=1.4;

    body.castShadow=true;

    scv.add(body);


    // 전면
    const front =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                2.7,
                1.2,
                1.3
            ),
            new THREE.MeshStandardMaterial({
                color:0xd8dad3,
                metalness:0.5
            })
        );

    front.position.set(
        0,
        1.5,
        -2
    );

    scv.add(front);


    // 바퀴
    for(
        let side of [-1,1]
    ){

        const wheel =
            new THREE.Mesh(
                new THREE.CylinderGeometry(
                    0.85,
                    0.85,
                    0.7,
                    12
                ),
                new THREE.MeshStandardMaterial({
                    color:0x141414
                })
            );

        wheel.rotation.z =
            Math.PI/2;

        wheel.position.set(
            side*1.6,
            0.8,
            0
        );

        scv.add(wheel);
    }


    // 파란 램프
    const lamp =
        new THREE.Mesh(
            new THREE.SphereGeometry(
                0.3,
                12,
                12
            ),
            new THREE.MeshStandardMaterial({
                color:0x00aaff,
                emissive:0x0088ff,
                emissiveIntensity:3
            })
        );

    lamp.position.set(
        0,
        2.5,
        -0.8
    );

    scv.add(lamp);


    // 생성 위치
    scv.position.set(
        -8 + index*4,
        0,
        55
    );


    scv.userData.type =
        "scv";

    scv.userData.id =
        index;

    scv.userData.state =
        "idle";

    scv.userData.target =
        null;

    scv.userData.resource =
        null;

    scv.userData.carrying =
        false;

    scene.add(scv);

    scvs.push(scv);

    updateSCVCount();

    return scv;
}


for(let i=0;i<5;i++){

    createSCV(i);

}


// =========================================================
// UI
// =========================================================

function updateResources(){

    document
        .getElementById("minerals")
        .innerText =
        Math.floor(mineralsCount);

    document
        .getElementById("gas")
        .innerText =
        Math.floor(gasCount);
}


function updateSCVCount(){

    document
        .getElementById("scvCount")
        .innerText =
        scvs.length;
}


function updateQueue(){

    document
        .getElementById("queue")
        .innerText =
        scvQueue;
}


function message(text){

    document
        .getElementById("message")
        .innerText =
        text;
}


// =========================================================
// SELECTION
// =========================================================

function clearSelection(){

    selectedUnits.forEach(
        unit=>{

            unit.userData.selected =
                false;

            removeSelectionRing(unit);
        }
    );

    selectedUnits=[];
}


function addSelection(unit){

    if(
        selectedUnits.includes(unit)
    )
        return;


    selectedUnits.push(unit);

    unit.userData.selected=true;

    addSelectionRing(unit);
}


function addSelectionRing(unit){

    if(unit.userData.ring)
        return;


    const ring =
        new THREE.Mesh(
            new THREE.RingGeometry(
                2.5,
                2.8,
                32
            ),
            new THREE.MeshBasicMaterial({
                color:0x20bfff,
                side:THREE.DoubleSide
            })
        );

    ring.rotation.x =
        -Math.PI/2;

    ring.position.y=0.08;

    unit.add(ring);

    unit.userData.ring=ring;
}


function removeSelectionRing(unit){

    if(
        unit.userData.ring
    ){

        unit.remove(
            unit.userData.ring
        );

        unit.userData.ring=null;
    }
}


function showSCVUI(){

    document
        .getElementById("commandUI")
        .style.display="block";

    document
        .getElementById("selectedTitle")
        .innerText =
        "👨‍🚀 SCV " +
        selectedUnits.length +
        "기 선택";

}


function showCommandUI(){

    document
        .getElementById("commandUI")
        .style.display="block";

    document
        .getElementById("selectedTitle")
        .innerText =
        "🏢 테란 사령부";
}


// =========================================================
// SCV 이동
// =========================================================

function moveUnitTo(
    unit,
    targetPosition
){

    unit.userData.state =
        "moving";

    unit.userData.moveTarget =
        targetPosition.clone();

    unit.userData.target=null;

    unit.userData.resource=null;
}


// =========================================================
// RESOURCE JOB
// =========================================================

function giveResourceCommand(
    unit,
    resourceObject
){

    unit.userData.resource =
        resourceObject;

    unit.userData.state =
        "movingResource";

    unit.userData.target =
        resourceObject;

    unit.userData.carrying=false;
}


// =========================================================
// SCV 선택 후 미네랄
// =========================================================

function orderSelectedMineral(
    mineral
){

    if(
        selectedUnits.length===0
    ){

        message(
            "먼저 SCV를 선택하세요."
        );

        return;
    }


    selectedUnits.forEach(
        unit=>{

            if(
                unit.userData.type==="scv"
            ){

                giveResourceCommand(
                    unit,
                    mineral
                );

            }

        }
    );


    message(
        "⛏️ SCV가 미네랄을 채취하러 갑니다."
    );
}


// =========================================================
// GAS ORDER
// =========================================================

function orderGas(){

    if(
        selectedUnits.length===0
    ){

        message(
            "먼저 SCV를 선택하세요."
        );

        return;
    }


    if(!gasFacility){

        message(
            "🟢 가스 채취 시설이 아직 없습니다."
        );

        return;
    }


    selectedUnits.forEach(
        unit=>{

            if(
                unit.userData.type==="scv"
            ){

                giveResourceCommand(
                    unit,
                    gasFacility
                );

            }

        }
    );


    message(
        "🟢 SCV가 가스를 채취하러 갑니다."
    );
}


// =========================================================
// BUILD GAS
// =========================================================

document
    .getElementById("buildGas")
    .onclick=function(){

        if(
            selectedUnits.length===0
        ){

            message(
                "SCV를 선택하세요."
            );

            return;
        }


        if(gasFacility){

            message(
                "이미 가스 시설이 있습니다."
            );

            return;
        }


        if(buildingGas){

            message(
                "이미 가스 시설을 건설 중입니다."
            );

            return;
        }


        buildingGas=true;


        const builder =
            selectedUnits[0];

        builder.userData.state =
            "buildingGas";

        builder.userData.target =
            gasGeyser;


        message(
            "🏗️ SCV가 가스 시설을 건설하러 이동합니다."
        );
    };


// =========================================================
// SCV PRODUCTION
// =========================================================

document
    .getElementById("trainSCV")
    .onclick=function(){

        if(
            scvQueue>=5
        ){

            message(
                "❌ SCV 생산 대기열이 가득 찼습니다. 최대 5기입니다."
            );

            return;
        }


        if(
            mineralsCount<50
        ){

            message(
                "❌ 미네랄이 부족합니다."
            );

            return;
        }


        mineralsCount-=50;

        scvQueue++;

        updateResources();

        updateQueue();

        message(
            "👨‍🚀 SCV가 생산 대기열에 추가되었습니다."
        );


        if(!producingSCV){

            produceNextSCV();

        }
    };


// =========================================================
// PRODUCE SCV
// =========================================================

function produceNextSCV(){

    if(
        scvQueue<=0
    ){

        producingSCV=false;

        return;
    }


    producingSCV=true;

    scvQueue--;

    updateQueue();


    document
        .getElementById("progressArea")
        .style.display="block";


    const start =
        Date.now();

    const duration =
        10000;


    const timer =
        setInterval(()=>{

            const elapsed =
                Date.now()-start;

            const percent =
                Math.min(
                    100,
                    elapsed/duration*100
                );


            document
                .getElementById(
                    "progressBar"
                )
                .style.width =
                percent+"%";


            if(percent>=100){

                clearInterval(timer);


                const newSCV =
                    createSCV(
                        scvs.length
                    );


                // 사령부 옆에서 생성
                newSCV.position.set(
                    15 +
                    (scvs.length%3)*4,
                    0,
                    50 +
                    Math.floor(
                        scvs.length/3
                    )*4
                );


                message(
                    "👨‍🚀 SCV 생산 완료!"
                );


                if(
                    scvQueue>0
                ){

                    produceNextSCV();

                }
                else{

                    producingSCV=false;

                    document
                        .getElementById(
                            "progressArea"
                        )
                        .style.display="none";

                    document
                        .getElementById(
                            "progressBar"
                        )
                        .style.width="0%";
                }

            }

        },100);
}


// =========================================================
// RAYCAST
// =========================================================

const raycaster =
    new THREE.Raycaster();

const mouse =
    new THREE.Vector2();


function getObjectFromClick(
    event
){

    mouse.x =
        event.clientX /
        window.innerWidth *
        2-1;

    mouse.y =
        -(event.clientY /
        window.innerHeight) *
        2+1;


    raycaster.setFromCamera(
        mouse,
        camera
    );


    const objects=[];

    scene.traverse(
        object=>{

            if(
                object.isMesh
            ){

                objects.push(object);

            }

        }
    );


    const hits =
        raycaster.intersectObjects(
            objects,
            true
        );


    if(
        hits.length===0
    )
        return null;


    let object =
        hits[0].object;


    while(
        object.parent &&
        object.parent!==scene
    ){

        if(
            object.userData.type
        )
            break;

        object=object.parent;
    }


    return object;
}


// =========================================================
// LEFT CLICK
// =========================================================

renderer.domElement.addEventListener(
    "click",
    function(event){

        // 드래그였으면 무시
        if(isDragging)
            return;


        const object =
            getObjectFromClick(event);


        if(!object)
            return;


        // SCV
        if(
            object.userData.type==="scv"
        ){

            clearSelection();

            addSelection(object);

            showSCVUI();

            message(
                "SCV 선택됨. 우클릭으로 이동하세요."
            );

            return;
        }


        // COMMAND CENTER
        if(
            object.userData.type==="command"
        ){

            clearSelection();

            showCommandUI();

            message(
                "🏢 사령부 선택됨. SCV 생산을 선택하세요."
            );

            return;
        }


        // MINERAL
        if(
            object.userData.type==="mineral"
        ){

            if(
                selectedUnits.length>0
            ){

                orderSelectedMineral(
                    object
                );

            }

            return;
        }


        // GAS FACILITY
        if(
            object.userData.type==="gasFacility"
        ){

            if(
                selectedUnits.length>0
            ){

                orderGas();

            }

            return;
        }


        // GAS GEYSER
        if(
            object.userData.type==="geyser"
        ){

            if(
                selectedUnits.length>0
            ){

                document
                    .getElementById(
                        "buildGas"
                    )
                    .click();

            }

            return;
        }

    }
);


// =========================================================
// RIGHT CLICK
// =========================================================

renderer.domElement.addEventListener(
    "contextmenu",
    function(event){

        event.preventDefault();


        if(
            selectedUnits.length===0
        )
            return;


        const object =
            getObjectFromClick(event);


        if(
            object &&
            object.userData.type==="mineral"
        ){

            orderSelectedMineral(
                object
            );

            return;
        }


        if(
            object &&
            object.userData.type==="gasFacility"
        ){

            orderGas();

            return;
        }


        // 땅 좌표 계산
        mouse.x =
            event.clientX /
            window.innerWidth *
            2-1;

        mouse.y =
            -(event.clientY /
            window.innerHeight) *
            2+1;


        raycaster.setFromCamera(
            mouse,
            camera
        );


        const groundHit =
            raycaster.intersectObject(
                ground
            );


        if(
            groundHit.length>0
        ){

            const point =
                groundHit[0].point;


            selectedUnits.forEach(
                (unit,index)=>{

                    if(
                        unit.userData.type==="scv"
                    ){

                        // 여러 유닛을 살짝 흩어지게 이동
                        const offset =
                            new THREE.Vector3(
                                (index%3-1)*4,
                                0,
                                Math.floor(index/3)*4
                            );

                        moveUnitTo(
                            unit,
                            point.clone()
                            .add(offset)
                        );

                    }

                }
            );


            message(
                "🚩 선택된 SCV가 지정 위치로 이동합니다."
            );
        }

    }
);


// =========================================================
// DRAG SELECTION
// =========================================================

let isDragging=false;

let dragStartX=0;
let dragStartY=0;

const selectionBox =
    document.getElementById(
        "selectionBox"
    );


renderer.domElement.addEventListener(
    "mousedown",
    function(event){

        if(event.button!==0)
            return;


        isDragging=true;

        dragStartX=
            event.clientX;

        dragStartY=
            event.clientY;


        selectionBox.style.left =
            dragStartX+"px";

        selectionBox.style.top =
            dragStartY+"px";

        selectionBox.style.width="0px";

        selectionBox.style.height="0px";

        selectionBox.style.display=
            "block";

    }
);


window.addEventListener(
    "mousemove",
    function(event){

        if(!isDragging)
            return;


        const x =
            Math.min(
                dragStartX,
                event.clientX
            );

        const y =
            Math.min(
                dragStartY,
                event.clientY
            );

        const width =
            Math.abs(
                event.clientX -
                dragStartX
            );

        const height =
            Math.abs(
                event.clientY -
                dragStartY
            );


        selectionBox.style.left =
            x+"px";

        selectionBox.style.top =
            y+"px";

        selectionBox.style.width =
            width+"px";

        selectionBox.style.height =
            height+"px";

    }
);


window.addEventListener(
    "mouseup",
    function(event){

        if(!isDragging)
            return;


        isDragging=false;

        selectionBox.style.display=
            "none";


        const endX =
            event.clientX;

        const endY =
            event.clientY;


        // 짧은 클릭은 일반 클릭 처리
        if(
            Math.abs(
                endX-dragStartX
            )<8 &&
            Math.abs(
                endY-dragStartY
            )<8
        ){

            return;
        }


        clearSelection();


        const minX =
            Math.min(
                dragStartX,
                endX
            );

        const maxX =
            Math.max(
                dragStartX,
                endX
            );

        const minY =
            Math.min(
                dragStartY,
                endY
            );

        const maxY =
            Math.max(
                dragStartY,
                endY
            );


        scvs.forEach(
            scv=>{

                const pos =
                    scv.position.clone();

                pos.project(camera);


                const screenX =
                    (pos.x+1)/2 *
                    window.innerWidth;

                const screenY =
                    (-pos.y+1)/2 *
                    window.innerHeight;


                if(
                    screenX>=minX &&
                    screenX<=maxX &&
                    screenY>=minY &&
                    screenY<=maxY
                ){

                    addSelection(scv);

                }

            }
        );


        if(
            selectedUnits.length>0
        ){

            showSCVUI();

            message(
                "👨‍🚀 SCV "+
                selectedUnits.length+
                "기 선택됨."
            );

        }

    }
);


// =========================================================
// MOVEMENT
// =========================================================

function moveUnit(
    unit,
    target,
    speed,
    delta
){

    const direction =
        new THREE.Vector3()
        .subVectors(
            target,
            unit.position
        );

    direction.y=0;


    const distance =
        direction.length();


    if(distance<1.5)
        return true;


    direction.normalize();


    unit.position.add(
        direction.multiplyScalar(
            speed*delta
        )
    );


    unit.rotation.y =
        Math.atan2(
            direction.x,
            direction.z
        );


    return false;
}


// =========================================================
// MINING
// =========================================================

function startMining(
    scv,
    type
){

    scv.userData.state =
        type==="mineral"
        ? "miningMineral"
        : "miningGas";


    scv.userData.miningStart =
        Date.now();


    scv.userData.miningDuration =
        3000;


    message(
        type==="mineral"
        ? "⛏️ 미네랄 채취 중... 3초"
        : "🟢 가스 채취 중... 3초"
    );
}


// =========================================================
// UPDATE SCV
// =========================================================

let lastTime =
    performance.now();


function updateSCVs(){

    const now =
        performance.now();

    const delta =
        (now-lastTime)/1000;

    lastTime=now;


    scvs.forEach(
        scv=>{

            const state =
                scv.userData.state;

            const target =
                scv.userData.target;


            // =========================================
            // 일반 이동
            // =========================================

            if(
                state==="moving"
            ){

                if(
                    moveUnit(
                        scv,
                        scv.userData.moveTarget,
                        14,
                        delta
                    )
                ){

                    scv.userData.state=
                        "idle";

                }

            }


            // =========================================
            // 미네랄 이동
            // =========================================

            if(
                state==="movingResource" &&
                target
            ){

                if(
                    moveUnit(
                        scv,
                        target.position,
                        13,
                        delta
                    )
                ){

                    startMining(
                        scv,
                        "mineral"
                    );

                }

            }


            // =========================================
            // 미네랄 채취
            // =========================================

            if(
                state==="miningMineral"
            ){

                const elapsed =
                    Date.now() -
                    scv.userData.miningStart;


                if(
                    elapsed>=3000
                ){

                    scv.userData.state =
                        "returnMineral";

                    scv.userData.target =
                        commandCenter;

                    scv.userData.carrying =
                        true;


                    message(
                        "📦 미네랄 채취 완료! 사령부로 돌아갑니다."
                    );
                }

            }


            // =========================================
            // 미네랄 귀환
            // =========================================

            if(
                state==="returnMineral"
            ){

                if(
                    moveUnit(
                        scv,
                        commandCenter.position,
                        15,
                        delta
                    )
                ){

                    mineralsCount+=10;

                    updateResources();


                    scv.userData.carrying=
                        false;


                    // 무한 반복
                    scv.userData.state =
                        "movingResource";


                    // 원래 광물 유지
                    // target은 resource를 다시 지정
                    if(
                        scv.userData.resource
                    ){

                        scv.userData.target =
                            scv.userData.resource;

                    }


                    message(
                        "🏢 미네랄 전달 완료! +10"
                    );

                }

            }


            // =========================================
            // 가스 이동
            // =========================================

            if(
                state==="movingGas"
            ){

                if(
                    target &&
                    moveUnit(
                        scv,
                        target.position,
                        13,
                        delta
                    )
                ){

                    startMining(
                        scv,
                        "gas"
                    );

                }

            }


            // =========================================
            // 가스 채취
            // =========================================

            if(
                state==="miningGas"
            ){

                const elapsed =
                    Date.now() -
                    scv.userData.miningStart;


                if(
                    elapsed>=3000
                ){

                    scv.userData.state =
                        "returnGas";

                    scv.userData.target =
                        commandCenter;

                    scv.userData.carrying =
                        true;


                    message(
                        "🟢 가스 채취 완료! 사령부로 돌아갑니다."
                    );

                }

            }


            // =========================================
            // 가스 귀환
            // =========================================

            if(
                state==="returnGas"
            ){

                if(
                    moveUnit(
                        scv,
                        commandCenter.position,
                        15,
                        delta
                    )
                ){

                    gasCount+=10;

                    updateResources();


                    scv.userData.carrying=
                        false;


                    // 무한 반복
                    scv.userData.state =
                        "movingGas";


                    scv.userData.target =
                        scv.userData.resource;


                    message(
                        "🏢 가스 전달 완료! +10"
                    );

                }

            }


            // =========================================
            // 가스 시설 건설
            // =========================================

            if(
                state==="buildingGas"
            ){

                if(
                    moveUnit(
                        scv,
                        gasGeyser.position,
                        11,
                        delta
                    )
                ){

                    if(
                        !scv.userData.buildStart
                    ){

                        scv.userData.buildStart =
                            Date.now();

                        message(
                            "🏗️ 가스 시설 건설 중... 15초"
                        );

                    }


                    const elapsed =
                        Date.now() -
                        scv.userData.buildStart;


                    if(
                        elapsed>=15000
                    ){

                        createGasFacility();

                        buildingGas=false;

                        scv.userData.state =
                            "idle";

                        scv.userData.target =
                            null;

                        scv.userData.buildStart =
                            null;

                    }

                }

            }

        }
    );
}


// =========================================================
// ANIMATION
// =========================================================

function animate(){

    requestAnimationFrame(
        animate
    );


    updateSCVs();


    // 광물 회전
    minerals.forEach(
        (mineral,index)=>{

            mineral.rotation.y +=
                0.004;

            mineral.position.y =
                3 +
                Math.sin(
                    Date.now()*0.002+
                    index
                )*0.25;

        }
    );


    // 가스 애니메이션
    if(gasGeyser){

        gasGeyser.children.forEach(
            child=>{

                if(
                    child.material &&
                    child.material.emissive
                ){

                    child.material.emissiveIntensity =
                        1.5+
                        Math.sin(
                            Date.now()*0.004
                        );
                }

            }
        );

    }


    controls.update();

    renderer.render(
        scene,
        camera
    );
}


animate();


// =========================================================
// RESIZE
// =========================================================

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

updateQueue();

</script>

</body>
</html>
"""


components.html(
    html,
    height=900,
    scrolling=False
)
