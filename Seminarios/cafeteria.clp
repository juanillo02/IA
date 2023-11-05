;<----PLANTILLAS---->
(deftemplate Personal
    (slot DNI)
    (slot nombre)
    (slot turno (allowed-values Manana Tarde Ambos))
    (slot totVentas)
    (slot encargado (allowed-values Si No))
);; Personal

(deftemplate Producto
    (slot id)
    (slot nombre)
    (slot stockCaf)
    (slot stockAlm)
    (slot precioUd)
    (slot max (default 30))
);; Producto

(deftemplate Ventas
    (slot camarero)
    (slot producto)
    (slot ud)
    (slot Pago (allowed-values Tarjeta Efectivo Bono))
);;Ventas

;<----REGLAS---->
(defrule AsignarVenta
    (declare (salience 1));; Dar prioridad
    ?pers <- (Personal (DNI ?dni) (totVentas ?totVentas))
    ?prod <- (Producto (id ?id) (stockCaf ?stockCaf) (precioUd ?precioUd))
    ?ventas <- (Ventas (camarero ?dni) (producto ?id) (ud ?ud) (Pago ?Pago))
    (test (<= ?ud ?stockCaf))
    (test (> ?ud 0))
    =>
    (bind aux(+ ?totVentas (* ?ud ?precioUd)))
    (modify ?pers (totVentas ?aux))
    (modify ?prod (stockCaf (- ?stockCaf ?ud)))
    (printout t ?aux)
    (retract ?ventas)
);; AsignarVenta

(defrule ReponerStock
    ?prod  <- (Producto (id ?id) (stockCaf ?stockCaf) (stockAlm ?stockAlm) (max ?max))
    (test (< ?stockAlm 10))
    =>
    (bind ?aux (Reposicion (?stockAlm ?stockCaf ?max)))
    (modify ?prod (stockAlm (- ?stockAlm ?aux)) (stockCaf (+ ?stockCaf ?aux)))
);;ReponerStock

;<----FUNCIONES---->
(deffunction Reposicion (?stockAlm (?stockCaf) (?max))
    (if (<= (- ?max ?stockCaf) ?stockAlm) then
    (return (- ?max ?stockCaf))
    else
    (return ?stockAlm)
    )
);;Reposicion