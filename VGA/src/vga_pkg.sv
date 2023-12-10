
package vga_pkg;

  typedef struct {
    int H_RES;
    int H_FRONT_PORCH;
    int H_SYNC_PULSE;
    int H_BACK_PORCH;
    int V_RES;
    int V_FRONT_PORCH;
    int V_SYNC_PULSE;
    int V_BACK_PORCH;
    real PIX_CLK;
  } t_vga_config;

  localparam t_vga_config vga_configs [7] = '{
    0: '{ // 640x350p70
      H_RES:         640,
      H_FRONT_PORCH: 16,
      H_SYNC_PULSE:  96,
      H_BACK_PORCH:  48,
      V_RES:         350,
      V_FRONT_PORCH: 37,
      V_SYNC_PULSE:  2,
      V_BACK_PORCH:  60,
      PIX_CLK:       25.175
    },
    1: '{ // 640x400p60
      H_RES:         640,
      H_FRONT_PORCH: 16,
      H_SYNC_PULSE:  96,
      H_BACK_PORCH:  48,
      V_RES:         400,
      V_FRONT_PORCH: 12,
      V_SYNC_PULSE:  2,
      V_BACK_PORCH:  35,
      PIX_CLK:       25.175
    },
    2: '{ // 640x480p60
      H_RES:         640,
      H_FRONT_PORCH: 16,
      H_SYNC_PULSE:  96,
      H_BACK_PORCH:  48,
      V_RES:         480,
      V_FRONT_PORCH: 10,
      V_SYNC_PULSE:  2,
      V_BACK_PORCH:  33,
      PIX_CLK:       25.175
    },
    3: '{ // 800x600p60
      H_RES:         800,
      H_FRONT_PORCH: 40,
      H_SYNC_PULSE:  128,
      H_BACK_PORCH:  88,
      V_RES:         600,
      V_FRONT_PORCH: 1,
      V_SYNC_PULSE:  4,
      V_BACK_PORCH:  23,
      PIX_CLK:       40.000
    },
    4: '{ // 1024x768p60
      H_RES:         1024,
      H_FRONT_PORCH: 24,
      H_SYNC_PULSE:  136,
      H_BACK_PORCH:  160,
      V_RES:         768,
      V_FRONT_PORCH: 3,
      V_SYNC_PULSE:  6,
      V_BACK_PORCH:  29,
      PIX_CLK:       65.000
    },
    5: '{ // 1280x1024p60
      H_RES:         1280,
      H_FRONT_PORCH: 48,
      H_SYNC_PULSE:  112,
      H_BACK_PORCH:  248,
      V_RES:         1024,
      V_FRONT_PORCH: 1,
      V_SYNC_PULSE:  3,
      V_BACK_PORCH:  39,
      PIX_CLK:       108.000
    },
    6: '{ // DEBUG
      H_RES:         10,
      H_FRONT_PORCH: 6,
      H_SYNC_PULSE:  7,
      H_BACK_PORCH:  8,
      V_RES:         3,
      V_FRONT_PORCH: 1,
      V_SYNC_PULSE:  2,
      V_BACK_PORCH:  3,
      PIX_CLK:       108.000
    }

  };


endpackage