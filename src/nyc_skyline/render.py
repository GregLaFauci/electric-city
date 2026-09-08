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
button{{border:0;border-radius:8px;padding:8px 11px;background:transparent;color:#b7c7d8;font:700 11px Inter,system-ui;letter-spacing:.04em;cursor:pointer}}
button:hover,button.active{{background:#ff3090;color:white}}
.legend{{position:fixed;z-index:3;right:22px;bottom:22px;padding:12px 14px;border:1px solid #273e58;border-radius:12px;background:#07111fda;backdrop-filter:blur(10px);font-size:10px;color:#91a6bb}}
.legend b{{display:block;color:#f7fbff;font-size:11px;letter-spacing:.08em;margin-bottom:7px}}.legend b small{{color:#91a6bb;font-size:8px;margin-left:8px}}
.legend-item{{position:relative;display:inline-flex;align-items:center;margin-right:10px;outline:none;cursor:help}}.legend i{{width:8px;height:8px;border-radius:50%;margin-right:5px;background:var(--swatch);box-shadow:0 0 8px var(--swatch)}}
.legend-item::after{{content:attr(data-range);position:absolute;left:50%;bottom:calc(100% + 10px);transform:translate(-50%,5px);padding:6px 8px;border:1px solid #35516e;border-radius:7px;background:#030814;color:#fff;font-size:10px;font-weight:750;white-space:nowrap;opacity:0;pointer-events:none;transition:.18s}}
.legend-item:hover::after,.legend-item:focus::after{{opacity:1;transform:translate(-50%,0)}}
#loading{{position:fixed;z-index:8;inset:0;display:grid;place-items:center;background:#030814;color:#ff3090;font-size:11px;font-weight:800;letter-spacing:.2em;transition:opacity .7s}}
.esri-ui-corner{{top:112px}}@media(max-width:700px){{.brand{{top:18px;left:18px}}.brand h1{{font-size:34px}}.controls{{top:auto;bottom:14px;left:14px;right:14px;overflow:auto}}.legend{{left:14px;right:14px;bottom:68px}}.legend b small{{display:block;margin:4px 0 0}}.legend-item{{margin-bottom:3px}}}}
</style><script src="https://js.arcgis.com/4.33/"></script></head>
<body><div id="viewDiv"></div><div id="loading">STREAMING MANHATTAN · CITY OF DREAMS</div>
<header class="brand"><p>MANHATTAN AFTER MIDNIGHT · PYTHON × PUBLIC 3D DATA</p><h1>Electric City</h1><em>City of Dreams. The real skyline, recoded in neon.</em></header>
<nav class="controls" aria-label="Camera views"><button class="active" data-view="skyline">Skyline</button><button data-view="liberty">Liberty</button><button data-view="downtown">Downtown</button><button data-view="midtown">Midtown</button><button data-view="uptown">Uptown</button></nav>
<aside class="legend"><b>BUILDING HEIGHT <small>HOVER COLORS · CLICK BUILDINGS</small></b>{legend}</aside>
<script>require(["esri/Map","esri/views/SceneView","esri/layers/SceneLayer","esri/layers/GraphicsLayer","esri/Graphic"],function(EsriMap,SceneView,SceneLayer,GraphicsLayer,Graphic){{
const buildings=new SceneLayer({{url:{json.dumps(SCENE_URL)},renderer:{renderer},popupTemplate:{{title:"{{NAME}}",content:[{{type:"fields",fieldInfos:[{{fieldName:"HEIGHTROOF",label:"Roof height (ft)",format:{{places:0,digitSeparator:true}}}},{{fieldName:"CNSTRCT_YR",label:"Construction year",format:{{places:0,digitSeparator:false}}}}]}}]}},outFields:["NAME","HEIGHTROOF","CNSTRCT_YR"]}});
const liberty=new SceneLayer({{url:{json.dumps(STATUE_SCENE_URL)},title:"Statue of Liberty",renderer:{{type:"simple",symbol:{{type:"mesh-3d",symbolLayers:[{{type:"fill",material:{{color:[62,196,174],colorMixMode:"tint"}},edges:{{type:"solid",color:[137,255,226,.65],size:.45}}}}]}}}},popupTemplate:{{title:"Statue of Liberty",content:"<b>Liberty Enlightening the World</b><br>Dedicated October 28, 1886<br>Ground to torch: 305 ft (93 m)<br><br>Public 3D mesh positioned on Liberty Island."}}}});
const torch=new GraphicsLayer({{title:"Liberty's torch",elevationInfo:{{mode:"absolute-height"}},listMode:"hide"}});
torch.add(new Graphic({{geometry:{{type:"point",longitude:{STATUE_LOCATION[0]},latitude:{STATUE_LOCATION[1]},z:{TORCH_ELEVATION_METERS},spatialReference:{{wkid:4326}}}},symbol:{{type:"point-3d",symbolLayers:[{{type:"object",resource:{{primitive:"sphere"}},material:{{color:[255,184,66,.98]}},height:5,width:3,depth:3}},{{type:"icon",resource:{{primitive:"circle"}},material:{{color:[255,126,38,.18]}},size:34,outline:{{color:[255,174,74,.28],size:1}}}},{{type:"icon",resource:{{primitive:"circle"}},material:{{color:[255,224,140,.72]}},size:10}}]}},popupTemplate:{{title:"The Torch",content:"A beacon of enlightenment, glowing 305 ft (93 m) above Liberty Island."}}}}));
const map=new EsriMap({{basemap:"dark-gray-vector",ground:"world-elevation",layers:[buildings,liberty,torch]}});
const cameras={{skyline:{{position:{{longitude:-74.065,latitude:40.675,z:1500}},heading:31,tilt:68}},liberty:{{position:{{longitude:-74.052,latitude:40.682,z:230}},heading:38,tilt:73}},downtown:{{position:{{longitude:-74.027,latitude:40.700,z:720}},heading:28,tilt:72}},midtown:{{position:{{longitude:-74.005,latitude:40.738,z:900}},heading:24,tilt:70}},uptown:{{position:{{longitude:-73.985,latitude:40.785,z:1050}},heading:25,tilt:67}}}};
const view=new SceneView({{container:"viewDiv",map,qualityProfile:"high",camera:cameras.skyline,environment:{{background:{{type:"color",color:[3,8,20,1]}},starsEnabled:true,atmosphereEnabled:true,lighting:{{type:"virtual",directShadowsEnabled:true,ambientOcclusionEnabled:true}}}},highlightOptions:{{color:[255,174,74],fillOpacity:.35,haloOpacity:.9}}}});
view.ui.move("zoom","bottom-left");view.whenLayerView(buildings).then(layerView=>{{const done=()=>{{if(!layerView.updating){{document.getElementById("loading").style.opacity="0";setTimeout(()=>document.getElementById("loading")?.remove(),750)}}}};layerView.watch("updating",done);done();}});
document.querySelectorAll("[data-view]").forEach(button=>button.addEventListener("click",()=>{{document.querySelectorAll("[data-view]").forEach(item=>item.classList.remove("active"));button.classList.add("active");view.goTo(cameras[button.dataset.view],{{duration:1800,easing:"ease-in-out"}});}}));
}});</script></body></html>"""
