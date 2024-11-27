# Grayscale testbench- Uses an image as input. Output is scaled down to optimize runtime. 
# Weights should sum to 255 (higher values can be used to trigger overflow check) 
# Used in pipelining exercise in IN3160/4160 course 
# Two checkers will require modification when making a pipelined module.  
#
# The testbench showcases leveraging python libraries (Python image library, PIL, Pillow)
# By the use of PIL, image input are passed to DUT, and DUT output is used 
# to build a grayscale image. The images can be of types supported by PIL 
# (jpg and png has been tested for input), and can be opened in image viewers.
# Images for input is put in the images folder, output images goes in the output folder
#
# By Yngve Hafting, UIO 2023, 2024
#

import cocotb
from cocotb.triggers import RisingEdge, FallingEdge, ReadOnly, ClockCycles
from cocotb.clock import Clock
from cocotb.utils import get_sim_time

# If not installed, use pip install Pillow. WSL has Pillow installed
# https://pillow.readthedocs.io/en/stable/reference/Image.html 
from PIL import Image

# For opening window in WSL-- can be omitted -- (used line 116, 139, main_test)))
# see https://stackoverflow.com/questions/12570859/how-to-show-pil-images-on-the-screen 
import os

CLOCK_PERIOD_NS = 10

# Downscale image output to make simulation run faster. (Typ 1-100)
SCALING = 4      # 1 renders full image size. Output will be Input/(Scaling^2) pixels

async def reset_dut(dut):
    await FallingEdge(dut.clk)
    dut.reset.value      = 1
    dut.R.value = 0
    dut.G.value = 0
    dut.B.value = 0
    dut.RGB_valid.value = 0
    dut.WR.value = 76
    dut.WG.value = 150
    dut.WB.value = 29
    await RisingEdge(dut.clk)
    dut.reset.value = 0

''' STIMULI '''
async def stimuli_generator(dut, img):
    width = img.width//SCALING
    height = img.height//SCALING
    await FallingEdge(dut.clk)
    dut.RGB_valid.value = 1
    for j in range(height):
        for i in range(width):
           xy = (i*SCALING, j*SCALING)
           RGB = img.getpixel(xy)
           dut.R.value = RGB[0]
           dut.G.value = RGB[1]
           dut.B.value = RGB[2]
           await FallingEdge(dut.clk)
    dut.RGB_valid.value = 0

    
''' MONITORS and checks '''
async def overflow_check(dut):
    while True:
        await RisingEdge(dut.overflow)
        assert False, "Overflow has occured"
        
async def gray_check(dut):
    while True:
        await RisingEdge(dut.clk)
        await ReadOnly()
        CheckR = dut.WR.value * dut.R.value
        CheckG = dut.WG.value * dut.G.value
        CheckB = dut.WB.value * dut.B.value
        if dut.Y_valid.value == True:
            CheckGray = (CheckR+CheckG+CheckB)>>8
            assert CheckGray == int(dut.Y.value), (
                f"Model value: {CheckGray} != simulated value: {int(dut.Y.value)} ")

async def valid_check(dut):
    while True:
        await FallingEdge(dut.clk)
        await ReadOnly()
        data_valid = dut.RGB_valid.value
        await RisingEdge(dut.clk)
        await ReadOnly()
        assert data_valid == dut.Y_valid.value, "Y_valid does not follow RGB_ready"
        

async def monitor(dut):
    cocotb.start_soon(overflow_check(dut))
    cocotb.start_soon(gray_check(dut))
    cocotb.start_soon(valid_check(dut))

async def grayscale_builder(dut, gray):
    for j in range(gray.height):
      for i in range(gray.width):
        await RisingEdge(dut.clk)
        await ReadOnly()
        if dut.Y_valid.value == True:
            Y_value = int(dut.Y.value)
            gray.putpixel((i,j), Y_value)
        else:    
          i= i-1

''' @cocotb test starts everything '''
@cocotb.test()
async def main_test(dut):
    dut._log.info("### Opening image ###")
    #img = Image.open('images/mc.jpg')
    img = Image.open('images/testbench.png')
    
    # Opening image from testbench is optional. (OS dependant)
    #img.show() # Default, should work on native linux, does not work using WSL 
    os.system("powershell.exe -c start images/testbench.png")  # works with WSL 
    
    width = img.width//SCALING
    height = img.height//SCALING
    gray = Image.new('L', (width, height)) # L for Luma = grayscale has only 1 value per pixel

    dut._log.info("### Starting test ###")
    cocotb.start_soon(Clock(dut.clk, CLOCK_PERIOD_NS, units='ns').start())
    await reset_dut(dut)
    cocotb.start_soon(monitor(dut))
    cocotb.start_soon(grayscale_builder(dut, gray))
    await stimuli_generator(dut, img);
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut._log.info("### Test finished, saving grayscale image ###")
    
    img.close()
    gray.save("output/grayscale.png")
    dut._log.info("### Grayscale image saved to output folder ###")
    gray.close()
    
    # Opening output image can be omitted. 
    #gray.show() #Linux default
    os.system("powershell.exe -c output/grayscale.png")  # WSL solution
