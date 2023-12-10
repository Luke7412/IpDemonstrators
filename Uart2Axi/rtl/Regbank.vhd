
--------------------------------------------------------------------------------
-- LIBRARIES
--------------------------------------------------------------------------------
library IEEE;
   use IEEE.STD_LOGIC_1164.ALL;
   use IEEE.numeric_std.all;


--------------------------------------------------------------------------------
-- ENTITY
--------------------------------------------------------------------------------
entity Regbank is
   Generic (
      g_ADDRESS_WIDTH : natural := 8
   );
   Port ( 
      -- Clock and Reset
      AClk         : in  std_logic;
      AResetn      : in  std_logic;
      -- AXI4-Lite Interface
      Ctrl_ARValid : in  std_logic;
      Ctrl_ARReady : out std_logic;
      Ctrl_ARAddr  : in  std_logic_vector(g_ADDRESS_WIDTH-1 downto 0);
      Ctrl_RValid  : out std_logic;
      Ctrl_RReady  : in  std_logic;
      Ctrl_RData   : out std_logic_vector(31 downto 0);
      Ctrl_RResp   : out std_logic_vector(1 downto 0);
      Ctrl_AWValid : in  std_logic;
      Ctrl_AWReady : out std_logic;
      Ctrl_AWAddr  : in  std_logic_vector(g_ADDRESS_WIDTH-1 downto 0);
      Ctrl_WValid  : in  std_logic;
      Ctrl_WReady  : out std_logic;
      Ctrl_WData   : in  std_logic_vector(31 downto 0);
      Ctrl_WStrb   : in  std_logic_vector(3 downto 0);
      Ctrl_BValid  : out std_logic;
      Ctrl_BReady  : in  std_logic;
      Ctrl_BResp   : out std_logic_vector(1 downto 0)
   );
end entity Regbank;


--------------------------------------------------------------------------------
-- ARCHITECTURE
--------------------------------------------------------------------------------
architecture rtl of Regbank is
   
   type t_RegArr is array (integer range <>) of std_logic_vector(31 downto 0);
   signal RegArr : t_RegArr(0 to 2**(g_ADDRESS_WIDTH-2));

   signal Ctrl_ARReady_i : std_logic;
   signal Ctrl_RValid_i  : std_logic;
   signal Ctrl_AWReady_i : std_logic;
   signal Ctrl_WReady_i  : std_logic;
   signal Ctrl_BValid_i  : std_logic;

   alias ARAddr : std_logic_vector(g_ADDRESS_WIDTH-3 downto 0) is Ctrl_ARAddr(Ctrl_ARAddr'high downto 2);
   alias AWAddr : std_logic_vector(g_ADDRESS_WIDTH-3 downto 0) is Ctrl_AWAddr(Ctrl_ARAddr'high downto 2);

begin

   Ctrl : process(AClk, AResetn) is
      variable Address : integer;
   begin
      if AResetn = '0' then
         Ctrl_RValid_i <= '0';
         Ctrl_BValid_i <= '0';

      elsif rising_edge(AClk) then
         
         -- Read Handshake
         if Ctrl_ARValid = '1' and Ctrl_ARReady_i = '1' then
            Address       := to_integer(unsigned(ARAddr));
            Ctrl_RValid_i <= '1';
            Ctrl_RData    <= RegArr(Address);

         elsif Ctrl_RValid_i = '1' and Ctrl_RReady = '1' then
            Ctrl_RValid_i <= '0';
         end if;


         -- Write Handshake
         if Ctrl_AWValid = '1' and Ctrl_AWReady_i = '1' and Ctrl_WValid = '1' and Ctrl_WReady_i = '1' then
            Address       := to_integer(unsigned(AWAddr));
            Ctrl_BValid_i <= '1';
            
            for I in 0 to 3 loop
               if Ctrl_WStrb(I) = '1' then
                  RegArr(Address)(8*(I+1)-1 downto 8*I) <= Ctrl_WData(8*(I+1)-1 downto 8*I);
               end if;
            end loop;

         elsif Ctrl_BValid_i = '1' and Ctrl_BReady = '1' then
            Ctrl_BValid_i <= '0';
         end if;

      end if;
   end process;


   Ctrl_ARReady_i <= not Ctrl_RValid_i;
   Ctrl_AWReady_i <= Ctrl_WValid  and not Ctrl_BValid_i;
   Ctrl_WReady_i  <= Ctrl_AWValid and not Ctrl_BValid_i;
   
   Ctrl_ARReady   <= Ctrl_ARReady_i;
   Ctrl_RValid    <= Ctrl_RValid_i;
   Ctrl_AWReady   <= Ctrl_AWReady_i;
   Ctrl_WReady    <= Ctrl_WReady_i ;
   Ctrl_BValid    <= Ctrl_BValid_i ;
   
   Ctrl_RResp     <= (others => '0');
   Ctrl_BResp     <= (others => '0');

end architecture rtl;
