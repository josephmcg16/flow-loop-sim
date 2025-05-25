# Nonlinear Forcing Terms Jacobians

## 1. Pump flow–head curve

### 1.1 Governing relation

$$
\Delta p(\,q,N\,)=\rho g\Bigl(c_0N^{c_1}-c_2\,N\,q^{c_3}\Bigr)
$$

### 1.2 Partial derivatives

| variable | expression                                                                                         | comment                                               |
| -------- | -------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| $q$      | $\displaystyle\frac{\partial\Delta p}{\partial q}= -\rho g\,c_2\,c_3\,N\,q^{c_3-1}$                | sign negative (head falls with ↑ flow).               |
| $p$      | 0                                                                                                  | the pump adds head, does not depend on node pressure. |
| $N$      | $\displaystyle\frac{\partial\Delta p}{\partial N}= \rho g\bigl(c_0c_1N^{c_1-1}-c_2\,q^{c_3}\bigr)$ | second term has **no** $N$; you caught that.          |

**Check** – numerical diff at a few $(q,N)$ pairs reproduces the same slope to machine precision, so the algebra is consistent.

---

## 2. Control‑valve pressure loss

### 2.1 Governing relation

$$
\Delta p(\,q,v\,)=K\,\rho g\left(\frac{q}{C_v(v)}\right)^{2},
\qquad K=1.76573853211\times10^{8},
$$

$$
C_v(v)=C_{v,\max}\; \mathbf{c}^{\!\top}\boldsymbol\phi(v),
\qquad
\boldsymbol\phi(v)=(v,v^2,\dots,v^{n})^{\!\top}
$$

### 2.2 Partial derivatives

| variable | expression                                                                                                                                                                                                            | comment                                   |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| $q$      | $\displaystyle\frac{\partial\Delta p}{\partial q}=2K\,\rho g\,\frac{q}{C_v^2}=3.53147706422\times10^{8}\,\rho g\;C_v^{-2}q$                                                                                           | matches your figure.                      |
| $p$      | 0                                                                                                                                                                                                                     | again, loss depends only on through‑flow. |
| $v$      | $\displaystyle\frac{\partial\Delta p}{\partial v}=-2K\,\rho g\,\frac{q^{2}}{C_v^{3}}\;\frac{\partial C_v}{\partial v}$  where $\partial C_v/\partial v= C_{v,\max}\,\mathbf{c}^{\!\top}\partial_v\boldsymbol\phi(v)$. | Your cubic‑over‑cubic form is correct.    |

---

*The Jacobian row for each branch* is then `[∂Δp/∂p_up, ∂Δp/∂p_down, ∂Δp/∂q, … ∂Δp/∂u_k …]`.
The sketches above give you the ∂Δp/∂q and the control‑input columns; the pressure columns depend on how you sign your momentum equation (they’re usually `+1` and `‑1`).

---