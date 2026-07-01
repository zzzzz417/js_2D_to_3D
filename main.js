const BACKGROUND = "#101010"
const FRONTGROUND = "#50FF50"
// const FRONTGROUND = "#fbee35"
import { vs, fs } from "./data.js";


const game = document.getElementById("game")
game.width = 600
game.height = 600
const ctx = game.getContext("2d")


console.log(game)
// const game = document.getElementById("game") 
console.log(ctx)

function clear(){
    ctx.fillStyle = BACKGROUND
    ctx.fillRect(0,0,game.width,game.height)
}

function point({x, y}){
    let s = 10
    ctx.fillStyle = FRONTGROUND
    ctx.fillRect(x - s/2,y - s/2,s,s)
}

function screen(p){
    return {
        x : (p.x + 1)/2*game.width,
        y : (1 - (p.y + 1)/2)*game.height,
    }
}

function project({x,y,z}){
    return{
        x : x/z,
        y : y/z,
    }
}

const FPS = 60;
let dz = 20;
let angle = 0;

function rotate_xz({x,y,z},angle){
    const c = Math.cos(angle)
    const s = Math.sin(angle)
    return{
        x : x*c - z*s,
        y : y,
        z : x*s + z*c,
    }
}



function translate_z({x,y,z},dz){
    return{ x,y ,z : z + dz }
}

function line(p1,p2){
    ctx.strokeStyle = FRONTGROUND
    ctx.lineWidth = 2;

    ctx.beginPath();
    ctx.moveTo(p1.x, p1.y);
    ctx.lineTo(p2.x, p2.y);
    ctx.stroke();
}


function farme(){
    const dt = 1/FPS
    dz -= 3 * dt
    // dz = 1
    clear()

    angle +=  Math.PI *dt * 2
    // for (const v of vs){
    //     point(screen(project(translate_z(rotate_xz(v,angle),dz))))
    // }

    for (const f of fs){
        for(let i = 0; i < f.length; i++){
            const a = vs[f[i]]
            const b = vs[f[(i + 1)%f.length]]
            line(
            (screen(project(translate_z(rotate_xz(a,angle),dz)))),
            (screen(project(translate_z(rotate_xz(b,angle),dz))))
            )
        }
    }

    setTimeout(farme, 1000/FPS)
}

setTimeout(farme, 1000/FPS)

