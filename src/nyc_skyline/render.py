"""Generate the Electric City ArcGIS SceneLayer experience."""

from __future__ import annotations

import json

SCENE_URL = (
    "https://services2.arcgis.com/cFEFS0EWrhfDeVw9/arcgis/rest/services/"
    "showcases_manhattan_buildings/SceneServer"
)

STATUE_SCENE_URL = (
    "https://tiles.arcgis.com/tiles/GzteEaZqBuJ6GIYr/arcgis/rest/services/"
    "StatueOfLiberty2/SceneServer"
)

# Torch tip derived from the highest vertex in the georeferenced public mesh.
STATUE_LOCATION = (-74.04457407, 40.68920027)
TORCH_ELEVATION_METERS = 90.31

NAMED_BUILDINGS_WHERE = "NAME IS NOT NULL AND NAME <> ''"

# Queens-bound BQE Central, from the Atlantic Avenue approach toward Sands Street.
BQE_ROUTE = (
    (-74.00414, 40.68472),
    (-74.00297, 40.68440),
    (-74.00236, 40.68575),
    (-74.00172, 40.68708),
    (-74.00092, 40.68874),
    (-74.00015, 40.69025),
    (-73.99924, 40.69283),
    (-73.99890, 40.69426),
    (-73.99838, 40.69537),
    (-73.99647, 40.69938),
    (-73.99541, 40.70052),
    (-73.99354, 40.70130),
    (-73.99216, 40.70156),
    (-73.99039, 40.70076),
)

HEIGHT_CLASSES = (
    (0, 120, "Street glow", [0, 224, 255, 0.9]),
    (120, 300, "City violet", [112, 54, 255, 0.92]),
    (300, 700, "Dream magenta", [255, 48, 144, 0.94]),
    (700, 2000, "Skyline gold", [255, 174, 74, 0.98]),
)


def mesh_symbol(color: list[float]) -> dict:
    return {
        "type": "mesh-3d",
        "symbolLayers": [{
            "type": "fill",
            "material": {"color": color[:3], "colorMixMode": "replace"},
            "edges": {"type": "solid", "color": [255, 105, 210, 0.2], "size": 0.35},
        }],
    }


def scene_renderer() -> dict:
    return {
        "type": "class-breaks",
        "field": "HEIGHTROOF",
        "defaultSymbol": mesh_symbol([36, 16, 64, 0.7]),
        "classBreakInfos": [
            {"minValue": low, "maxValue": high, "label": label, "symbol": mesh_symbol(color)}
            for low, high, label, color in HEIGHT_CLASSES
        ],
    }


