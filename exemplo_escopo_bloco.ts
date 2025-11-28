// Demonstração de escopo de bloco em condicionais e loops

// Exemplo 1: Escopo em if
let x: number = 10;
if (x > 5) {
    let y: number = 20;  // y só existe dentro do if
    print(y);
}
// print(y);  // ERRO: y não existe aqui

// Exemplo 2: Variável de loop tem escopo próprio
for (let i: number = 0; i < 3; i = i + 1) {
    let temp: number = i * 2;
    print(temp);
}
// print(i);    // ERRO: i não existe aqui
// print(temp); // ERRO: temp não existe aqui

// Exemplo 3: Shadowing (permitido)
let a: number = 100;
if (true) {
    let a: number = 200;  // Nova variável a, sombra a anterior
    print(a);             // Imprime 200
}
print(a);  // Imprime 100

// Exemplo 4: Escopo em while
let count: number = 0;
while (count < 2) {
    let message: string = "iteração";
    print(message);
    count = count + 1;
}
// print(message); // ERRO: message não existe aqui

// Exemplo 5: if-else com escopos independentes
let cond: boolean = true;
if (cond) {
    let ifVar: number = 10;
} else {
    let elseVar: number = 20;
}
// print(ifVar);   // ERRO: ifVar não existe
// print(elseVar); // ERRO: elseVar não existe
