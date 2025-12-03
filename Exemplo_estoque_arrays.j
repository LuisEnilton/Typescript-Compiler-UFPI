.class public Exemplo_estoque_arrays
.super java/lang/Object

.field public static precos Ljava/util/ArrayList;
.field public static quantidades Ljava/util/ArrayList;
.field public static total I
.field public static media I
.field public static ultimo_preco I

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
    putstatic Exemplo_estoque_arrays/precos Ljava/util/ArrayList;
    new java/util/ArrayList
    dup
    invokespecial java/util/ArrayList/<init>()V
    putstatic Exemplo_estoque_arrays/quantidades Ljava/util/ArrayList;
    getstatic Exemplo_estoque_arrays/precos Ljava/util/ArrayList;
    ldc 3000
    invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
    invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z
    pop
    getstatic Exemplo_estoque_arrays/quantidades Ljava/util/ArrayList;
    ldc 5
    invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
    invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z
    pop
    getstatic Exemplo_estoque_arrays/precos Ljava/util/ArrayList;
    ldc 50
    invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
    invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z
    pop
    getstatic Exemplo_estoque_arrays/quantidades Ljava/util/ArrayList;
    ldc 20
    invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
    invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z
    pop
    getstatic Exemplo_estoque_arrays/precos Ljava/util/ArrayList;
    ldc 150
    invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
    invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z
    pop
    getstatic Exemplo_estoque_arrays/quantidades Ljava/util/ArrayList;
    ldc 10
    invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
    invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z
    pop
    getstatic Exemplo_estoque_arrays/precos Ljava/util/ArrayList;
    ldc 800
    invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
    invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z
    pop
    getstatic Exemplo_estoque_arrays/quantidades Ljava/util/ArrayList;
    ldc 3
    invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
    invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z
    pop
    getstatic java/lang/System/out Ljava/io/PrintStream;
    ldc "=== SISTEMA DE ESTOQUE ==="
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    ldc 0
    putstatic Exemplo_estoque_arrays/total I
    ldc 0
    istore 1
L1:
    iload 1
    getstatic Exemplo_estoque_arrays/precos Ljava/util/ArrayList;
    invokevirtual java/util/ArrayList/size()I
    if_icmplt L3
    iconst_0
    goto L4
L3:
    iconst_1
L4:
    ifeq L2
    getstatic Exemplo_estoque_arrays/precos Ljava/util/ArrayList;
    iload 1
    invokevirtual java/util/ArrayList/get(I)Ljava/lang/Object;
    checkcast java/lang/Integer
    invokevirtual java/lang/Integer/intValue()I
    istore 2
    getstatic Exemplo_estoque_arrays/quantidades Ljava/util/ArrayList;
    iload 1
    invokevirtual java/util/ArrayList/get(I)Ljava/lang/Object;
    checkcast java/lang/Integer
    invokevirtual java/lang/Integer/intValue()I
    istore 3
    iload 2
    iload 3
    imul
    istore 4
    getstatic java/lang/System/out Ljava/io/PrintStream;
    new java/lang/StringBuilder
    dup
    invokespecial java/lang/StringBuilder/<init>()V
    ldc "Produto"
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    ldc " "
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    iload 1
    ldc 1
    iadd
    invokevirtual java/lang/StringBuilder/append(I)Ljava/lang/StringBuilder;
    ldc " "
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    ldc "- Preco:"
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    ldc " "
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    iload 2
    invokevirtual java/lang/StringBuilder/append(I)Ljava/lang/StringBuilder;
    ldc " "
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    ldc "Qtd:"
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    ldc " "
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    iload 3
    invokevirtual java/lang/StringBuilder/append(I)Ljava/lang/StringBuilder;
    ldc " "
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    ldc "Valor:"
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    ldc " "
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    iload 4
    invokevirtual java/lang/StringBuilder/append(I)Ljava/lang/StringBuilder;
    invokevirtual java/lang/StringBuilder/toString()Ljava/lang/String;
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    getstatic Exemplo_estoque_arrays/total I
    iload 4
    iadd
    dup
    putstatic Exemplo_estoque_arrays/total I
    pop
    iload 1
    ldc 1
    iadd
    dup
    istore 1
    pop
    goto L1
