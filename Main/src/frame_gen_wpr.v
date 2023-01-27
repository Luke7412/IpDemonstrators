//------------------------------------------------------------------------------
module frame_gen_wpr #(
  parameter H_RES = 640,
  parameter V_RES = 480
)( 
  input aclk,
  input aresetn,

  input sof,

  output pix_tvalid,
  input  pix_tready,
  output  [2:0][3:0]  pix_tdata,
  output pix_tlast,
  output pix_tuser
);


//------------------------------------------------------------------------------
  frame_gen #(
    .H_RES (H_RES),
    .V_RES (V_RES)
  ) i_frame_gen ( 
    .aclk (aclk),
    .aresetn (aresetn),
    .sof (sof),
    .pix_tvalid (pix_tvalid),
    .pix_tready (pix_tready),
    .pix_tdata (pix_tdata),
    .pix_tlast (pix_tlast),
    .pix_tuser (pix_tuser)
  );

endmodule