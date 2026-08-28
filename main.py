import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Terran RTS",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

GAME = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

<style>

*{
    box-sizing:border-box;
    user-select:none;
}

html,body{
    margin:0;
    width:100%;
    height:100%;
    overflow:hidden;
    background:#050809;
    font-family:Arial,sans-serif;
}

#game{
    position:fixed;
    inset:0;
}

canvas{
    display:block;
}


/* =========================================================
   종족 선택
========================================================= */

#raceScreen{
    position:fixed;
    inset:0;
    z-index:1000;

    display:flex;
    align-items:center;
    justify-content:center;

    background:
        radial-gradient(
            circle at center,
            #35434a 0%,
            #11181c 35%,
            #050708 100%
        );
}

.raceBox{
    width:460px;
    padding:45px;

    text-align:center;

    background:
        linear-gradient(
            145deg,
            rgba(54,65,70,.98),
            rgba(8,11,13,.98)
        );

    border:2px solid #7f8b90;
    border-radius:8px;

    box-shadow:
        0 0 80px rgba(0,0,0,.9);
}

.raceTitle{
    color:#edf2f3;
    font-size:45px;
    font-weight:bold;
    letter-spacing:8px;
    margin-bottom:35px;
}

.raceSub{
    color:#aeb9bd;
    margin-bottom:25px;
}

.raceButton{
    width:100%;
    padding:18px;

    color:white;

    font-size:23px;
    font-weight:bold;

    background:
        linear-gradient(
            #718086,
            #303b40
        );

    border:2px solid #a2adb1;
    border-radius:5px;

    cursor:pointer;
}

.raceButton:hover{
    background:
        linear-gradient(
            #89979c,
            #3c494e
        );
}


/* =========================================================
   자원 UI
========================================================= */

#topUI{
    position:fixed;
    top:10px;
    left:50%;

    transform:translateX(-50%);

    z-index:50;

    display:flex;
    gap:10px;
}

.resource{
    min-width:135px;

    padding:9px 16px;

    text-align:center;

    color:#eef2f3;

    background:
        rgba(5,10,13,.92);

    border:
        1px solid #69777c;

    border-radius:5px;

    box-shadow:
        0 4px 12px rgba(0,0,0,.4);
}


/* =========================================================
   상태창
========================================================= */

#sidePanel{
    position:fixed;

    top:70px;
    right:12px;

    width:290px;
    min-height:220px;

    z-index:50;

    display:none;

    padding:15px;

    color:#edf1f2;

    background:
        linear-gradient(
            145deg,
            rgba(28,36,40,.98),
            rgba(7,10,12,.98)
        );

    border:
        1px solid #738087;

    border-radius:6px;

    box-shadow:
        0 0 30px rgba(0,0,0,.8);
}

.panelTitle{
    font-size:22px;
    font-weight:bold;

    padding-bottom:10px;
    margin-bottom:10px;

    border-bottom:
        1px solid #465258;
}

.stat{
    padding:6px 0;
    color:#cbd3d6;
}

.actionButton{
    width:100%;

    padding:11px;
    margin-top:7px;

    color:white;

    background:
        linear-gradient(
            #5d6b71,
            #30393d
        );

    border:
        1px solid #849096;

    border-radius:4px;

    cursor:pointer;
}

.actionButton:hover{
    background:
        linear-gradient(
            #78878d,
            #3b474c
        );
}


/* =========================================================
   메시지
========================================================= */

#buildMessage{
    position:fixed;

    left:50%;
    bottom:105px;

    transform:translateX(-50%);

    z-index:100;

    display:none;

    padding:11px 20px;

    color:white;

    text-align:center;

    background:
        rgba(0,0,0,.85);

    border:
        1px solid #738086;

    border-radius:5px;

    box-shadow:
        0 4px 20px rgba(0,0,0,.6);
}


/* =========================================================
   드래그 선택
========================================================= */

#selectionBox{
    position:fixed;

    z-index:90;

    display:none;

    border:
        1px solid #6dbfff;

    background:
        rgba(60,160,255,.15);

    pointer-events:none;
}


/* =========================================================
   미니맵
========================================================= */

#miniMap{
    position:fixed;

    left:15px;
    bottom:15px;

    width:250px;
    height:165px;

    z-index:60;

    overflow:hidden;

    background:#132219;

    border:
        2px solid #68767b;

    border-radius:5px;

    cursor:pointer;

    box-shadow:
        0 4px 20px rgba(0,0,0,.7);
}

#miniCanvas{
    width:100%;
    height:100%;
}


/* =========================================================
   도움말
========================================================= */

#help{
    position:fixed;

    left:50%;
    bottom:15px;

    transform:translateX(-50%);

    z-index:50;

    padding:8px 14px;

    color:#b9c3c6;

    background:
        rgba(0,0,0,.65);

    border-radius:4px;

    font-size:13px;
}

</style>
</head>

<body>

<div id="game"></div>


<!-- =======================================================
     종족 선택
======================================================= -->

<div id="raceScreen">

    <div class="raceBox">

        <div class="raceTitle">
            TERRAN
        </div>

        <div class="raceSub">
            테란 기지를 선택하여 게임을 시작합니다.
        </div>

        <button
            class="raceButton"
            id="startButton"
        >
            테란으로 시작
        </button>

    </div>

</div>


<!-- =======================================================
     상단 자원
======================================================= -->

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


<!-- =======================================================
     상태창
======================================================= -->

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


<!-- =======================================================
     미니맵
======================================================= -->

<div id="miniMap">

    <canvas
        id="miniCanvas"
        width="250"
        height="165"
    ></canvas>

</div>


<div id="help">
    좌클릭: 선택 │ 좌클릭 드래그: 다중 선택 │
    우클릭: 이동 │ 화면 가장자리: 카메라 이동
</div>


<script>

/* =========================================================
   THREE 기본 설정
========================================================= */

const scene =
    new THREE.Scene();

scene.background =
    new THREE.Color(0x07100b);


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
    28
);


const renderer =
    new THREE.WebGLRenderer({
        antialias:true
    });


renderer.setSize(
    window.innerWidth,
    window.innerHeight
);


renderer.shadowMap.enabled=true;


document
    .getElementById("game")
    .appendChild(renderer.domElement);


/* =========================================================
   조명
========================================================= */

scene.add(
    new THREE.AmbientLight(
        0x89959a,
        .75
    )
);


