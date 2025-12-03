.class public Exemplo_2
.super java/lang/Object

.field public static arr Ljava/util/ArrayList;

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
    putstatic Exemplo_2/arr Ljava/util/ArrayList;
    getstatic Exemplo_2/arr Ljava/util/ArrayList;
    ldc 2
    invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
    invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z
    pop
    getstatic Exemplo_2/arr Ljava/util/ArrayList;
    ldc 40
    invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
    invokevirtual java/util/ArrayList/add(Ljava/lang/Object;)Z
    pop
    getstatic java/lang/System/out Ljava/io/PrintStream;
    getstatic Exemplo_2/arr Ljava/util/ArrayList;
    ldc 0
    invokevirtual java/util/ArrayList/get(I)Ljava/lang/Object;
    checkcast java/lang/Integer
    invokevirtual java/lang/Integer/intValue()I
    invokevirtual java/io/PrintStream/println(I)V
    getstatic java/lang/System/out Ljava/io/PrintStream;
    getstatic Exemplo_2/arr Ljava/util/ArrayList;
    ldc 1
    invokevirtual java/util/ArrayList/get(I)Ljava/lang/Object;
    checkcast java/lang/Integer
    invokevirtual java/lang/Integer/intValue()I
    invokevirtual java/io/PrintStream/println(I)V
    return
.end method