from models.base import Approximation
from constants.const import *

from scipy.integrate import odeint
import numpy as np
import numexpr as ne


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
        # ?! LOG ERROR
        ERR.append(abs(DEP[-1] - eval_func(  # ? exact_value(approx, consts))) #
            approx.f, consts,
            {approx.dep_var: _dep,
             approx.ind_var: _ind}
        )))

    print('\n\nEULER METHOD COMPLETED')

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
        # ?! LOG ERROR
        ERR.append(abs(DEP[-1] - eval_func(  # ? exact_value(approx, consts))) ? #
            approx.f, consts,
            {approx.dep_var: _dep,
             approx.ind_var: _ind}
        )))

    print('\n\nRK2 METHOD COMPLETED')

    return {IND_KEY: DEP, DEP_KEY: IND, ERR_KEY: ERR}


def rk4_approx(
    approx: Approximation, consts: dict[str: float]
) -> dict[str, list[float]]:
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
        {approx.ind_var: _ind + approx.h/2,
         approx.dep_var: _dep + approx.h*K1[-1]/2}
    )]
    K3 = [eval_func(
        approx.f, consts,
        {approx.ind_var: _ind + approx.h/2,
         approx.dep_var: _dep + approx.h*K2[-1]/2}
    )]
    K4 = [eval_func(
        approx.f, consts,
        {approx.ind_var: _ind + approx.h,
         approx.dep_var: _dep + approx.h*K3[-1]}
    )]
    for _ in range(approx.N):
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
            )/6  # ! Inside or outside?!
        )
        # ?! LOG ERROR
        ERR.append(abs(DEP[-1] - eval_func(  # ? exact_value(approx, consts))) #
            approx.f, consts,
            {approx.dep_var: _dep,
             approx.ind_var: _ind}
        )))

    print('\n\nRK4 METHOD COMPLETED')
    return {IND_KEY: IND, DEP_KEY: DEP, ERR_KEY: ERR}


def eval_func(func: str, consts: dict[str: float], vars_vals: dict[str: float]):
    # Combinar las variables y los parámetros en un solo diccionario
    all_vars = {**vars_vals, **consts}
    if 'E' in func and 'E' not in all_vars:
        all_vars['E'] = np.e
    # Preparar el entorno de variables para numexpr
    ne.set_num_threads(1)  # Utilizar un solo hilo para la evaluación
    # Convertir valores a arrays de numpy
    local_vars = {k: np.array(v) for k, v in all_vars.items()}

    # Evaluar la expresión usando numexpr
    result = ne.evaluate(func, local_dict=local_vars)

    return result


def odeint_adapter(dep, ind, func, dep_var, ind_var, constants):
    var_values = {dep_var: dep, ind_var: ind}
    return eval_func(func, constants, var_values)


def rk45_approx(func, dep_var, ind_var, dep_val, IND, constants):
    ode_result = odeint(
        odeint_adapter, dep_val, IND,
        args=(func, dep_var, ind_var, constants)
    )
    return ode_result
