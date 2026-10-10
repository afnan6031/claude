import fs from 'fs'; import * as topo from 'topojson-client'; import * as d3 from 'd3-geo';
const w=JSON.parse(fs.readFileSync('node_modules/world-atlas/countries-10m.json'));
const fc=topo.feature(w,w.objects.countries);
const W=960,H=820;
const box={type:'MultiPoint',coordinates:[[-87.2,3.6],[-76.2,11.6]]};
const proj=d3.geoMercator().fitExtent([[0,0],[W,H]],box);
const path=d3.geoPath(proj).digits(1);
const want={'Panama':'pa','Costa Rica':'cr','Colombia':'co','Nicaragua':'ni','Ecuador':'ec'};
const out={W,H,countries:{},points:{}};
for(const f of fc.features){const id=want[f.properties.name]; if(id) out.countries[id]=path(f);}
const pt=(lon,lat)=>proj([lon,lat]).map(v=>Math.round(v*10)/10);
out.points={burica:pt(-82.87,8.03),epi:pt(-82.87,5.38),panamaCity:pt(-79.52,8.98),sanJose:pt(-84.09,9.93)};
// graticule
out.grat=path(d3.geoGraticule().step([2,2]).extent([[-90,2],[-74,13]])());
fs.writeFileSync(process.argv[2],JSON.stringify(out));
console.log(Object.keys(out.countries), out.points, Object.values(out.countries).map(s=>s.length));
