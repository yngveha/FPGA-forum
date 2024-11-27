-- Grayscale conversion using weights
-- To get valid output, weights should sum to 255 using 8 bit. 
-- Used in a pipelining exercise with Python based testbench for IN3160/4160
-- 
-- By Yngve Hafting, UiO
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all; 

entity grayscale is
  generic (N : natural := 8);
  port(
    reset, clk           : in  std_logic;
    R, G, B, WR, WG, WB  : in  std_logic_vector(N-1 downto 0);
    RGB_valid            : in  std_logic;
    Y                    : out std_logic_vector(N-1 downto 0);     
    overflow, Y_valid    : out std_logic
  );
end entity grayscale;


architecture RTL of grayscale is
  signal next_Y, r_Y               : unsigned(N-1 downto 0);
  signal next_valid, r_valid, 
         next_overflow, r_overflow : std_logic;
begin
  -- output from registers
  Y        <= std_logic_vector(r_Y);
  overflow <= r_overflow;
  Y_valid  <= r_valid;
  
  REG_ASSIGNMENT: process(clk) is  
  begin 
    if rising_edge(clk) then 
      if reset then 
        r_Y        <= (others => '0');
        r_valid    <= '0';
        r_overflow <= '0';
      else 
        r_Y        <= next_Y;
        r_valid    <= next_valid;
        r_overflow <= next_overflow;
      end if;
    end if;
  end process; 
  
  CALCULCATION: process (all) is
    variable i_sum  : unsigned(2*N+1 downto 0);
    variable i_R, i_G, i_B : unsigned(2*N-1 downto 0);
    variable i_overflow   : std_logic; 
  begin
    i_R := unsigned(WR) * unsigned(R);
    i_G := unsigned(WG) * unsigned(G);
    i_B := unsigned(WB) * unsigned(B);
    i_sum := unsigned("00" & i_R) + unsigned("00" & i_G) + unsigned("00" & i_B);
    i_overflow := or(i_sum(i_sum'left downto i_sum'left-1)); 
    next_Y <= (others => '1') when i_overflow else i_sum(2*N-1 downto N);
    next_overflow <= i_overflow;
    next_valid <= RGB_valid;
  end process;
  
end architecture RTL;