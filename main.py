import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="StarCraft-style RTS", layout="wide")

HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>RTS Prototype</title>
<style>
*{box-sizing:border-box} html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#07100b;font-family:Arial,sans-serif}
#game{position:fixed;inset:0} canvas{display:block}
#faction{position:fixed;inset:0;background:radial-gradient(circle,#263c2c,#07100b 70%);z-index:100;display:flex;align-items:center;justify-content:center}
.card{width:430px;padding:28px;background:#101a16ee;border:1px solid #718078;border-radius:14px;box-shadow:0 20px 70px #000c;color:#fff;text-align:center}
.card h1{margin:0 0 8px;font-size:34px}.card p{color:#b9c5be}
.factionBtn{padding:18px;margin-top:18px;font-size:20px;border:1px solid #7f9a8b;border-radius:9px;background:#25372d;color:#fff;cursor:pointer}.factionBtn:hover{background:#38523f}
#hud{display:none}
#top{position:fixed;left:12px;top:12px;z-index:20;display:flex;gap:8px;color:#fff}
.res{background:#0b1310e8;border:1px solid #5e7065;border-radius:7px;padding:9px 13px}
#panel{position:fixed;right:12px;top:12px;width:270px;min-height:190px;padding:15px;color:#fff;background:#0b1310ed;border:1px solid #5e7065;border-radius:9px;z-index:30}
#panel h3{margin:0 0 12px}.stat{margin:7px 0;color:#d8e0db}
button{width:100%;padding:9px;margin-top:7px;border:1px solid #65766d;border-radius:6px;background:#26382e;color:#fff;cursor:pointer}
button:hover{background:#3b5544}button:disabled{opacity:.45;cursor:default}
#mini{position:fixed;left:12px;bottom:12px;width:250px;height:165px;z-index:30;border:2px solid #83948a;border-radius:5px;background:#1c2b20;box-shadow:0 4px 20px #0009;cursor:pointer}
#mini canvas{width:100%;height:100%}
#drag{position:fixed;z-index:50;display:none;border:1px solid #6dff82;background:#6dff8222;pointer-events:none}
#build{position:fixed;z-index:60;left:50%;top:70px;transform:translateX(-50%);display:none;padding:10px 17px;border:1px solid #ffb66b;border-radius:7px;color:#fff;background:#703b1cdd;text-align:center}
#msg{position:fixed;z-index:70;left:50%;bottom:24px;transform:translateX(-50%);padding:9px 16px;color:#fff;background:#000d;border-radius:7px;opacity:0;transition:.2s;pointer-events:none}
</style>
</head>
<body>
<div id="faction">
  <div class="card">
    <h1>STARCRAFT RTS</h1>
    <p>종족을 선택하세요.</p>
    <button class="factionBtn" onclick="startTerran()">🚀 테란</button>
  </div>
</div>

<div id="hud">
  <div id="game"></div>
  <div id="top">
    <div class="res">💎 미네랄 <b id="minerals">500</b></div>
    <div class="res">🟢 가스 <b id="gas">0</b></div>
    <div class="res">👨‍🚀 SCV <b id="scvCount">5</b></div>
    <div class="res">🏭 생산대기 <b id="queueTop">0/5</b></div>
  </div>
  <div id="panel"><h3 id="ptitle">선택 없음</h3><div id="pbody">유닛이나 건물을 선택하세요.</div></div>
  <div id="mini"><canvas id="minicanvas"></canvas></div>
  <div id="drag"></div>
  <div id="build">🏗️ 가스 채취 시설 건설 모드<br><small>가스 지역을 클릭하세요. 다른 대상을 클릭하면 취소됩니다.</small></div>
  <div id="msg"></div>
</div>

<script type="module">
import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.module.js";

let started=false;
window.startTerran=()=>{document.getElementById("faction").style.display="none";document.getElementById("hud").style.display="block";started=true};

const scene=new THREE.Scene();
scene.background=new THREE.Color(0x18241a);
scene.fog=new THREE.Fog(0x18241a,75,190);
const camera=new THREE.PerspectiveCamera(50,innerWidth/innerHeight,.1,500);
let camTarget=new THREE.Vector3(0,0,0),camHeight=55;
const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setSize(innerWidth,innerHeight);renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.shadowMap.enabled=true;document.getElementById("game").appendChild(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xd7e9ff,0x26321f,1.7));
const sun=new THREE.DirectionalLight(0xffffff,2.2);sun.position.set(30,80,25);sun.castShadow=true;scene.add(sun);

const ground=new THREE.Mesh(new THREE.PlaneGeometry(180,180),new THREE.MeshStandardMaterial({color:0x354930,roughness:1}));
ground.rotation.x=-Math.PI/2;ground.receiveShadow=true;ground.userData.type="ground";scene.add(ground);

const minerals=[],geysers=[],facilities=[],scvs=[];
let commandCenter=null,selectedUnits=[],selectedObject=null;
let mineralsAmount=500,gasAmount=0,productionQueue=0,buildMode=false,buildSCV=null;
const raycaster=new THREE.Raycaster(),mouse=new THREE.Vector2();
let mouseX=0,mouseY=0,mouseDown=false,dragStartX=0,dragStartY=0;

function M(c,r=.5,metal=.2,e=0){return new THREE.MeshStandardMaterial({color:c,roughness:r,metalness:metal,emissive:e?c:0,emissiveIntensity:e})}
function msg(t){const e=document.getElementById("msg");e.textContent=t;e.style.opacity=1;clearTimeout(msg.t);msg.t=setTimeout(()=>e.style.opacity=0,1600)}
function resources(){mineralsAmount=Math.max(0,mineralsAmount);gasAmount=Math.max(0,gasAmount);document.getElementById("minerals").textContent=Math.floor(mineralsAmount);document.getElementById("gas").textContent=Math.floor(gasAmount);document.getElementById("scvCount").textContent=scvs.length;document.getElementById("queueTop").textContent=productionQueue+"/5"}

for(let i=0;i<115;i++){
  const x=(Math.random()-.5)*170,z=(Math.random()-.5)*170;
  if(Math.abs(x)<28&&Math.abs(z)<28)continue;
  const rock=new THREE.Mesh(new THREE.DodecahedronGeometry(.35+Math.random()*.8,0),M(0x485149,.95,.05));
  rock.position.set(x,.3+Math.random()*.35,z);rock.rotation.y=Math.random()*6;rock.castShadow=true;scene.add(rock);
}

function createMineral(x,z){
  const g=new THREE.Group(),m=M(0x168cff,.25,.15,0.6);
  for(let i=0;i<6;i++){
    const h=1.5+Math.random()*1.8;
    const c=new THREE.Mesh(new THREE.CylinderGeometry(.3,.5,h,6),m);
    c.position.set((Math.random()-.5)*1.9,h/2,(Math.random()-.5)*1.9);
    c.rotation.z=(Math.random()-.5)*.3;c.rotation.y=Math.random()*6;c.castShadow=true;g.add(c);
  }
  g.position.set(x,0,z);g.userData={type:"mineral",amount:1500};minerals.push(g);scene.add(g);
}
[[-31,-11],[-29,-7],[-31,-3],[-29,1],[-31,5],[-28,9],[-25,-10],[-24,-6],[-25,-2],[-24,2],[-25,6],
[30,-12],[32,-8],[30,-4],[32,0],[30,4],[32,8],[27,-10],[28,-6],[28,-2],[27,2]].forEach(p=>createMineral(...p));

function createGeyser(x,z){
  const g=new THREE.Group();
  const rock=new THREE.Mesh(new THREE.DodecahedronGeometry(3.1,1),M(0x4c544f,.95,.1));rock.scale.y=.65;rock.position.y=1.1;rock.castShadow=true;g.add(rock);
  const hole=new THREE.Mesh(new THREE.CylinderGeometry(1.35,1.55,.35,32),M(0x102318,.35,.1,1));hole.position.y=2.35;g.add(hole);
  const gas=new THREE.Mesh(new THREE.SphereGeometry(1.35,16,16),new THREE.MeshBasicMaterial({color:0x35ff89,transparent:true,opacity:.35}));gas.position.y=3.05;g.add(gas);
  g.position.set(x,0,z);g.userData={type:"geyser",hasFacility:false,gasMesh:gas};geysers.push(g);scene.add(g);
}
createGeyser(-9,-16);createGeyser(14,-14);

function createCommand(x,z){
  const g=new THREE.Group();
  const base=new THREE.Mesh(new THREE.BoxGeometry(12,2.2,9),M(0x565f63,.4,.8));base.position.y=1.1;base.castShadow=true;g.add(base);
  const body=new THREE.Mesh(new THREE.BoxGeometry(8,5,6),M(0x747b7d,.45,.65));body.position.y=4;body.castShadow=true;g.add(body);
  const roof=new THREE.Mesh(new THREE.BoxGeometry(9,1,7),M(0x3b4448,.4,.85));roof.position.y=6.8;g.add(roof);
  const core=new THREE.Mesh(new THREE.CylinderGeometry(1.2,1.2,.6,24),new THREE.MeshStandardMaterial({color:0x55ccff,emissive:0x168cff,emissiveIntensity:1.7}));core.position.y=7.5;g.add(core);
  const tower=new THREE.Mesh(new THREE.CylinderGeometry(.12,.12,4,8),M(0x24292b,.3,.9));tower.position.y=9.3;g.add(tower);
  const lamp=new THREE.Mesh(new THREE.SphereGeometry(.3,12,12),new THREE.MeshBasicMaterial({color:0xff4433}));lamp.position.y=11.3;g.add(lamp);
  for(let s of [-1,1]){const vent=new THREE.Mesh(new THREE.BoxGeometry(1.2,.7,2.5),M(0x30373a,.35,.8));vent.position.set(s*5.1,2.3,0);g.add(vent)}
  g.position.set(x,0,z);g.userData={type:"command",hp:1500,maxHp:1500};scene.add(g);commandCenter=g;
}

function createSCV(x,z){
  const g=new THREE.Group();
  const body=new THREE.Mesh(new THREE.BoxGeometry(2.2,.8,2.8),M(0x8d9493,.35,.8));body.position.y=1;body.castShadow=true;g.add(body);
  const cabin=new THREE.Mesh(new THREE.BoxGeometry(1.5,.9,1.3),M(0x252c30,.3,.65));cabin.position.set(0,1.7,-.25);cabin.castShadow=true;g.add(cabin);
  const arm=new THREE.Mesh(new THREE.BoxGeometry(1.5,.35,1.2),M(0xb2b6b5,.4,.85));arm.position.set(0,.75,1.8);g.add(arm);
  for(const s of [-1,1])for(const p of [-.85,.85]){const w=new THREE.Mesh(new THREE.CylinderGeometry(.45,.45,.3,12),M(0x151719,.9,.05));w.rotation.z=Math.PI/2;w.position.set(s*1.15,.55,p);w.castShadow=true;g.add(w)}
  for(const s of [-.6,.6]){const l=new THREE.Mesh(new THREE.SphereGeometry(.13,10,10),new THREE.MeshBasicMaterial({color:0xffe9a3}));l.position.set(s,1.15,1.45);g.add(l)}
  g.position.set(x,0,z);g.userData={type:"scv",hp:50,maxHp:50,state:"idle",target:null,carrying:0,carryType:null,building:false,path:null};
  scvs.push(g);scene.add(g);return g;
}
[-5,-2,1,4,7].forEach((x,i)=>createSCV(x,6+(i%2)));
createCommand(0,0);

function createFacility(geyser){
  const g=new THREE.Group();
  const base=new THREE.Mesh(new THREE.CylinderGeometry(2.3,2.6,1.2,16),M(0x555d60,.4,.8));base.position.y=.7;base.castShadow=true;g.add(base);
  const tank=new THREE.Mesh(new THREE.CylinderGeometry(1.7,1.7,3.5,16),M(0x4d5558,.35,.75));tank.position.y=2.8;tank.castShadow=true;g.add(tank);
  const core=new THREE.Mesh(new THREE.SphereGeometry(1,16,16),new THREE.MeshStandardMaterial({color:0x37ff8b,emissive:0x18b85e,emissiveIntensity:1.6}));core.position.y=4.7;g.add(core);
  for(let i=0;i<3;i++){const p=new THREE.Mesh(new THREE.CylinderGeometry(.13,.13,2.7,8),M(0x202527,.3,.9));p.position.set((i-1)*.8,2.2,1.5);p.rotation.x=Math.PI/2;g.add(p)}
  g.position.copy(geyser.position);g.userData={type:"gasFacility",hp:500,maxHp:500,gas:2500};facilities.push(g);geyser.userData.hasFacility=true;scene.add(g);return g;
}
function ring(){const r=new THREE.Mesh(new THREE.RingGeometry(1.5,1.7,32),new THREE.MeshBasicMaterial({color:0x55ff55,side:THREE.DoubleSide}));r.rotation.x=-Math.PI/2;r.position.y=.06;return r}
function addSel(o){if(!o||o.userData.selectionRing)return;const r=ring();o.add(r);o.userData.selectionRing=r}
function remSel(o){if(o?.userData.selectionRing){o.remove(o.userData.selectionRing);o.userData.selectionRing=null}}
function clearSelection(){selectedUnits.forEach(remSel);if(selectedObject)remSel(selectedObject);selectedUnits=[];selectedObject=null;showPanel(null)}
function showPanel(o){
  const t=document.getElementById("ptitle"),b=document.getElementById("pbody");
  if(!o){t.textContent="선택 없음";b.textContent="유닛이나 건물을 선택하세요.";return}
  const d=o.userData;
  if(d.type==="scv"){t.textContent="SCV";b.innerHTML=`<div class="stat">❤️ 체력 ${d.hp}/50</div><div class="stat">상태: ${d.state}</div><div class="stat">운반: ${d.carrying} ${d.carryType||""}</div><button onclick="startBuild()">🏗️ 가스 채취 시설 건설</button>`}
  else if(d.type==="command"){t.textContent="사령부";b.innerHTML=`<div class="stat">❤️ 체력 ${d.hp}/${d.maxHp}</div><div class="stat">SCV 생산 대기 ${productionQueue}/5</div><button onclick="makeSCV()" ${productionQueue>=5?"disabled":""}>👨‍🚀 SCV 생산<br>💎 50 / ⏱️ 10초</button>`}
  else if(d.type==="gasFacility"){t.textContent="가스 채취 시설";b.innerHTML=`<div class="stat">❤️ 체력 ${d.hp}/${d.maxHp}</div><div class="stat">남은 가스 ${d.gas}</div><div class="stat">상태: 채취 가능</div>`}
  else if(d.type==="geyser"){t.textContent="가스 지역";b.innerHTML=`<div class="stat">${d.hasFacility?"시설 건설 완료":"시설 없음"}</div>`}
  else if(d.type==="mineral"){t.textContent="미네랄";b.innerHTML=`<div class="stat">남은 미네랄 ${d.amount}</div>`}
}
window.makeSCV=()=>{
  if(productionQueue>=5){msg("생산 대기열이 가득 찼습니다.");return}
  if(mineralsAmount<50){msg("미네랄이 부족합니다.");return}
  mineralsAmount-=50;productionQueue++;resources();showPanel(commandCenter);msg("SCV 생산 시작!");
  setTimeout(()=>{productionQueue--;createSCV(7+scvs.length*.65,2);resources();showPanel(commandCenter);msg("SCV 생산 완료!")},10000);
};
window.startBuild=()=>{
  if(!selectedUnits.length||selectedUnits[0].userData.type!=="scv"){msg("SCV를 선택하세요.");return}
  buildMode=true;buildSCV=selectedUnits[0];document.getElementById("build").style.display="block";msg("가스 지역을 클릭하세요.");
};
function moveUnitTo(u,x,z,cb=null){u.userData.path={x,z,callback:cb};u.userData.state="moving"}
function stopAuto(u){u.userData.target=null;u.userData.path=null;u.userData.carrying=0;u.userData.carryType=null;u.userData.building=false;u.userData.state="idle"}
function updateUnits(dt){
  for(const s of scvs){
    const p=s.userData.path;if(!p)continue;
    const dx=p.x-s.position.x,dz=p.z-s.position.z,dist=Math.hypot(dx,dz);
    if(dist<.3){s.position.x=p.x;s.position.z=p.z;s.userData.path=null;if(p.callback)p.callback();else s.userData.state="idle";continue}
    const speed=6;s.position.x+=dx/dist*speed*dt;s.position.z+=dz/dist*speed*dt;
    const rot=Math.atan2(dx,dz);let diff=rot-s.rotation.y;while(diff>Math.PI)diff-=Math.PI*2;while(diff<-Math.PI)diff+=Math.PI*2;s.rotation.y+=diff*Math.min(dt*8,1);
  }
}
function mineMineral(s,m){
  if(m.userData.amount<=0){msg("이 미네랄은 고갈되었습니다.");return}
  s.userData.target=m;s.userData.state="mining";moveUnitTo(s,m.position.x,m.position.z,()=>{
    setTimeout(()=>{
      if(s.userData.target!==m||m.userData.amount<=0)return;
      m.userData.amount=Math.max(0,m.userData.amount-5);s.userData.carrying=5;s.userData.carryType="mineral";
      moveUnitTo(s,commandCenter.position.x+5,commandCenter.position.z+5,()=>{
        if(s.userData.target!==m)return;mineralsAmount+=s.userData.carrying;s.userData.carrying=0;s.userData.carryType=null;mineMineral(s,m);
      });
    },3000);
  });
}
function mineGas(s,f){
  s.userData.target=f;s.userData.state="gas";moveUnitTo(s,f.position.x,f.position.z,()=>{
    setTimeout(()=>{
      if(s.userData.target!==f||f.userData.gas<=0)return;
      f.userData.gas=Math.max(0,f.userData.gas-5);s.userData.carrying=5;s.userData.carryType="gas";
      moveUnitTo(s,commandCenter.position.x+5,commandCenter.position.z+5,()=>{
        if(s.userData.target!==f)return;gasAmount+=s.userData.carrying;s.userData.carrying=0;s.userData.carryType=null;mineGas(s,f);
      });
    },3000);
  });
}
function beginConstruction(s,g){
  if(g.userData.hasFacility){msg("이미 시설이 있습니다.");return}
  s.userData.target=g;s.userData.building=true;s.userData.state="building";
  moveUnitTo(s,g.position.x,g.position.z,()=>{
    msg("가스 시설 건설 중... (15초)");
    setTimeout(()=>{
      if(!s.userData.building||s.userData.target!==g)return;
      const f=createFacility(g);s.userData.building=false;s.userData.target=f;s.userData.state="gas";mineGas(s,f);msg("가스 시설 완성!");
    },15000);
  });
}
function cancelBuild(){
  if(!buildMode)return;buildMode=false;document.getElementById("build").style.display="none";
  if(buildSCV){buildSCV.userData.building=false;buildSCV.userData.target=null;buildSCV.userData.path=null;buildSCV.userData.state="idle"}buildSCV=null;msg("건설 명령이 취소되었습니다.");
}
function setMouse(e){mouseX=e.clientX;mouseY=e.clientY;const r=renderer.domElement.getBoundingClientRect();mouse.x=((e.clientX-r.left)/r.width)*2-1;mouse.y=-((e.clientY-r.top)/r.height)*2+1}
function objectAt(){
  raycaster.setFromCamera(mouse,camera);
  const roots=[...scvs,commandCenter,...geysers,...facilities,...minerals];
  const hits=raycaster.intersectObjects(roots,true);if(!hits.length)return null;
  let o=hits[0].object;while(o.parent&&!o.userData.type)o=o.parent;return o;
}
function select(o){clearSelection();if(!o)return;selectedObject=o;addSel(o);if(o.userData.type==="scv")selectedUnits=[o];showPanel(o)}
function dragSelect(){
  const minX=Math.min(dragStartX,mouseX),maxX=Math.max(dragStartX,mouseX),minY=Math.min(dragStartY,mouseY),maxY=Math.max(dragStartY,mouseY);
  clearSelection();
  for(const s of scvs){const p=s.position.clone();p.project(camera);const x=(p.x+1)/2*innerWidth,y=(-p.y+1)/2*innerHeight;if(x>=minX&&x<=maxX&&y>=minY&&y<=maxY){selectedUnits.push(s);addSel(s)}}
  if(selectedUnits.length){selectedObject=selectedUnits[0];showPanel(selectedObject)}
}
renderer.domElement.addEventListener("mousedown",e=>{setMouse(e);if(e.button===0){mouseDown=true;dragStartX=mouseX;dragStartY=mouseY}});
renderer.domElement.addEventListener("mousemove",e=>{setMouse(e);if(mouseDown){const dx=Math.abs(mouseX-dragStartX),dy=Math.abs(mouseY-dragStartY);if(dx>5||dy>5){const b=document.getElementById("drag");b.style.display="block";b.style.left=Math.min(dragStartX,mouseX)+"px";b.style.top=Math.min(dragStartY,mouseY)+"px";b.style.width=dx+"px";b.style.height=dy+"px"}}});
renderer.domElement.addEventListener("mouseup",e=>{
  setMouse(e);if(e.button!==0)return;const dx=Math.abs(mouseX-dragStartX),dy=Math.abs(mouseY-dragStartY);mouseDown=false;document.getElementById("drag").style.display="none";
  if(dx>8||dy>8){if(buildMode)cancelBuild();else dragSelect();return}
  if(buildMode){const o=objectAt();if(o?.userData.type==="geyser"&&!o.userData.hasFacility){beginConstruction(buildSCV,o);buildMode=false;document.getElementById("build").style.display="none";buildSCV=null}else cancelBuild();return}
  select(objectAt());
});
renderer.domElement.addEventListener("contextmenu",e=>{
  e.preventDefault();setMouse(e);if(!selectedUnits.length)return;
  const o=objectAt();
  if(o?.userData.type==="mineral"){selectedUnits.forEach(s=>mineMineral(s,o));return}
  if(o?.userData.type==="gasFacility"){selectedUnits.forEach(s=>mineGas(s,o));return}
  if(o?.userData.type==="geyser"){if(!o.userData.hasFacility)beginConstruction(selectedUnits[0],o);return}
  raycaster.setFromCamera(mouse,camera);const hit=raycaster.intersectObject(ground);if(!hit.length)return;
  const p=hit[0].point,n=selectedUnits.length;
  selectedUnits.forEach((s,i)=>{stopAuto(s);const a=i/n*Math.PI*2,r=2;moveUnitTo(s,p.x+Math.cos(a)*r,p.z+Math.sin(a)*r)});
});
renderer.domElement.addEventListener("wheel",e=>{e.preventDefault();camHeight=THREE.MathUtils.clamp(camHeight+e.deltaY*.04,25,85)},{passive:false});

function updateCamera(){
  const edge=45;let dx=0,dz=0;
  if(mouseX<=edge)dx=-1;if(mouseX>=innerWidth-edge)dx=1;
  if(mouseY<=edge)dz=-1;if(mouseY>=innerHeight-edge)dz=1;
  if(dx||dz){const l=Math.hypot(dx,dz);camTarget.x+=dx/l*.7;camTarget.z+=dz/l*.7}
  camTarget.x=THREE.MathUtils.clamp(camTarget.x,-75,75);camTarget.z=THREE.MathUtils.clamp(camTarget.z,-75,75);
  camera.position.set(camTarget.x,camHeight,camTarget.z+camHeight*.87);camera.lookAt(camTarget.x,0,camTarget.z);
}
const mini=document.getElementById("minicanvas"),ctx=mini.getContext("2d");
function miniMap(){
  const w=500,h=330;mini.width=w;mini.height=h;ctx.clearRect(0,0,w,h);ctx.fillStyle="#263728";ctx.fillRect(0,0,w,h);
  const sx=x=>(x+90)/180*w,sy=z=>(z+90)/180*h;
  ctx.fillStyle="#168cff";minerals.forEach(m=>ctx.fillRect(sx(m.position.x)-4,sy(m.position.z)-4,8,8));
  ctx.fillStyle="#39ff8a";geysers.forEach(g=>{ctx.beginPath();ctx.arc(sx(g.position.x),sy(g.position.z),6,0,Math.PI*2);ctx.fill()});
  ctx.fillStyle="#fff";ctx.fillRect(sx(0)-7,sy(0)-7,14,14);
  ctx.fillStyle="#ffd34d";scvs.forEach(s=>ctx.fillRect(sx(s.position.x)-2,sy(s.position.z)-2,4,4));
  ctx.strokeStyle="#fff";ctx.strokeRect(sx(camTarget.x)-35,sy(camTarget.z)-25,70,50);
}
document.getElementById("mini").addEventListener("click",e=>{const r=e.currentTarget.getBoundingClientRect();camTarget.x=((e.clientX-r.left)/r.width)*180-90;camTarget.z=((e.clientY-r.top)/r.height)*180-90});
addEventListener("resize",()=>{camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight)});
let last=performance.now();
function animate(){
  requestAnimationFrame(animate);const now=performance.now(),dt=Math.min((now-last)/1000,.05);last=now;
  updateCamera();updateUnits(dt);resources();miniMap();
  geysers.forEach(g=>g.userData.gasMesh.scale.y=1+Math.sin(now*.003)*.12);
  if(selectedObject)showPanel(selectedObject);
  renderer.render(scene,camera);
}
resources();animate();
</script>
</body>
</html>
"""

components.html(HTML, height=900, scrolling=False)
