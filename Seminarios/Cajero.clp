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
    (slot limite (default 100))
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
    ?t <- (Tarjeta (dni ?dni) (pin ?pin) (intentos ?intentos) (annio ?annio) (validada No))
    (Cuenta (dni ?dni))
    (test (< 2023 ?annio))
    =>
    (modify ?t (validada Si))
    (println "Validado OK")
);; Supera_Intentos