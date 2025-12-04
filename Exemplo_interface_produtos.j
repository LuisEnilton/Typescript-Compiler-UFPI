.class public Exemplo_interface_produtos
.super java/lang/Object

.field public static produtos Ljava/util/ArrayList;
.field public static p1 LProduto;
.field public static p2 LProduto;
.field public static p3 LProduto;
.field public static total I

.method public static <clinit>()V
    .limit stack 200
    .limit locals 200
    return
.end method

.method public <init>()V
    aload_0
    invokespecial java/lang/Object/<init>()V
    return
.end method

.method public static main([Ljava/lang/String;)V
    .limit stack 200
    .limit locals 200
    new java/util/ArrayList
    dup
    invokespecial java/util/ArrayList/<init>()V
    astore 1
    new Produto
    dup
    invokespecial Produto/<init>()V
    putstatic Exemplo_interface_produtos/p1 LProduto;
    ldc "Notebook"
    getstatic Exemplo_interface_produtos/p1 LProduto;
    swap
    putfield Produto/nome Ljava/lang/String;
    ldc 3000
    getstatic Exemplo_interface_produtos/p1 LProduto;
    swap
    putfield Produto/preco I
    ldc 5
    getstatic Exemplo_interface_produtos/p1 LProduto;
    swap
    putfield Produto/quantidade I
    aload 1
    getstatic Exemplo_interface_produtos/p1 LProduto;
    invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z
    pop
    new Produto
    dup
    invokespecial Produto/<init>()V
    putstatic Exemplo_interface_produtos/p2 LProduto;
    ldc "Mouse"
    getstatic Exemplo_interface_produtos/p2 LProduto;
    swap
    putfield Produto/nome Ljava/lang/String;
    ldc 50
    getstatic Exemplo_interface_produtos/p2 LProduto;
    swap
    putfield Produto/preco I
    ldc 20
    getstatic Exemplo_interface_produtos/p2 LProduto;
    swap
    putfield Produto/quantidade I
    aload 1
    getstatic Exemplo_interface_produtos/p2 LProduto;
    invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z
    pop
    new Produto
    dup
    invokespecial Produto/<init>()V
    putstatic Exemplo_interface_produtos/p3 LProduto;
    ldc "Teclado"
    getstatic Exemplo_interface_produtos/p3 LProduto;
    swap
    putfield Produto/nome Ljava/lang/String;
    ldc 150
    getstatic Exemplo_interface_produtos/p3 LProduto;
    swap
    putfield Produto/preco I
    ldc 10
    getstatic Exemplo_interface_produtos/p3 LProduto;
    swap
    putfield Produto/quantidade I
    aload 1
    getstatic Exemplo_interface_produtos/p3 LProduto;
    invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z
    pop
    getstatic java/lang/System/out Ljava/io/PrintStream;
    ldc "=== LISTA DE PRODUTOS ==="
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    ldc 0
    istore 2
L1:
    iload 2
    aload 1
    invokevirtual java/util/ArrayList/size()I
    if_icmplt L3
    iconst_0
    goto L4
L3:
    iconst_1
L4:
    ifeq L2
    aload 1
    iload 2
    invokevirtual java/util/ArrayList/get(I)Ljava/lang/Object;
    checkcast Produto
    checkcast Produto
    astore 3
    getstatic java/lang/System/out Ljava/io/PrintStream;
    new java/lang/StringBuilder
    dup
    invokespecial java/lang/StringBuilder/<init>()V
    ldc "Produto:"
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    ldc " "
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    aload 3
    getfield Produto/nome Ljava/lang/String;
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    invokevirtual java/lang/StringBuilder/toString()Ljava/lang/String;
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    getstatic java/lang/System/out Ljava/io/PrintStream;
    new java/lang/StringBuilder
    dup
    invokespecial java/lang/StringBuilder/<init>()V
    ldc "Preco:"
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    ldc " "
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    aload 3
    getfield Produto/preco I
    invokevirtual java/lang/StringBuilder/append(I)Ljava/lang/StringBuilder;
    invokevirtual java/lang/StringBuilder/toString()Ljava/lang/String;
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    getstatic java/lang/System/out Ljava/io/PrintStream;
    new java/lang/StringBuilder
    dup
    invokespecial java/lang/StringBuilder/<init>()V
    ldc "Quantidade:"
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    ldc " "
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    aload 3
    getfield Produto/quantidade I
    invokevirtual java/lang/StringBuilder/append(I)Ljava/lang/StringBuilder;
    invokevirtual java/lang/StringBuilder/toString()Ljava/lang/String;
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    getstatic java/lang/System/out Ljava/io/PrintStream;
    ldc "---"
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    iload 2
    ldc 1
    iadd
    dup
    istore 2
    pop
    goto L1
L2:
    ldc 0
    istore 4
    ldc 0
    istore 2
L5:
    iload 2
    aload 1
    invokevirtual java/util/ArrayList/size()I
    if_icmplt L7
    iconst_0
    goto L8
L7:
    iconst_1
L8:
    ifeq L6
    aload 1
    iload 2
    invokevirtual java/util/ArrayList/get(I)Ljava/lang/Object;
    checkcast Produto
    checkcast Produto
    astore 3
    aload 3
    getfield Produto/preco I
    aload 3
    getfield Produto/quantidade I
    imul
    istore 5
    iload 4
    iload 5
    iadd
    dup
    istore 4
    pop
    iload 2
    ldc 1
    iadd
    dup
    istore 2
    pop
    goto L5
L6:
    getstatic java/lang/System/out Ljava/io/PrintStream;
    new java/lang/StringBuilder
    dup
    invokespecial java/lang/StringBuilder/<init>()V
    ldc "Valor Total do Estoque:"
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    ldc " "
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    iload 4
    invokevirtual java/lang/StringBuilder/append(I)Ljava/lang/StringBuilder;
    invokevirtual java/lang/StringBuilder/toString()Ljava/lang/String;
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    return
.end method