.class public Exemplo_5
.super java/lang/Object

.field public static numero I
.field public static resultado I

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

.method public static fatorialRecursivo(I)I
    .limit stack 200
    .limit locals 200
    iload 0
    ldc 1
    if_icmple L3
    iconst_0
    goto L4
L3:
    iconst_1
L4:
    ifeq L1
    ldc 1
    ireturn
    goto L2
L1:
L2:
    iload 0
    iload 0
    ldc 1
    isub
    invokestatic Exemplo_5/fatorialRecursivo(I)I
    imul
    ireturn
.end method

.method public static main([Ljava/lang/String;)V
    .limit stack 200
    .limit locals 200
    getstatic java/lang/System/out Ljava/io/PrintStream;
    ldc "Digite um numero: "
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    new java/util/Scanner
    dup
    getstatic java/lang/System/in Ljava/io/InputStream;
    invokespecial java/util/Scanner/<init>(Ljava/io/InputStream;)V
    invokevirtual java/util/Scanner/nextInt()I
    dup
    istore 1
    pop
    iload 1
    invokestatic Exemplo_5/fatorialRecursivo(I)I
    istore 2
    getstatic java/lang/System/out Ljava/io/PrintStream;
    new java/lang/StringBuilder
    dup
    invokespecial java/lang/StringBuilder/<init>()V
    ldc "Recursivo: O fatorial de"
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    ldc " "
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    iload 1
    invokevirtual java/lang/StringBuilder/append(I)Ljava/lang/StringBuilder;
    ldc " "
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    ldc "é"
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    ldc " "
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    iload 2
    invokevirtual java/lang/StringBuilder/append(I)Ljava/lang/StringBuilder;
    invokevirtual java/lang/StringBuilder/toString()Ljava/lang/String;
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    return
.end method