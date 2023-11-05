;<----PLANTILLAS---->
(deftemplate valvula
    (slot nombre)
    (slot estado (allowed-values abierta cerrada) (default cerrada))
    (slot presion (default 0))
    (slot temperaturainterna (default 0))
    (slot temperaturaexterna (default 0))
);;valvula

;<----HECHOS---->
(deffacts v1
    (nombre Entrada)
    (temperaturainterna 101)
    (temperaturaexterna 35)
    (presion 1)
);;v1

(deffacts v2
    (nombre Salida)
    (temperaturainterna 101)
    (temperaturaexterna 155)
    (presion 5)
);;v2

(deffacts v3
    (nombre Pasillo1)
    (temperaturainterna 99)
    (temperaturaexterna 37)
);;v3

;<----REGLAS---->
(defrule R1
    ?v <- (valvula (presion ?p) (estado ~cerrada))
    (test (= ?p 5))
    =>
    (modify ?v (presion 0))
    (modify ?v (estado cerrada))
)R1

(defrule R2
    ?v <- (valvula (estado cerrada) (presion ?p) (temperaturainterna ?ti))
    (test (< ?p 10))
    (test (> ?ti 35))
    =>
    (modify ?v (estado abierta) (presion aumento(?p ?ti)))
);;R2

(defrule R3
    ?v1 <- (valvula (nombre ?n1) (temperaturainterna ?ti1) (temperaturaexterna ?te1))
    ?v2 <- (valvula (nombre ?n2) (temperaturainterna ?ti2) (temperaturaexterna ?te2))
    (test (= ?te1 ?te2))
    (test (< ?ti2 ?te2))
    =>
    (modify ?v1 (estado abierta))
    (modify ?v2 (estado abierta) (temperaturaexterna decremento (?ti2 ?te2)))
)

;<----FUNCIONES---->
(deffuction aumento (?p ?ti)
    (while (>= ?ti 35)
        (bind ?p1 (+ p 1))
        (bind ?ti1 (- ?ti 5))
    )
    (return ?p1)
);; aumento

(deffuction decremento (?ti2 ?te2)
    (if (> ?te2 ?ti2) then
        (bind ?teaux (- ?te2 ?ti2))
        (return ?teaux)
    )
);; aumento