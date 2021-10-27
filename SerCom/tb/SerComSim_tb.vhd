
--------------------------------------------------------------------------------
-- LIBRARIES
--------------------------------------------------------------------------------
library IEEE;
   use IEEE.STD_LOGIC_1164.ALL;
   use IEEE.NUMERIC_STD.ALL;


library lvin_Verification_Axi4LiteIntf_v1_0;
   use lvin_Verification_Axi4LiteIntf_v1_0.Axi4LiteIntf_pkg.all;

library lvin_Verification_Axi4LiteTransactor_v1_0;
   use lvin_Verification_Axi4LiteTransactor_v1_0.Axi4LiteTransactor_pkg.all;


--------------------------------------------------------------------------------
-- ENTITY
--------------------------------------------------------------------------------
entity SerComSim_tb is
end SerComSim_tb;


--------------------------------------------------------------------------------
-- ARCHITECTURE
--------------------------------------------------------------------------------
architecture tb of SerComSim_tb is

   signal AClk     : std_logic;
   signal AResetn  : std_logic;

   constant c_PeriodAClk : time    := 10 ns;
   signal ClockEnable    : boolean := False;

   constant IntfIndex : natural := 0;
   alias CtrlIntf : t_Axi4LiteIntf is lvin_Verification_Axi4LiteIntf_v1_0.Axi4LiteIntf_pkg.Axi4LiteIntfArray(IntfIndex);

begin

   -----------------------------------------------------------------------------
   -- CLOCKS
   -----------------------------------------------------------------------------
   p_AClk : process
   begin
      AClk <= '0';
      wait until ClockEnable = True;
      while ClockEnable loop
         wait for c_PeriodAClk/2;
         AClk <= not AClk;
      end loop;
      wait;
   end process p_AClk;


   -----------------------------------------------------------------------------
   -- DUT
   -----------------------------------------------------------------------------
   DUT : entity work.SerComSim
      port map(
         AClk     => AClk   ,
         AResetn  => AResetn
      );


   -----------------------------------------------------------------------------
   -- MAIN
   -----------------------------------------------------------------------------
   process 
      variable slv_data : std_logic_vector(31 downto 0);
      variable int_data : integer;
   begin
      AResetn <= '0';
      InitAxi(CtrlIntf);

      wait for 10*c_PeriodAClk;
      ClockEnable <= True;

      Idle(CtrlIntf, 10);
      AResetn <= '1';

      Idle(CtrlIntf, 50);
      --------------------------------------------------------------------------

      
      Idle(CtrlIntf, 30);
      WriteAxi(CtrlIntf, x"A3A2A1A0", x"D3D2D1D0");

      Idle(CtrlIntf, 30);
      ReadAxi(CtrlIntf,  x"A7A6A5A4", slv_data);


      --------------------------------------------------------------------------
      Idle(CtrlIntf, 10);
      AResetn <= '0';

      Idle(CtrlIntf, 10);
      ClockEnable <= False;

      wait for 10*c_PeriodAClk;
      report "Simulation Finished";

      wait;
   end process;

   
end tb;
