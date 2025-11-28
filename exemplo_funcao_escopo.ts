// Teste de escopo de função com parâmetros

function test(param1: number, param2: string): void {
    let local: number = param1 + 10;
    print(local);
    
    if (true) {
        let innerLocal: number = 20;
        print(innerLocal);
    }
    // print(innerLocal); // ERRO: innerLocal não existe aqui
}

test(5, "hello");
