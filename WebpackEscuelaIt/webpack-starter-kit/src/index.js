import './style.css'
import './scss/main.scss'
import data from './data.json' // A partir de Webpack4 no hace falta añadir un json-loader para esto

console.log(...['hola', 'mundo'])
console.log(data, data.name)