def build_html() -> str:
    renderer = json.dumps(scene_renderer(), separators=(",", ":"))
    bqe_route = json.dumps(BQE_ROUTE, separators=(",", ":"))
    legend = "".join(
        f'<span class="legend-item" tabindex="0" data-range="{low:,}–{high:,} ft" '
        f'aria-label="{label}: {low:,} to {high:,} feet"><i '
        f'style="--swatch:rgb({color[0]},{color[1]},{color[2]})"></i>{label}</span>'
        for low, high, label, color in HEIGHT_CLASSES
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<meta name="theme-color" content="#030814" />
<title>Electric City · City of Dreams</title>
<link rel="stylesheet" href="https://js.arcgis.com/4.33/esri/themes/dark/main.css" />
<style>
html,body,#viewDiv{{width:100%;height:100%;margin:0;background:#030814;overflow:hidden}}
body{{font-family:Inter,ui-sans-serif,system-ui,sans-serif;color:#f7fbff}}#viewDiv{{position:absolute;inset:0}}
.brand{{position:fixed;z-index:3;top:28px;left:34px;pointer-events:none;text-shadow:0 3px 24px #030814}}
.brand p{{margin:0 0 8px;color:#ff3090;font-size:11px;font-weight:850;letter-spacing:.19em}}
.brand h1{{margin:0;font-size:46px;line-height:.98;letter-spacing:-.06em}}
.brand em{{display:block;margin-top:10px;color:#b7c7d8;font-size:13px;font-style:normal}}
.controls{{position:fixed;z-index:4;right:22px;top:22px;display:flex;gap:6px;padding:6px;border:1px solid #273e58;border-radius:12px;background:#07111fda;backdrop-filter:blur(10px)}}
.brand,.controls,.search-panel,.legend{{transition:opacity .65s ease}}body.intro .brand,body.intro .controls,body.intro .search-panel,body.intro .legend{{opacity:0;pointer-events:none}}
button{{border:0;border-radius:8px;padding:8px 11px;background:transparent;color:#b7c7d8;font:700 11px Inter,system-ui;letter-spacing:.04em;cursor:pointer}}
button:hover,button.active{{background:#ff3090;color:white}}
.search-panel{{position:fixed;z-index:5;left:76px;bottom:22px;width:286px;padding:12px;border:1px solid #273e58;border-radius:12px;background:#07111fea;box-shadow:0 12px 34px #0008;backdrop-filter:blur(12px)}}
.search-panel>label:first-child{{display:block;margin-bottom:7px;color:#f7fbff;font-size:10px;font-weight:850;letter-spacing:.12em}}.search-row{{display:flex;gap:6px}}.search-row input{{min-width:0;flex:1;padding:9px 10px;border:1px solid #35516e;border-radius:8px;outline:0;background:#030814;color:#fff;font:12px Inter,system-ui}}.search-row input:focus{{border-color:#ff3090;box-shadow:0 0 0 2px #ff309033}}.search-row button{{background:#ff3090;color:#fff}}.search-row button:disabled{{cursor:wait;opacity:.45}}
.search-results{{position:absolute;left:0;right:0;bottom:calc(100% + 8px);max-height:280px;margin:0;padding:6px;overflow:auto;list-style:none;border:1px solid #35516e;border-radius:12px;background:#07111ff7;box-shadow:0 -16px 38px #000a}}.search-results[hidden]{{display:none}}.search-results button{{display:flex;width:100%;align-items:center;justify-content:space-between;gap:12px;padding:9px 10px;text-align:left;color:#dbe8f4}}.search-results button:hover,.search-results button:focus{{background:#ff3090;color:#fff;outline:0}}.search-results span{{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}.search-results small{{flex:none;color:#91a6bb;font-size:9px}}.search-results button:hover small,.search-results button:focus small{{color:#fff}}
.filter-toggle{{display:flex;align-items:center;gap:7px;margin-top:10px;color:#b7c7d8;font-size:10px;cursor:pointer}}.filter-toggle input{{accent-color:#ff3090}}#searchStatus{{display:block;margin-top:7px;color:#71889e;font-size:9px}}
.legend{{position:fixed;z-index:3;right:22px;bottom:22px;padding:12px 14px;border:1px solid #273e58;border-radius:12px;background:#07111fda;backdrop-filter:blur(10px);font-size:10px;color:#91a6bb}}
.legend b{{display:block;color:#f7fbff;font-size:11px;letter-spacing:.08em;margin-bottom:7px}}.legend b small{{color:#91a6bb;font-size:8px;margin-left:8px}}
.legend-item{{position:relative;display:inline-flex;align-items:center;margin-right:10px;outline:none;cursor:help}}.legend i{{width:8px;height:8px;border-radius:50%;margin-right:5px;background:var(--swatch);box-shadow:0 0 8px var(--swatch)}}
.legend-item::after{{content:attr(data-range);position:absolute;left:50%;bottom:calc(100% + 10px);transform:translate(-50%,5px);padding:6px 8px;border:1px solid #35516e;border-radius:7px;background:#030814;color:#fff;font-size:10px;font-weight:750;white-space:nowrap;opacity:0;pointer-events:none;transition:.18s}}
.legend-item:hover::after,.legend-item:focus::after{{opacity:1;transform:translate(-50%,0)}}
.inspector{{position:fixed;z-index:7;width:238px;padding:16px;border:1px solid #ff3090;border-radius:12px;background:#07111ff2;box-shadow:0 12px 44px #000b,0 0 24px #ff309033;backdrop-filter:blur(14px)}}
.inspector[hidden]{{display:none}}.inspector h2{{margin:0 24px 12px 0;color:#fff;font-size:16px;line-height:1.15}}.inspector dl{{display:grid;grid-template-columns:1fr auto;gap:7px 12px;margin:0;font-size:11px}}.inspector dt{{color:#91a6bb}}.inspector dd{{margin:0;color:#f7fbff;font-weight:750;text-align:right}}.inspector-close{{position:absolute;top:7px;right:7px;padding:4px 7px;color:#91a6bb;font-size:16px;line-height:1}}.inspector-close:hover{{background:#ff3090;color:#fff}}
.drive-intro{{position:fixed;z-index:6;inset:0;overflow:hidden;pointer-events:none;opacity:1;transition:opacity .9s ease,background-color .65s ease;background:radial-gradient(circle at 50% 55%,transparent 0 30%,#03081488 80%),linear-gradient(180deg,#03081433,#03081499)}}.drive-intro[hidden]{{display:none}}.drive-intro::before{{content:"";position:absolute;inset:0;background:repeating-linear-gradient(180deg,transparent 0 3px,#77fff508 3px 4px);mix-blend-mode:screen}}.drive-intro.slowmo::before{{animation:scan .8s linear infinite}}.drive-intro.to-map{{background-color:#030814}}.drive-intro.done{{opacity:0}}
.drive-hud{{position:absolute;left:50%;bottom:8%;width:min(620px,82vw);transform:translateX(-50%);text-align:center;text-shadow:0 3px 20px #000}}.drive-kicker{{margin:0;color:#23e8ff;font-size:11px;font-weight:900;letter-spacing:.25em}}.drive-hud h2{{margin:8px 0 5px;color:#fff;font-size:clamp(28px,5vw,62px);font-style:italic;line-height:.95;letter-spacing:-.05em;text-transform:uppercase}}.drive-stage{{color:#ff3090;font-size:12px;font-weight:850;letter-spacing:.16em}}.drive-speed{{position:absolute;right:5%;bottom:8%;color:#ffae4a;font:900 34px/1 Inter,system-ui;font-style:italic}}.drive-speed small{{display:block;color:#91a6bb;font-size:8px;letter-spacing:.16em;text-align:right}}.skip-drive{{position:absolute;top:24px;right:24px;z-index:2;pointer-events:auto;border:1px solid #35516e;background:#07111fdd}}@keyframes scan{{to{{transform:translateY(4px)}}}}
.orbit-hud{{position:fixed;z-index:5;top:132px;left:34px;padding:10px 13px;border:1px solid #ffae4a66;border-radius:10px;background:#07111fdd;box-shadow:0 0 24px #ffae4a22;backdrop-filter:blur(10px);pointer-events:none}}.orbit-hud[hidden]{{display:none}}.orbit-hud b{{display:block;color:#ffae4a;font-size:9px;letter-spacing:.16em}}.orbit-hud span{{display:block;margin-top:4px;color:#f7fbff;font-size:11px;font-weight:750}}.orbit-hud small{{display:block;margin-top:3px;color:#91a6bb;font-size:8px;letter-spacing:.06em}}
#loading{{position:fixed;z-index:8;inset:0;display:grid;place-items:center;background:#030814;color:#ff3090;font-size:11px;font-weight:800;letter-spacing:.2em;transition:opacity .7s}}
.esri-ui-corner{{top:112px}}@media(max-width:700px){{.brand{{top:18px;left:18px}}.brand h1{{font-size:34px}}.search-panel{{left:14px;right:14px;bottom:150px;width:auto}}.controls{{top:auto;bottom:14px;left:14px;right:14px;overflow:auto}}.legend{{left:14px;right:14px;bottom:68px}}.legend b small{{display:block;margin:4px 0 0}}.legend-item{{margin-bottom:3px}}.inspector{{left:14px!important;right:14px;top:auto!important;bottom:310px;width:auto}}.drive-speed{{right:18px;bottom:18%}}.skip-drive{{top:14px;right:14px}}}}
@media(prefers-reduced-motion:reduce){{*{{scroll-behavior:auto!important}}.drive-intro{{display:none!important}}}}
</style><script src="https://js.arcgis.com/4.33/"></script></head>
<body class="intro"><div id="viewDiv"></div><div id="loading">STREAMING MANHATTAN · CITY OF DREAMS</div>
<section id="driveIntro" class="drive-intro" hidden aria-label="BQE night-drive introduction"><button id="skipDrive" class="skip-drive">SKIP DRIVE</button><div class="drive-hud"><p class="drive-kicker">I-278 · QUEENS-BOUND · 2:13 AM</p><h2>Electric City</h2><div id="driveStage" class="drive-stage">BQE NIGHT RUN</div></div><div class="drive-speed"><span id="driveSpeedValue">88</span><small>MPH</small></div></section>
<aside id="orbitHud" class="orbit-hud" hidden><b>DAY / NIGHT ORBIT</b><span id="orbitTime"></span><small>MOVE · CLICK · TYPE TO WAKE</small></aside>
<header class="brand"><p>MANHATTAN AFTER MIDNIGHT · PYTHON × PUBLIC 3D DATA</p><h1>Electric City</h1><em>City of Dreams. The real skyline, recoded in neon.</em></header>
<section class="search-panel" aria-label="Search named Manhattan buildings"><ul id="searchResults" class="search-results" role="listbox" hidden></ul><label for="buildingSearch">FIND A NAMED BUILDING</label><div class="search-row"><input id="buildingSearch" type="search" placeholder="Loading building names…" autocomplete="off" aria-controls="searchResults" aria-autocomplete="list" disabled /><button id="searchGo" disabled>GO</button></div><label class="filter-toggle"><input id="namedOnly" type="checkbox" disabled /> Show only named buildings</label><small id="searchStatus" aria-live="polite">Loading the 717 known names…</small></section>
<nav class="controls" aria-label="Camera views"><button id="replayDrive">BQE Run</button><button class="active" data-view="skyline">Skyline</button><button data-view="liberty">Liberty</button><button data-view="downtown">Downtown</button><button data-view="midtown">Midtown</button><button data-view="uptown">Uptown</button></nav>
<aside class="legend"><b>BUILDING HEIGHT <small>HOVER COLORS · CLICK BUILDINGS</small></b>{legend}</aside>
<section id="inspector" class="inspector" hidden aria-live="polite"><button id="inspectorClose" class="inspector-close" aria-label="Close building details">×</button><h2 id="inspectorTitle"></h2><dl id="inspectorFields"></dl></section>
<script>require(["esri/Map","esri/views/SceneView","esri/layers/SceneLayer","esri/layers/GraphicsLayer","esri/Graphic","esri/core/reactiveUtils"],function(EsriMap,SceneView,SceneLayer,GraphicsLayer,Graphic,reactiveUtils){{
const buildings=new SceneLayer({{url:{json.dumps(SCENE_URL)},renderer:{renderer},popupEnabled:true,popupTemplate:{{title:"{{NAME}}",content:[{{type:"fields",fieldInfos:[{{fieldName:"HEIGHTROOF",label:"Roof height (ft)",format:{{places:0,digitSeparator:true}}}},{{fieldName:"NUM_FLOORS",label:"Floors",format:{{places:0,digitSeparator:true}}}},{{fieldName:"CNSTRCT_YR",label:"Construction year",format:{{places:0,digitSeparator:false}}}},{{fieldName:"GROUNDELEV",label:"Ground elevation (ft)",format:{{places:0,digitSeparator:true}}}}]}}]}},outFields:["OBJECTID","NAME","HEIGHTROOF","NUM_FLOORS","CNSTRCT_YR","GROUNDELEV"]}});
const liberty=new SceneLayer({{url:{json.dumps(STATUE_SCENE_URL)},title:"Statue of Liberty",renderer:{{type:"simple",symbol:{{type:"mesh-3d",symbolLayers:[{{type:"fill",material:{{color:[62,196,174],colorMixMode:"tint"}},edges:{{type:"solid",color:[137,255,226,.65],size:.45}}}}]}}}},popupTemplate:{{title:"Statue of Liberty",content:"<b>Liberty Enlightening the World</b><br>Dedicated October 28, 1886<br>Ground to torch: 305 ft (93 m)<br><br>Public 3D mesh positioned on Liberty Island."}}}});
const torch=new GraphicsLayer({{title:"Liberty's torch",elevationInfo:{{mode:"absolute-height"}},listMode:"hide"}});
torch.add(new Graphic({{geometry:{{type:"point",longitude:{STATUE_LOCATION[0]},latitude:{STATUE_LOCATION[1]},z:{TORCH_ELEVATION_METERS},spatialReference:{{wkid:4326}}}},symbol:{{type:"point-3d",symbolLayers:[{{type:"object",resource:{{primitive:"sphere"}},material:{{color:[255,184,66,.98]}},height:5,width:3,depth:3}},{{type:"icon",resource:{{primitive:"circle"}},material:{{color:[255,126,38,.18]}},size:34,outline:{{color:[255,174,74,.28],size:1}}}},{{type:"icon",resource:{{primitive:"circle"}},material:{{color:[255,224,140,.72]}},size:10}}]}},popupTemplate:{{title:"The Torch",content:"A beacon of enlightenment, glowing 305 ft (93 m) above Liberty Island."}}}}));
const moonLayer=new GraphicsLayer({{title:"Simulated moon",elevationInfo:{{mode:"absolute-height"}},listMode:"hide",visible:false}});
const moonGraphic=new Graphic({{symbol:{{type:"point-3d",symbolLayers:[{{type:"icon",resource:{{primitive:"circle"}},material:{{color:[218,234,255,.9]}},size:24,outline:{{color:[255,255,255,.8],size:1}}}},{{type:"icon",resource:{{primitive:"circle"}},material:{{color:[148,194,255,.16]}},size:48}}]}}}});moonLayer.add(moonGraphic);
const bqeRoute={bqe_route};
const introRoad=new GraphicsLayer({{title:"BQE night run",elevationInfo:{{mode:"relative-to-ground"}},listMode:"hide"}});
const routeGeometry={{type:"polyline",paths:[bqeRoute.map(([longitude,latitude])=>[longitude,latitude,1])],spatialReference:{{wkid:4326}}}};
introRoad.addMany([new Graphic({{geometry:routeGeometry,symbol:{{type:"line-3d",symbolLayers:[{{type:"line",material:{{color:[255,48,144,.18]}},size:13}}]}}}}),new Graphic({{geometry:routeGeometry,symbol:{{type:"line-3d",symbolLayers:[{{type:"line",material:{{color:[35,232,255,.95]}},size:2.5}}]}}}})]);
const map=new EsriMap({{basemap:"dark-gray-vector",ground:"world-elevation",layers:[buildings,liberty,torch,moonLayer]}});
const NAMED_WHERE={json.dumps(NAMED_BUILDINGS_WHERE)};
const cameras={{skyline:{{position:{{longitude:-74.080,latitude:40.660,z:5000}},heading:28,tilt:65}},liberty:{{position:{{longitude:-74.052,latitude:40.682,z:230}},heading:38,tilt:73}},downtown:{{position:{{longitude:-74.027,latitude:40.700,z:720}},heading:28,tilt:72}},midtown:{{position:{{longitude:-74.005,latitude:40.738,z:900}},heading:24,tilt:70}},uptown:{{position:{{longitude:-73.985,latitude:40.785,z:1050}},heading:25,tilt:67}}}};
const driveCameras=[{{position:{{longitude:-74.00414,latitude:40.68472,z:45}},heading:18,tilt:84}},{{position:{{longitude:-74.00015,latitude:40.69025,z:48}},heading:8,tilt:84}},{{position:{{longitude:-73.99838,latitude:40.69537,z:62}},heading:322,tilt:82}},{{position:{{longitude:-73.99354,latitude:40.70130,z:72}},heading:58,tilt:82}}];
const reduceMotion=window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const view=new SceneView({{container:"viewDiv",map,qualityProfile:"high",camera:reduceMotion?cameras.skyline:driveCameras[0],popupEnabled:false,popup:{{dockEnabled:false,collapseEnabled:false}},environment:{{background:{{type:"color",color:[3,8,20,1]}},starsEnabled:true,atmosphereEnabled:true,lighting:{{type:"virtual",directShadowsEnabled:true,ambientOcclusionEnabled:true}}}},highlightOptions:{{color:[255,174,74],fillOpacity:.35,haloOpacity:.9}}}});
const inspector=document.getElementById("inspector"),inspectorTitle=document.getElementById("inspectorTitle"),inspectorFields=document.getElementById("inspectorFields");
const searchInput=document.getElementById("buildingSearch"),searchGo=document.getElementById("searchGo"),searchResults=document.getElementById("searchResults"),namedOnly=document.getElementById("namedOnly"),searchStatus=document.getElementById("searchStatus");
const driveIntro=document.getElementById("driveIntro"),driveStage=document.getElementById("driveStage"),driveSpeedValue=document.getElementById("driveSpeedValue");
const orbitHud=document.getElementById("orbitHud"),orbitTime=document.getElementById("orbitTime");
const orbitFormatter=new Intl.DateTimeFormat("en-US",{{timeZone:"America/New_York",weekday:"short",month:"short",day:"numeric",hour:"numeric",minute:"2-digit"}});
let buildingLayerView,highlight;
let namedBuildingRecords=[];
let driveRun=0;
let idleTimer,orbitTimer,orbitActive=false,sunCalc,sunCalcPromise,simulatedTime=new Date(),lastActivity=0;
function closeInspector(){{inspector.hidden=true;highlight?.remove();highlight=null;}}
function showInspector(title,rows,event){{inspectorTitle.textContent=title;inspectorFields.replaceChildren();rows.forEach(([label,value])=>{{const dt=document.createElement("dt"),dd=document.createElement("dd");dt.textContent=label;dd.textContent=value;inspectorFields.append(dt,dd);}});inspector.hidden=false;inspector.style.left=`${{Math.max(12,Math.min(event.x+18,window.innerWidth-286))}}px`;inspector.style.top=`${{Math.max(12,Math.min(event.y+18,window.innerHeight-230))}}px`;}}
function number(value,suffix=""){{if(value==null||value==="")return "Not recorded";const parsed=Number(value);return Number.isFinite(parsed)?`${{Math.round(parsed).toLocaleString()}}${{suffix}}`:"Not recorded";}}
async function buildingAttributes(feature){{const attrs=feature.attributes||{{}},fields=["NAME","HEIGHTROOF","NUM_FLOORS","CNSTRCT_YR","GROUNDELEV"];if(fields.every(field=>Object.hasOwn(attrs,field))||attrs.OBJECTID==null)return attrs;const query=buildings.createQuery();query.objectIds=[attrs.OBJECTID];query.outFields=["OBJECTID",...fields];query.returnGeometry=false;const result=await buildings.queryFeatures(query);return result.features[0]?.attributes||attrs;}}
async function loadNamedBuildings(){{const query=buildings.createQuery();query.where=NAMED_WHERE;query.outFields=["OBJECTID","NAME","CNSTRCT_YR"];query.returnGeometry=false;query.orderByFields=["NAME ASC"];const result=await buildings.queryFeatures(query);namedBuildingRecords=result.features.map(feature=>({{id:feature.attributes.OBJECTID,name:String(feature.attributes.NAME||"").trim(),year:feature.attributes.CNSTRCT_YR}})).filter(record=>record.name).sort((a,b)=>a.name.localeCompare(b.name));searchInput.disabled=false;searchGo.disabled=false;searchInput.placeholder="Empire State Building…";searchStatus.textContent=`${{namedBuildingRecords.length.toLocaleString()}} named buildings ready`;}}
function findNamedBuilding(value){{const term=value.trim().toLocaleLowerCase();if(!term)return null;return namedBuildingRecords.find(record=>record.name.toLocaleLowerCase()===term)||namedBuildingRecords.find(record=>record.name.toLocaleLowerCase().startsWith(term))||namedBuildingRecords.find(record=>record.name.toLocaleLowerCase().includes(term));}}
function renderSearchResults(){{const term=searchInput.value.trim().toLocaleLowerCase();const matches=(term?namedBuildingRecords.filter(record=>record.name.toLocaleLowerCase().includes(term)):namedBuildingRecords).slice(0,12);searchResults.replaceChildren();matches.forEach(record=>{{const item=document.createElement("li"),button=document.createElement("button"),name=document.createElement("span"),year=document.createElement("small");button.type="button";button.setAttribute("role","option");name.textContent=record.name;year.textContent=number(record.year);button.append(name,year);button.addEventListener("click",()=>jumpToNamedBuilding(record));item.append(button);searchResults.append(item);}});searchResults.hidden=!matches.length;}}
async function jumpToNamedBuilding(selectedRecord=null){{const record=selectedRecord||findNamedBuilding(searchInput.value);if(!record){{searchStatus.textContent="No named building matches that search";searchResults.hidden=true;return;}}searchInput.value=record.name;searchResults.hidden=true;searchGo.disabled=true;searchStatus.textContent=`Flying to ${{record.name}}…`;try{{const [extentResult,attrs]=await Promise.all([buildings.queryExtent({{objectIds:[record.id]}}),buildingAttributes({{attributes:{{OBJECTID:record.id}}}})]);if(!extentResult.extent)throw new Error("No building extent returned");document.querySelectorAll("[data-view]").forEach(item=>item.classList.remove("active"));await view.goTo({{target:extentResult.extent.expand(6),heading:25,tilt:68}},{{duration:1800,easing:"ease-in-out"}});showInspector(attrs.NAME||record.name,[["Building name",attrs.NAME||record.name],["Year built",number(attrs.CNSTRCT_YR)],["Roof height",number(attrs.HEIGHTROOF," ft")],["Floors",number(attrs.NUM_FLOORS)],["Ground elevation",number(attrs.GROUNDELEV," ft")]],{{x:window.innerWidth*.55,y:110}});highlight?.remove();highlight=buildingLayerView?.highlight(record.id)||null;searchStatus.textContent=`Showing ${{record.name}}`;}}catch(error){{searchStatus.textContent="Could not open that building";console.error("Electric City named-building search failed",error);}}finally{{searchGo.disabled=false;}}}}
const pause=milliseconds=>new Promise(resolve=>setTimeout(resolve,milliseconds));
function loadSunCalc(){{return sunCalcPromise||(sunCalcPromise=import("https://cdn.jsdelivr.net/npm/suncalc@2.0.1/+esm").then(module=>(sunCalc=module)));}}
function updateMoon(date){{if(!sunCalc)return;const position=sunCalc.getMoonPosition(date,40.758,-73.9855),illumination=sunCalc.getMoonIllumination(date);if(position.altitude<=-1){{moonLayer.visible=false;return;}}const altitude=position.altitude*Math.PI/180,azimuth=position.azimuth*Math.PI/180,range=60000,horizontal=Math.cos(altitude)*range,earthRadius=6371000,angular=horizontal/earthRadius,observer=view.camera.position,latitude=(observer.latitude??40.758)*Math.PI/180,longitude=(observer.longitude??-73.9855)*Math.PI/180,targetLatitude=Math.asin(Math.sin(latitude)*Math.cos(angular)+Math.cos(latitude)*Math.sin(angular)*Math.cos(azimuth)),targetLongitude=longitude+Math.atan2(Math.sin(azimuth)*Math.sin(angular)*Math.cos(latitude),Math.cos(angular)-Math.sin(latitude)*Math.sin(targetLatitude)),brightness=.45+illumination.fraction*.5,curvature=horizontal*horizontal/(2*earthRadius);moonGraphic.geometry={{type:"point",longitude:targetLongitude*180/Math.PI,latitude:targetLatitude*180/Math.PI,z:(observer.z||0)+Math.sin(altitude)*range+curvature,spatialReference:{{wkid:4326}}}};moonGraphic.symbol={{type:"point-3d",symbolLayers:[{{type:"icon",resource:{{primitive:"circle"}},material:{{color:[218,234,255,brightness]}},size:22+illumination.fraction*7,outline:{{color:[255,255,255,.8],size:1}}}},{{type:"icon",resource:{{primitive:"circle"}},material:{{color:[148,194,255,.14]}},size:48}}]}};moonLayer.visible=true;}}
function updateOrbit(){{simulatedTime=new Date(simulatedTime.getTime()+288000);view.environment.lighting.date=simulatedTime;const illumination=sunCalc?.getMoonIllumination(simulatedTime),moon=illumination?illumination.phase<.125?"●":illumination.phase<.375?"◐":illumination.phase<.625?"○":illumination.phase<.875?"◑":"●":"";orbitTime.textContent=`${{moon}} ${{orbitFormatter.format(simulatedTime)}}`;updateMoon(simulatedTime);}}
function startOrbit(){{if(orbitActive||document.hidden||document.body.classList.contains("intro")){{armIdleMode();return;}}orbitActive=true;orbitHud.hidden=false;view.environment.lighting={{type:"sun",date:simulatedTime,directShadowsEnabled:true}};loadSunCalc().then(()=>updateMoon(simulatedTime)).catch(error=>console.error("Electric City moon calculation failed",error));updateOrbit();orbitTimer=setInterval(updateOrbit,200);}}
function stopOrbit(){{if(!orbitActive)return;orbitActive=false;clearInterval(orbitTimer);orbitHud.hidden=true;moonLayer.visible=false;view.environment.lighting={{type:"virtual",directShadowsEnabled:true,ambientOcclusionEnabled:true}};}}
function armIdleMode(){{clearTimeout(idleTimer);if(!document.hidden&&!document.body.classList.contains("intro"))idleTimer=setTimeout(startOrbit,18000);}}
function noteActivity(){{stopOrbit();const now=Date.now();if(now-lastActivity<500)return;lastActivity=now;armIdleMode();}}
function endDriveImmediately(){{driveRun++;view.animation?.stop();if(introRoad.parent)map.remove(introRoad);view.camera=cameras.skyline;driveIntro.hidden=true;driveIntro.className="drive-intro";document.body.classList.remove("intro");armIdleMode();}}
async function startDrive(){{stopOrbit();clearTimeout(idleTimer);const run=++driveRun;closeInspector();searchResults.hidden=true;document.body.classList.add("intro");driveIntro.hidden=false;driveIntro.className="drive-intro";driveStage.textContent="BQE NIGHT RUN";driveSpeedValue.textContent="88";if(!introRoad.parent)map.add(introRoad,0);view.camera=driveCameras[0];try{{await pause(450);if(run!==driveRun)return;driveStage.textContent="ATLANTIC AVE · QUEENS-BOUND";await view.goTo(driveCameras[1],{{duration:1900,easing:"linear"}});if(run!==driveRun)return;driveIntro.classList.add("slowmo");driveStage.textContent="CITY OF DREAMS";driveSpeedValue.textContent="42";await view.goTo(driveCameras[2],{{duration:3600,easing:"ease-in-out"}});if(run!==driveRun)return;driveStage.textContent="BROOKLYN HEIGHTS · SLOW MOTION";await view.goTo(driveCameras[3],{{duration:2100,easing:"ease-in-out"}});if(run!==driveRun)return;driveIntro.classList.add("to-map");await pause(700);if(run!==driveRun)return;if(introRoad.parent)map.remove(introRoad);view.camera=cameras.skyline;document.body.classList.remove("intro");driveIntro.classList.add("done");await pause(900);if(run===driveRun){{driveIntro.hidden=true;armIdleMode();}}}}catch(error){{if(error?.name!=="AbortError")console.error("Electric City BQE drive failed",error);endDriveImmediately();}}}}
document.getElementById("inspectorClose").addEventListener("click",event=>{{event.stopPropagation();closeInspector();}});
function hideLoading(){{const loading=document.getElementById("loading");if(!loading)return;loading.style.opacity="0";setTimeout(()=>loading.remove(),750);}}
view.ui.move("zoom","bottom-left");view.whenLayerView(buildings).then(layerView=>{{buildingLayerView=layerView;namedOnly.disabled=false;return reactiveUtils.whenOnce(()=>!layerView.updating);}}).then(()=>{{hideLoading();if(reduceMotion)endDriveImmediately();else setTimeout(startDrive,800);}}).catch(error=>{{hideLoading();endDriveImmediately();console.error("Electric City scene loading failed",error);}});
buildings.load().then(loadNamedBuildings).catch(error=>{{searchStatus.textContent="Named-building search unavailable";console.error("Electric City name index failed",error);}});
document.getElementById("skipDrive").addEventListener("click",endDriveImmediately);document.getElementById("replayDrive").addEventListener("click",startDrive);
["pointerdown","pointermove","touchstart","wheel","keydown"].forEach(eventName=>window.addEventListener(eventName,noteActivity,{{passive:true}}));document.addEventListener("visibilitychange",()=>{{if(document.hidden){{clearTimeout(idleTimer);stopOrbit();}}else armIdleMode();}});
searchGo.addEventListener("click",()=>jumpToNamedBuilding());searchInput.addEventListener("focus",renderSearchResults);searchInput.addEventListener("input",renderSearchResults);searchInput.addEventListener("keydown",event=>{{if(event.key==="Enter"){{event.preventDefault();jumpToNamedBuilding();}}else if(event.key==="Escape")searchResults.hidden=true;}});document.addEventListener("click",event=>{{if(!event.target.closest(".search-panel"))searchResults.hidden=true;}});
namedOnly.addEventListener("change",()=>{{if(!buildingLayerView)return;buildingLayerView.filter=namedOnly.checked?{{where:NAMED_WHERE}}:null;closeInspector();searchStatus.textContent=namedOnly.checked?`${{namedBuildingRecords.length.toLocaleString()}} named buildings shown`:"All Manhattan buildings shown";}});
let clickRequest=0;
view.on("click",async event=>{{
  const request=++clickRequest;
  try{{
    const response=await view.hitTest(event,{{include:[buildings,liberty,torch]}});
    if(request!==clickRequest)return;
    const hit=response.results.find(result=>result.type==="graphic"&&result.graphic&&[buildings,liberty,torch].includes(result.graphic.layer));
    if(!hit){{closeInspector();return;}}
    const feature=hit.graphic;
    if(feature.layer===buildings){{
      const attrs=await buildingAttributes(feature);if(request!==clickRequest)return;
      showInspector(attrs.NAME||"Manhattan Building",[["Building name",attrs.NAME||"Not recorded"],["Year built",number(attrs.CNSTRCT_YR)],["Roof height",number(attrs.HEIGHTROOF," ft")],["Floors",number(attrs.NUM_FLOORS)],["Ground elevation",number(attrs.GROUNDELEV," ft")]],event);
      highlight?.remove();highlight=buildingLayerView?.highlight(feature)||null;
    }}else if(feature.layer===liberty){{showInspector("Statue of Liberty",[["Dedicated","October 28, 1886"],["Ground to torch","305 ft (93 m)"],["Location","Liberty Island"]],event);}}
    else{{showInspector("Liberty's Torch",[["Height","305 ft (93 m)"],["Symbol","Enlightenment"]],event);}}
  }}catch(error){{console.error("Electric City building inspection failed",error);}}
}});
document.querySelectorAll("[data-view]").forEach(button=>button.addEventListener("click",()=>{{document.querySelectorAll("[data-view]").forEach(item=>item.classList.remove("active"));button.classList.add("active");view.goTo(cameras[button.dataset.view],{{duration:1800,easing:"ease-in-out"}});}}));
}});</script></body></html>"""
