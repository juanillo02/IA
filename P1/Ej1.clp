;Ejercicio mapa
; Utilizamos el siguiente mapa:
;   A B C
;   D E F
;   G H I

; <----Hechos---->

(deffacts mapa
    (ubicacion A Norte D)
    (ubicacion A Oeste B)
    (ubicacion B Norte H)
    (ubicacion B Oeste C)
    (ubicacion C Norte F)
    (ubicacion D Norte G)
    (ubicacion D Oeste E)
    (ubicacion E Norte H)
    (ubicacion E Oeste F)
    (ubicacion F Norte I)
    (ubicacion G Oeste H)
    (ubicacion H Oeste I)
)

; <----Reglas---->

(defrule EstaAlSur
    (ubicacion ?a Norte ?b)
    =>
    (assert(ubicacion ?b Sur ?a))
);;EstaAlSur

(defrule EstaAlEste
    (ubicacion ?a Oeste ?b)
    =>
    (assert(ubicacion ?b Este ?a))
);;EstaAlEste

(defrule Transitividad
    (ubicacion ?a ?d ?b)  ;;d es la ubicación
    (ubicacion ?b ?d ?c)
    =>
    (assert(ubicacion ?a ?d ?c))
);;Transitividad

(defrule EstaAlNoresteSuroeste
    (ubicacion ?a Norte ?b)
    (ubicacion ?b Este ?c)
    =>
    (assert(ubicacion ?a NorEste ?c))
    (assert(ubicacion ?c SurOeste ?a))
);;EstaAlNorsteSuroeste

(defrule EstaAlNorOeste
    (ubicacion ?a Norte ?b)
    (ubicacion ?b Oeste ?c)
    =>
    (assert(ubicacion ?a NorOeste ?c))
    (assert(ubicacion ?c Sureste ?a))
);;EstaAlNorOesteSureste

(defrule DecirUbicacion
    ?f1 <-(situacion ?x ?y)
    (ubicacion ?x ?u ?y)
    =>
    (printout t ?x " esta al " ?u " de " ?y crlf)
    (retract ?f1)
);; DecirUbicación