import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Terran RTS",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if "started" not in st.session_state:
    st.session_state.started = False


# =========================================================
# 종족 선택
# =========================================================

if not st.session_state.started:

    st.markdown("""
    <style>
    .title {
        text-align:center;
        font-size:70px;
        font-weight:900;
        margin-top:150px;
        letter-spacing:8px;
    }

    .subtitle {
        text-align:center;
        color:#8ea3b5;
        font-size:20px;
        letter-spacing:5px;
        margin-bottom:45px;
    }
    </style>

    <div class="title">
        STARCRAFT
    </div>

    <div class="subtitle">
        TERRAN COMMAND
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c2:

        if st.button(
            "🔵 TERRAN",
            use_container_width=True
        ):
            st.session_state.started = True
            st.rerun()

    st.info("현재 플레이 가능한 종족은 테란입니다.")

    st.stop()


# =========================================================
# 게임 HTML
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

    background:#05080b;

    font-family:
        Arial,
        Helvetica,
        sans-serif;
}


/* =====================================================
   GAME
===================================================== */

#game {

    position:absolute;

    left:0;
    top:0;

    width:100%;
    height:100%;
}


/* =====================================================
   상단 자원 UI
===================================================== */

#topUI {

    position:absolute;

    top:15px;
    left:15px;

    z-index:100;

    background:
        rgba(5,10,15,0.94);

    border:
        1px solid #516575;

    border-radius:8px;

    padding:12px 18px;

    color:white;

    min-width:560px;

    box-shadow:
        0 5px 25px
        rgba(0,0,0,0.55);
}


.resource {

    display:inline-block;

    margin-right:25px;

    font-size:17px;
}


.resource b {

    color:#7fdcff;
}


#message {

    margin-top:8px;

    color:#8fcfff;

    font-size:13px;
}


/* =====================================================
   오른쪽 상태창
===================================================== */

#unitPanel {

    position:absolute;

    right:20px;
    top:90px;

    width:285px;

    min-height:320px;

    z-index:110;

    display:none;

    padding:18px;

    box-sizing:border-box;

    color:white;

    background:
        linear-gradient(
            145deg,
            rgba(19,28,34,0.98),
            rgba(5,10,14,0.98)
        );

    border:
        2px solid #566b77;

    border-radius:8px;

    box-shadow:
        0 8px 30px
        rgba(0,0,0,0.7);
}


#unitIcon {

    width:65px;
    height:65px;

    margin:auto;

    display:flex;

    align-items:center;
    justify-content:center;

    font-size:38px;

    background:#18242b;

    border:
        1px solid #607581;

    border-radius:6px;
}


#unitName {

    text-align:center;

    margin-top:10px;

    font-size:21px;

    font-weight:bold;
}


.panelLine {

    height:1px;

    background:#455761;

    margin:14px 0;
}


#healthText {

    font-size:14px;

    margin-bottom:6px;
}


#healthBar {

    width:100%;

    height:12px;

    background:#252b2e;

    border-radius:5px;

    overflow:hidden;
}


#healthFill {

    width:100%;

    height:100%;

    background:#39c95a;
}


.panelTitle {

    margin-top:18px;

    margin-bottom:8px;

    color:#bdd4df;

    font-weight:bold;
}


#scvStatus {

    padding:9px;

    background:#111b20;

    border-radius:5px;

    color:#8fd2ff;

    font-size:13px;
}


#unitPanel button {

    width:100%;

    padding:12px;

    margin-top:7px;

    color:white;

    background:#182e3b;

    border:
        1px solid #4b7387;

    border-radius:5px;

    cursor:pointer;

    font-size:14px;
}


#unitPanel button:hover {

    background:#285269;
}


#unitPanel small {

    color:#a8bac3;
}


#productionQueue {

    margin-top:10px;

    padding:8px;

    text-align:center;

    background:#111a1f;

    border-radius:4px;

    color:#a9c0ca;
}


/* =====================================================
   드래그 선택 박스
===================================================== */

#selectionBox {

    position:absolute;

    z-index:90;

    display:none;

    border:
        1px solid #55caff;

    background:
        rgba(30,170,255,0.12);

    pointer-events:none;
}


/* =====================================================
   미니맵
===================================================== */

#minimapContainer {

    position:absolute;

    left:50%;
    bottom:10px;

    transform:
        translateX(-50%);

    width:380px;
    height:145px;

    z-index:120;

    background:
        rgba(4,8,11,0.97);

    border:
        2px solid #526775;

    border-radius:7px;

    padding:5px;

    box-shadow:
        0 4px 20px
        rgba(0,0,0,0.8);
}


#minimap {

    width:100%;
    height:100%;

    display:block;

    cursor:pointer;
}


#minimapLabel {

    position:absolute;

    left:8px;
    top:5px;

    color:#bcd1dd;

    font-size:10px;

    pointer-events:none;

    text-shadow:
        0 1px 3px black;
}


/* =====================================================
   도움말
===================================================== */

#help {

    position:absolute;

    left:15px;
    bottom:15px;

    z-index:100;

    background:
        rgba(0,0,0,0.72);

    padding:9px 13px;

    border-radius:5px;

    color:#ddd;

    font-size:12px;

    line-height:1.6;
}

</style>


<script type="importmap">

{
    "imports": {
        "three":
        "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js"
    }
}

</script>

</head>


<body>


<div id="game"></div>


<!-- =====================================================
     자원
===================================================== -->

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
        📦 대기:
        <b id="queue">0</b>/5
    </span>

    <div id="message">
        SCV를 선택하세요.
    </div>

</div>


<!-- =====================================================
     오른쪽 상태창
===================================================== -->

<div id="unitPanel">

    <div id="unitIcon">
        👨‍🚀
    </div>

    <div id="unitName">
        SCV
    </div>

    <div class="panelLine"></div>

    <div id="healthText">
        체력: 50 / 50
    </div>

    <div id="healthBar">
        <div id="healthFill"></div>
    </div>


    <!-- SCV 상태 -->

    <div id="scvStatusPanel">

        <div class="panelTitle">
            현재 상태
        </div>

        <div id="scvStatus">
            대기 중
        </div>


        <div class="panelTitle">
            🏗️ 건설 가능
        </div>

        <button id="gasBuildButton">

            🟢 가스 채취 시설

            <br>

            <small>
                건설 시간: 15초
            </small>

        </button>

    </div>


    <!-- 사령부 -->

    <div id="commandPanel">

        <div class="panelTitle">
            👨‍🚀 유닛 생산
        </div>

        <button id="scvProduceButton">

            👨‍🚀 SCV

            <br>

            <small>
                💎 50 미네랄
                | ⏱️ 10초
            </small>

        </button>

        <div id="productionQueue">
            생산 대기: 0 / 5
        </div>

    </div>

</div>


<!-- =====================================================
     선택 박스
===================================================== -->

<div id="selectionBox"></div>


<!-- =====================================================
     미니맵
===================================================== -->

<div id="minimapContainer">

    <canvas id="minimap"></canvas>

    <div id="minimapLabel">
        MINI MAP
    </div>

</div>


<!-- =====================================================
     도움말
===================================================== -->

<div id="help">

    <b>조작법</b><br>

    좌클릭 : 유닛 선택<br>

    좌클릭 드래그 : 여러 유닛 선택<br>

    우클릭 : 이동 / 자원 채취<br>

    SCV 상태창 → 가스 시설 : 건설<br>

    사령부 클릭 → SCV : 생산<br>

    화면 끝 : 카메라 이동<br>

    미니맵 클릭 : 화면 이동

</div>


<script type="module">

import * as THREE from "three";


// ========================================================
// 설정
// ========================================================

const MAP_SIZE = 320;

const HALF_MAP =
    MAP_SIZE / 2;

const EDGE_SIZE = 45;

const CAMERA_SPEED = 1.5;


// ========================================================
// 게임 변수
// ========================================================

let mineralsCount = 500;

let gasCount = 0;

let scvQueue = 0;

let producingSCV = false;

let buildingGas = false;

let gasFacility = null;

let gasGeyser = null;

let commandCenter = null;

let scvs = [];

let mineralObjects = [];

let selectedUnits = [];

let selectedBuilding = null;


// ========================================================
// THREE SCENE
// ========================================================

const scene =
    new THREE.Scene();


scene.background =
    new THREE.Color(
        0x101920
    );


scene.fog =
    new THREE.Fog(
        0x101920,
        160,
        380
    );


// ========================================================
// CAMERA
// ========================================================

const camera =
    new THREE.PerspectiveCamera(
        48,
        window.innerWidth /
        window.innerHeight,
        0.1,
        700
    );


camera.position.set(
    0,
    180,
    35
);


let cameraTarget =
    new THREE.Vector3(
        0,
        0,
        35
    );


// ========================================================
// RENDERER
// ========================================================

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


renderer.shadowMap.enabled =
    true;


renderer.shadowMap.type =
    THREE.PCFSoftShadowMap;


document
    .getElementById("game")
    .appendChild(renderer.domElement);


// ========================================================
// LIGHT
// ========================================================

scene.add(
    new THREE.HemisphereLight(
        0xb8d5ff,
        0x20251f,
        2.5
    )
);


const sunlight =
    new THREE.DirectionalLight(
        0xffffff,
        3
    );


sunlight.position.set(
    80,
    180,
    50
);


sunlight.castShadow =
    true;


sunlight.shadow.mapSize.width =
    2048;

sunlight.shadow.mapSize.height =
    2048;


scene.add(sunlight);


// ========================================================
// GROUND
// ========================================================

const ground =
    new THREE.Mesh(

        new THREE.PlaneGeometry(
            MAP_SIZE,
            MAP_SIZE,
            80,
            80
        ),

        new THREE.MeshStandardMaterial({
            color:0x26382e,
            roughness:0.95
        })

    );


ground.rotation.x =
    -Math.PI / 2;


ground.receiveShadow =
    true;


ground.userData.type =
    "ground";


scene.add(ground);


// ========================================================
// GRID
// ========================================================

const grid =
    new THREE.GridHelper(
        MAP_SIZE,
        32,
        0x355044,
        0x26382e
    );


grid.position.y =
    0.03;


scene.add(grid);


// ========================================================
// MAP BORDER
// ========================================================

const borderMaterial =
    new THREE.MeshStandardMaterial({

        color:0x111820,

        metalness:0.8,

        roughness:0.35

    });


const borderHeight = 3;


const northBorder =
    new THREE.Mesh(
        new THREE.BoxGeometry(
            MAP_SIZE,
            borderHeight,
            3
        ),
        borderMaterial
    );


northBorder.position.set(
    0,
    1.5,
    -HALF_MAP
);


scene.add(northBorder);


const southBorder =
    northBorder.clone();


southBorder.position.z =
    HALF_MAP;


scene.add(southBorder);


const westBorder =
    new THREE.Mesh(
        new THREE.BoxGeometry(
            3,
            borderHeight,
            MAP_SIZE
        ),
        borderMaterial
    );


westBorder.position.set(
    -HALF_MAP,
    1.5,
    0
);


scene.add(westBorder);


const eastBorder =
    westBorder.clone();


eastBorder.position.x =
    HALF_MAP;


scene.add(eastBorder);


// ========================================================
// ROCKS
// ========================================================

for(let i=0; i<170; i++){

    const size =
        Math.random()*3 + 1;


    const rock =
        new THREE.Mesh(

            new THREE.DodecahedronGeometry(
                size
            ),

            new THREE.MeshStandardMaterial({

                color:0x3a4640,

                roughness:0.9

            })

        );


    rock.position.set(

        Math.random() *
        (MAP_SIZE-20)
        - HALF_MAP + 10,

        size/2,

        Math.random() *
        (MAP_SIZE-20)
        - HALF_MAP + 10

    );


    rock.castShadow =
        true;


    scene.add(rock);

}


// ========================================================
// COMMAND CENTER
// ========================================================

function createCommandCenter(){

    const group =
        new THREE.Group();


    const base =
        new THREE.Mesh(

            new THREE.BoxGeometry(
                24,
                5,
                20
            ),

            new THREE.MeshStandardMaterial({

                color:0x4f5b62,

                metalness:0.8,

                roughness:0.3

            })

        );


    base.position.y =
        2.5;


    base.castShadow =
        true;


    group.add(base);


    const body =
        new THREE.Mesh(

            new THREE.BoxGeometry(
                13,
                13,
                12
            ),

            new THREE.MeshStandardMaterial({

                color:0x747f86,

                metalness:0.75,

                roughness:0.3

            })

        );


    body.position.y =
        10;


    body.castShadow =
        true;


    group.add(body);


    const door =
        new THREE.Mesh(

            new THREE.BoxGeometry(
                6,
                5,
                1
            ),

            new THREE.MeshStandardMaterial({

                color:0x12181c,

                metalness:0.6

            })

        );


    door.position.set(
        0,
        3,
        -6.5
    );


    group.add(door);


    for(
        const x of [-9,9]
    ){

        const engine =
            new THREE.Mesh(

                new THREE.CylinderGeometry(
                    3,
                    3,
                    6,
                    16
                ),

                new THREE.MeshStandardMaterial({

                    color:0x30393e,

                    metalness:0.9,

                    roughness:0.25

                })

            );


        engine.position.set(
            x,
            3,
            3
        );


        engine.castShadow =
            true;


        group.add(engine);


        const light =
            new THREE.PointLight(
                0x008cff,
                4,
                14
            );


        light.position.set(
            x,
            4,
            0
        );


        group.add(light);

    }


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


    roof.position.y =
        17;


    roof.rotation.y =
        Math.PI/8;


    group.add(roof);


    const energy =
        new THREE.Mesh(

            new THREE.CylinderGeometry(
                2.5,
                2.5,
                5,
                16
            ),

            new THREE.MeshStandardMaterial({

                color:0x129fff,

                emissive:0x0077ff,

                emissiveIntensity:3

            })

        );


    energy.position.y =
        20;


    group.add(energy);


    const antenna =
        new THREE.Mesh(

            new THREE.CylinderGeometry(
                0.3,
                0.3,
                12
            ),

            new THREE.MeshStandardMaterial({

                color:0x202427,

                metalness:0.8

            })

        );


    antenna.position.y =
        26;


    group.add(antenna);


    const antennaLight =
        new THREE.PointLight(
            0x00aaff,
            5,
            25
        );


    antennaLight.position.y =
        32;


    group.add(
        antennaLight
    );


    group.position.set(
        0,
        0,
        35
    );


    group.userData.type =
        "command";

    group.userData.maxHealth =
        1500;

    group.userData.health =
        1500;


    scene.add(group);


    commandCenter =
        group;

}


createCommandCenter();


// ========================================================
// MINERALS
// ========================================================

const mineralPositions = [

    [-70,-65],
    [-58,-70],
    [-46,-68],
    [-34,-65],

    [55,-70],
    [67,-66],
    [78,-58],
    [87,-48],

    [-110,-15],
    [-102,-2],
    [-95,10],
    [-88,22],

    [82,5],
    [92,15],
    [102,25],
    [110,36],

    [-75,88],
    [-62,96],
    [-48,102],

    [65,88],
    [78,96],
    [92,90]

];


function createMineral(x,z){

    const group =
        new THREE.Group();


    const crystal =
        new THREE.Mesh(

            new THREE.OctahedronGeometry(
                3
            ),

            new THREE.MeshStandardMaterial({

                color:0x16caff,

                emissive:0x007799,

                emissiveIntensity:2,

                metalness:0.7,

                roughness:0.15

            })

        );


    crystal.scale.y =
        1.7;


    crystal.castShadow =
        true;


    group.add(crystal);


    for(let i=0;i<4;i++){

        const small =
            new THREE.Mesh(

                new THREE.OctahedronGeometry(
                    1.1
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


    scene.add(group);


    mineralObjects.push(group);

}


mineralPositions.forEach(
    p =>
        createMineral(
            p[0],
            p[1]
        )
);


// ========================================================
// GAS GEYSER
// ========================================================

function createGasGeyser(){

    const group =
        new THREE.Group();


    const base =
        new THREE.Mesh(

            new THREE.CylinderGeometry(
                8,
                9,
                2,
                24
            ),

            new THREE.MeshStandardMaterial({

                color:0x303b35,

                roughness:0.8

            })

        );


    base.position.y =
        1;


    group.add(base);


    const gas =
        new THREE.Mesh(

            new THREE.CylinderGeometry(
                4.5,
                5,
                4,
                24
            ),

            new THREE.MeshStandardMaterial({

                color:0x23e868,

                emissive:0x00aa44,

                emissiveIntensity:2

            })

        );


    gas.position.y =
        3.5;


    group.add(gas);


    group.position.set(
        32,
        0,
        75
    );


    group.userData.type =
        "geyser";


    scene.add(group);


    gasGeyser =
        group;

}


createGasGeyser();


// ========================================================
// GAS FACILITY
// ========================================================

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


    body.position.y =
        4;


    body.castShadow =
        true;


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


    top.position.y =
        9;


    group.add(top);


    group.position.copy(
        gasGeyser.position
    );


    group.userData.type =
        "gasFacility";

    group.userData.maxHealth =
        500;

    group.userData.health =
        500;


    scene.add(group);


    gasFacility =
        group;


    buildingGas =
        false;


    message(
        "🏗️ 가스 채취 시설 건설 완료!"
    );

}


// ========================================================
// SCV
// ========================================================

function createSCV(index){

    const scv =
        new THREE.Group();


    const body =
        new THREE.Mesh(

            new THREE.BoxGeometry(
                3.3,
                1.6,
                3.8
            ),

            new THREE.MeshStandardMaterial({

                color:0xbfc1bb,

                metalness:0.65,

                roughness:0.35

            })

        );


    body.position.y =
        1.4;


    body.castShadow =
        true;


    scv.add(body);


    const front =
        new THREE.Mesh(

            new THREE.BoxGeometry(
                2.7,
                1.2,
                1.4
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


    for(
        const side of [-1,1]
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

                    color:0x151515

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


    scv.position.set(

        -8 + index*4,

        0,

        53

    );


    scv.userData.type =
        "scv";


    scv.userData.id =
        index;


    scv.userData.maxHealth =
        50;


    scv.userData.health =
        50;


    scv.userData.state =
        "idle";


    scv.userData.resource =
        null;


    scv.userData.target =
        null;


    scv.userData.carrying =
        false;


    scv.userData.miningStart =
        null;


    scv.userData.buildStart =
        null;


    scene.add(scv);


    scvs.push(scv);


    updateSCVCount();


    return scv;

}


// 시작 SCV 5기

for(let i=0;i<5;i++){

    createSCV(i);

}


// ========================================================
// UI
// ========================================================

function updateResources(){

    document
        .getElementById("minerals")
        .innerText =
        Math.floor(
            mineralsCount
        );


    document
        .getElementById("gas")
        .innerText =
        Math.floor(
            gasCount
        );

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

    const pq =
        document.getElementById(
            "productionQueue"
        );

    if(pq){

        pq.innerText =
            "생산 대기: " +
            scvQueue +
            " / 5";

    }

}


function message(text){

    document
        .getElementById("message")
        .innerText =
        text;

}


// ========================================================
// 오른쪽 상태창
// ========================================================

const unitPanel =
    document.getElementById(
        "unitPanel"
    );


const unitIcon =
    document.getElementById(
        "unitIcon"
    );


const unitName =
    document.getElementById(
        "unitName"
    );


const healthText =
    document.getElementById(
        "healthText"
    );


const healthFill =
    document.getElementById(
        "healthFill"
    );


const scvStatus =
    document.getElementById(
        "scvStatus"
    );


function hideUnitPanel(){

    unitPanel.style.display =
        "none";

}


function showSCVStatus(scv){

    selectedBuilding =
        null;


    unitPanel.style.display =
        "block";


    unitIcon.innerText =
        "👨‍🚀";


    unitName.innerText =
        "SCV";


    healthText.innerText =
        "체력: " +
        scv.userData.health +
        " / " +
        scv.userData.maxHealth;


    healthFill.style.width =
        (
            scv.userData.health /
            scv.userData.maxHealth *
            100
        ) + "%";


    document
        .getElementById(
            "scvStatusPanel"
        )
        .style.display =
        "block";


    document
        .getElementById(
            "commandPanel"
        )
        .style.display =
        "none";


    updateSCVStatus(scv);

}


function updateSCVStatus(scv){

    if(!scv)
        return;


    let text =
        "대기 중";


    switch(
        scv.userData.state
    ){

        case "idle":

            text =
                "대기 중";

            break;


        case "moving":

            text =
                "이동 중";

            break;


        case "movingToMineral":

            text =
                "⛏️ 미네랄로 이동 중";

            break;


        case "miningMineral":

            text =
                "⛏️ 미네랄 채취 중";

            break;


        case "returnMineral":

            text =
                "📦 미네랄 운반 중";

            break;


        case "movingToBuildGas":

            text =
                "🏗️ 가스 시설 건설 장소로 이동 중";

            break;


        case "buildingGas":

            text =
                "🏗️ 가스 채취 시설 건설 중";

            break;


        case "movingToGas":

            text =
                "🟢 가스 시설로 이동 중";

            break;


        case "miningGas":

            text =
                "🟢 가스 채취 중";

            break;


        case "returnGas":

            text =
                "📦 가스 운반 중";

            break;

    }


    scvStatus.innerText =
        text;

}


function showCommandStatus(){

    selectedBuilding =
        commandCenter;


    unitPanel.style.display =
        "block";


    unitIcon.innerText =
        "🏢";


    unitName.innerText =
        "테란 사령부";


    healthText.innerText =
        "체력: " +
        commandCenter.userData.health +
        " / " +
        commandCenter.userData.maxHealth;


    healthFill.style.width =
        "100%";


    document
        .getElementById(
            "scvStatusPanel"
        )
        .style.display =
        "none";


    document
        .getElementById(
            "commandPanel"
        )
        .style.display =
        "block";


    updateQueue();

}


// ========================================================
// 선택
// ========================================================

function clearSelection(){

    selectedUnits.forEach(
        unit=>{

            removeSelectionRing(
                unit
            );

            unit.userData.selected =
                false;

        }
    );


    selectedUnits = [];

}


function addSelection(unit){

    if(
        selectedUnits.includes(unit)
    )
        return;


    selectedUnits.push(unit);


    unit.userData.selected =
        true;


    addSelectionRing(unit);

}


function addSelectionRing(unit){

    if(unit.userData.ring)
        return;


    const ring =
        new THREE.Mesh(

            new THREE.RingGeometry(
                2.6,
                2.9,
                32
            ),

            new THREE.MeshBasicMaterial({

                color:0x20cfff,

                side:
                    THREE.DoubleSide

            })

        );


    ring.rotation.x =
        -Math.PI/2;


    ring.position.y =
        0.08;


    unit.add(ring);


    unit.userData.ring =
        ring;

}


function removeSelectionRing(unit){

    if(
        unit.userData.ring
    ){

        unit.remove(
            unit.userData.ring
        );

        unit.userData.ring =
            null;

    }

}


// ========================================================
// RAYCAST
// ========================================================

const raycaster =
    new THREE.Raycaster();


const mouse =
    new THREE.Vector2();


function getObjectFromClick(event){

    mouse.x =
        event.clientX /
        window.innerWidth *
        2 - 1;


    mouse.y =
        -(event.clientY /
        window.innerHeight) *
        2 + 1;


    raycaster.setFromCamera(
        mouse,
        camera
    );


    const objects = [];


    scene.traverse(
        object=>{

            if(object.isMesh){

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
        hits.length === 0
    )
        return null;


    let object =
        hits[0].object;


    while(
        object.parent &&
        object.parent !== scene
    ){

        if(
            object.userData.type
        )
            break;


        object =
            object.parent;

    }


    return object;

}


// ========================================================
// LEFT CLICK
// ========================================================

let suppressNextClick = false;


renderer.domElement.addEventListener(
    "click",
    function(event){

        if(suppressNextClick){

            suppressNextClick =
                false;

            return;

        }


        const object =
            getObjectFromClick(
                event
            );


        if(!object)
            return;


        // SCV
        if(
            object.userData.type ===
            "scv"
        ){

            clearSelection();

            addSelection(object);

            showSCVStatus(object);

            message(
                "SCV 선택됨."
            );

            return;

        }


        // 사령부
        if(
            object.userData.type ===
            "command"
        ){

            clearSelection();

            showCommandStatus();

            message(
                "사령부 선택됨."
            );

            return;

        }


        // 미네랄
        if(
            object.userData.type ===
            "mineral"
        ){

            if(
                selectedUnits.length > 0
            ){

                orderMineral(
                    object
                );

            }

            return;

        }


        // 가스 시설
        if(
            object.userData.type ===
            "gasFacility"
        ){

            if(
                selectedUnits.length > 0
            ){

                orderGas(
                    object
                );

            }

            return;

        }

    }
);


// ========================================================
// MINERAL ORDER
// ========================================================

function orderMineral(mineral){

    selectedUnits.forEach(
        unit=>{

            if(
                unit.userData.type !==
                "scv"
            )
                return;


            unit.userData.resource =
                mineral;


            unit.userData.target =
                mineral;


            unit.userData.state =
                "movingToMineral";

        }
    );


    if(
        selectedUnits.length > 0
    ){

        showSCVStatus(
            selectedUnits[0]
        );

    }


    message(
        "⛏️ SCV가 미네랄을 채취하러 갑니다."
    );

}


// ========================================================
// GAS ORDER
// ========================================================

function orderGas(facility){

    selectedUnits.forEach(
        unit=>{

            if(
                unit.userData.type !==
                "scv"
            )
                return;


            unit.userData.resource =
                facility;


            unit.userData.target =
                facility;


            unit.userData.state =
                "movingToGas";

        }
    );


    if(
        selectedUnits.length > 0
    ){

        showSCVStatus(
            selectedUnits[0]
        );

    }


    message(
        "🟢 SCV가 가스를 채취하러 갑니다."
    );

}


// ========================================================
// GAS BUILD BUTTON
// ========================================================

document
    .getElementById(
        "gasBuildButton"
    )
    .onclick =
    function(){

        if(
            selectedUnits.length === 0
        ){

            message(
                "SCV를 먼저 선택하세요."
            );

            return;

        }


        const builder =
            selectedUnits[0];


        startGasBuilding();

    };


// ========================================================
// BUILD GAS
// ========================================================

function startGasBuilding(){

    if(gasFacility){

        message(
            "이미 가스 채취 시설이 있습니다."
        );

        return;

    }


    if(buildingGas){

        message(
            "가스 채취 시설을 건설 중입니다."
        );

        return;

    }


    if(
        selectedUnits.length === 0
    ){

        message(
            "SCV를 선택하세요."
        );

        return;

    }


    const builder =
        selectedUnits[0];


    builder.userData.target =
        gasGeyser;


    builder.userData.state =
        "movingToBuildGas";


    builder.userData.buildStart =
        null;


    buildingGas =
        true;


    showSCVStatus(builder);


    message(
        "🏗️ SCV가 가스 시설을 건설하러 이동합니다."
    );

}


// ========================================================
// RIGHT CLICK
// ========================================================

renderer.domElement.addEventListener(
    "contextmenu",
    function(event){

        event.preventDefault();


        if(
            selectedUnits.length === 0
        )
            return;


        const object =
            getObjectFromClick(
                event
            );


        // 미네랄
        if(
            object &&
            object.userData.type ===
            "mineral"
        ){

            orderMineral(
                object
            );

            return;

        }


        // 가스 시설
        if(
            object &&
            object.userData.type ===
            "gasFacility"
        ){

            orderGas(
                object
            );

            return;

        }


        mouse.x =
            event.clientX /
            window.innerWidth *
            2 - 1;


        mouse.y =
            -(event.clientY /
            window.innerHeight) *
            2 + 1;


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


        selectedUnits.forEach(
            (unit,index)=>{

                if(
                    unit.userData.type !==
                    "scv"
                )
                    return;


                const offset =
                    new THREE.Vector3(

                        (index % 3 - 1)*4,

                        0,

                        Math.floor(index/3)*4

                    );


                unit.userData.target =
                    point.clone()
                    .add(offset);


                unit.userData.state =
                    "moving";

            }
        );


        message(
            "🚩 선택된 SCV가 이동합니다."
        );

    }
);


// ========================================================
// DRAG SELECT
// ========================================================

let isMouseDown = false;

let isDragging = false;

let dragStartX = 0;

let dragStartY = 0;


const selectionBox =
    document.getElementById(
        "selectionBox"
    );


renderer.domElement.addEventListener(
    "mousedown",
    function(event){

        if(
            event.button !== 0
        )
            return;


        isMouseDown =
            true;


        isDragging =
            false;


        dragStartX =
            event.clientX;


        dragStartY =
            event.clientY;

    }
);


window.addEventListener(
    "mousemove",
    function(event){

        if(!isMouseDown)
            return;


        const distance =
            Math.sqrt(

                Math.pow(
                    event.clientX -
                    dragStartX,
                    2
                )

                +

                Math.pow(
                    event.clientY -
                    dragStartY,
                    2
                )

            );


        if(
            distance > 8
        ){

            isDragging =
                true;

        }


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
            x + "px";


        selectionBox.style.top =
            y + "px";


        selectionBox.style.width =
            width + "px";


        selectionBox.style.height =
            height + "px";


        selectionBox.style.display =
            "block";

    }
);


window.addEventListener(
    "mouseup",
    function(event){

        if(
            event.button !== 0
        )
            return;


        isMouseDown =
            false;


        if(!isDragging)
            return;


        suppressNextClick =
            true;


        isDragging =
            false;


        selectionBox.style.display =
            "none";


        const endX =
            event.clientX;


        const endY =
            event.clientY;


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


        clearSelection();


        scvs.forEach(
            scv=>{

                const screen =
                    scv.position
                        .clone()
                        .project(camera);


                const sx =
                    (screen.x+1)/2 *
                    window.innerWidth;


                const sy =
                    (-screen.y+1)/2 *
                    window.innerHeight;


                if(

                    sx >= minX &&
                    sx <= maxX &&
                    sy >= minY &&
                    sy <= maxY

                ){

                    addSelection(
                        scv
                    );

                }

            }
        );


        if(
            selectedUnits.length > 0
        ){

            showSCVStatus(
                selectedUnits[0]
            );


            message(
                "👨‍🚀 SCV " +
                selectedUnits.length +
                "기 선택됨."
            );

        }

    }
);


// ========================================================
// UNIT MOVEMENT
// ========================================================

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


    direction.y =
        0;


    const distance =
        direction.length();


    if(
        distance < 1.5
    ){

        return true;

    }


    direction.normalize();


    unit.position.add(

        direction.multiplyScalar(
            speed * delta
        )

    );


    unit.rotation.y =
        Math.atan2(
            direction.x,
            direction.z
        );


    return false;

}


// ========================================================
// MINING START
// ========================================================

function startMining(
    scv,
    type
){

    scv.userData.state =
        type === "mineral"
        ? "miningMineral"
        : "miningGas";


    scv.userData.miningStart =
        Date.now();


    scv.userData.miningDuration =
        3000;


    updateSCVStatus(scv);


    message(
        type === "mineral"
        ? "⛏️ 미네랄 채취 중... 3초"
        : "🟢 가스 채취 중... 3초"
    );

}


// ========================================================
// SCV UPDATE
// ========================================================

let lastTime =
    performance.now();


function updateSCVs(){

    const now =
        performance.now();


    const delta =
        (now-lastTime)/1000;


    lastTime =
        now;


    scvs.forEach(
        scv=>{

            const state =
                scv.userData.state;


            const target =
                scv.userData.target;


            // ==========================================
            // 일반 이동
            // ==========================================

            if(
                state === "moving" &&
                target
            ){

                if(
                    moveUnit(
                        scv,
                        target,
                        15,
                        delta
                    )
                ){

                    scv.userData.state =
                        "idle";


                    updateSCVStatus(scv);

                }

            }


            // ==========================================
            // 미네랄 이동
            // ==========================================

            if(
                state ===
                "movingToMineral" &&
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


            // ==========================================
            // 미네랄 채취
            // ==========================================

            if(
                state ===
                "miningMineral"
            ){

                const elapsed =
                    Date.now() -
                    scv.userData.miningStart;


                if(
                    elapsed >= 3000
                ){

                    scv.userData.state =
                        "returnMineral";


                    scv.userData.target =
                        commandCenter;


                    scv.userData.carrying =
                        true;


                    updateSCVStatus(scv);


                    message(
                        "📦 미네랄을 사령부로 운반합니다."
                    );

                }

            }


            // ==========================================
            // 미네랄 귀환
            // ==========================================

            if(
                state ===
                "returnMineral"
            ){

                if(
                    moveUnit(
                        scv,
                        commandCenter.position,
                        15,
                        delta
                    )
                ){

                    mineralsCount +=
                        10;


                    updateResources();


                    scv.userData.carrying =
                        false;


                    scv.userData.target =
                        scv.userData.resource;


                    scv.userData.state =
                        "movingToMineral";


                    updateSCVStatus(scv);


                    message(
                        "🏢 미네랄 전달 완료! +10"
                    );

                }

            }


            // ==========================================
            // 가스 이동
            // ==========================================

            if(
                state ===
                "movingToGas" &&
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
                        "gas"
                    );

                }

            }


            // ==========================================
            // 가스 채취
            // ==========================================

            if(
                state ===
                "miningGas"
            ){

                const elapsed =
                    Date.now() -
                    scv.userData.miningStart;


                if(
                    elapsed >= 3000
                ){

                    scv.userData.state =
                        "returnGas";


                    scv.userData.target =
                        commandCenter;


                    scv.userData.carrying =
                        true;


                    updateSCVStatus(scv);


                    message(
                        "📦 가스를 사령부로 운반합니다."
                    );

                }

            }


            // ==========================================
            // 가스 귀환
            // ==========================================

            if(
                state ===
                "returnGas"
            ){

                if(
                    moveUnit(
                        scv,
                        commandCenter.position,
                        15,
                        delta
                    )
                ){

                    gasCount +=
                        10;


                    updateResources();


                    scv.userData.carrying =
                        false;


                    scv.userData.target =
                        scv.userData.resource;


                    scv.userData.state =
                        "movingToGas";


                    updateSCVStatus(scv);


                    message(
                        "🏢 가스 전달 완료! +10"
                    );

                }

            }


            // ==========================================
            // 가스 시설 건설 이동
            // ==========================================

            if(
                state ===
                "movingToBuildGas" &&
                target
            ){

                if(
                    moveUnit(
                        scv,
                        target.position,
                        12,
                        delta
                    )
                ){

                    scv.userData.state =
                        "buildingGas";


                    scv.userData.buildStart =
                        Date.now();


                    updateSCVStatus(scv);


                    message(
                        "🏗️ 가스 시설 건설 중... 15초"
                    );

                }

            }


            // ==========================================
            // 가스 시설 건설
            // ==========================================

            if(
                state ===
                "buildingGas"
            ){

                const elapsed =
                    Date.now() -
                    scv.userData.buildStart;


                if(
                    elapsed >= 15000
                ){

                    createGasFacility();


                    scv.userData.state =
                        "idle";


                    scv.userData.target =
                        null;


                    scv.userData.buildStart =
                        null;


                    buildingGas =
                        false;


                    updateSCVStatus(scv);

                }

            }

        }
    );

}


// ========================================================
// SCV 생산
// ========================================================

document
    .getElementById(
        "scvProduceButton"
    )
    .onclick =
    function(){

        if(
            scvQueue >= 5
        ){

            message(
                "❌ 생산 대기열은 최대 5기입니다."
            );

            return;

        }


        if(
            mineralsCount < 50
        ){

            message(
                "❌ 미네랄이 부족합니다."
            );

            return;

        }


        mineralsCount -=
            50;


        scvQueue++;


        updateResources();

        updateQueue();


        message(
            "👨‍🚀 SCV 생산 대기열에 추가되었습니다."
        );


        if(
            !producingSCV
        ){

            produceSCV();

        }

    };


// ========================================================
// SCV 생산 처리
// ========================================================

function produceSCV(){

    if(
        scvQueue <= 0
    ){

        producingSCV =
            false;

        return;

    }


    producingSCV =
        true;


    scvQueue--;


    updateQueue();


    const start =
        Date.now();


    const duration =
        10000;


    const timer =
        setInterval(
            function(){

                const elapsed =
                    Date.now() -
                    start;


                if(
                    elapsed >= duration
                ){

                    clearInterval(
                        timer
                    );


                    const newSCV =
                        createSCV(
                            scvs.length
                        );


                    const n =
                        scvs.length;


                    newSCV.position.set(

                        16 +
                        (n % 3)*4,

                        0,

                        48 +
                        Math.floor(n/3)*4

                    );


                    message(
                        "👨‍🚀 SCV 생산 완료!"
                    );


                    if(
                        scvQueue > 0
                    ){

                        produceSCV();

                    }
                    else{

                        producingSCV =
                            false;

                    }

                }

            },
            100
        );

}


// ========================================================
// EDGE CAMERA
// ========================================================

let mouseX =
    window.innerWidth / 2;


let mouseY =
    window.innerHeight / 2;


window.addEventListener(
    "mousemove",
    function(event){

        mouseX =
            event.clientX;


        mouseY =
            event.clientY;

    }
);


function updateEdgeCamera(){

    const minimap =
        document.getElementById(
            "minimapContainer"
        );


    const rect =
        minimap.getBoundingClientRect();


    // 미니맵 위에서는 이동하지 않음

    if(

        mouseX >= rect.left &&
        mouseX <= rect.right &&
        mouseY >= rect.top &&
        mouseY <= rect.bottom

    ){

        return;

    }


    let dx = 0;

    let dz = 0;


    // 왼쪽

    if(
        mouseX <= EDGE_SIZE
    ){

        dx = -1;

    }


    // 오른쪽

    if(
        mouseX >=
        window.innerWidth -
        EDGE_SIZE
    ){

        dx = 1;

    }


    // 위쪽

    if(
        mouseY <= EDGE_SIZE
    ){

        dz = -1;

    }


    // 아래쪽

    if(
        mouseY >=
        window.innerHeight -
        45
    ){

        if(
            mouseY < rect.top
        ){

            dz = 1;

        }

    }


    if(
        dx === 0 &&
        dz === 0
    ){

        return;

    }


    const length =
        Math.sqrt(
            dx*dx +
            dz*dz
        );


    dx /= length;

    dz /= length;


    cameraTarget.x +=
        dx * CAMERA_SPEED;


    cameraTarget.z +=
        dz * CAMERA_SPEED;


    clampCamera();

}


// ========================================================
// CAMERA LIMIT
// ========================================================

function clampCamera(){

    const limit =
        HALF_MAP - 35;


    cameraTarget.x =
        Math.max(
            -limit,
            Math.min(
                limit,
                cameraTarget.x
            )
        );


    cameraTarget.z =
        Math.max(
            -limit,
            Math.min(
                limit,
                cameraTarget.z
            )
        );

}


// ========================================================
// CAMERA UPDATE
// ========================================================

function updateCamera(){

    camera.position.x =
        cameraTarget.x;


    camera.position.z =
        cameraTarget.z;


    camera.position.y =
        180;


    camera.lookAt(
        cameraTarget.x,
        0,
        cameraTarget.z
    );

}


// ========================================================
// MINIMAP
// ========================================================

const minimap =
    document.getElementById(
        "minimap"
    );


const miniCtx =
    minimap.getContext(
        "2d"
    );


function resizeMinimap(){

    const rect =
        minimap.getBoundingClientRect();


    const dpr =
        window.devicePixelRatio || 1;


    minimap.width =
        rect.width*dpr;


    minimap.height =
        rect.height*dpr;


    miniCtx.setTransform(
        dpr,
        0,
        0,
        dpr,
        0,
        0
    );

}


resizeMinimap();


function worldToMini(x,z){

    const width =
        minimap.clientWidth;


    const height =
        minimap.clientHeight;


    return {

        x:
            (x + HALF_MAP) /
            MAP_SIZE *
            width,

        y:
            (z + HALF_MAP) /
            MAP_SIZE *
            height

    };

}


function drawMinimap(){

    const width =
        minimap.clientWidth;


    const height =
        minimap.clientHeight;


    miniCtx.clearRect(
        0,
        0,
        width,
        height
    );


    // 배경

    miniCtx.fillStyle =
        "#18261f";


    miniCtx.fillRect(
        0,
        0,
        width,
        height
    );


    // 격자

    miniCtx.strokeStyle =
        "#294137";


    miniCtx.lineWidth =
        1;


    for(
        let i=0;
        i<=8;
        i++
    ){

        const x =
            i/8*width;


        const y =
            i/8*height;


        miniCtx.beginPath();

        miniCtx.moveTo(
            x,
            0
        );

        miniCtx.lineTo(
            x,
            height
        );

        miniCtx.stroke();


        miniCtx.beginPath();

        miniCtx.moveTo(
            0,
            y
        );

        miniCtx.lineTo(
            width,
            y
        );

        miniCtx.stroke();

    }


    // 미네랄

    mineralObjects.forEach(
        mineral=>{

            const p =
                worldToMini(
                    mineral.position.x,
                    mineral.position.z
                );


            miniCtx.fillStyle =
                "#19cfff";


            miniCtx.beginPath();

            miniCtx.arc(
                p.x,
                p.y,
                3,
                0,
                Math.PI*2
            );

            miniCtx.fill();

        }
    );


    // 가스

    if(gasGeyser){

        const p =
            worldToMini(
                gasGeyser.position.x,
                gasGeyser.position.z
            );


        miniCtx.fillStyle =
            "#25e86b";


        miniCtx.beginPath();

        miniCtx.arc(
            p.x,
            p.y,
            5,
            0,
            Math.PI*2
        );

        miniCtx.fill();

    }


    // 가스 시설

    if(gasFacility){

        const p =
            worldToMini(
                gasFacility.position.x,
                gasFacility.position.z
            );


        miniCtx.strokeStyle =
            "#8affae";


        miniCtx.lineWidth =
            2;


        miniCtx.strokeRect(
            p.x-5,
            p.y-5,
            10,
            10
        );

    }


    // 사령부

    if(commandCenter){

        const p =
            worldToMini(
                commandCenter.position.x,
                commandCenter.position.z
            );


        miniCtx.fillStyle =
            "#aaaaaa";


        miniCtx.fillRect(
            p.x-7,
            p.y-5,
            14,
            10
        );

    }


    // SCV

    scvs.forEach(
        scv=>{

            const p =
                worldToMini(
                    scv.position.x,
                    scv.position.z
                );


            miniCtx.fillStyle =
                scv.userData.selected
                ? "#ffffff"
                : "#4cb9ff";


            miniCtx.fillRect(
                p.x-2,
                p.y-2,
                4,
                4
            );

        }
    );


    // 현재 화면

    const viewSize =
        75;


    const half =
        viewSize/2;


    const left =
        worldToMini(
            cameraTarget.x-half,
            cameraTarget.z
        ).x;


    const right =
        worldToMini(
            cameraTarget.x+half,
            cameraTarget.z
        ).x;


    const top =
        worldToMini(
            cameraTarget.x,
            cameraTarget.z-half
        ).y;


    const bottom =
        worldToMini(
            cameraTarget.x,
            cameraTarget.z+half
        ).y;


    miniCtx.strokeStyle =
        "#ffffff";


    miniCtx.lineWidth =
        1.5;


    miniCtx.strokeRect(
        left,
        top,
        right-left,
        bottom-top
    );

}


// ========================================================
// MINIMAP CLICK
// ========================================================

minimap.addEventListener(
    "click",
    function(event){

        const rect =
            minimap.getBoundingClientRect();


        const x =
            event.clientX -
            rect.left;


        const y =
            event.clientY -
            rect.top;


        const worldX =
            x /
            rect.width *
            MAP_SIZE -
            HALF_MAP;


        const worldZ =
            y /
            rect.height *
            MAP_SIZE -
            HALF_MAP;


        cameraTarget.x =
            worldX;


        cameraTarget.z =
            worldZ;


        clampCamera();


        message(
            "📍 미니맵 위치로 이동했습니다."
        );

    }
);


// ========================================================
// ANIMATION
// ========================================================

function animate(){

    requestAnimationFrame(
        animate
    );


    updateEdgeCamera();

    updateCamera();

    updateSCVs();


    // 미네랄 애니메이션

    mineralObjects.forEach(
        (mineral,index)=>{

            mineral.rotation.y +=
                0.005;


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

                    child.material
                        .emissiveIntensity =
                        1.5 +
                        Math.sin(
                            Date.now()*0.004
                        );

                }

            }
        );

    }


    // 선택된 SCV 상태 업데이트

    if(
        selectedUnits.length > 0
    ){

        updateSCVStatus(
            selectedUnits[0]
        );

    }


    drawMinimap();


    renderer.render(
        scene,
        camera
    );

}


animate();


// ========================================================
// RESIZE
// ========================================================

window.addEventListener(
    "resize",
    function(){

        camera.aspect =
            window.innerWidth /
            window.innerHeight;


        camera.updateProjectionMatrix();


        renderer.setSize(
            window.innerWidth,
            window.innerHeight
        );


        resizeMinimap();

    }
);


// ========================================================
// INITIAL
// ========================================================

updateResources();

updateSCVCount();

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
