# Delta delay demo 
# Yngve Hafting 2024

import cocotb
from cocotb import start_soon
from cocotb.triggers import Edge, Timer, First, ReadOnly 
from cocotb.utils import get_sim_time   

async def monitor(dut):
    while True:
        ta = Edge(dut.a)
        tb = Edge(dut.b)
        tc = Edge(dut.c)
        await First(ta, tb, tc)
        #await ReadOnly()
        print(f"{get_sim_time(units='ps'):{9}.0f}ps   ",
              f"a:{(dut.a.value)}   ",
              f"b:{(dut.b.value)}   ",
              f"c:{(dut.c.value)}")

@cocotb.test()
async def main_test(dut):
    dut.a.value = 0
    start_soon(monitor(dut))
    for i in range(5):
        await Timer(100, units='ps')
        dut.a.value = not dut.a.value
    dut._log.info("test done")
