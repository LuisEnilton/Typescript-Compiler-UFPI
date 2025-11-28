// Teste que deve gerar ERRO: y não existe fora do if

let x: number = 10;
if (x > 5) {
    let y: number = 20;
}
let z: number = y;  // ERRO: y é indefinido
