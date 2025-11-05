

# Python packages
import matplotlib.pyplot
import numpy
import os


# MRG packages
import _env
import preprocessing
import processing
import postprocessing
import solutions
import compute_alpha
numpy.set_printoptions(threshold=numpy.inf)
def binary_projection(chi, beta):
    beta = numpy.clip(beta, 0.0, 1.0)
    chi_flat = chi.flatten()
    n = len(chi_flat)
    chi_bin_flat = numpy.zeros_like(chi_flat, dtype=int)

    if beta > 0:
        threshold_index = int(round(beta * n))
        idx_sorted = numpy.argsort(-chi_flat)
        chi_bin_flat[idx_sorted[:threshold_index]] = 1

    # Reforme la matrice originale
    chi_bin = chi_bin_flat.reshape(chi.shape)
    return chi_bin

def your_optimization_procedure(domain_omega, spacestep, wavenumber, f, f_dir, f_neu, f_rob,
                           beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
                           Alpha, mu, chi, V_obj):
    """This function returns the optimized density.

    Parameter:
        cf solvehelmholtz's remarks
        Alpha: complex, it corresponds to the absorbtion coefficient;
        mu: float, it is the initial step of the gradient's descent;
        V_obj: float, it characterizes the volume constraint on the density chi.
    """
    #Parameters' initialisation
    k = 0
    (M, N) = numpy.shape(domain_omega)
    null=numpy.zeros((M,N))
    numb_iter = 100
    energy = numpy.zeros((numb_iter+1, 1), dtype=numpy.float64)
    while k < numb_iter and mu > 1e-7:
        print('---- iteration number = ', k)
        print('1. computing solution of Helmholtz problem, i.e., u')
        #u solution of the Helmholtz problem
        u = processing.solve_helmholtz(domain_omega, spacestep, wavenumber, f, f_dir, f_neu, f_rob,
                        beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob)
        print('2. computing solution of adjoint problem, i.e., p')
        #p solution of the adjoint problem
        p = processing.solve_helmholtz(domain_omega, spacestep, wavenumber, -2*numpy.conjugate(u), null, f_neu, f_rob,
                        beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob)
        print('3. computing objective function, i.e., energy')
        ene=energy[k]=your_compute_objective_function(domain_omega, u, spacestep)
        print('current energy:',ene)
        print('4. computing parametric gradient')
        #We set the new gradient on the robin's boundary
        grad=null.copy()
        for i in range(0, M):
            for j in range(0, N):
                if domain_omega[i, j] == _env.NODE_ROBIN:
                    grad[i,j]=-numpy.real(Alpha*u[i-1,j]*p[i-1,j])
        # While the energy is not diminishing
        while ene >= energy[k] and mu > 1e-7:
            #print('    a. computing gradient descent')
            chi_temp = chi -mu*grad
            # chi_temp=compute_gradient_descent(chi,grad,domain_omega,mu)
            #print('    b. computing projected gradient')
            chi_temp=compute_projected(chi_temp,domain_omega,V_obj)
            #print('    c. computing solution of Helmholtz problem, i.e., u')
            alpha_rob_temp=Alpha*chi_temp
            u=processing.solve_helmholtz(domain_omega, spacestep, wavenumber, f, f_dir, f_neu, f_rob,
                        beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob_temp)
            #print('    d. computing objective function, i.e., energy (E)')
            ene = your_compute_objective_function(domain_omega, u, spacestep)
            if ene<energy[k]:
                # The step is increased if the energy decreased
                mu = mu*1.1
                print('current energy good',ene)
            else:
                # The step is decreased if the energy increased
                mu = mu/2
                print('current energy bad',ene,'mu=',mu)
        #the chi we found is stored
        if ene<energy[k]:
            chi=chi_temp
            alpha_rob=alpha_rob_temp
        k += 1

    print('end. computing solution of Helmholtz problem, i.e., u')
    print('nb_iter',k)
    print('energy',energy[energy>0])
    return chi, energy, u, grad

def compute_projected(chi, domain, V_obj):
    """This function performs the projection of $\chi^n - mu*grad

    To perform the optimization, we use a projected gradient algorithm. This
    function caracterizes the projection of chi onto the admissible space
    (the space of $L^{infty}$ function which volume is equal to $V_{obj}$ and whose
    values are located between 0 and 1).

    :param chi: density matrix
    :param domain: domain of definition of the equations
    :param V_obj: characterizes the volume constraint
    :type chi: numpy.array((M,N), dtype=float64)
    :type domain: numpy.array((M,N), dtype=complex128)
    :type float: float
    :return:
    :rtype:
    """

    (M, N) = numpy.shape(domain)
    S = 0
    for i in range(M):
        for j in range(N):
            if domain[i, j] == _env.NODE_ROBIN:
                S = S + 1

    B = chi.copy()
    l = 0
    chi = preprocessing.set2zero(chi, domain)

    V = numpy.sum(numpy.sum(chi)) / S
    debut = -numpy.max(chi)
    fin = numpy.max(chi)
    ecart = fin - debut
    # We use dichotomy to find a constant such that chi^{n+1}=max(0,min(chi^{n}+l,1)) is an element of the admissible space
    while ecart > 10 **-6:
        # calcul du milieu
        l = (debut + fin) / 2
        for i in range(M):
            for j in range(N):
                chi[i, j] = numpy.maximum(0, numpy.minimum(B[i, j] + l, 1))
        chi = preprocessing.set2zero(chi, domain)
        V = sum(sum(chi)) / S
        if V > V_obj:
            fin = l
        else:
            debut = l
        ecart = fin - debut
        # print('le volume est', V, 'le volume objectif est', V_obj)

    return chi


