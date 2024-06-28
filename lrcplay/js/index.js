import {lrc} from './data.js'
function parseLrc(str){
    const strs=[];
    str.split("\n").forEach(x=>strs.push({time:x.splice(0,10),word:x.splice(10)}))
    console.log(strs)
}
parseLrc(lrc)
