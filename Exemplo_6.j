.class public Exemplo_6
.super java/lang/Object

.field public static nota I

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
    getstatic java/lang/System/out Ljava/io/PrintStream;
    ldc "=== Sistema de Avaliacao ==="
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    ldc 2
    dup
    istore 1
    pop
    getstatic java/lang/System/out Ljava/io/PrintStream;
    new java/lang/StringBuilder
    dup
    invokespecial java/lang/StringBuilder/<init>()V
    ldc "Nota Informada:"
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    ldc " "
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    iload 1
    invokevirtual java/lang/StringBuilder/append(I)Ljava/lang/StringBuilder;
    invokevirtual java/lang/StringBuilder/toString()Ljava/lang/String;
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    iload 1
    ldc 0
    if_icmplt L3
    iconst_0
    goto L4
L3:
    iconst_1
L4:
    ifeq L1
    getstatic java/lang/System/out Ljava/io/PrintStream;
    ldc "ERRO: A nota nao pode ser negativa."
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    goto L2
L1:
    iload 1
    ldc 10
    if_icmpgt L7
    iconst_0
    goto L8
L7:
    iconst_1
L8:
    ifeq L5
    getstatic java/lang/System/out Ljava/io/PrintStream;
    ldc "ERRO: A nota maxima e 10."
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    goto L6
L5:
    iload 1
    ldc 6
    if_icmplt L11
    iconst_0
    goto L12
L11:
    iconst_1
L12:
    ifeq L9
    getstatic java/lang/System/out Ljava/io/PrintStream;
    ldc "Situacao: PROVA FINAL"
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    ldc 6
    iload 1
    isub
    istore 2
    getstatic java/lang/System/out Ljava/io/PrintStream;
    new java/lang/StringBuilder
    dup
    invokespecial java/lang/StringBuilder/<init>()V
    ldc "Faltam"
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    ldc " "
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    iload 2
    invokevirtual java/lang/StringBuilder/append(I)Ljava/lang/StringBuilder;
    ldc " "
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    ldc "pontos para alcancar a media 6."
    invokevirtual java/lang/StringBuilder/append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    invokevirtual java/lang/StringBuilder/toString()Ljava/lang/String;
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    goto L10
L9:
    getstatic java/lang/System/out Ljava/io/PrintStream;
    ldc "Situacao: APROVADO"
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    getstatic java/lang/System/out Ljava/io/PrintStream;
    ldc "Parabens pelo desempenho!"
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
L10:
L6:
L2:
    getstatic java/lang/System/out Ljava/io/PrintStream;
    ldc "=== Fim do Processo ==="
    invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
    return
.end method