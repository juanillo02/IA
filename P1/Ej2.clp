;Concesionario
;<----PLANTILLAS---->

(deftemplate Modelo
    (slot modelo)
    (slot precio (type INTEGER))
    (slot maletero (allowed-values pequeno mediano grande))
    (slot caballos (type INTEGER))
    (slot ABS (allowed-values si no))
    (slot consumo (type FLOAT))
);;Modelo

(deftemplate Formulario
    (slot Fprecio (type INTEGER)(default 13000))
    (slot Fmaletero (allowed-values pequeno mediano grande)(default grande))
    (slot Fcaballos (type INTEGER)(default 80))
    (slot FABS (allowed-values si no)(default si))
    (slot Fconsumo (type FLOAT)(default 8.0))
);;Formulario

;<----PLANTILLAS---->
(deffacts Defecto
    (Modelo
        (modelo Modelo1)
        (precio 12000)
        (maletero pequeno)
        (caballos 65)
        (ABS no)
        (consumo 4.7)
    )

    (Modelo
        (modelo Modelo2)
        (precio 12500)
        (maletero pequeno)
        (caballos 80)
        (ABS si)
        (consumo 4.9)
    )

    (Modelo
        (modelo Modelo3)
        (precio 13000)
        (maletero mediano)
        (caballos 100)
        (ABS si)
        (consumo 7.8)
    )

    (Modelo
        (modelo Modelo4)
        (precio 14000)
        (maletero grande)
        (caballos 125)
        (ABS si)
        (consumo 6.0)
    )

    (Modelo
        (modelo Modelo5)
        (precio 15000)
        (maletero pequeno)
        (caballos 147)
        (ABS si)
        (consumo 8.5)
    )

    (Formulario
        (Fprecio 13000)
    )
)

;<----Reglas---->
(defrule Recomendacion
    (Modelo (modelo ?m) (precio ?p) (maletero ?mal) (caballos ?c) (ABS ?a) (consumo ?con))
    (Formulario (Fprecio ?Fp) (Fmaletero ?Fmal) (Fcaballos ?Fc) (FABS ?Fa) (Fconsumo ?Fcon))
    (test (<= ?p ?Fp))
    (test (>= ?c ?Fc))
    (test (<= ?con ?Fcon))
    =>
    (assert(Recomendacion ?m))
);;Recomendación