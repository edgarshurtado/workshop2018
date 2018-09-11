import './style.css'
import './scss/main.scss'
import data from './data.json' // A partir de Webpack4 no hace falta añadir un json-loader para esto

console.log(...['hola', 'mundo', 'vanilla'])
console.log(data, data.name)

const d = document
const app = d.getElementById('app')
const h1 = d.createElement('h1')

h1.innerText = "Hola VanillaJS"
app.appendChild(h1)

const menu = d.createElement('nav')
menu.innerText = ''

//data.links.forEach(link => menu.innerText += `<a href="${link[1]}">${link[0]}</a>`)
