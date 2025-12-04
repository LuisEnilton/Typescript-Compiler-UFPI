.class public Exemplo_7
.super java/lang/Object

.field public static x I

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
    ldc 5
    istore 1
    getstatic java/lang/System/out Ljava/io/PrintStream;
    ldc "Inicio da contagem..."
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
L1:
    iload 1
    ldc 0
    if_icmpgt L3
    iconst_0
    goto L4
L3:
    iconst_1
L4:
    ifeq L2
    getstatic java/lang/System/out Ljava/io/PrintStream;
    iload 1
    invokevirtual java/io/PrintStream/println(I)V
    iload 1
    ldc 1
    isub
    dup
    istore 1
    pop
    goto L1
L2:
    getstatic java/lang/System/out Ljava/io/PrintStream;
    ldc "FIM!"
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    return
.end method