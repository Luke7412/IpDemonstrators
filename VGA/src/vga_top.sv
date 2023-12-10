
module vga_top(
  input logic sys_clock,
  input logic reset,

  output logic       vga_vsync,
  output logic       vga_hsync,
  output logic [3:0] vga_r, 
  output logic [3:0] vga_g, 
  output logic [3:0] vga_b
);


  //----------------------------------------------------------------------------
  import vga_pkg::*;

  localparam int RESOLUTION = 3;
  localparam int H_RES           = vga_configs[RESOLUTION].H_RES;
  localparam int H_FRONT_PORCH   = 0;   //vga_configs[RESOLUTION].H_FRONT_PORCH;
  localparam int H_SYNC_PULSE    = 256; //vga_configs[RESOLUTION].H_SYNC_PULSE;
  localparam int H_BACK_PORCH    = 0;   //vga_configs[RESOLUTION].H_BACK_PORCH;
  localparam int V_RES           = vga_configs[RESOLUTION].V_RES;
  localparam int V_FRONT_PORCH   = vga_configs[RESOLUTION].V_FRONT_PORCH;
  localparam int V_SYNC_PULSE    = vga_configs[RESOLUTION].V_SYNC_PULSE;
  localparam int V_BACK_PORCH    = vga_configs[RESOLUTION].V_BACK_PORCH;
  
  logic aclk;
  logic aresetn;

  logic sof;
  logic pix_tvalid;
  logic pix_tready;
  logic [2:0][3:0] pix_tdata;
  logic pix_tlast;
  logic pix_tuser;
  
  logic [15:0] h_res;
  logic [15:0] h_front_porch;
  logic [15:0] h_sync_pulse;
  logic [15:0] h_back_porch;
  logic [15:0] v_res;
  logic [15:0] v_front_porch;
  logic [15:0] v_sync_pulse;
  logic [15:0] v_back_porch;


  //----------------------------------------------------------------------------
  assign h_res          = H_RES; 
  assign h_front_porch  = H_FRONT_PORCH; 
  assign h_sync_pulse   = H_SYNC_PULSE; 
  assign h_back_porch   = H_BACK_PORCH; 
  assign v_res          = V_RES; 
  assign v_front_porch  = V_FRONT_PORCH; 
  assign v_sync_pulse   = V_SYNC_PULSE; 
  assign v_back_porch   = V_BACK_PORCH; 


  core_wrapper i_core_wrapper (
    .aclk (aclk),
    .aresetn (aresetn),
    .reset (reset),
    .sys_clock (sys_clock)
  );


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
    .pix_tdata  (pix_tdata),
    .pix_tlast (pix_tlast),
    .pix_tuser (pix_tuser),
    // VGA Config
    .H_RES         (h_res),
    .H_FRONT_PORCH (h_front_porch),
    .H_SYNC_PULSE  (h_sync_pulse),
    .H_BACK_PORCH  (h_back_porch),
    .V_RES         (v_res),
    .V_FRONT_PORCH (v_front_porch),
    .V_SYNC_PULSE  (v_sync_pulse),
    .V_BACK_PORCH  (v_back_porch),
    // VGA Interface
    .vga_vsync (vga_vsync),
    .vga_hsync (vga_hsync),
    .vga_r     (vga_r), 
    .vga_g     (vga_g), 
    .vga_b     (vga_b),

    .sof (sof)
  );


endmodule
