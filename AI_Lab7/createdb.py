import torch
import math

values = (20. * torch.rand(1000, 2) - 10.)

function_values = []
for i in range(1000):
    a = values[i][0]
    b = values[i][1]
    function_result = torch.sin(a + b / math.pi)
    function_values.append(function_result)

function_values = torch.tensor(function_values)
result = torch.column_stack((values,function_values))

torch.save(result, "mydataset.dat")
