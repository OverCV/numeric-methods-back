import math
# def eval_func(
#     func: str, consts: dict[str, float],
#     ind_var: str, ind_val: float,
#     dep_var: str, dep_val: float
# ) -> float:

#     ind_key = sp.symbols(ind_var)
#     dep_key = sp.symbols(dep_var)

#     expr = sp.sympify(func)
#     expr = expr.subs({dep_key: dep_val, ind_key: ind_val})

#     for const, value in consts.items():
#         expr = expr.subs(sp.symbols(const), value)

#     return expr.evalf()


def ln(values):
    return list(map(lambda x: math.log(x), values))


# def euler_approx(approx: Approximation) -> None:
#     T: list[int] = []
#     X: list[int] = []

#     approx.h = (approx.t - approx.t0) / approx.N
#     t = approx.t0
#     x = approx.x0

#     T = [t]
#     X = [x]

#     for i in range(int(approx.N)):
#         x += approx.h * func(approx.func, t, x)
#         t += approx.h
#         T.append(t)
#         X.append(x)


# ! Parte del método Create_Graphs (como no sirve):
    # # Crear directamente la instancia de Graph
    # db_graph = instance_graph(euler_graph, db)
    # # db_graph = Graph(**euler_graph, approximation_id=db_approx.id)

    # # Asociar el Graph con Approximation
    # db_approx.graphs.append(db_graph)
    # db.commit()
    # db.refresh(db_approx)

    # print(db_approx.graphs)  # Verificar la asociación

    # return ApproxRead(**db_approx.__dict__), status.HTTP_201_CREATED