L2:
    getstatic java/lang/System/out Ljava/io/PrintStream;
    ldc ""
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    getstatic java/lang/System/out Ljava/io/PrintStream;
    ldc "=== RESUMO ==="
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    getstatic java/lang/System/out Ljava/io/PrintStream;
    new java/lang/StringBuilder
    dup
    invokespecial java/lang/StringBuilder/<init>()V
    ldc "Total de Produtos:"
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    ldc " "
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    getstatic Exemplo_estoque_arrays/precos Ljava/util/ArrayList;
    invokevirtual java/util/ArrayList/size()I
    invokevirtual java/lang/StringBuilder/append(I)Ljava/lang/StringBuilder;
    invokevirtual java/lang/StringBuilder/toString()Ljava/lang/String;
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    getstatic java/lang/System/out Ljava/io/PrintStream;
    new java/lang/StringBuilder
    dup
    invokespecial java/lang/StringBuilder/<init>()V
    ldc "Valor Total do Estoque:"
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    ldc " "
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    getstatic Exemplo_estoque_arrays/total I
    invokevirtual java/lang/StringBuilder/append(I)Ljava/lang/StringBuilder;
    invokevirtual java/lang/StringBuilder/toString()Ljava/lang/String;
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    getstatic Exemplo_estoque_arrays/total I
    getstatic Exemplo_estoque_arrays/precos Ljava/util/ArrayList;
    invokevirtual java/util/ArrayList/size()I
    idiv
    putstatic Exemplo_estoque_arrays/media I
    getstatic java/lang/System/out Ljava/io/PrintStream;
    new java/lang/StringBuilder
    dup
    invokespecial java/lang/StringBuilder/<init>()V
    ldc "Valor Medio por Produto:"
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    ldc " "
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    getstatic Exemplo_estoque_arrays/media I
    invokevirtual java/lang/StringBuilder/append(I)Ljava/lang/StringBuilder;
    invokevirtual java/lang/StringBuilder/toString()Ljava/lang/String;
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    getstatic java/lang/System/out Ljava/io/PrintStream;
    ldc ""
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    getstatic java/lang/System/out Ljava/io/PrintStream;
    ldc "=== TESTANDO POP ==="
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    getstatic Exemplo_estoque_arrays/precos Ljava/util/ArrayList;
    dup
    invokevirtual java/util/ArrayList/size()I
    iconst_1
    isub
    dup
    istore 99
    invokevirtual java/util/ArrayList/remove(I)Ljava/lang/Object;
    checkcast java/lang/Integer
    invokevirtual java/lang/Integer/intValue()I
    putstatic Exemplo_estoque_arrays/ultimo_preco I
    getstatic java/lang/System/out Ljava/io/PrintStream;
    new java/lang/StringBuilder
    dup
    invokespecial java/lang/StringBuilder/<init>()V
    ldc "Ultimo preco removido:"
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    ldc " "
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    getstatic Exemplo_estoque_arrays/ultimo_preco I
    invokevirtual java/lang/StringBuilder/append(I)Ljava/lang/StringBuilder;
    invokevirtual java/lang/StringBuilder/toString()Ljava/lang/String;
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    getstatic java/lang/System/out Ljava/io/PrintStream;
    new java/lang/StringBuilder
    dup
    invokespecial java/lang/StringBuilder/<init>()V
    ldc "Produtos restantes:"
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    ldc " "
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    getstatic Exemplo_estoque_arrays/precos Ljava/util/ArrayList;
    invokevirtual java/util/ArrayList/size()I
    invokevirtual java/lang/StringBuilder/append(I)Ljava/lang/StringBuilder;
    invokevirtual java/lang/StringBuilder/toString()Ljava/lang/String;
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    return
.end method