const sun =
    new THREE.DirectionalLight(
        0xffffff,
        1.5
    );


sun.position.set(
    20,
    45,
    20
);


sun.castShadow=true;

scene.add(sun);


/* =========================================================
   게임 변수
========================================================= */

let gameStarted=false;

let minerals=500;
let gas=0;

const WORLD_SIZE=90;

const SCV_COST=50;
const SCV_BUILD_TIME=10;

const MINERAL_TIME=3;
const GAS_TIME=3;

const SCV_MINERAL_AMOUNT=50;
const SCV_GAS_AMOUNT=25;

const GAS_BUILD_TIME=15;

const MAX_SCV_QUEUE=5;

const AVOID_RADIUS=2.0;
const AVOID_FORCE=2.5;

let scvQueue=0;

let selectedUnits=[];
let selectedObject=null;

let buildMode=false;
let buildPreview=null;
let buildPreviewValid=false;
let currentBuilder=null;

const scvs=[];
const mineralNodes=[];
const geysers=[];
const gasFacilities=[];
const buildings=[];


/* =========================================================
   바닥
========================================================= */

const ground =
    new THREE.Mesh(

        new THREE.PlaneGeometry(
            WORLD_SIZE,
            WORLD_SIZE,
            30,
            30
        ),

        new THREE.MeshStandardMaterial({
            color:0x17251a,
            roughness:.95
        })
    );


ground.rotation.x=
    -Math.PI/2;


ground.receiveShadow=true;


ground.userData.type="ground";


scene.add(ground);


/* =========================================================
   맵 장식
========================================================= */

for(let i=0;i<180;i++){

    const rock =
        new THREE.Mesh(

            new THREE.DodecahedronGeometry(
                .15+Math.random()*.45,
                0
            ),

            new THREE.MeshStandardMaterial({
                color:0x2b3530
            })
        );


    rock.position.set(
        (Math.random()-.5)*82,
        .15,
        (Math.random()-.5)*82
    );


    rock.rotation.set(
        Math.random(),
        Math.random(),
        Math.random()
    );


    scene.add(rock);
}


/* =========================================================
   미네랄
   사령부에서 조금 떨어져 있음
========================================================= */

const mineralPositions=[

    [-20,-10],
    [-18,-8],
    [-16,-11],
    [-14,-9],
    [-12,-12],

    [-20,-5],
    [-18,-3],
    [-16,-6],
    [-14,-4],
    [-12,-7],

    [-20,0],
    [-18,2],
    [-16,-1],
    [-14,1],
    [-12,-2],

    [-19,5],
    [-17,7],
    [-15,4],
    [-13,6],

    [-19,10],
    [-16,11],
    [-13,9]

];


function createMineral(x,z){

    const group=
        new THREE.Group();


    for(let i=0;i<4;i++){

        const crystal=
            new THREE.Mesh(

                new THREE.DodecahedronGeometry(
                    .65+
                    Math.random()*.45,
                    0
                ),

                new THREE.MeshStandardMaterial({

                    color:0x2196ff,

                    emissive:0x064c85,

                    emissiveIntensity:.65,

                    metalness:.45,

                    roughness:.25

                })
            );


        crystal.position.set(

            (Math.random()-.5)*1.3,

            .7+
            Math.random()*.4,

            (Math.random()-.5)*1.3

        );


        crystal.scale.y=
            1.4+
            Math.random();


        crystal.rotation.set(
            Math.random(),
            Math.random(),
            Math.random()
        );


        crystal.castShadow=true;


        group.add(crystal);

    }


    group.position.set(
        x,
        0,
        z
    );


    group.userData={

        type:"mineral",

        amount:1500

    };


    mineralNodes.push(group);

    scene.add(group);

}


/* 미네랄 생성 */

mineralPositions.forEach(
    p =>
    createMineral(
        p[0],
        p[1]
    )
);


/* =========================================================
   가스 분출구
   딱 1개
========================================================= */

function createGeyser(x,z){

    const group=
        new THREE.Group();


    const rock=
        new THREE.Mesh(

            new THREE.CylinderGeometry(
                3,
                3.4,
                .6,
                24
            ),

            new THREE.MeshStandardMaterial({
                color:0x303a35,
                roughness:.9
            })
        );


    rock.position.y=.3;


    group.add(rock);


    const gasMesh=
        new THREE.Mesh(

            new THREE.CylinderGeometry(
                1.8,
                2.2,
                1.2,
                20
            ),

            new THREE.MeshStandardMaterial({

                color:0x16b765,

                emissive:0x075d30,

                emissiveIntensity:1.5,

                transparent:true,

                opacity:.72

            })
        );


    gasMesh.position.y=1;


    group.add(gasMesh);


    group.position.set(
        x,
        0,
        z
    );


    group.userData={

        type:"geyser",

        hasFacility:false,

        gasMesh:gasMesh

    };


    geysers.push(group);

    scene.add(group);

}


createGeyser(
    14,
    7
);


/* =========================================================
   사령부
========================================================= */

function createCommandCenter(){

    const group=
        new THREE.Group();


    const base=
        new THREE.Mesh(

            new THREE.BoxGeometry(
                8,
                4,
                7
            ),

            new THREE.MeshStandardMaterial({

                color:0x555f63,

                metalness:.75,

                roughness:.35

            })
        );


    base.position.y=2;

    base.castShadow=true;

    group.add(base);


    const upper=
        new THREE.Mesh(

            new THREE.BoxGeometry(
                5.5,
                1.6,
                4.7
            ),

            new THREE.MeshStandardMaterial({

                color:0x3b4549,

                metalness:.8,

                roughness:.3

            })
        );


    upper.position.y=4.7;

    group.add(upper);


    const glass=
        new THREE.Mesh(

            new THREE.BoxGeometry(
                3.3,
                1.5,
                3
            ),

            new THREE.MeshStandardMaterial({

                color:0x17445a,

                metalness:.6,

                roughness:.15,

                transparent:true,

                opacity:.85

            })
        );


    glass.position.y=5.5;

    group.add(glass);


    const antenna=
        new THREE.Mesh(

            new THREE.CylinderGeometry(
                .12,
                .12,
                4,
                10
            ),

            new THREE.MeshStandardMaterial({

                color:0x202628,

                metalness:.8

            })
        );


    antenna.position.y=8;

    group.add(antenna);


    const beacon=
        new THREE.Mesh(

            new THREE.SphereGeometry(
                .25,
                12,
                12
            ),

            new THREE.MeshBasicMaterial({
                color:0x3caeff
            })
        );


    beacon.position.y=10;

    group.add(beacon);


    for(
        let side of [-1,1]
    ){

        const module=
            new THREE.Mesh(

                new THREE.BoxGeometry(
                    1.5,
                    2,
                    5
                ),

                new THREE.MeshStandardMaterial({

                    color:0x30383b,

                    metalness:.7

                })
            );


        module.position.set(
            side*4.3,
            1.5,
            0
        );


        group.add(module);

    }


    group.userData={

        type:"commandCenter",

        hp:1500,

        maxHp:1500

    };


    buildings.push(group);

    scene.add(group);


    return group;

}


