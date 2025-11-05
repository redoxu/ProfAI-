    """    chin = chi.copy()
        un = u.copy()
    """
        # -- plot chi, u, and energy
    """    postprocessing._plot_uncontroled_solution(u0, chi0)
        postprocessing._plot_controled_solution(un, chin)
        err = un - u0
        postprocessing._plot_error(err)
    """    
