.class public Exemplo_interface_produtos
.super java/lang/Object

.field public static produtos Ljava/util/ArrayList;
.field public static p1 I
.field public static p2 I
.field public static p3 I
.field public static total I
.field public static p1_preco I
.field public static p1_quantidade I
.field public static p2_preco I
.field public static p2_quantidade I
.field public static p3_preco I
.field public static p3_quantidade I

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
    putstatic Exemplo_interface_produtos/produtos Ljava/util/ArrayList;
    ldc 3000
    dup
    putstatic Exemplo_interface_produtos/p1_preco I
    pop
    ldc 5
    dup
    putstatic Exemplo_interface_produtos/p1_quantidade I
    pop
    getstatic Exemplo_interface_produtos/produtos Ljava/util/ArrayList;
    getstatic Exemplo_interface_produtos/p1 I
    invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
    invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z
    pop
    ldc 50
    dup
    putstatic Exemplo_interface_produtos/p2_preco I
    pop
    ldc 20
    dup
    putstatic Exemplo_interface_produtos/p2_quantidade I
    pop
    getstatic Exemplo_interface_produtos/produtos Ljava/util/ArrayList;
    getstatic Exemplo_interface_produtos/p2 I
    invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
    invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z
    pop
    ldc 150
    dup
    putstatic Exemplo_interface_produtos/p3_preco I
    pop
    ldc 10
    dup
    putstatic Exemplo_interface_produtos/p3_quantidade I
    pop
    getstatic Exemplo_interface_produtos/produtos Ljava/util/ArrayList;
    getstatic Exemplo_interface_produtos/p3 I
    invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
    invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z
    pop
    getstatic java/lang/System/out Ljava/io/PrintStream;
    ldc "=== LISTA DE PRODUTOS ==="
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    ldc 0
    istore 1
L1:
    iload 1
    getstatic Exemplo_interface_produtos/produtos Ljava/util/ArrayList;
    invokevirtual java/util/ArrayList/size()I
    if_icmplt L3
    iconst_0
    goto L4
L3:
    iconst_1
L4:
    ifeq L2
    getstatic Exemplo_interface_produtos/produtos Ljava/util/ArrayList;
    iload 1
    invokevirtual java/util/ArrayList/get(I)Ljava/lang/Object;
    checkcast java/lang/Integer
    invokevirtual java/lang/Integer/intValue()I
    istore 2
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
    iload 2
    getstatic Exemplo_interface_produtos/prod_preco I
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
    iload 2
    getstatic Exemplo_interface_produtos/prod_quantidade I
    invokevirtual java/lang/StringBuilder/append(I)Ljava/lang/StringBuilder;
    invokevirtual java/lang/StringBuilder/toString()Ljava/lang/String;
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    getstatic java/lang/System/out Ljava/io/PrintStream;
    ldc "---"
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    iload 1
    ldc 1
    iadd
    dup
    istore 1
    pop
    goto L1
L2:
    ldc 0
    putstatic Exemplo_interface_produtos/total I
    ldc 0
    istore 1
L5:
    iload 1
    getstatic Exemplo_interface_produtos/produtos Ljava/util/ArrayList;
    invokevirtual java/util/ArrayList/size()I
    if_icmplt L7
    iconst_0
    goto L8
L7:
    iconst_1
L8:
    ifeq L6
    getstatic Exemplo_interface_produtos/produtos Ljava/util/ArrayList;
    iload 1
    invokevirtual java/util/ArrayList/get(I)Ljava/lang/Object;
    checkcast java/lang/Integer
    invokevirtual java/lang/Integer/intValue()I
    istore 2
    iload 2
    getstatic Exemplo_interface_produtos/prod_preco I
    iload 2
    getstatic Exemplo_interface_produtos/prod_quantidade I
    imul
    istore 3
    getstatic Exemplo_interface_produtos/total I
    iload 3
    iadd
    dup
    putstatic Exemplo_interface_produtos/total I
    pop
    iload 1
    ldc 1
    iadd
    dup
    istore 1
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
    getstatic Exemplo_interface_produtos/total I
    invokevirtual java/lang/StringBuilder/append(I)Ljava/lang/StringBuilder;
    invokevirtual java/lang/StringBuilder/toString()Ljava/lang/String;
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    return
.end method