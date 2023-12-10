
//------------------------------------------------------------------------------
module vga ( 
  input  logic aclk,
  input  logic aresetn,

  input  logic             pix_tvalid,
  output logic             pix_tready,
  input  logic [2:0][3:0]  pix_tdata,
  input  logic             pix_tlast,
  input  logic             pix_tuser,
  // VGA Config
  input  logic init,
  output logic sof,
  input  logic [15:0] H_RES,
  input  logic [15:0] H_FRONT_PORCH,
  input  logic [15:0] H_SYNC_PULSE,
  input  logic [15:0] H_BACK_PORCH,
  input  logic [15:0] V_RES,
  input  logic [15:0] V_FRONT_PORCH,
  input  logic [15:0] V_SYNC_PULSE,
  input  logic [15:0] V_BACK_PORCH,
  // VGA Interface
  output logic       vga_vsync,
  output logic       vga_hsync,
  output logic [3:0] vga_r, 
  output logic [3:0] vga_g, 
  output logic [3:0] vga_b
);


  //----------------------------------------------------------------------------
  logic [15:0] h_cnt;
  logic [15:0] v_cnt;

  enum {H_BLANK, H_FP, H_PIX, H_BP} h_state;
  enum {V_BLANK, V_FP, V_PIX, V_BP} v_state;

  logic vga_vsync_q;


  //----------------------------------------------------------------------------
  always_ff @(posedge aclk or negedge aresetn) begin
    if (!aresetn) begin
      h_cnt   <= H_SYNC_PULSE-1;
      h_state <= H_BLANK;

    end else begin
      if (init) begin
        h_cnt   <= H_SYNC_PULSE-1;
        h_state <= H_BLANK;
      end else begin
        case (h_state)
          H_BLANK : begin
            h_cnt <= h_cnt - 1;
            if (h_cnt == 0) begin
              h_cnt   <= H_BACK_PORCH-1;
              h_state <= H_BP;
            end
          end

          H_BP : begin
            h_cnt <= h_cnt - 1;
            if (h_cnt == 0) begin
              h_cnt   <= H_RES-1;
              h_state <= H_PIX;
            end
          end

          H_PIX : begin
            h_cnt <= h_cnt - 1;
            if (h_cnt == 0) begin
              h_cnt   <= H_FRONT_PORCH-1;
              h_state <= H_FP;
            end
          end

          H_FP : begin
            h_cnt <= h_cnt - 1;
            if (h_cnt == 0) begin
              h_cnt   <= H_SYNC_PULSE-1;
              h_state <= H_BLANK;
            end
          end

        endcase
      end

    end
  end


  always_ff @(posedge aclk or negedge aresetn) begin
    if (!aresetn) begin
      v_cnt   <= V_SYNC_PULSE-1;
      v_state <= V_BLANK;

    end else begin
      if (init) begin
        v_cnt   <= V_SYNC_PULSE-1;
        v_state <= V_BLANK;

      end else if (h_state == H_FP && h_cnt == 0) begin
        case (v_state)
          V_BLANK : begin
            v_cnt <= v_cnt - 1;
            if (v_cnt == 0) begin
              v_cnt   <= V_BACK_PORCH-1;
              v_state <= V_BP;
            end
          end

          V_BP : begin
            v_cnt <= v_cnt - 1;
            if (v_cnt == 0) begin
              v_cnt   <= V_RES-1;
              v_state <= V_PIX;
            end
          end

          V_PIX : begin
            v_cnt <= v_cnt - 1;
            if (v_cnt == 0) begin
              v_cnt   <= V_FRONT_PORCH-1;
              v_state <= V_FP;
            end
          end

          V_FP : begin
            v_cnt <= v_cnt - 1;
            if (v_cnt == 0) begin
              v_cnt   <= V_SYNC_PULSE-1;
              v_state <= V_BLANK;
            end
          end

        endcase
      end

    end
  end


  assign pix_tready = h_state == H_PIX && v_state == V_PIX;

  assign {vga_b, vga_g, vga_r} = pix_tready ? pix_tdata : '0; 
  assign vga_vsync = v_state != V_BLANK;
  assign vga_hsync = h_state != H_BLANK;


  always @(posedge aclk or negedge aresetn) begin
    if (!aresetn) begin
      vga_vsync_q <= '0;
    end else begin
      vga_vsync_q <= vga_vsync;
    end
  end

  assign sof = vga_vsync && !vga_vsync_q;

endmodule