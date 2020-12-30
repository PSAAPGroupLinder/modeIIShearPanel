import matplotlib.pyplot as plt
import numpy as np

# tex for pretty plots
plt.rcParams.update({
    "text.usetex": True,
    'text.latex.preamble':r'\usepackage{siunitx}'
    })

fig = plt.figure()
ax = fig.add_subplot(111)

# plot gradient_enhanced_rankine curves
files_gradient_enhanced_rankine = {
# './gradient_enhanced_rankine/rankine_epsf=1e-1_ldam=1e-2.csv' : r'ge rankine: $\epsilon_f=\num{1e-1}, l=\SI{2}{1e-2}{mm}$', # too ductile
# './gradient_enhanced_rankine/rankine_epsf=1e-1_ldam=2e-2.csv' : r'ge rankine: $\epsilon_f=\num{1e-1}, l=\SI{2}{2e-2}{mm}$', # too ductile
'./gradient_enhanced_rankine/rankine_epsf=1e-3_ldam=1e-2.csv' : r'ge rankine: $\epsilon_f=\num{1e-3}, l=\SI{1e-2}{mm}$', 
'./gradient_enhanced_rankine/rankine_epsf=1e-3_ldam=2e-2.csv' : r'ge rankine: $\epsilon_f=\num{1e-3}, l=\SI{2e-2}{mm}$', 
'./gradient_enhanced_rankine/rankine_epsf=2.5e-3_ldam=1e-2.csv' : r'ge rankine: $\epsilon_f=\num{2.5e-3}, l=\SI{1e-2}{mm}$', 
'./gradient_enhanced_rankine/rankine_epsf=2.5e-3_ldam=2e-2.csv' : r'ge rankine: $\epsilon_f=\num{2.5e-3}, l=\SI{2e-2}{mm}$', 
'./gradient_enhanced_rankine/rankine_epsf=5e-3_ldam=1e-2.csv' : r'ge rankine: $\epsilon_f=\num{5e-3}, l=\SI{1e-2}{mm}$', 
'./gradient_enhanced_rankine/rankine_epsf=5e-3_ldam=1e-2.csv' : r'ge rankine: $\epsilon_f=\num{5e-3}, l=\SI{2e-2}{mm}$', 
'./gradient_enhanced_rankine/rankine_epsf=7.5e-3_ldam=1e-2.csv' : r'ge rankine: $\epsilon_f=\num{7.5e-3}, l=\SI{1e-2}{mm}$', 
'./gradient_enhanced_rankine/rankine_epsf=7.5e-3_ldam=2e-2.csv' : r'ge rankine: $\epsilon_f=\num{7.5e-3}, l=\SI{2e-2}{mm}$', 
# './gradient_enhanced_rankine/rankine_epsf=5e-3_ldam=2e-2.csv' : r'ge rankine: $\epsilon_f=\num{5e-3}, l=\SI{2e-2}{mm}$',  # aborted early
# './gradient_enhanced_rankine/rankine_epsf=5e-5_ldam=1e-2.csv' : r'ge rankine: $\epsilon_f=\num{5e-5}, l=\SI{2}{1e-2}{mm}$', # too brittle
# './gradient_enhanced_rankine/rankine_epsf=5e-5_ldam=2e-2.csv' : r'ge rankine: $\epsilon_f=\num{5e-5}, l=\SI{2}{2e-2}{mm}$', # too brittle
}

colors_rankine = plt.cm.viridis(np.linspace(0.0, .8, len(files_gradient_enhanced_rankine) ))

for color , (f, lab) in zip (colors_rankine, files_gradient_enhanced_rankine.items() ):
    
    data = np.loadtxt ( f, delimiter=',', skiprows=1)

    U = data[:,0] * 1e-2 # time to displacment
    RF = data[:,1] * -1  # correct sign

    ax.plot(U, RF, label=lab, c = color)
# end plot gradient_enhanced_rankine curves

# plot the efem results
files_efem = {'./embedded_fem/efem_lin_coarse_mode2.csv' : r'efem-lin-coarse-mesh-mode2',
              './embedded_fem/efem_lin_coarse_mixed.csv' : r'efem-lin-coarse-mesh-mixed',
              './embedded_fem/efem_lin_medium_mixed.csv' : r'efem-lin-medium-mesh-mixed',              
	      './embedded_fem/efem_lin_fine_mixed.csv' : r'efem-lin-fine-mesh-mixed',}

colors_efem = plt.cm.Reds_r(np.linspace(0.0, 0.7, len(files_efem) ))

for color , (f, lab) in zip(colors_efem, files_efem.items()):
    
    data = np.loadtxt ( f, delimiter=' ', skiprows=0)

    U = data[:,0]
    RF = data[:,1]

    ax.plot(U, RF, label=lab, c = color, linestyle = '--')
# end plot embedded_fem curves

# make plots readable
ax.set_xlabel('shear (mm)')
ax.set_ylabel('reaction force (N)')
ax.grid(True)
fig.legend()

fig.savefig('load_displacement_curves_comparison.png')

plt.show()
