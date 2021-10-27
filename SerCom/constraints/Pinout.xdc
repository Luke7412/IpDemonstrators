
set_property -dict { PACKAGE_PIN A9    IOSTANDARD LVCMOS33 } [get_ports Uart_rxd];
set_property -dict { PACKAGE_PIN D10   IOSTANDARD LVCMOS33 } [get_ports Uart_txd];

set_property -dict { PACKAGE_PIN H5    IOSTANDARD LVCMOS33 } [get_ports AResetn[0]];
set_property -dict { PACKAGE_PIN J5    IOSTANDARD LVCMOS33 } [get_ports AReset[0] ];
