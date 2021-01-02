E = 10000 # N/mm2
nu = 0.25
Gc = 0.001
l = 0.015 # mm
psic = 14.88
k = 1e-09

[MultiApps]
  [fracture]
    type = TransientMultiApp
    input_files = 'fracture.i'
    app_type = raccoonApp
    execute_on = 'TIMESTEP_BEGIN'
    cli_args = 'Gc=${Gc};l=${l};psic=${psic};k=${k}'
  []
[]

[Transfers]
  [send_E_el_active]
    type = MultiAppCopyTransfer
    multi_app = fracture
    direction = to_multiapp
    source_variable = 'E_el_active'
    variable = 'E_el_active'
  []
  [get_d]
    type = MultiAppCopyTransfer
    multi_app = fracture
    direction = from_multiapp
    source_variable = 'd'
    variable = 'd'
  []
[]

[Mesh]
  type = FileMesh
  file = '../mesh/mesh_linear_fine.inp'
  construct_node_list_from_side_list = false
[]

[Variables]
  [disp_x]
  []
  [disp_y]
  []
  [disp_z]
  []
[]

[AuxVariables]
  [d]
  []
  [E_el_active]
    order = CONSTANT
    family = MONOMIAL
  []
  [fx]
  []
[]

[AuxKernels]
  [E_el]
    type = ADMaterialRealAux
    variable = 'E_el_active'
    property = 'E_el_active'
    execute_on = 'TIMESTEP_END'
  []
[]

[Kernels]
  [solid_x]
    type = ADStressDivergenceTensors
    variable = 'disp_x'
    component = 0
    displacements = 'disp_x disp_y disp_z'
    save_in = 'fx'
  []
  [solid_y]
    type = ADStressDivergenceTensors
    variable = 'disp_y'
    component = 1
    displacements = 'disp_x disp_y disp_z'
  []
  [solid_z]
    type = ADStressDivergenceTensors
    variable = 'disp_z'
    component = 2
    displacements = 'disp_x disp_y disp_z'
  []
[]

[BCs]
  [bottom_x]
    type = DirichletBC
    variable = disp_x
    boundary = bottom
    value = 0
  []
  [bottom_y]
    type = DirichletBC
    variable = disp_y
    boundary = bottom
    value = 0
  []
  [bottom_z]
    type = DirichletBC
    variable = disp_z
    boundary = bottom 
    value = 0
  []
  [top_x]
    type = FunctionDirichletBC
    variable = disp_x
    boundary = top
    function = '1 * t'
  []
  [top_y]
    type = DirichletBC
    variable = disp_y
    boundary = top
    value = 0
  []
  [top_z]
    type = DirichletBC
    variable = disp_z
    boundary = top 
    value = 0
  []
[]

[Materials]
  [elasticity_tensor]
    type = ADComputeIsotropicElasticityTensor
    youngs_modulus = ${E}
    poissons_ratio = ${nu}
  []
  [strain]
    type = ADComputeSmallStrain
    displacements = 'disp_x disp_y disp_z'
  []
  [stress]
    type = SmallStrainDegradedElasticPK2Stress_StrainSpectral
    d = 'd'
  []
  [fracture_properties]
    type = ADGenericFunctionMaterial
    prop_names = 'energy_release_rate phase_field_regularization_length critical_fracture_energy'
    prop_values = '${Gc} ${l} ${psic}'
  []
  [local_dissipation]
    type = LinearLocalDissipation
    d = d
  []
  [phase_field_properties]
    type = ADFractureMaterial
    local_dissipation_norm = 8/3
  []
  [degradation]
    type = QuadraticDegradation
    d = d
    residual_degradation = ${k}
  []
[]

[Executioner]
  type = Transient
  solve_type = 'NEWTON'
  petsc_options_iname = '-pc_type -pc_factor_mat_solver_package'
  petsc_options_value = 'lu       superlu_dist'

  dt = 1e-5
  end_time = 2e-3
  nl_rel_tol = 1e-06
  nl_abs_tol = 1e-08

  automatic_scaling = true

  picard_max_its = 100
  picard_abs_tol = 1e-50
  picard_rel_tol = 1e-03
  accept_on_max_picard_iteration = true
[]

[Postprocessors]
  [Fx]
    type = NodalSum
    variable = 'fx'
    boundary = 'top'
  []
[]

[Outputs]
  print_linear_residuals = false
  print_linear_converged_reason = false
  print_nonlinear_converged_reason = false
  [csv]
    type = CSV
    file_base = 'fd'
  []
  [exodus]
    type = Exodus
    file_base = 'pv'
  []
[]
