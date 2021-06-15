"""
This file has been adapted from an example found at https://github.com/GenXProject/GenX
"""

cd(dirname(@__FILE__))
settings_path = joinpath(pwd(), "Settings")
#=
environment_path = "../../../package_activate.jl"
include(environment_path) #Run this line to activate the Julia virtual environment for GenX; skip it, if the appropriate package versions are installed
=#
### Set relevant directory paths
src_path = "$GENX_REPO_PATH"

inpath = pwd()

### Load GenX
println("Loading packages")
push!(LOAD_PATH, src_path)
using GenX
using YAML

genx_settings = joinpath(settings_path, "genx_settings.yml") #Settings YAML file path
mysetup = YAML.load(open(genx_settings)) # mysetup dictionary stores settings and GenX-specific parameters

### Cluster time series inputs if necessary and if specified by the user
TDRpath = joinpath(inpath, mysetup["TimeDomainReductionFolder"])
if mysetup["TimeDomainReduction"] == 1
    if (!isfile(TDRpath*"/Load_data.csv")) || (!isfile(TDRpath*"/Generators_variability.csv")) || (!isfile(TDRpath*"/Fuels_data.csv"))
        println("Clustering Time Series Data...")
        cluster_inputs(inpath, settings_path, mysetup)
    else
        println("Time Series Data Already Clustered.")
    end
end

### Configure solver
println("Configuring Solver")
OPTIMIZER = configure_solver(mysetup["Solver"], settings_path)

#### Running a case

### Load inputs
println("Loading Inputs")
myinputs = Dict() # myinputs dictionary will store read-in data and computed parameters
myinputs = load_inputs(mysetup, inpath)

### Generate model
println("Generating the Optimization Model")
EP = generate_model(mysetup, myinputs, OPTIMIZER)

### Solve model
println("Solving Model")
EP, solve_time = solve_model(EP, mysetup)
myinputs["solve_time"] = solve_time # Store the model solve time in myinputs

### Write output
# Run MGA if the MGA flag is set to 1 else only save the least cost solution
println("Writing Output")
outpath = "$inpath/Results"
write_outputs(EP, outpath, mysetup, myinputs)
if mysetup["ModelingToGenerateAlternatives"] == 1
    println("Starting Model to Generate Alternatives (MGA) Iterations")
    mga(EP, inpath, mysetup, myinputs, outpath)
end