def your_compute_objective_function(domain_omega, u, spacestep):
    """
    This function compute the objective function:
    J(u,domain_omega)= \int_{domain_omega}||u||^2 + mu1*(Vol(domain_omega)-V_0)
    """
    return numpy.sum(numpy.abs(u)**2)*spacestep*spacestep




if __name__ == '__main__':

    # ----------------------------------------------------------------------
    # -- Feel free to modify the function call in this cell.
    # ----------------------------------------------------------------------
    # -- set parameters of the geometry
    N = 50  # number of points along x-axis
    M = 2 * N  # number of points along y-axis
    level = 0 # level of the fractal
    spacestep = 1.0 / N  # mesh size

    # -- set parameters of the partial differential equation
    kx = -1.0
    ky = -1.0
    wavenumber = numpy.sqrt(kx**2 + ky**2)  # wavenumber
    speed = 343.0  # speed of sound in air
    wavenumber = 2*numpy.pi*800/340
    omega = wavenumber * speed  # angular frequency


    # ----------------------------------------------------------------------
    # -- Do not modify this cell, these are the values that you will be assessed against.
    # ----------------------------------------------------------------------
    # --- set coefficients of the partial differential equation
    beta_pde, alpha_pde, alpha_dir, beta_neu, alpha_rob, beta_rob = preprocessing._set_coefficients_of_pde(M, N)

    # -- set right hand sides of the partial differential equation
    f, f_dir, f_neu, f_rob = preprocessing._set_rhs_of_pde(M, N)

    # -- set geometry of domain
    domain_omega, x, y, _, _ = preprocessing._set_geometry_of_domain(M, N, level)

    # ----------------------------------------------------------------------
    # -- Fell free to modify the function call in this cell.
    # ----------------------------------------------------------------------
    # -- define boundary conditions
    # planar wave defined on top
    f_dir[:, :] = 0.0
    f_dir[0, 0:N] = 1.0
    # spherical wave defined on top
    #f_dir[:, :] = 0.0
    #f_dir[0, int(N/2)] = 10.0

    # -- initialize
    alpha_rob[:, :] = - wavenumber * 1j

    # -- define material density matrix
    chi = preprocessing._set_chi(M, N, x, y)
    chi = preprocessing.set2zero(chi, domain_omega)
    # -- define absorbing material
    #Alpha = 10.0 - 10.0 * 1j
    # -- this is the function you have written during your project
    Alpha = compute_alpha.real_to_complex(compute_alpha.compute_alpha(omega,'POLYESTER'))
    alpha_rob = Alpha * chi

    # -- set parameters for optimization
    S = 0  # surface of the fractal
    for i in range(0, M):
        for j in range(0, N):
            if domain_omega[i, j] == _env.NODE_ROBIN:
                S += 1
    V_0 = 1  # initial volume of the domain
    
    V_obj = 0.4  # constraint on the density
    mu = 5  # initial gradient step

    # ----------------------------------------------------------------------
    # -- Do not modify this cell, these are the values that you will be assessed against.
    # ----------------------------------------------------------------------
    # -- compute finite difference solution
    u = processing.solve_helmholtz(domain_omega, spacestep, wavenumber, f, f_dir, f_neu, f_rob,
                        beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob)
        
    chi0 = chi.copy()
    u0 = u.copy()
    

    # ----------------------------------------------------------------------
    # -- Fell free to modify the function call in this cell.
    # ----------------------------------------------------------------------
    # -- compute optimization
    energy = numpy.zeros((100+1, 1), dtype=numpy.float64)
    #chi, energy, u, grad = your_optimization_procedure(domain_omega, spacestep, omega, f, f_dir, f_neu, f_rob,
    #                       beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
    #                       Alpha, mu, chi, V_obj, mu1, V_0)
    chi, energy, u, grad = your_optimization_procedure(domain_omega, spacestep, wavenumber, f, f_dir, f_neu, f_rob,
                        beta_pde, alpha_pde, alpha_dir, beta_neu, beta_rob, alpha_rob,
                        Alpha, mu, chi, V_obj)
    # --- en of optimization

    chin = chi.copy()
    chibinary=binary_projection(chin,V_obj)
    print(chibinary)
    un = u.copy()
        # -- plot chi, u, and energy
    postprocessing._plot_uncontroled_solution(u0, chi0)
    postprocessing._plot_controled_solution(un, chibinary)
    


    err = un - u0
    postprocessing._plot_error(err)
     
    postprocessing._plot_energy_history(energy)


    print('End.')
