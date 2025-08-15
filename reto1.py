import sympy as sp
import streamlit as st

st.markdown("# 📊 Análisis Estructural Interactivo")
st.markdown("Genera valores, calcula reacciones y comprueba tus respuestas")

x=sp.Symbol("x")
R2=sp.Symbol("R2")

st.image("Analisis\examen1.png", caption="Reto 1. Método de Trabajo Virtual", use_container_width=True)

#función para hallar Area y centro de un trapecio
def trapecio(p,q,base):
    h=q-p
    m1=base*p*(base/2)
    m2=base*h*(base/6)
    mt=m1+m2
    return mt

def trapecio2(p,q,base,ext):
    h=q-p
    m1=base*p*(base/2+ext)
    m2=base*h*(base/3+ext)/2
    mt=m1+m2
    return mt

#Ecuación para el primer trapecio
def y1(base):
    m1=(w2-w1)/(6)
    b1=w1
    y1=m1*base+b1
    return y1

#Ecuación para el segundo trapecio
def y2(base):
    m2=(w3-w1)/4
    b2=w1
    y2=m2*base+b2
    return y2

# Si no existen en session_state, los inicializamos
if "w1" not in st.session_state:
    st.session_state.w1 = 5
if "w2" not in st.session_state:
    st.session_state.w2 = 15
if "w3" not in st.session_state:
    st.session_state.w3 = 12

# Inputs que usan los valores de session_state
w1 = st.number_input("Ingrese el valor de w1", value=st.session_state.w1, step=1)
w2 = st.number_input("Ingrese el valor de w2", value=st.session_state.w2, step=1)
w3 = st.number_input("Ingrese el valor de w3", value=st.session_state.w3, step=1)

R1 = (trapecio2(w1,w2,6,4) + trapecio(w1,w3,4))/10
r1=7/10

#CORTE 1
corte1_F1=trapecio(w1,y1(x),x)
corte1_R1= -R1*x

#CORTE 2
corte2_F1= trapecio(w1,y1(x+3),x+3)
corte2_R1= -R1*(x+3)

#CORTE 3
corte3_F1=trapecio2(w1,y1(6),6,x)
corte3_F2=trapecio(w1,y2(x),x)
corte3_R1= -R1*(x+6)

#Momentos de la Parte Real
M1= -(corte1_F1+ corte1_R1)
M2= -(corte2_F1+ corte2_R1)
M3= -(corte3_F1+ corte3_F2 + corte3_R1)

#PARTE VIRTUAL
#corte1
corte1_r1= r1*x

#corte2
corte2_f1= -1*x
corte2_r1= r1*(x+3)

#corte3
corte3_f1= -1*(x+3)
corte3_r1= r1*(x+6)


#momentos de la parte virtual
m1=  -corte1_r1
m2= -(corte2_f1 + corte2_r1)
m3= -(corte3_r1 + corte3_f1)

#integrales para delta1

delta1_x1 = sp.integrate(M1*m1,(x,0,3))
delta1_x2 = sp.integrate(M2*m2,(x,0,3))
delta1_x3 = sp.integrate(M3*m3,(x,0,4))

delta1_final = delta1_x1+delta1_x2+delta1_x3

#integrales para delta2
delta2_x1 = sp.integrate(m1**2,(x,0,3))
delta2_x2 = sp.integrate(m2**2,(x,0,3))
delta2_x3 = sp.integrate(m3**2,(x,0,4))

delta2_final = delta2_x1+delta2_x2+delta2_x3

#Ecuación para la reacción

eq = sp.Eq(delta1_final+R2*delta2_final,0)
sol = sp.solve(eq,R2)[0]


# 1️⃣ Input del usuario
respuesta = st.number_input("Ingrese el valor de R2", value=0.0)

# 2️⃣ Respuesta correcta (puede ser fija o calculada en tu código)
respuesta_correcta = sol.evalf(4)

# 3️⃣ Botón para evaluar
if st.button("Calificar"):
    if abs(respuesta - respuesta_correcta) < 1.5:  # margen de tolerancia
        st.success(f"✅ Correcto.")
    else:

        st.error(f"❌ Incorrecto.")
