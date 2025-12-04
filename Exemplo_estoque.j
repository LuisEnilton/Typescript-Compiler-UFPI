.class public Exemplo_estoque
.super java/lang/Object

.field public static precos Ljava/util/ArrayList;
.field public static quantidades Ljava/util/ArrayList;
.field public static total I
.field public static media I

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
    new java/util/ArrayList
    dup
    invokespecial java/util/ArrayList/<init>()V
    astore 2
    aload 1
    ldc 3000
    invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
    invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z
    pop
    aload 2
    ldc 5
    invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
    invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z
    pop
    aload 1
    ldc 50
    invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
    invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z
    pop
    aload 2
    ldc 20
    invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
    invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z
    pop
    aload 1
    ldc 150
    invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
    invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z
    pop
    aload 2
    ldc 10
    invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
    invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z
    pop
    aload 1
    ldc 200
    invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
    invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z
    pop
    aload 2
    ldc 15
    invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
    invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z
    pop
    getstatic java/lang/System/out Ljava/io/PrintStream;
    ldc "=== SISTEMA DE ESTOQUE ==="
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    getstatic java/lang/System/out Ljava/io/PrintStream;
    ldc ""
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    ldc 0
    istore 3
    ldc 0
    istore 4
L1:
    iload 4
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
    iload 4
    invokevirtual java/util/ArrayList/get(I)Ljava/lang/Object;
    checkcast java/lang/Integer
    invokevirtual java/lang/Integer/intValue()I
    istore 5
    aload 2
    iload 4
    invokevirtual java/util/ArrayList/get(I)Ljava/lang/Object;
    checkcast java/lang/Integer
    invokevirtual java/lang/Integer/intValue()I
    istore 6
    iload 5
    iload 6
    imul
    istore 7
    getstatic java/lang/System/out Ljava/io/PrintStream;
    new java/lang/StringBuilder
    dup
    invokespecial java/lang/StringBuilder/<init>()V
    ldc "Produto"
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    ldc " "
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    iload 4
    ldc 1
    iadd
    invokevirtual java/lang/StringBuilder/append(I)Ljava/lang/StringBuilder;
    ldc " "
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    ldc "- Preco:"
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    ldc " "
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    iload 5
    invokevirtual java/lang/StringBuilder/append(I)Ljava/lang/StringBuilder;
    ldc " "
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    ldc "Qtd:"
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    ldc " "
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    iload 6
    invokevirtual java/lang/StringBuilder/append(I)Ljava/lang/StringBuilder;
    ldc " "
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    ldc "Valor:"
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    ldc " "
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    iload 7
    invokevirtual java/lang/StringBuilder/append(I)Ljava/lang/StringBuilder;
    invokevirtual java/lang/StringBuilder/toString()Ljava/lang/String;
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    iload 3
    iload 7
    iadd
    dup
    istore 3
    pop
    iload 4
    ldc 1
    iadd
    dup
    istore 4
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
    aload 1
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
    iload 3
    invokevirtual java/lang/StringBuilder/append(I)Ljava/lang/StringBuilder;
    invokevirtual java/lang/StringBuilder/toString()Ljava/lang/String;
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    iload 3
    aload 1
    invokevirtual java/util/ArrayList/size()I
    idiv
    istore 8
    getstatic java/lang/System/out Ljava/io/PrintStream;
    new java/lang/StringBuilder
    dup
    invokespecial java/lang/StringBuilder/<init>()V
    ldc "Valor Medio por Produto:"
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    ldc " "
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    iload 8
    invokevirtual java/lang/StringBuilder/append(I)Ljava/lang/StringBuilder;
    invokevirtual java/lang/StringBuilder/toString()Ljava/lang/String;
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    return
.end method