
module vga_subsys(
  input logic aclk,
  input logic aresetn,

  input  logic        ctrl_arvalid,
  output logic        ctrl_arready,
  input  logic [11:0] ctrl_araddr,
  output logic        ctrl_rvalid,
  input  logic        ctrl_rready,
  output logic [31:0] ctrl_rdata,
  output logic [1:0]  ctrl_rresp,
  input  logic        ctrl_awvalid,
  output logic        ctrl_awready,
  input  logic [11:0] ctrl_awaddr,
  input  logic        ctrl_wvalid,
  output logic        ctrl_wready,
  input  logic [31:0] ctrl_wdata,
  input  logic [3:0]  ctrl_wstrb,
  output logic        ctrl_bvalid,
  input  logic        ctrl_bready,
  output logic [1:0]  ctrl_bresp,

  output logic       vga_vsync,
  output logic       vga_hsync,
  output logic [3:0] vga_r, 
  output logic [3:0] vga_g, 
  output logic [3:0] vga_b
);


  //----------------------------------------------------------------------------
  localparam int NOF_REGOUT = 9;
  localparam int NOF_REGIN  = 1;
  
  logic [31:0] reg_out [NOF_REGOUT];

  logic [15:0] h_res;
  logic [15:0] h_front_porch;
  logic [15:0] h_sync_pulse;
  logic [15:0] h_back_porch;
  logic [15:0] v_res;
  logic [15:0] v_front_porch;
  logic [15:0] v_sync_pulse;
  logic [15:0] v_back_porch;

  logic sof;
  logic pix_tvalid;
  logic pix_tready;
  logic [2:0][3:0] pix_tdata;
  logic pix_tlast;
  logic pix_tuser;

  logic init;


  //----------------------------------------------------------------------------
   axi4lite_regbank #(
    .NOF_REGOUT (NOF_REGOUT),
    .NOF_REGIN (NOF_REGIN)
  ) i_axi4lite_regbank ( 
    .aclk (aclk),
    .aresetn (aresetn),
    .ctrl_arvalid (ctrl_arvalid),
    .ctrl_arready (ctrl_arready),
    .ctrl_araddr (ctrl_araddr),
    .ctrl_rvalid (ctrl_rvalid),
    .ctrl_rready (ctrl_rready),
    .ctrl_rdata (ctrl_rdata),
    .ctrl_rresp (ctrl_rresp),
    .ctrl_awvalid (ctrl_awvalid),
    .ctrl_awready (ctrl_awready),
    .ctrl_awaddr (ctrl_awaddr),
    .ctrl_wvalid (ctrl_wvalid),
    .ctrl_wready (ctrl_wready),
    .ctrl_wdata (ctrl_wdata),
    .ctrl_wstrb (ctrl_wstrb),
    .ctrl_bvalid (ctrl_bvalid),
    .ctrl_bready (ctrl_bready),
    .ctrl_bresp (ctrl_bresp),
    .reg_out (reg_out),
    .reg_in () 
  );  

  assign h_res          = reg_out[0][15:0];
  assign h_front_porch  = reg_out[1][15:0];
  assign h_sync_pulse   = reg_out[2][15:0];
  assign h_back_porch   = reg_out[3][15:0];
  assign v_res          = reg_out[4][15:0];
  assign v_front_porch  = reg_out[5][15:0];
  assign v_sync_pulse   = reg_out[6][15:0];
  assign v_back_porch   = reg_out[7][15:0];
  assign init           = reg_out[8][0];


  frame_gen i_frame_gen ( 
    .aclk (aclk),
    .aresetn (aresetn),
    .H_RES (h_res),
    .V_RES (v_res),
    .sof (sof),
    .pix_tvalid (pix_tvalid),
    .pix_tready (pix_tready),
    .pix_tdata (pix_tdata),
    .pix_tlast (pix_tlast),
    .pix_tuser (pix_tuser)
  );


  vga i_vga ( 
    .aclk (aclk),
    .aresetn (aresetn),
    .pix_tvalid (pix_tvalid),
    .pix_tready (pix_tready),
    .pix_tdata (pix_tdata),
    .pix_tlast (pix_tlast),
    .pix_tuser (pix_tuser),
    // VGA Config
    .init (init),
    .sof (sof),
    .H_RES (h_res),
    .H_FRONT_PORCH (h_front_porch),
    .H_SYNC_PULSE (h_sync_pulse),
    .H_BACK_PORCH (h_back_porch),
    .V_RES (v_res),
    .V_FRONT_PORCH (v_front_porch),
    .V_SYNC_PULSE (v_sync_pulse),
    .V_BACK_PORCH (v_back_porch),
    // VGA Interface
    .vga_vsync (vga_vsync),
    .vga_hsync (vga_hsync),
    .vga_r     (vga_r), 
    .vga_g     (vga_g), 
    .vga_b     (vga_b)

  );

endmodule