// Configuración global y constantes
let currentProfile = null;
const API_URL = 'http://localhost:5000';
let darkMode = localStorage.getItem('darkMode') !== 'false';
let board = [], turn = "X";
let p = {X: "J1", O: "J2"};
let score = {X: 0, O: 0, D: 0};
let games = 0;
let nextStarter = "X";
let gameOver = false;
let winningCells = [];
let timerInterval, seconds = 0;
let moveHistory = [];

const win = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
const q = id => document.getElementById(id);