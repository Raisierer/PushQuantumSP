import neal

from data.sp_data import SPData
from lunaHelper import write_json
from models import SPQuboBinary
from evaluation.evaluation import SPEvaluation
from plotting.sp_plot import SPPlot

params = {"lidar_density": 0.1, "street_point_density": 0.1}
data = SPData().create_problem_from_glb_file(**params)
plt = SPPlot(data).plot_problem()
plt.show()

config = {"num_reads":1000,"num_sweeps":1000}
solve_func = neal.SimulatedAnnealingSampler().sample_qubo
qubo_model_bin = SPQuboBinary(data, P1=.5)

print(qubo_model_bin.model)
write_json(qubo_model_bin.model.tolist(), "./input/qubo_glb.json")

answer = qubo_model_bin.solve(solve_func, **config)

evaluation = SPEvaluation(data, answer['solution'])
print(f"solution clean: {evaluation.solution}")

print(f"objective = {evaluation.get_objective()}")
for constraint, violations in evaluation.check_solution().items():
    if len(violations) > 0:
        print(f"constraint {constraint} was violated {len(violations)} times")

plt = SPPlot(data, evaluation).plot_solution(hide_never_covered = True)
plt.show()
