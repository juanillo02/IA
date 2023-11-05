;<----VARIABLES GLOBALES---->
(defglobal ?*ANNO*=2023)
(defglobal  ?*LIMITE1*=900)

;<----PLANTILLAS---->
(deftemplate Usuario
    (slot dni)
    (slot pin)
    (slot dinero)
);; Usuario

(deftemplate Tarjeta
    (slot dni)
    (slot pin)
    (slot intentos (default 3))
    (slot limite (default 500))
    (slot annio (default 2030))
    (slot validada (allowed-values Si No) (default No)) ;;Siempre tiene que estar todo igual
);; Tarjeta

(deftemplate Cuenta
    (slot dni)
    (slot saldo)
    (slot estado (allowed-values enPantalla dineroEntregado Inicial SuperaLimite SinSaldo) (default Inicial ))
);; Cuenta

;<----HECHOS---->
(deffacts Iniciales
    (Tarjeta (dni 1234567) (pin 1212) (limite 500))
    (Cuenta (dni 1234567) (Saldo 5000) (estado Inicial))
);; Iniciales

;<----REGLAS---->
(defrule Supera_Intentos
    (declare (salience 1))
    (Usuario (dni ?dni))
    ?t <- (Tarjeta (intentos 0) (dni ?dni))
    (Cuenta (dni ?dni))
    ;(Tarjeta (Intentos ?int))
    ;(test (eq ?int 0))
    =>
    (println "Ha superado sus intentos.")
    (retract ?t)
);; Supera_Intentos

(defrule Pin_Invalido
    ?u <- (Usuario (dni ?dni) (pin ?pin2))
    ?t <- (Tarjeta (dni ?dni) (pin ?pin2&~?pin) (intentos ?intentos))
    (Cuenta (dni ?dni))
    =>
    (println "Pin invalido.")
    (modify ?t (intentos (- ?intentos 1)))
    (retract ?u)
);; Supera_Intentos

(defrule Validar
    ?u <- (Usuario (dni ?dni) (pin ?pin2))
    ?t <- (Tarjeta (dni ?dni) (pin ?pin) (intentos ?intentos) (annio ?*ANNO*) (validada No))
    (Cuenta (dni ?dni))
    =>
    (modify ?t (validada Si))
    (println "Validado OK")
);; Supera_Intentos

(defrule Regla Muestra_Saldo
    (Tarjeta (dni ?dni) (validada si))
    c <- (Cuenta (dni ?dni) (saldo ?s) (estado ~enPantalla))
    =>
    (modify ?c (estado enPantalla))
    (println "El saldo de su cuenta es" ?s)
);; Regla Muestra_Saldo

(defrule Regla Saldo_NoSuficiente
    (Usuario (dni ?dni) (dinero ?d))
    (Cuenta (dni ?dni) (saldo ?s) (estado ~SinSaldo))
    (test (< ?s ?d))
    =>
    (println "Saldo insuficiente.")
);;Regla Saldo_NoSuficiente

(defrule Regla Comprueba_Limite1
    (Usuario (dni ?dni) (dinero ?d))
    ?c <- (Cuenta (dni ?dni) (saldo ?s) (estado ~SuperaLimite))
    (test (> ?d ?*LIMITE1*))
    =>
    (modify ?c (estado SuperaLimite))
    (println "Superas el limite establecido por el banco.")
);;Regla Comprueba_Limite1

(defrule Regla Comprueba_Limite2
    (Usuario (dni ?dni) (dinero ?d))
    (Tarjeta (dni ?dni) (limite ?l))
    ?c <- (Cuenta (dni ?dni) (saldo ?s) (estado ~SuperaLimite))
    (test (> ?d ?l))
    =>
    (modify ?c (estado SuperaLimite))
    (println "Superas el limite establecido por la tarjeta.")
);;Regla Comprueba_Limite1

(defrule Regla Entrega_Dinero
    (Usuario (dni ?dni) (dinero ?d))
    ?c <- (Cuenta (dni ?dni) (saldo ?saldo) (estado ~DineroEntregado))
    =>
    (bind ?nuevo (- ?s ?d))
    (modify ?c (estado DineroEntregado))
    (modify ?c (saldo ?nuevo))
    (println "Dinero en cuenta nuevo: " ?nuevo)
);;Regla Entrega_Dinero