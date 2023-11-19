from models.base import Approximation
from constants.const import *

from scipy.integrate import odeint
import sympy as sp


def euler_approx(
    approx: Approximation, consts: dict[str: float]
) -> dict[str, list[float]]:

    IND: list[float] = []
    DEP: list[float] = []
    ERR = [0]

    approx.h = (approx.eval_value - approx.ind_value) / approx.N
    _ind = approx.ind_value
    _dep = approx.dep_value

    IND = [_ind]
    DEP = [_dep]

    for _ in range(int(approx.N)):
        IND.append(IND[-1] + approx.h)
        DEP.append(eval_func(
            approx.f, consts,
            {approx.ind_var: IND[-1],
             approx.dep_var: DEP[-1]}
        ))
        ERR.append(abs(DEP[-1] - eval_func(  # ? exact_value(approx, consts))) #
            approx.f, consts,
            {approx.ind_var: _ind,
             approx.dep_var: _dep}
        )))
        # ERR.append(abs(DEP[-1] - exact_value(approx)))

    return {IND_KEY: DEP, DEP_KEY: IND, ERR_KEY: ERR}


def rk2_approx(
    approx: Approximation, consts: dict[str: float]
) -> dict[str, list[float]]:

    IND: list[float] = []
    DEP: list[float] = []

    approx.h = (approx.eval_value - approx.ind_value) / approx.N
    _ind = approx.ind_value
    _dep = approx.dep_value

    IND = [_ind]
    DEP = [_dep]
    ERR = [0]

    K1 = [eval_func(
        approx.f, consts,
        {approx.ind_var: _ind,
         approx.dep_var: _dep}
    )]
    K2 = [eval_func(
        approx.f, consts,
        {approx.ind_var: _ind + approx.h,
         approx.dep_var: _dep + approx.h*K1[-1]}
    )]
    for _ in range(int(approx.N)):
        IND.append(IND[-1] + approx.h)
        K1.append(eval_func(
            approx.f, consts,
            {approx.ind_var: IND[-1],
             approx.dep_var: DEP[-1]}
        ))
        K2.append(eval_func(
            approx.f, consts,
            {approx.ind_var: IND[-1] + approx.h,
             approx.dep_var: DEP[-1] + approx.h*K1[-1]}
        ))
        DEP.append(
            DEP[-1] + approx.h*(K1[-1] + K2[-1])/2  # ! Inside or outside?!
        )
        ERR.append(abs(DEP[-1] - eval_func(  # ? exact_value(approx, consts))) #
            approx.f, consts,
            {approx.ind_var: _ind,
             approx.dep_var: _dep}
        )))
    return {IND_KEY: DEP, DEP_KEY: IND, ERR_KEY: ERR}


def rk4_approx(
    approx: Approximation, consts: dict[str: float]
) -> dict[str, list[float]]:

    ind_ = approx.ind_value
    dep_ = approx.dep_value

    IND = [approx.ind_value]
    DEP = [approx.dep_value]
    ERR = [0]

    approx.h = (approx.eval_value-approx.ind_value) / approx.N
    K1 = [eval_func(
        approx.f, consts,
        {approx.ind_var: approx.ind_value,
          approx.dep_var: approx.dep_value}
    )]
    K2 = [eval_func(
        approx.f, consts,
        {approx.ind_var: approx.ind_value + approx.h/2,
         approx.dep_var: approx.dep_value + approx.h*K1[-1]/2}
    )]
    K3 = [eval_func(
        approx.f, consts,
        {approx.ind_var: approx.ind_value + approx.h/2,
         approx.dep_var: approx.dep_value + approx.h*K2[-1]/2}
    )]
    K4 = [eval_func(
        approx.f, consts,
        {approx.ind_var: approx.ind_value + approx.h,
         approx.dep_var: approx.dep_value + approx.h*K3[-1]}
    )]
    for i in range(approx.N):
        IND.append(IND[-1]+approx.h)
        K1.append(eval_func(
            approx.f, consts,
            {approx.ind_var: IND[-1],
             approx.dep_var: DEP[-1]}
        ))
        K2.append(eval_func(
            approx.f, consts,
            {approx.ind_var: IND[-1]+approx.h/2,
             approx.dep_var: DEP[-1]+approx.h*K1[-1]/2}
        ))
        K3.append(eval_func(
            approx.f, consts,
            {approx.ind_var: IND[-1]+approx.h/2,
             approx.dep_var: DEP[-1]+approx.h*K2[-1]/2}
        ))
        K4.append(eval_func(
            approx.f, consts,
            {approx.ind_var: IND[-1]+approx.h,
             approx.dep_var: DEP[-1]+approx.h*K3[-1]}
        ))
        DEP.append(
            DEP[-1] + approx.h*(
                K1[-1] + 2*K2[-1] + 2*K3[-1] + K4[-1]
            )/6
        )
        ERR.append(abs(DEP[-1] - eval_func(  # ? exact_value(approx, consts))) #
            approx.f, consts,
            {approx.ind_var: ind_,
             approx.dep_var: dep_}
        )))
    return {IND_KEY: IND, DEP_KEY: DEP, ERR_KEY: ERR}


def rk45_approx(func, dep_var, ind_var, dep_val, IND, constants):
    ode_result = odeint(
        odeint_adapter, dep_val, IND,
        args=(func, dep_var, ind_var, constants)
    )
    return ode_result


def eval_func(func, constants, vars_vals):
    # Convierte la función a una expresión sympy
    expr = sp.sympify(func)

    # Sustituye las variables y constantes en la expresión
    for var, val in vars_vals.items():
        expr = expr.subs(sp.symbols(var), val)
    for cte, val in constants.items():
        expr = expr.subs(sp.symbols(cte), val)

    # Evalúa la expresión
    return expr.evalf()

#


def odeint_adapter(y, x, func, dep_var, ind_var, constants):
    var_values = {dep_var: y, ind_var: x}
    return eval_func(func, constants, var_values)