const commandCenter=
    createCommandCenter();


/* =========================================================
   SCV
========================================================= */

function createSCV(x,z){

    const group=
        new THREE.Group();


    /* 본체 */

    const body=
        new THREE.Mesh(

            new THREE.BoxGeometry(
                1.7,
                .8,
                2
            ),

            new THREE.MeshStandardMaterial({

                color:0xc3a53b,

                metalness:.6,

                roughness:.4

            })
        );


    body.position.y=.8;

    body.castShadow=true;

    group.add(body);


    /* 조종석 */

    const cabin=
        new THREE.Mesh(

            new THREE.BoxGeometry(
                1.2,
                .7,
                1
            ),

            new THREE.MeshStandardMaterial({

                color:0x59666b,

                metalness:.65,

                roughness:.25

            })
        );


    cabin.position.set(
        0,
        1.35,
        -.2
    );


    group.add(cabin);


    /* 앞 장비 */

    const drill=
        new THREE.Mesh(

            new THREE.BoxGeometry(
                1.9,
                .25,
                .55
            ),

            new THREE.MeshStandardMaterial({

                color:0x8e7628,

                metalness:.7

            })
        );


    drill.position.set(
        0,
        .75,
        -1.3
    );


    group.add(drill);


    /* 바퀴 */

    for(
        let side of [-1,1]
    ){

        for(
            let zpos of [-.7,.7]
        ){

            const wheel=
                new THREE.Mesh(

                    new THREE.CylinderGeometry(
                        .38,
                        .38,
                        .35,
                        12
                    ),

                    new THREE.MeshStandardMaterial({

                        color:0x171a1b,

                        metalness:.8

                    })
                );


            wheel.rotation.z=
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


    group.userData={

        type:"scv",

        hp:50,

        maxHp:50,

        state:"대기",

        speed:7,

        moveTarget:null,

        moveCallback:null,

        target:null,

        carryingMineral:0,

        carryingGas:0,

        selected:false,

        ignoreObstacles:false

    };


    scvs.push(group);

    scene.add(group);


    return group;

}


/* 처음 SCV 5개 */

for(let i=0;i<5;i++){

    createSCV(
        6+i*1.7,
        5
    );

}


/* =========================================================
   가스 시설
========================================================= */

function createGasFacility(geyser){

    const group=
        new THREE.Group();


    const platform=
        new THREE.Mesh(

            new THREE.CylinderGeometry(
                3.2,
                3.5,
                .7,
                24
            ),

            new THREE.MeshStandardMaterial({

                color:0x30383b,

                metalness:.8,

                roughness:.35

            })
        );


    platform.position.y=.35;

    group.add(platform);


    const ring=
        new THREE.Mesh(

            new THREE.TorusGeometry(
                2.5,
                .25,
                10,
                32
            ),

            new THREE.MeshStandardMaterial({

                color:0x737d80,

                metalness:.8

            })
        );


    ring.rotation.x=
        Math.PI/2;

    ring.position.y=.85;

    group.add(ring);


    const tank=
        new THREE.Mesh(

            new THREE.CylinderGeometry(
                1.55,
                1.85,
                3.8,
                20
            ),

            new THREE.MeshStandardMaterial({

                color:0x4b5558,

                metalness:.8,

                roughness:.35

            })
        );


    tank.position.y=2.7;

    group.add(tank);


    const top=
        new THREE.Mesh(

            new THREE.CylinderGeometry(
                1.15,
                1.15,
                .45,
                20
            ),

            new THREE.MeshStandardMaterial({

                color:0x272d2f,

                metalness:.8

            })
        );


    top.position.y=4.75;

    group.add(top);


    const core=
        new THREE.Mesh(

            new THREE.SphereGeometry(
                .85,
                20,
                20
            ),

            new THREE.MeshStandardMaterial({

                color:0x35ff91,

                emissive:0x0fae54,

                emissiveIntensity:2,

                transparent:true,

                opacity:.9

            })
        );


    core.position.y=5.2;

    group.add(core);


    /* 파이프 */

    for(
        let i=0;
        i<4;
        i++
    ){

        const angle=
            i/4*Math.PI*2;


        const pipe=
            new THREE.Mesh(

                new THREE.CylinderGeometry(
                    .16,
                    .16,
                    3.2,
                    10
                ),

                new THREE.MeshStandardMaterial({

                    color:0x242a2c,

                    metalness:.8

                })
            );


        pipe.position.set(

            Math.cos(angle)*2,

            1.9,

            Math.sin(angle)*2

        );


        group.add(pipe);

    }


    /* 가스 파티클 */

    const particles=
        new THREE.Group();


    for(let i=0;i<55;i++){

        const p=
            new THREE.Mesh(

                new THREE.SphereGeometry(
                    .07+
                    Math.random()*.12,
                    6,
                    6
                ),

                new THREE.MeshBasicMaterial({

                    color:0x45ff91,

                    transparent:true,

                    opacity:
                        .3+
                        Math.random()*.4

                })
            );


        p.position.set(

            (Math.random()-.5)*1.7,

            5.3+
            Math.random()*4,

            (Math.random()-.5)*1.7

        );


        p.userData.speed=
            .5+
            Math.random()*.8;


        particles.add(p);

    }


    group.add(particles);


    group.position.copy(
        geyser.position
    );


    group.userData={

        type:"gasFacility",

        hp:500,

        maxHp:500,

        particles:particles,

        core:core

    };


    gasFacilities.push(group);

    scene.add(group);


    return group;

}


/* =========================================================
   가스 시설 미리보기
========================================================= */

function createGasPreview(){

    const group=
        new THREE.Group();


    const mat=
        new THREE.MeshStandardMaterial({

            color:0x55ff88,

            emissive:0x227744,

            emissiveIntensity:.7,

            transparent:true,

            opacity:.35

        });


    const base=
        new THREE.Mesh(

            new THREE.CylinderGeometry(
                3.2,
                3.5,
                .7,
                24
            ),

            mat
        );


    base.position.y=.35;

    group.add(base);


    const ring=
        new THREE.Mesh(

            new THREE.TorusGeometry(
                2.5,
                .25,
                10,
                32
            ),

            mat
        );


    ring.rotation.x=
        Math.PI/2;

    ring.position.y=.85;

    group.add(ring);


    const tank=
        new THREE.Mesh(

            new THREE.CylinderGeometry(
                1.55,
                1.85,
                3.8,
                20
            ),

            mat
        );


    tank.position.y=2.7;

    group.add(tank);


    const top=
        new THREE.Mesh(

            new THREE.CylinderGeometry(
                1.15,
                1.15,
                .45,
                20
            ),

            mat
        );


    top.position.y=4.75;

    group.add(top);


    const core=
        new THREE.Mesh(

            new THREE.SphereGeometry(
                .85,
                20,
                20
            ),

            mat
        );


    core.position.y=5.2;

    group.add(core);


    group.visible=false;

    scene.add(group);

    return group;

}


buildPreview=
    createGasPreview();


/* =========================================================
   메시지
========================================================= */

function showMessage(text){

    const box=
        document.getElementById(
            "buildMessage"
        );


    box.innerHTML=text;

    box.style.display="block";


    clearTimeout(
        box.hideTimer
    );


    box.hideTimer=
        setTimeout(
            ()=>{
                box.style.display="none";
            },
            1800
        );

}


/* =========================================================
   선택 해제
========================================================= */

function clearSelection(){

    selectedUnits.forEach(
        unit=>{
            unit.userData.selected=false;
        }
    );


    selectedUnits=[];

}


/* =========================================================
   유닛 선택
========================================================= */

function selectUnit(unit){

    clearSelection();

    unit.userData.selected=true;

    selectedUnits.push(unit);

    selectedObject=unit;

    showPanel(unit);

}


/* =========================================================
   상태창
========================================================= */

function showPanel(obj){

    const panel=
        document.getElementById(
            "sidePanel"
        );


    const title=
        document.getElementById(
            "panelTitle"
        );


    const content=
        document.getElementById(
            "panelContent"
        );


    panel.style.display="block";


    /* SCV */

    if(
        obj.userData.type==="scv"
    ){

        title.innerHTML="👷 SCV";


        content.innerHTML=`

            <div class="stat">
                체력:
                ${obj.userData.hp}
                /
                ${obj.userData.maxHp}
            </div>

            <div class="stat">
                상태:
                ${obj.userData.state}
            </div>

            <div class="stat">
                건설 가능한 건물
            </div>

            <button
                class="actionButton"
                onclick="startGasBuild()"
            >
                🏗️ 가스 채취 시설 건설
            </button>

        `;

    }


    /* 사령부 */

    else if(
        obj.userData.type===
        "commandCenter"
    ){

        title.innerHTML="🏢 사령부";


        content.innerHTML=`

            <div class="stat">
                체력:
                ${obj.userData.hp}
                /
                ${obj.userData.maxHp}
            </div>

            <button
                class="actionButton"
                onclick="produceSCV()"
            >
                👷 SCV 만들기
                <br>
                💎 50 미네랄 / ⏱️ 10초
            </button>

            <div class="stat">
                생산 대기:
                <span id="queueDisplay">
                    ${scvQueue}
                </span>
                / ${MAX_SCV_QUEUE}
            </div>

        `;

    }


    /* 가스 시설 */

    else if(
        obj.userData.type===
        "gasFacility"
    ){

        title.innerHTML=
            "🟢 가스 채취 시설";


        content.innerHTML=`

            <div class="stat">
                체력:
                ${obj.userData.hp}
                /
                ${obj.userData.maxHp}
            </div>

            <div class="stat">
                가스:
                무한
            </div>

            <div class="stat">
                SCV 1회 채취량:
                ${SCV_GAS_AMOUNT}
            </div>

        `;

    }

}


/* =========================================================
   SCV 생산
========================================================= */

function produceSCV(){

    if(
        scvQueue>=MAX_SCV_QUEUE
    ){

        showMessage(
            "🔴 SCV 생산 대기열이 가득 찼습니다."
        );

        return;
    }


    if(
        minerals<SCV_COST
    ){

        showMessage(
            "🔴 미네랄이 부족합니다."
        );

        return;
    }


    minerals-=SCV_COST;

    scvQueue++;


    updateResources();

    updateQueue();


    showMessage(
        "👷 SCV 생산 시작! 10초"
    );


    setTimeout(
        ()=>{

            /*
             * 사령부 근처에 생성
             */

            const angle=
                Math.random()*
                Math.PI*2;


            const distance=7;


            createSCV(

                commandCenter.position.x+
                Math.cos(angle)*
                distance,

                commandCenter.position.z+
                Math.sin(angle)*
                distance

            );


            scvQueue--;


            updateResources();

            updateQueue();


            showMessage(
                "👷 SCV 생산 완료!"
            );

        },

        SCV_BUILD_TIME*1000
    );

}


function updateQueue(){

    const el=
        document.getElementById(
            "queueDisplay"
        );


    if(el){
        el.innerHTML=scvQueue;
    }

}


/* =========================================================
   가스 건설 모드
========================================================= */

function startGasBuild(){

    if(
        selectedUnits.length===0
    ){

        showMessage(
            "SCV를 먼저 선택하세요."
        );

        return;
    }


    const builder=
        selectedUnits.find(
            u =>
            u.userData.type==="scv"
        );


    if(!builder){

        showMessage(
            "SCV를 선택하세요."
        );

        return;
    }


    buildMode=true;

    currentBuilder=builder;

    buildPreview.visible=true;


    const message=
        document.getElementById(
            "buildMessage"
        );


    message.style.display="block";


    message.innerHTML=
        "🏗️ 가스 채취 시설 설치 위치를 선택하세요<br>" +
        "<small>가스 분출구 위에 놓으면 건설 가능합니다.</small>";

}


/* =========================================================
   미리보기 색
========================================================= */

function previewColor(hex){

    buildPreview.traverse(
        obj=>{

            if(obj.material){

                obj.material.color.setHex(
                    hex
                );

                obj.material.emissive.setHex(
                    hex
                );

            }

        }
    );

}


/* =========================================================
   건설 위치 미리보기
========================================================= */

function updateBuildPreview(){

    if(!buildMode)
        return;


    raycaster.setFromCamera(
        mouse,
        camera
    );


    const hits=
        raycaster.intersectObject(
            ground
        );


    if(!hits.length)
        return;


    const point=
        hits[0].point;


    let nearest=null;

    let nearestDistance=
        Infinity;


    geysers.forEach(
        geyser=>{

            const d=
                Math.hypot(

                    point.x-
                    geyser.position.x,

                    point.z-
                    geyser.position.z

                );


            if(
                d<nearestDistance
            ){

                nearestDistance=d;

                nearest=geyser;

            }

        }
    );


    if(
        nearest &&
        nearestDistance<5 &&
        !nearest.userData.hasFacility
    ){

        buildPreviewValid=true;


        buildPreview.position.copy(
            nearest.position
        );


        previewColor(
            0x55ff88
        );


        document.getElementById(
            "buildMessage"
        ).innerHTML=
            "🟢 건설 가능<br>" +
            "<small>좌클릭하여 건설</small>";

    }

    else{

        buildPreviewValid=false;


        buildPreview.position.set(
            point.x,
            0,
            point.z
        );


        previewColor(
            0xff3333
        );


        document.getElementById(
            "buildMessage"
        ).innerHTML=
            "🔴 건설할 수 없음<br>" +
            "<small>가스 분출구에 설치하세요.</small>";

    }

}


/* =========================================================
   가스 시설 건설 확정
========================================================= */

function confirmGasBuild(){

    if(
        !buildMode ||
        !currentBuilder
    )
        return;


    if(!buildPreviewValid){

        showMessage(
            "🔴 이 위치에는 건설할 수 없습니다."
        );

        return;
    }


    let target=null;


    geysers.forEach(
        geyser=>{

            if(
                geyser.position.distanceTo(
                    buildPreview.position
                )<.1
            ){

                target=geyser;

            }

        }
    );


    if(!target)
        return;


    buildMode=false;

    buildPreview.visible=false;


    const builder=
        currentBuilder;


    currentBuilder=null;


    builder.userData.state=
        "가스 시설 건설 중";


    builder.userData.target=
        target;


    showMessage(
        "🏗️ SCV가 가스 시설을 건설하러 갑니다."
    );


    moveUnitTo(
        builder,
        target.position,
        ()=>{

            builder.userData.state=
                "건설 중";


            showMessage(
                "🏗️ 가스 시설 건설 중... 15초"
            );


            setTimeout(
                ()=>{

                    if(
                        target.userData.hasFacility
                    )
                        return;


                    target.userData.hasFacility=
                        true;


                    createGasFacility(
                        target
                    );


                    builder.userData.state=
                        "대기";


                    builder.userData.target=
                        null;


                    showMessage(
                        "🟢 가스 채취 시설 건설 완료!"
                    );

                },

                GAS_BUILD_TIME*1000
            );

        },

        false
    );

}


/* =========================================================
   건설 취소
========================================================= */

function cancelBuild(){

    buildMode=false;

    buildPreview.visible=false;

    currentBuilder=null;


    document.getElementById(
        "buildMessage"
    ).style.display="none";

}


/* =========================================================
   장애물 회피 여부
========================================================= */

function isResourceMovement(unit){

    const state=
        unit.userData.state;


    return (

        state==="미네랄로 이동" ||

        state==="미네랄 채취 중" ||

        state==="사령부로 복귀" ||

        state==="가스 시설로 이동" ||

        state==="가스 채취 중"

    );

}


/* =========================================================
   장애물 회피 계산
========================================================= */

function getAvoidance(
    unit,
    direction
){

    const avoidance=
        new THREE.Vector3();


    /*
     * 자원 채취 관련 이동에서는
     * 장애물을 무시한다.
     */

    if(
        isResourceMovement(unit)
    ){

        return avoidance;

    }


    /* SCV끼리 피하기 */

    scvs.forEach(
        other=>{

            if(
                other===unit
            )
                return;


            const offset=
                new THREE.Vector3()
                .subVectors(
                    unit.position,
                    other.position
                );


            offset.y=0;


            const distance=
                offset.length();


            if(
                distance>0 &&
                distance<AVOID_RADIUS
            ){

                offset.normalize();


                const strength=
                    (
                        AVOID_RADIUS-
                        distance
                    )/
                    AVOID_RADIUS;


                avoidance.add(
                    offset.multiplyScalar(
                        strength*
                        AVOID_FORCE
                    )
                );

            }

        }
    );


    /* 사령부 피하기 */

    if(commandCenter){

        const offset=
            new THREE.Vector3()
            .subVectors(
                unit.position,
                commandCenter.position
            );


        offset.y=0;


        const distance=
            offset.length();


        const radius=6;


        if(
            distance>0 &&
            distance<radius
        ){

            offset.normalize();


            const strength=
                (
                    radius-distance
                )/
                radius;


            avoidance.add(
                offset.multiplyScalar(
                    strength*
                    AVOID_FORCE
                )
            );

        }

    }


    /* 가스 시설 피하기 */

    gasFacilities.forEach(
        facility=>{

            const offset=
                new THREE.Vector3()
                .subVectors(
                    unit.position,
                    facility.position
                );


            offset.y=0;


            const distance=
                offset.length();


            const radius=4;


            if(
                distance>0 &&
                distance<radius
            ){

                offset.normalize();


                const strength=
                    (
                        radius-distance
                    )/
                    radius;


                avoidance.add(
                    offset.multiplyScalar(
                        strength*
                        AVOID_FORCE
                    )
                );

            }

        }
    );


    /*
     * 미네랄은 장애물로 취급하지 않는다.
     */

    return avoidance;

}


/* =========================================================
   이동 명령
========================================================= */

function moveUnitTo(
    unit,
    target,
    callback=null,
    ignoreObstacles=false
){

    unit.userData.moveTarget=
        target.clone();


    unit.userData.moveCallback=
        callback;


    unit.userData.ignoreObstacles=
        ignoreObstacles;


    if(
        !isResourceMovement(unit)
    ){

        unit.userData.state=
            "이동 중";

    }

}


/* =========================================================
   유닛 이동 업데이트
========================================================= */

function updateUnitMovement(
    unit,
    delta
){

    const data=
        unit.userData;


    if(
        !data.moveTarget
    )
        return;


    const direction=
        new THREE.Vector3()
        .subVectors(
            data.moveTarget,
            unit.position
        );


    direction.y=0;


    const distance=
        direction.length();


    /* 도착 */

    if(
        distance<.45
    ){

        unit.userData.moveTarget=
            null;


        const callback=
            unit.userData.moveCallback;


        unit.userData.moveCallback=
            null;


        if(callback)
            callback();


        return;

    }


    direction.normalize();


    let finalDirection=
        direction.clone();


    /*
     * 일반 이동이면 장애물 회피
     *
     * 자원 채취 이동이면 무시
     */

    if(
        !data.ignoreObstacles &&
        !isResourceMovement(unit)
    ){

        const avoidance=
            getAvoidance(
                unit,
                direction
            );


        finalDirection.add(
            avoidance
        );


        if(
            finalDirection.length()>
            .01
        ){

            finalDirection.normalize();

        }

    }


    unit.position.add(

        finalDirection.multiplyScalar(
            data.speed*
            delta
        )

    );


    unit.rotation.y=
        Math.atan2(
            finalDirection.x,
            finalDirection.z
        );

}


/* =========================================================
   미네랄 채취
========================================================= */

function orderMineMineral(
    scv,
    mineral
){

    if(
        !mineral ||
        mineral.userData.amount<=0
    ){

        scv.userData.state=
            "대기";

        return;

    }


    scv.userData.target=
        mineral;


    scv.userData.state=
        "미네랄로 이동";


    /*
     * 자원 이동이므로
     * 장애물 회피를 무시
     */

    moveUnitTo(
        scv,
        mineral.position,
        ()=>{

            scv.userData.state=
                "미네랄 채취 중";


            showMessage(
                "⛏️ SCV가 미네랄을 채취합니다."
            );


            setTimeout(
                ()=>{

                    if(
                        mineral.userData.amount<=0
                    ){

                        scv.userData.state=
                            "대기";

                        return;

                    }


                    /*
                     * SCV 미네랄 획득량 = 50
                     */

                    const amount=
                        Math.min(
                            SCV_MINERAL_AMOUNT,
                            mineral.userData.amount
                        );


                    mineral.userData.amount-=
                        amount;


                    scv.userData.carryingMineral=
                        amount;


                    scv.userData.state=
                        "사령부로 복귀";


                    /*
                     * 사령부 복귀
                     * 장애물 회피 무시
                     */

                    moveUnitTo(
                        scv,
                        commandCenter.position,
                        ()=>{

                            minerals+=
                                scv.userData
                                .carryingMineral;


                            scv.userData
                                .carryingMineral=0;


                            updateResources();


                            /*
                             * 다시 같은 미네랄로 이동
                             */

                            orderMineMineral(
                                scv,
                                mineral
                            );

                        },

                        true
                    );


                },

                MINERAL_TIME*1000
            );

        },

        true
    );

}


/* =========================================================
   가스 채취
========================================================= */

function orderMineGas(
    scv,
    facility
){

    if(!facility){

        return;

    }


    /*
     * 가스는 무한이므로
     * 잔량 체크를 하지 않는다.
     */

    scv.userData.target=
        facility;


    scv.userData.state=
        "가스 시설로 이동";


    moveUnitTo(
        scv,
        facility.position,
        ()=>{

            scv.userData.state=
                "가스 채취 중";


            showMessage(
                "🟢 SCV가 가스를 채취합니다."
            );


            setTimeout(
                ()=>{

                    /*
                     * 가스 무한
                     */

                    scv.userData.carryingGas=
                        SCV_GAS_AMOUNT;


                    scv.userData.state=
                        "사령부로 복귀";


                    /*
                     * 사령부로 이동
                     */

                    moveUnitTo(
                        scv,
                        commandCenter.position,
                        ()=>{

                            gas+=
                                scv.userData
                                .carryingGas;


                            scv.userData.carryingGas=
                                0;


                            updateResources();


                            /*
                             * 다시 가스 시설로 이동
                             */

                            orderMineGas(
                                scv,
                                facility
                            );

                        },

                        true
                    );


                },

                GAS_TIME*1000
            );

        },

        true
    );

}


/* =========================================================
   레이캐스터
========================================================= */

const mouse=
    new THREE.Vector2();


const raycaster=
    new THREE.Raycaster();


let mouseDown=false;

let dragging=false;

let dragStartX=0;
let dragStartY=0;

let mouseX=0;
let mouseY=0;


/* =========================================================
   마우스 이동
========================================================= */

renderer.domElement.addEventListener(
    "mousemove",
    e=>{

        mouseX=e.clientX;
        mouseY=e.clientY;


        mouse.x=
            (
                e.clientX/
                window.innerWidth
            )*2-1;


        mouse.y=
            -(
                e.clientY/
                window.innerHeight
            )*2+1;


        if(mouseDown){

            const dx=
                e.clientX-
                dragStartX;


            const dy=
                e.clientY-
                dragStartY;


            if(
                Math.abs(dx)>5 ||
                Math.abs(dy)>5
            ){

                dragging=true;


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


/* =========================================================
   좌클릭 누름
========================================================= */

renderer.domElement.addEventListener(
    "mousedown",
    e=>{

        if(e.button!==0)
            return;


        mouseDown=true;

        dragging=false;


        dragStartX=e.clientX;

        dragStartY=e.clientY;

    }
);


/* =========================================================
   좌클릭 뗌
========================================================= */

renderer.domElement.addEventListener(
    "mouseup",
    e=>{

        if(e.button!==0)
            return;


        mouseDown=false;


        /*
         * 건설 모드
         */

        if(buildMode){

            if(!dragging){

                confirmGasBuild();

            }

            return;

        }


        /*
         * 드래그 선택
         */

        if(dragging){

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

        dragging=false;

    }
);


/* =========================================================
   우클릭
========================================================= */

renderer.domElement.addEventListener(
    "contextmenu",
    e=>{

        e.preventDefault();


        /*
         * 건설 모드에서 우클릭하면 취소
         */

        if(buildMode){

            cancelBuild();

            return;

        }


        if(
            selectedUnits.length===0
        )
            return;


        mouse.x=
            (
                e.clientX/
                window.innerWidth
            )*2-1;


        mouse.y=
            -(
                e.clientY/
                window.innerHeight
            )*2+1;


        raycaster.setFromCamera(
            mouse,
            camera
        );


        const hits=
            raycaster.intersectObject(
                ground
            );


        if(!hits.length)
            return;


        const point=
            hits[0].point;


        /*
         * 선택된 모든 SCV 이동
         */

        selectedUnits.forEach(
            unit=>{

                if(
                    unit.userData.type===
                    "scv"
                ){

                    unit.userData.target=
                        null;


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


/* =========================================================
   클릭 선택
========================================================= */

function clickSelect(x,y){

    mouse.x=
        (x/window.innerWidth)*2-1;


    mouse.y=
        -(y/window.innerHeight)*2+1;


    raycaster.setFromCamera(
        mouse,
        camera
    );


    const objects=[];


    scvs.forEach(
        x=>objects.push(x)
    );


    buildings.forEach(
        x=>objects.push(x)
    );


    gasFacilities.forEach(
        x=>objects.push(x)
    );


    mineralNodes.forEach(
        x=>objects.push(x)
    );


    geysers.forEach(
        x=>objects.push(x)
    );


    const hits=
        raycaster.intersectObjects(
            objects,
            true
        );


    if(!hits.length){

        clearSelection();


        document.getElementById(
            "sidePanel"
        ).style.display="none";


        return;

    }


    let obj=
        hits[0].object;


    while(
        obj.parent &&
        !obj.userData.type
    ){

        obj=obj.parent;

    }


    if(
        !obj.userData.type
    )
        return;


    /* 미네랄 */

    if(
        obj.userData.type===
        "mineral"
    ){

        if(
            selectedUnits.length>0
        ){

            selectedUnits.forEach(
                unit=>{

                    if(
                        unit.userData.type===
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


    /* 가스 분출구 */

    if(
        obj.userData.type===
        "geyser"
    ){

        if(
            !obj.userData.hasFacility
        ){

            showMessage(
                "🔴 가스 채취 시설을 먼저 건설하세요."
            );

            return;

        }


        const facility=
            gasFacilities.find(
                f =>
                f.position.distanceTo(
                    obj.position
                )<1
            );


        if(facility){

            selectedUnits.forEach(
                unit=>{

                    if(
                        unit.userData.type===
                        "scv"
                    ){

                        orderMineGas(
                            unit,
                            facility
                        );

                    }

                }
            );

        }

        return;

    }


    /* 가스 시설 */

    if(
        obj.userData.type===
        "gasFacility"
    ){

        /*
         * SCV가 선택되어 있으면
         * 가스 채취 명령
         */

        if(
            selectedUnits.length>0
        ){

            const hasSCV=
                selectedUnits.some(
                    u =>
                    u.userData.type===
                    "scv"
                );


            if(hasSCV){

                selectedUnits.forEach(
                    unit=>{

                        if(
                            unit.userData.type===
                            "scv"
                        ){

                            orderMineGas(
                                unit,
                                obj
                            );

                        }

                    }
                );


                return;

            }

        }


        selectObject(obj);

        return;

    }


    /* 사령부 */

    if(
        obj.userData.type===
        "commandCenter"
    ){

        clearSelection();

        selectedObject=obj;

        showPanel(obj);

        return;

    }


    /* SCV */

    if(
        obj.userData.type===
        "scv"
    ){

        selectUnit(obj);

        return;

    }

}


/* =========================================================
   일반 오브젝트 선택
========================================================= */

function selectObject(obj){

    clearSelection();

    selectedObject=obj;

    showPanel(obj);

}


/* =========================================================
   드래그 선택 박스
========================================================= */

function updateSelectionBox(
    x1,
    y1,
    x2,
    y2
){

    const box=
        document.getElementById(
            "selectionBox"
        );


    box.style.display="block";


    box.style.left=
        Math.min(x1,x2)+"px";


    box.style.top=
        Math.min(y1,y2)+"px";


    box.style.width=
        Math.abs(x2-x1)+"px";


    box.style.height=
        Math.abs(y2-y1)+"px";

}


function hideSelectionBox(){

    document.getElementById(
        "selectionBox"
    ).style.display="none";

}


/* =========================================================
   여러 SCV 선택
========================================================= */

function selectUnitsInBox(
    x1,
    y1,
    x2,
    y2
){

    clearSelection();


    const left=
        Math.min(x1,x2);


    const right=
        Math.max(x1,x2);


    const top=
        Math.min(y1,y2);


    const bottom=
        Math.max(y1,y2);


    scvs.forEach(
        scv=>{

            const screen=
                worldToScreen(
                    scv.position
                );


            if(

                screen.x>=left &&

                screen.x<=right &&

                screen.y>=top &&

                screen.y<=bottom

            ){

                scv.userData.selected=
                    true;


                selectedUnits.push(
                    scv
                );

            }

        }
    );


    if(
        selectedUnits.length>0
    ){

        showPanel(
            selectedUnits[0]
        );

    }

}


function worldToScreen(position){

    const vector=
        position.clone();


    vector.project(camera);


    return {

        x:
            (vector.x+1)/2*
            window.innerWidth,

        y:
            (-vector.y+1)/2*
            window.innerHeight

    };

}


/* =========================================================
   카메라
========================================================= */

let cameraX=0;

let cameraZ=0;

const CAMERA_EDGE=45;

const CAMERA_SPEED=.55;


function updateCamera(){

    /*
     * 왼쪽
     */

    if(
        mouseX<CAMERA_EDGE
    ){

        cameraX-=
            CAMERA_SPEED;

    }


    /*
     * 오른쪽
     */

    if(
        mouseX>
        window.innerWidth-
        CAMERA_EDGE
    ){

        cameraX+=
            CAMERA_SPEED;

    }


    /*
     * 위
     */

    if(
        mouseY<CAMERA_EDGE
    ){

        cameraZ-=
            CAMERA_SPEED;

    }


    /*
     * 아래
     */

    if(
        mouseY>
        window.innerHeight-
        CAMERA_EDGE
    ){

        cameraZ+=
            CAMERA_SPEED;

    }


    cameraX=
        THREE.MathUtils.clamp(
            cameraX,
            -38,
            38
        );


    cameraZ=
        THREE.MathUtils.clamp(
            cameraZ,
            -38,
            38
        );


    /*
     * 위에서 내려다보는 RTS 카메라
     */

    camera.position.set(
        cameraX,
        42,
        cameraZ+28
    );


    camera.lookAt(
        cameraX,
        0,
        cameraZ
    );

}


/* =========================================================
   미니맵
========================================================= */

const miniCanvas=
    document.getElementById(
        "miniCanvas"
    );


const miniCtx=
    miniCanvas.getContext(
        "2d"
    );


document
    .getElementById("miniMap")
    .addEventListener(
        "click",
        e=>{

            const rect=
                miniCanvas
                .getBoundingClientRect();


            const x=
                (
                    e.clientX-
                    rect.left
                )/
                rect.width;


            const y=
                (
                    e.clientY-
                    rect.top
                )/
                rect.height;


            cameraX=
                (x-.5)*78;


            cameraZ=
                (y-.5)*78;

        }
    );


function drawMiniMap(){

    /*
     * 배경
     */

    miniCtx.fillStyle=
        "#15251a";


    miniCtx.fillRect(
        0,
        0,
        250,
        165
    );


    /*
     * 미네랄
     */

    mineralNodes.forEach(
        m=>{

            const x=
                (m.position.x+45)/
                90*250;


            const y=
                (m.position.z+45)/
                90*165;


            miniCtx.fillStyle=
                "#29a9ff";


            miniCtx.fillRect(
                x-2,
                y-2,
                4,
                4
            );

        }
    );


    /*
     * 가스
     */

    geysers.forEach(
        g=>{

            const x=
                (g.position.x+45)/
                90*250;


            const y=
                (g.position.z+45)/
                90*165;


            miniCtx.fillStyle=
                "#32ff77";


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


    /*
     * 가스 시설
     */

    gasFacilities.forEach(
        f=>{

            const x=
                (f.position.x+45)/
                90*250;


            const y=
                (f.position.z+45)/
                90*165;


            miniCtx.fillStyle=
                "#00ff91";


            miniCtx.fillRect(
                x-4,
                y-4,
                8,
                8
            );

        }
    );


    /*
     * 사령부
     */

    const cx=
        (commandCenter.position.x+45)/
        90*250;


    const cy=
        (commandCenter.position.z+45)/
        90*165;


    miniCtx.fillStyle=
        "#eeeeee";


    miniCtx.fillRect(
        cx-6,
        cy-6,
        12,
        12
    );


    /*
     * SCV
     */

    scvs.forEach(
        s=>{

            const x=
                (s.position.x+45)/
                90*250;


            const y=
                (s.position.z+45)/
                90*165;


            miniCtx.fillStyle=
                "#e7bd42";


            miniCtx.fillRect(
                x-2,
                y-2,
                4,
                4
            );

        }
    );


    /*
     * 현재 카메라 위치
     */

    const vx=
        (cameraX+45)/
        90*250;


    const vy=
        (cameraZ+45)/
        90*165;


    miniCtx.strokeStyle=
        "#ffffff";


    miniCtx.strokeRect(
        vx-18,
        vy-12,
        36,
        24
    );

}


/* =========================================================
   자원 UI
========================================================= */

function updateResources(){

    document.getElementById(
        "minerals"
    ).innerHTML=
        minerals;


    document.getElementById(
        "gas"
    ).innerHTML=
        gas;


    document.getElementById(
        "scvCount"
    ).innerHTML=
        scvs.length;

}


/* =========================================================
   가스 파티클
========================================================= */

function animateGas(delta){

    gasFacilities.forEach(
        facility=>{

            const particles=
                facility.userData
                .particles
                .children;


            particles.forEach(
                p=>{

                    p.position.y+=
                        p.userData.speed*
                        delta;


                    if(
                        p.position.y>9.5
                    ){

                        p.position.y=5.3;


                        p.position.x=
                            (Math.random()-.5)*
                            1.7;


                        p.position.z=
                            (Math.random()-.5)*
                            1.7;

                    }

                }
            );


            const core=
                facility.userData.core;


            core.scale.setScalar(

                1+
                Math.sin(
                    performance.now()*.004
                )*.08

            );

        }
    );

}


/* =========================================================
   선택 표시
========================================================= */

function updateSelectionVisual(){

    scvs.forEach(
        scv=>{

            let ring=
                scv.getObjectByName(
                    "selectionRing"
                );


            if(
                scv.userData.selected
            ){

                if(!ring){

                    ring=
                        new THREE.Mesh(

                            new THREE.RingGeometry(
                                1.1,
                                1.3,
                                24
                            ),

                            new THREE.MeshBasicMaterial({

                                color:0x66bbff,

                                side:
                                    THREE.DoubleSide

                            })
                        );


                    ring.name=
                        "selectionRing";


                    ring.rotation.x=
                        -Math.PI/2;


                    ring.position.y=
                        .05;


                    scv.add(ring);

                }

            }

            else{

                if(ring)
                    scv.remove(ring);

            }

        }
    );

}


/* =========================================================
   게임 시작
========================================================= */

document
    .getElementById(
        "startButton"
    )
    .addEventListener(
        "click",
        ()=>{

            gameStarted=true;


            document
                .getElementById(
                    "raceScreen"
                )
                .style.display=
                    "none";


            updateResources();

        }
    );


/* =========================================================
   애니메이션
========================================================= */

let lastTime=
    performance.now();


function animate(){

    requestAnimationFrame(
        animate
    );


    const now=
        performance.now();


    const delta=
        Math.min(
            (now-lastTime)/1000,
            .05
        );


    lastTime=now;


    if(gameStarted){

        updateCamera();


        scvs.forEach(
            scv=>{

                updateUnitMovement(
                    scv,
                    delta
                );

            }
        );


        animateGas(delta);


        updateBuildPreview();


        updateSelectionVisual();


        drawMiniMap();

    }


    renderer.render(
        scene,
        camera
    );

}


animate();


/* =========================================================
   창 크기 변경
========================================================= */

window.addEventListener(
    "resize",
    ()=>{

        camera.aspect=
            window.innerWidth/
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
    GAME,
    height=900,
    scrolling=False
)
