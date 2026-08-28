import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Terran RTS",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

html = r"""
<!DOCTYPE html>
<html>
<head>

<meta charset="UTF-8">

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

<style>

*{
    box-sizing:border-box;
}

html,body{
    margin:0;
    padding:0;
    overflow:hidden;
    width:100%;
    height:100%;
    background:#05070a;
    font-family:Arial,sans-serif;
    user-select:none;
}

#game{
    position:fixed;
    inset:0;
}

canvas{
    display:block;
}

#raceScreen{

    position:fixed;
    inset:0;

    background:
        radial-gradient(
            circle at center,
            #182536 0%,
            #05070a 70%
        );

    display:flex;
    justify-content:center;
    align-items:center;

    z-index:100;
}

.raceBox{

    width:430px;
    padding:35px;

    text-align:center;

    background:
        linear-gradient(
            145deg,
            rgba(35,45,55,.96),
            rgba(8,12,16,.96)
        );

    border:2px solid #68747c;

    box-shadow:
        0 0 50px rgba(0,0,0,.8),
        inset 0 0 30px rgba(255,255,255,.03);

    border-radius:8px;
}

.raceTitle{

    font-size:42px;
    color:#d9e0e4;
    font-weight:bold;
    letter-spacing:5px;

    margin-bottom:30px;
}

.raceButton{

    width:100%;
    padding:20px;

    background:
        linear-gradient(
            #68757b,
            #30383c
        );

    color:white;

    border:2px solid #9aa6aa;

    font-size:24px;
    font-weight:bold;

    cursor:pointer;

    border-radius:5px;
}

.raceButton:hover{

    background:
        linear-gradient(
            #8b999e,
            #404a4e
        );

    box-shadow:
        0 0 20px rgba(180,220,255,.4);
}

#topUI{

    position:fixed;

    top:10px;
    left:50%;

    transform:translateX(-50%);

    z-index:20;

    display:flex;
    gap:12px;
}

.resource{

    min-width:130px;

    padding:10px 18px;

    background:
        rgba(10,15,20,.88);

    border:
        1px solid #52616a;

    border-radius:5px;

    color:white;

    font-size:17px;

    text-align:center;

    box-shadow:
        0 0 12px rgba(0,0,0,.5);
}

#sidePanel{

    position:fixed;

    right:12px;
    top:80px;

    width:260px;

    min-height:220px;

    z-index:20;

    background:
        linear-gradient(
            145deg,
            rgba(20,27,31,.96),
            rgba(7,10,13,.96)
        );

    border:1px solid #69757b;

    border-radius:6px;

    padding:15px;

    color:#e8eef0;

    display:none;

    box-shadow:
        0 0 25px rgba(0,0,0,.7);
}

.panelTitle{

    font-size:22px;

    font-weight:bold;

    padding-bottom:10px;

    border-bottom:
        1px solid #455158;

    margin-bottom:12px;
}

.stat{

    padding:6px 0;

    color:#c4cdd1;
}

.actionButton{

    width:100%;

    padding:11px;

    margin-top:7px;

    background:
        linear-gradient(
            #59676d,
            #30383d
        );

    color:white;

    border:1px solid #829096;

    cursor:pointer;

    border-radius:4px;
}

.actionButton:hover{

    background:
        linear-gradient(
            #718087,
            #3d494e
        );
}

.actionButton:disabled{

    opacity:.4;
    cursor:not-allowed;
}

#buildMessage{

    position:fixed;

    left:50%;
    bottom:100px;

    transform:translateX(-50%);

    z-index:30;

    padding:10px 18px;

    background:
        rgba(0,0,0,.75);

    border:
        1px solid #55636a;

    border-radius:5px;

    color:white;

    display:none;

    text-align:center;
}

#miniMap{

    position:fixed;

    left:15px;
    bottom:15px;

    width:230px;
    height:150px;

    z-index:25;

    background:#101820;

    border:
        2px solid #64727a;

    border-radius:5px;

    overflow:hidden;

    box-shadow:
        0 0 20px rgba(0,0,0,.7);

    cursor:pointer;
}

#miniCanvas{

    width:100%;
    height:100%;
}

#selectionBox{

    position:fixed;

    border:
        1px solid #61b8ff;

    background:
        rgba(70,160,255,.12);

    display:none;

    z-index:50;

    pointer-events:none;
}

#help{

    position:fixed;

    left:50%;

    bottom:15px;

    transform:translateX(-50%);

    color:#aeb8bd;

    background:
        rgba(0,0,0,.55);

    padding:8px 15px;

    border-radius:4px;

    font-size:13px;

    z-index:20;
}

</style>
</head>

<body>

<div id="game"></div>

<div id="raceScreen">

    <div class="raceBox">

        <div class="raceTitle">
            TERRAN
        </div>

        <button
            class="raceButton"
            id="startButton"
        >
            테란으로 시작
        </button>

    </div>

</div>

<div id="topUI">

    <div class="resource">
        💎 미네랄
        <span id="minerals">500</span>
    </div>

    <div class="resource">
        🟢 가스
        <span id="gas">0</span>
    </div>

    <div class="resource">
        👷 SCV
        <span id="scvCount">5</span>
    </div>

</div>

<div id="sidePanel">

    <div
        class="panelTitle"
        id="panelTitle"
    >
        상태
    </div>

    <div id="panelContent"></div>

</div>

<div id="buildMessage"></div>

<div id="selectionBox"></div>

<div id="miniMap">

    <canvas
        id="miniCanvas"
        width="230"
        height="150"
    ></canvas>

</div>

<div id="help">

    좌클릭: 선택 / 드래그 선택　|　
    우클릭: 이동　|　
    화면 끝: 카메라 이동　|　
    미니맵 클릭: 위치 이동

</div>


<script>


// ============================================================
// 기본 설정
// ============================================================

const scene =
    new THREE.Scene();

scene.background =
    new THREE.Color(0x070b0e);


const camera =
    new THREE.PerspectiveCamera(
        55,
        window.innerWidth /
        window.innerHeight,
        .1,
        500
    );


camera.position.set(
    0,
    42,
    25
);

camera.lookAt(
    0,
    0,
    0
);


const renderer =
    new THREE.WebGLRenderer({
        antialias:true
    });

renderer.setSize(
    window.innerWidth,
    window.innerHeight
);

renderer.shadowMap.enabled =
    true;

document
    .getElementById("game")
    .appendChild(renderer.domElement);


// ============================================================
// 조명
// ============================================================

const ambient =
    new THREE.AmbientLight(
        0x82909a,
        .7
    );

scene.add(ambient);


const sun =
    new THREE.DirectionalLight(
        0xffffff,
        1.5
    );

sun.position.set(
    15,
    35,
    20
);

sun.castShadow =
    true;

scene.add(sun);


// ============================================================
// 상태
// ============================================================

let gameStarted = false;

let minerals = 500;
let gas = 0;

let selectedUnits = [];

let selectedObject = null;

let buildMode = false;

let buildPreview = null;

let buildPreviewValid = false;

let currentBuildSCV = null;

let scvProductionQueue = 0;

const MAX_SCV_QUEUE = 5;

const SCV_COST = 50;

const SCV_BUILD_TIME = 10;

const GAS_BUILD_TIME = 15;

const MINERAL_TIME = 3;

const SCV_MINERAL_AMOUNT = 50;

const SCV_GAS_AMOUNT = 25;


// ============================================================
// 배열
// ============================================================

const scvs = [];

const mineralsNodes = [];

const geysers = [];

const gasFacilities = [];

const buildings = [];


// ============================================================
// 맵
// ============================================================

const WORLD_SIZE = 90;

const groundGeometry =
    new THREE.PlaneGeometry(
        WORLD_SIZE,
        WORLD_SIZE,
        40,
        40
    );

const groundMaterial =
    new THREE.MeshStandardMaterial({
        color:0x17241b,
        roughness:.95
    });

const ground =
    new THREE.Mesh(
        groundGeometry,
        groundMaterial
    );

ground.rotation.x =
    -Math.PI / 2;

ground.receiveShadow =
    true;

scene.add(ground);


// ============================================================
// 지형 장식
// ============================================================

for(let i=0;i<170;i++){

    const rock =
        new THREE.Mesh(
            new THREE.DodecahedronGeometry(
                .15 +
                Math.random()*.45,
                0
            ),
            new THREE.MeshStandardMaterial({
                color:
                    0x29332f
            })
        );

    rock.position.set(
        (Math.random()-.5)*80,
        .1,
        (Math.random()-.5)*80
    );

    rock.rotation.set(
        Math.random(),
        Math.random(),
        Math.random()
    );

    scene.add(rock);
}


// ============================================================
// 재질
// ============================================================

function material(
    color,
    metal=.2,
    rough=.7
){

    return new THREE.MeshStandardMaterial({
        color:color,
        metalness:metal,
        roughness:rough
    });

}


// ============================================================
// 사령부
// ============================================================

function createCommandCenter(){

    const group =
        new THREE.Group();


    // 본체

    const body =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                8,
                4,
                7
            ),
            material(
                0x555f62,
                .8,
                .35
            )
        );

    body.position.y = 2;

    body.castShadow = true;

    group.add(body);


    // 상부

    const upper =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                5,
                1.5,
                4.5
            ),
            material(
                0x3c4548,
                .8,
                .3
            )
        );

    upper.position.y = 4.6;

    group.add(upper);


    // 지휘실

    const glass =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                3.2,
                1.5,
                3
            ),
            new THREE.MeshStandardMaterial({
                color:0x173747,
                metalness:.5,
                roughness:.15,
                transparent:true,
                opacity:.85
            })
        );

    glass.position.set(
        0,
        5.4,
        0
    );

    group.add(glass);


    // 안테나

    const antenna =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                .12,
                .12,
                4,
                10
            ),
            material(
                0x22282a,
                .8,
                .3
            )
        );

    antenna.position.y = 7.5;

    group.add(antenna);


    const light =
        new THREE.Mesh(
            new THREE.SphereGeometry(
                .25,
                12,
                12
            ),
            new THREE.MeshBasicMaterial({
                color:0x44aaff
            })
        );

    light.position.y = 9.4;

    group.add(light);


    // 양쪽 구조물

    for(let side of [-1,1]){

        const module =
            new THREE.Mesh(
                new THREE.BoxGeometry(
                    1.5,
                    2,
                    5
                ),
                material(
                    0x30383b,
                    .75,
                    .4
                )
            );

        module.position.set(
            side*4.2,
            1.5,
            0
        );

        group.add(module);
    }


    group.position.set(
        0,
        0,
        0
    );


    group.userData = {

        type:"commandCenter",

        hp:1500,
        maxHp:1500

    };


    buildings.push(group);

    scene.add(group);

    return group;
}


const commandCenter =
    createCommandCenter();


// ============================================================
// 미네랄
// ============================================================

const mineralPositions = [

    [-13,-9],
    [-11,-7],
    [-9,-10],
    [-7,-8],
    [-5,-11],

    [-13,-4],
    [-11,-2],
    [-9,-5],
    [-7,-3],
    [-5,-6],

    [-13,1],
    [-11,3],
    [-9,0],
    [-7,2],
    [-5,-1],

    [-12,6],
    [-10,8],
    [-8,5],
    [-6,7],

    [-12,11],
    [-9,12],
    [-6,10]
];


function createMineral(x,z){

    const group =
        new THREE.Group();


    for(let i=0;i<3;i++){

        const crystal =
            new THREE.Mesh(
                new THREE.DodecahedronGeometry(
                    .8 +
                    Math.random()*.5,
                    0
                ),
                new THREE.MeshStandardMaterial({
                    color:0x27a8ff,
                    emissive:0x075080,
                    emissiveIntensity:.5,
                    metalness:.4,
                    roughness:.3
                })
            );

        crystal.position.set(
            (Math.random()-.5)*1.2,
            .7 +
            Math.random()*.5,
            (Math.random()-.5)*1.2
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

        group.add(crystal);
    }


    group.position.set(
        x,
        0,
        z
    );


    group.userData = {

        type:"mineral",

        amount:1500,

        busy:false

    };


    mineralsNodes.push(group);

    scene.add(group);
}


mineralPositions.forEach(
    p =>
        createMineral(
            p[0],
            p[1]
        )
);


// ============================================================
// 가스 채취 장소
// ============================================================

function createGeyser(x,z){

    const group =
        new THREE.Group();


    const base =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                2.7,
                3,
                .5,
                20
            ),
            material(
                0x343b37,
                .4,
                .9
            )
        );

    base.position.y =
        .25;

    group.add(base);


    const gas =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                1.8,
                2.2,
                1.3,
                20
            ),
            new THREE.MeshStandardMaterial({
                color:0x21bd6a,
                emissive:0x0d6f3c,
                emissiveIntensity:1,
                transparent:true,
                opacity:.7
            })
        );

    gas.position.y =
        .9;

    group.add(gas);


    group.position.set(
        x,
        0,
        z
    );


    group.userData = {

        type:"geyser",

        gasMesh:gas,

        hasFacility:false

    };


    geysers.push(group);

    scene.add(group);
}


createGeyser(
    14,
    7
);


// ============================================================
// SCV
// ============================================================

function createSCV(x,z){

    const group =
        new THREE.Group();


    // 몸체

    const body =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                1.7,
                .8,
                2
            ),
            material(
                0xc0a73e,
                .65,
                .4
            )
        );

    body.position.y =
        .8;

    body.castShadow =
        true;

    group.add(body);


    // 운전석

    const cabin =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                1.2,
                .7,
                1
            ),
            material(
                0x59656a,
                .7,
                .3
            )
        );

    cabin.position.set(
        0,
        1.4,
        -.2
    );

    group.add(cabin);


    // 앞쪽 작업 장치

    const arm =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                1.8,
                .25,
                .5
            ),
            material(
                0x8b772d,
                .7,
                .4
            )
        );

    arm.position.set(
        0,
        .75,
        -1.25
    );

    group.add(arm);


    // 바퀴

    for(let side of [-1,1]){

        for(let zpos of [-.7,.7]){

            const wheel =
                new THREE.Mesh(
                    new THREE.CylinderGeometry(
                        .4,
                        .4,
                        .35,
                        12
                    ),
                    material(
                        0x16191a,
                        .8,
                        .8
                    )
                );

            wheel.rotation.z =
                Math.PI/2;

            wheel.position.set(
                side*.95,
                .4,
                zpos
            );

            group.add(wheel);
        }
    }


    group.position.set(
        x,
        0,
        z
    );


    group.userData = {

        type:"scv",

        hp:50,

        maxHp:50,

        state:"idle",

        target:null,

        carrying:0,

        carryingGas:0,

        buildTarget:null,

        selected:false,

        speed:7

    };


    scvs.push(group);

    scene.add(group);

    return group;
}


// 초기 SCV 5개

for(let i=0;i<5;i++){

    createSCV(
        5 + i*1.7,
        5
    );
}


// ============================================================
// 가스 시설
// ============================================================

function createGasFacility(
    geyser
){

    const group =
        new THREE.Group();


    const platform =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                3.2,
                3.5,
                .7,
                24
            ),
            material(
                0x30383a,
                .8,
                .35
            )
        );

    platform.position.y =
        .35;

    group.add(platform);


    const ring =
        new THREE.Mesh(
            new THREE.TorusGeometry(
                2.5,
                .25,
                10,
                32
            ),
            material(
                0x737b7d,
                .8,
                .3
            )
        );

    ring.rotation.x =
        Math.PI/2;

    ring.position.y =
        .85;

    group.add(ring);


    const tank =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                1.55,
                1.85,
                3.8,
                20
            ),
            material(
                0x4b5558,
                .8,
                .35
            )
        );

    tank.position.y =
        2.7;

    group.add(tank);


    const top =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                1.15,
                1.15,
                .45,
                20
            ),
            material(
                0x272d2f,
                .8,
                .3
            )
        );

    top.position.y =
        4.75;

    group.add(top);


    const core =
        new THREE.Mesh(
            new THREE.SphereGeometry(
                .85,
                20,
                20
            ),
            new THREE.MeshStandardMaterial({
                color:0x35ff91,
                emissive:0x12b95e,
                emissiveIntensity:2.2,
                transparent:true,
                opacity:.9
            })
        );

    core.position.y =
        5.15;

    group.add(core);


    // 파이프

    for(let i=0;i<4;i++){

        const angle =
            i/4*Math.PI*2;

        const pipe =
            new THREE.Mesh(
                new THREE.CylinderGeometry(
                    .16,
                    .16,
                    3.2,
                    10
                ),
                material(
                    0x252b2d,
                    .8,
                    .3
                )
            );

        pipe.position.set(
            Math.cos(angle)*2,
            1.9,
            Math.sin(angle)*2
        );

        group.add(pipe);
    }


    // 경고등

    for(let i=0;i<4;i++){

        const angle =
            i/4*Math.PI*2;

        const light =
            new THREE.Mesh(
                new THREE.SphereGeometry(
                    .13,
                    10,
                    10
                ),
                new THREE.MeshBasicMaterial({
                    color:0xff4422
                })
            );

        light.position.set(
            Math.cos(angle)*2.45,
            1.1,
            Math.sin(angle)*2.45
        );

        group.add(light);
    }


    // 가스 파티클

    const particleGroup =
        new THREE.Group();


    for(let i=0;i<40;i++){

        const particle =
            new THREE.Mesh(
                new THREE.SphereGeometry(
                    .08 +
                    Math.random()*.12,
                    6,
                    6
                ),
                new THREE.MeshBasicMaterial({
                    color:0x55ff99,
                    transparent:true,
                    opacity:
                        .35 +
                        Math.random()*.35
                })
            );

        particle.position.set(
            (Math.random()-.5)*1.5,
            5.3 +
            Math.random()*4,
            (Math.random()-.5)*1.5
        );

        particle.userData.speed =
            .4 +
            Math.random()*.8;

        particleGroup.add(
            particle
        );
    }

    group.add(
        particleGroup
    );


    group.position.copy(
        geyser.position
    );


    group.userData = {

        type:"gasFacility",

        hp:500,

        maxHp:500,

        gas:2500,

        particleGroup:
            particleGroup,

        core:core

    };


    gasFacilities.push(group);

    scene.add(group);

    return group;
}


// ============================================================
// 건설 미리보기
// ============================================================

function createGasPreview(){

    const group =
        new THREE.Group();


    const previewMaterial =
        new THREE.MeshStandardMaterial({

            color:0x55ff88,

            transparent:true,

            opacity:.3,

            emissive:0x22aa55,

            emissiveIntensity:.6

        });


    const platform =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                3.2,
                3.5,
                .7,
                24
            ),
            previewMaterial
        );

    platform.position.y =
        .35;

    group.add(platform);


    const ring =
        new THREE.Mesh(
            new THREE.TorusGeometry(
                2.5,
                .25,
                10,
                32
            ),
            previewMaterial
        );

    ring.rotation.x =
        Math.PI/2;

    ring.position.y =
        .85;

    group.add(ring);


    const tank =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                1.55,
                1.85,
                3.8,
                20
            ),
            previewMaterial
        );

    tank.position.y =
        2.7;

    group.add(tank);


    const top =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                1.15,
                1.15,
                .45,
                20
            ),
            previewMaterial
        );

    top.position.y =
        4.75;

    group.add(top);


    const core =
        new THREE.Mesh(
            new THREE.SphereGeometry(
                .85,
                20,
                20
            ),
            previewMaterial
        );

    core.position.y =
        5.15;

    group.add(core);


    group.visible =
        false;

    scene.add(group);

    return group;
}


buildPreview =
    createGasPreview();


// ============================================================
// 건설 미리보기 색상
// ============================================================

function setPreviewColor(
    color
){

    buildPreview.traverse(
        object => {

            if(
                object.material
            ){

                object.material.color
                    .setHex(color);

                object.material.emissive
                    .setHex(color);
            }
        }
    );

}


// ============================================================
// 선택
// ============================================================

function clearSelection(){

    selectedUnits
        .forEach(
            unit => {

                unit.userData.selected =
                    false;
            }
        );

    selectedUnits = [];

}


function selectUnit(unit){

    clearSelection();

    unit.userData.selected =
        true;

    selectedUnits.push(
        unit
    );

    selectedObject =
        unit;

    showUnitPanel(
        unit
    );

}


// ============================================================
// 상태창
// ============================================================

function showUnitPanel(
    object
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


    if(
        object.userData.type ===
        "scv"
    ){

        title.innerHTML =
            "👷 SCV";

        content.innerHTML = `

            <div class="stat">
                체력:
                ${object.userData.hp}
                /
                ${object.userData.maxHp}
            </div>

            <div class="stat">
                상태:
                ${object.userData.state}
            </div>

            <button
                class="actionButton"
                onclick="startGasBuild()"
            >
                🏗️ 가스 채취 시설 건설
            </button>

        `;

    }


    else if(
        object.userData.type ===
        "commandCenter"
    ){

        title.innerHTML =
            "🏢 사령부";

        content.innerHTML = `

            <div class="stat">
                체력:
                ${object.userData.hp}
                /
                ${object.userData.maxHp}
            </div>

            <div class="stat">
                SCV 생산
            </div>

            <button
                class="actionButton"
                onclick="produceSCV()"
                id="scvProduceButton"
            >
                👷 SCV 만들기
                <br>
                💎 50
                / 10초
            </button>

            <div class="stat">
                생산 대기:
                <span id="queueDisplay">
                    ${scvProductionQueue}
                </span>
                / ${MAX_SCV_QUEUE}
            </div>

        `;

    }


    else if(
        object.userData.type ===
        "gasFacility"
    ){

        title.innerHTML =
            "🟢 가스 채취 시설";

        content.innerHTML = `

            <div class="stat">
                체력:
                ${object.userData.hp}
                /
                ${object.userData.maxHp}
            </div>

            <div class="stat">
                남은 가스:
                ${object.userData.gas}
            </div>

        `;
    }

}


// ============================================================
// SCV 생산
// ============================================================

function produceSCV(){

    if(
        scvProductionQueue >=
        MAX_SCV_QUEUE
    ){

        alert(
            "SCV 생산 대기열이 가득 찼습니다."
        );

        return;
    }


    if(
        minerals < SCV_COST
    ){

        alert(
            "미네랄이 부족합니다."
        );

        return;
    }


    minerals -=
        SCV_COST;

    updateResources();


    scvProductionQueue++;


    updateQueue();


    setTimeout(
        () => {

            createSCV(
                6 +
                Math.random()*3,

                5 +
                Math.random()*3
            );

            scvProductionQueue--;

            updateQueue();

            updateResources();

        },

        SCV_BUILD_TIME*1000
    );

}


function updateQueue(){

    const el =
        document.getElementById(
            "queueDisplay"
        );

    if(el)
        el.innerHTML =
            scvProductionQueue;

}


// ============================================================
// 가스 건설 시작
// ============================================================

function startGasBuild(){

    const builder =
        selectedUnits
            .find(
                u =>
                u.userData.type ===
                "scv"
            );


    if(!builder){

        alert(
            "SCV를 선택하세요."
        );

        return;
    }


    buildMode = true;

    currentBuildSCV =
        builder;

    buildPreview.visible =
        true;


    document.getElementById(
        "buildMessage"
    ).style.display =
        "block";

    document.getElementById(
        "buildMessage"
    ).innerHTML =
        "🏗️ 가스 시설 위치를 선택하세요";


    setPreviewColor(
        0x55ff88
    );

}


// ============================================================
// 건설 미리보기
// ============================================================

function updateBuildPreview(){

    if(
        !buildMode ||
        !buildPreview
    )
        return;


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


    let nearest =
        null;

    let distance =
        Infinity;


    geysers.forEach(
        geyser => {

            const d =
                Math.hypot(
                    point.x -
                    geyser.position.x,

                    point.z -
                    geyser.position.z
                );


            if(
                d <
                distance
            ){

                distance = d;

                nearest =
                    geyser;
            }

        }
    );


    if(
        nearest &&
        distance < 6 &&
        !nearest.userData.hasFacility
    ){

        buildPreviewValid =
            true;

        buildPreview.position.copy(
            nearest.position
        );

        setPreviewColor(
            0x55ff88
        );


        document.getElementById(
            "buildMessage"
        ).innerHTML =
            "🟢 건설 가능<br>" +
            "<small>클릭하여 건설</small>";

    }

    else{

        buildPreviewValid =
            false;

        buildPreview.position.set(
            point.x,
            0,
            point.z
        );

        setPreviewColor(
            0xff3333
        );


        document.getElementById(
            "buildMessage"
        ).innerHTML =
            "🔴 건설할 수 없음<br>" +
            "<small>가스 지역에 설치하세요</small>";
    }

}


// ============================================================
// 건설
// ============================================================

function confirmGasBuild(){

    if(
        !buildMode ||
        !currentBuildSCV
    )
        return;


    if(!buildPreviewValid){

        document.getElementById(
            "buildMessage"
        ).innerHTML =
            "🔴 건설할 수 없음";

        return;
    }


    let targetGeyser =
        null;


    geysers.forEach(
        geyser => {

            if(
                geyser.position.distanceTo(
                    buildPreview.position
                ) < .1
            ){

                targetGeyser =
                    geyser;
            }

        }
    );


    if(!targetGeyser)
        return;


    buildMode =
        false;

    buildPreview.visible =
        false;


    document.getElementById(
        "buildMessage"
    ).innerHTML =
        "🏗️ 가스 시설 건설 중...";


    const scv =
        currentBuildSCV;


    scv.userData.state =
        "building";

    scv.userData.buildTarget =
        targetGeyser;


    moveUnitTo(
        scv,
        targetGeyser.position,
        () => {

            setTimeout(
                () => {

                    if(
                        targetGeyser.userData
                            .hasFacility
                    )
                        return;


                    targetGeyser.userData
                        .hasFacility =
                        true;


                    createGasFacility(
                        targetGeyser
                    );


                    scv.userData.state =
                        "idle";

                    scv.userData.buildTarget =
                        null;

                    currentBuildSCV =
                        null;


                    document.getElementById(
                        "buildMessage"
                    ).innerHTML =
                        "🟢 가스 시설 건설 완료";


                    setTimeout(
                        () => {

                            document.getElementById(
                                "buildMessage"
                            ).style.display =
                                "none";

                        },
                        1500
                    );


                },

                GAS_BUILD_TIME*1000
            );

        }
    );

}


// ============================================================
// 이동
// ============================================================

function moveUnitTo(
    unit,
    target,
    callback
){

    unit.userData.moveTarget =
        target.clone();

    unit.userData.moveCallback =
        callback || null;

    unit.userData.state =
        "moving";

}


// ============================================================
// SCV 자원 시스템
// ============================================================

function updateSCV(
    scv,
    delta
){

    const data =
        scv.userData;


    if(
        data.state ===
        "mining"
    ){

        return;
    }


    if(
        data.state ===
        "returning"
    ){

        return;
    }


    if(
        data.moveTarget
    ){

        const target =
            data.moveTarget;


        const direction =
            new THREE.Vector3()
                .subVectors(
                    target,
                    scv.position
                );


        const distance =
            direction.length();


        if(
            distance < .5
        ){

            scv.userData.moveTarget =
                null;


            const callback =
                scv.userData.moveCallback;

            scv.userData.moveCallback =
                null;


            if(callback)
                callback();


        }

        else{

            direction.normalize();

            scv.position.add(
                direction.multiplyScalar(
                    data.speed *
                    delta
                )
            );


            scv.rotation.y =
                Math.atan2(
                    direction.x,
                    direction.z
                );
        }

    }

}


// ============================================================
// 미네랄 명령
// ============================================================

function orderMineMineral(
    scv,
    node
){

    scv.userData.state =
        "movingToMineral";

    scv.userData.target =
        node;


    moveUnitTo(
        scv,
        node.position,
        () => {

            scv.userData.state =
                "mining";


            setTimeout(
                () => {

                    if(
                        node.userData.amount <= 0
                    ){

                        scv.userData.state =
                            "idle";

                        return;
                    }


                    const amount =
                        Math.min(
                            SCV_MINERAL_AMOUNT,
                            node.userData.amount
                        );


                    node.userData.amount -=
                        amount;


                    scv.userData.carrying =
                        amount;


                    scv.userData.state =
                        "returning";


                    moveUnitTo(
                        scv,
                        commandCenter.position,
                        () => {

                            minerals +=
                                scv.userData.carrying;

                            scv.userData.carrying =
                                0;


                            updateResources();


                            // 다시 채취

                            orderMineMineral(
                                scv,
                                node
                            );

                        }
                    );

                },

                MINERAL_TIME*1000
            );

        }
    );

}


// ============================================================
// 가스 명령
// ============================================================

function orderMineGas(
    scv,
    facility
){

    scv.userData.state =
        "movingToGas";

    scv.userData.target =
        facility;


    moveUnitTo(
        scv,
        facility.position,
        () => {

            scv.userData.state =
                "gasMining";


            setTimeout(
                () => {

                    if(
                        facility.userData.gas <= 0
                    ){

                        scv.userData.state =
                            "idle";

                        return;
                    }


                    const amount =
                        Math.min(
                            SCV_GAS_AMOUNT,
                            facility.userData.gas
                        );


                    facility.userData.gas -=
                        amount;


                    scv.userData.carryingGas =
                        amount;


                    scv.userData.state =
                        "returningGas";


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


                            orderMineGas(
                                scv,
                                facility
                            );

                        }
                    );

                },

                MINERAL_TIME*1000
            );

        }
    );

}


// ============================================================
// 마우스
// ============================================================

const mouse =
    new THREE.Vector2();

const raycaster =
    new THREE.Raycaster();

let mouseDown =
    false;

let dragStartX = 0;

let dragStartY = 0;

let isDragging =
    false;


renderer.domElement
    .addEventListener(
        "mousemove",
        e => {

            mouse.x =
                (e.clientX /
                window.innerWidth)
                * 2 - 1;

            mouse.y =
                -(e.clientY /
                window.innerHeight)
                * 2 + 1;


            if(mouseDown){

                const dx =
                    e.clientX -
                    dragStartX;

                const dy =
                    e.clientY -
                    dragStartY;


                if(
                    Math.abs(dx) > 5 ||
                    Math.abs(dy) > 5
                ){

                    isDragging =
                        true;

                    updateSelectionBox(
                        dragStartX,
                        dragStartY,
                        e.clientX,
                        e.clientY
                    );
                }
            }


            updateBuildPreview();

        }
    );


// ============================================================
// 좌클릭
// ============================================================

renderer.domElement
    .addEventListener(
        "mousedown",
        e => {

            if(e.button !== 0)
                return;


            mouseDown =
                true;

            isDragging =
                false;

            dragStartX =
                e.clientX;

            dragStartY =
                e.clientY;


            if(buildMode){

                confirmGasBuild();

                return;
            }

        }
    );


renderer.domElement
    .addEventListener(
        "mouseup",
        e => {

            if(e.button !== 0)
                return;


            mouseDown =
                false;


            if(isDragging){

                selectUnitsInBox(
                    dragStartX,
                    dragStartY,
                    e.clientX,
                    e.clientY
                );

            }

            else{

                clickSelect(
                    e.clientX,
                    e.clientY
                );

            }


            hideSelectionBox();

            isDragging =
                false;

        }
    );


// ============================================================
// 우클릭
// ============================================================

renderer.domElement
    .addEventListener(
        "contextmenu",
        e => {

            e.preventDefault();


            if(buildMode){

                cancelBuild();

                return;
            }


            if(
                selectedUnits.length === 0
            )
                return;


            raycaster.setFromCamera(
                mouse,
                camera
            );


            const intersects =
                raycaster.intersectObject(
                    ground
                );


            if(!intersects.length)
                return;


            const point =
                intersects[0].point;


            selectedUnits.forEach(
                unit => {

                    if(
                        unit.userData.type ===
                        "scv"
                    ){

                        moveUnitTo(
                            unit,
                            point
                        );

                        unit.userData.target =
                            null;
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
        (x /
        window.innerWidth)
        * 2 - 1;

    mouse.y =
        -(y /
        window.innerHeight)
        * 2 + 1;


    raycaster.setFromCamera(
        mouse,
        camera
    );


    const objects = [];


    scvs.forEach(
        scv =>
            objects.push(scv)
    );

    buildings.forEach(
        b =>
            objects.push(b)
    );

    gasFacilities.forEach(
        f =>
            objects.push(f)
    );

    mineralsNodes.forEach(
        m =>
            objects.push(m)
    );


    const hits =
        raycaster.intersectObjects(
            objects,
            true
        );


    if(!hits.length){

        clearSelection();

        document.getElementById(
            "sidePanel"
        ).style.display =
            "none";

        return;
    }


    let obj =
        hits[0].object;


    while(
        obj.parent &&
        !obj.userData.type
    ){

        obj =
            obj.parent;
    }


    if(!obj.userData.type)
        return;


    if(
        obj.userData.type ===
        "mineral"
    ){

        if(
            selectedUnits.length
        ){

            selectedUnits.forEach(
                unit => {

                    if(
                        unit.userData.type ===
                        "scv"
                    ){

                        orderMineMineral(
                            unit,
                            obj
                        );
                    }

                }
            );

        }

        return;
    }


    if(
        obj.userData.type ===
        "geyser"
    ){

        if(
            selectedUnits.length
        ){

            selectedUnits.forEach(
                unit => {

                    if(
                        unit.userData.type ===
                        "scv"
                    ){

                        if(
                            obj.userData
                                .hasFacility
                        ){

                            const facility =
                                gasFacilities.find(
                                    f =>
                                    f.position
                                    .distanceTo(
                                        obj.position
                                    ) < .1
                                );

                            if(facility)
                                orderMineGas(
                                    unit,
                                    facility
                                );
                        }
                    }

                }
            );

        }

        return;
    }


    selectUnit(
        obj
    );

}


// ============================================================
// 드래그 선택
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


    const left =
        Math.min(x1,x2);

    const top =
        Math.min(y1,y2);

    const width =
        Math.abs(x2-x1);

    const height =
        Math.abs(y2-y1);


    box.style.left =
        left+"px";

    box.style.top =
        top+"px";

    box.style.width =
        width+"px";

    box.style.height =
        height+"px";

}


function hideSelectionBox(){

    document.getElementById(
        "selectionBox"
    ).style.display =
        "none";

}


function selectUnitsInBox(
    x1,
    y1,
    x2,
    y2
){

    clearSelection();


    const left =
        Math.min(x1,x2);

    const right =
        Math.max(x1,x2);

    const top =
        Math.min(y1,y2);

    const bottom =
        Math.max(y1,y2);


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
        selectedUnits.length
    ){

        showUnitPanel(
            selectedUnits[0]
        );
    }

}


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
            (vector.x+1)/2 *
            window.innerWidth,

        y:
            (-vector.y+1)/2 *
            window.innerHeight

    };

}


// ============================================================
// 건설 취소
// ============================================================

function cancelBuild(){

    buildMode =
        false;

    currentBuildSCV =
        null;

    buildPreview.visible =
        false;


    const message =
        document.getElementById(
            "buildMessage"
        );

    message.style.display =
        "none";

}


// ============================================================
// 카메라
// ============================================================

let cameraX = 0;
let cameraZ = 0;

const cameraSpeed = .8;


function updateCamera(){

    const edge = 35;

    if(
        mouseX <
        edge
    )
        cameraX -=
            cameraSpeed;

    if(
        mouseX >
        window.innerWidth-edge
    )
        cameraX +=
            cameraSpeed;

    if(
        mouseY <
        edge
    )
        cameraZ -=
            cameraSpeed;

    if(
        mouseY >
        window.innerHeight-edge
    )
        cameraZ +=
            cameraSpeed;


    cameraX =
        THREE.MathUtils.clamp(
            cameraX,
            -35,
            35
        );

    cameraZ =
        THREE.MathUtils.clamp(
            cameraZ,
            -35,
            35
        );


    camera.position.x =
        cameraX;

    camera.position.z =
        cameraZ + 25;


    camera.lookAt(
        cameraX,
        0,
        cameraZ
    );

}


let mouseX = 0;
let mouseY = 0;


window.addEventListener(
    "mousemove",
    e => {

        mouseX =
            e.clientX;

        mouseY =
            e.clientY;

    }
);


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


document
    .getElementById("miniMap")
    .addEventListener(
        "click",
        e => {

            const rect =
                miniCanvas
                .getBoundingClientRect();


            const x =
                (e.clientX -
                rect.left) /
                rect.width;

            const y =
                (e.clientY -
                rect.top) /
                rect.height;


            cameraX =
                (x-.5)*70;

            cameraZ =
                (y-.5)*70;

        }
    );


function drawMiniMap(){

    miniCtx.fillStyle =
        "#14221a";

    miniCtx.fillRect(
        0,
        0,
        230,
        150
    );


    // 미네랄

    mineralsNodes.forEach(
        m => {

            const x =
                (m.position.x+45) /
                90 * 230;

            const y =
                (m.position.z+45) /
                90 * 150;


            miniCtx.fillStyle =
                "#22aaff";

            miniCtx.fillRect(
                x-2,
                y-2,
                4,
                4
            );

        }
    );


    // 가스

    geysers.forEach(
        g => {

            const x =
                (g.position.x+45) /
                90 * 230;

            const y =
                (g.position.z+45) /
                90 * 150;


            miniCtx.fillStyle =
                "#30ff75";

            miniCtx.beginPath();

            miniCtx.arc(
                x,
                y,
                5,
                0,
                Math.PI*2
            );

            miniCtx.fill();

        }
    );


    // 사령부

    const cx =
        (commandCenter.position.x+45) /
        90 * 230;

    const cy =
        (commandCenter.position.z+45) /
        90 * 150;


    miniCtx.fillStyle =
        "#eeeeee";

    miniCtx.fillRect(
        cx-5,
        cy-5,
        10,
        10
    );


    // SCV

    scvs.forEach(
        s => {

            const x =
                (s.position.x+45) /
                90 * 230;

            const y =
                (s.position.z+45) /
                90 * 150;


            miniCtx.fillStyle =
                "#ffd23f";

            miniCtx.fillRect(
                x-2,
                y-2,
                4,
                4
            );

        }
    );


    // 현재 카메라

    const vx =
        (cameraX+45) /
        90 * 230;

    const vy =
        (cameraZ+45) /
        90 * 150;


    miniCtx.strokeStyle =
        "#ffffff";

    miniCtx.strokeRect(
        vx-15,
        vy-10,
        30,
        20
    );

}


// ============================================================
// 자원 UI
// ============================================================

function updateResources(){

    document.getElementById(
        "minerals"
    ).innerHTML =
        minerals;

    document.getElementById(
        "gas"
    ).innerHTML =
        gas;

    document.getElementById(
        "scvCount"
    ).innerHTML =
        scvs.length;

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
                facility.userData
                    .particleGroup
                    .children;


            particles.forEach(
                particle => {

                    particle.position.y +=
                        particle.userData.speed *
                        delta;


                    particle.position.x +=
                        Math.sin(
                            performance.now()*.002
                        )*.001;


                    if(
                        particle.position.y >
                        9.5
                    ){

                        particle.position.y =
                            5.2;

                        particle.position.x =
                            (Math.random()-.5)*1.5;

                        particle.position.z =
                            (Math.random()-.5)*1.5;
                    }

                }
            );


            if(
                facility.userData.core
            ){

                facility.userData.core
                    .scale.setScalar(
                        1 +
                        Math.sin(
                            performance.now()*.004
                        )*.08
                    );

            }

        }
    );

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

        }
    );


// ============================================================
// 애니메이션
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
            (now-lastTime)/1000,
            .05
        );

    lastTime =
        now;


    if(gameStarted){

        updateCamera();


        scvs.forEach(
            scv =>
                updateSCV(
                    scv,
                    delta
                )
        );


        animateGas(
            delta
        );


        updateBuildPreview();


        drawMiniMap();

    }


    renderer.render(
        scene,
        camera
    );

}


animate();


// ============================================================
// 리사이즈
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

</script>

</body>
</html>
"""

components.html(
    html,
    height=900,
    scrolling=False
)
