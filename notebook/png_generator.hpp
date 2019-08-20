#ifndef PNG_GENERATOR_H
#define PNG_GENERATOR_H

#include "color_maps.hpp"
#include <pngwriter.h>

template <typename varTyp>
std::vector<unsigned char>
generate_png(varTyp *matrix, const unsigned int width,
             const unsigned int height, ColorMap<varTyp> *colorTable,
             bool ghostcells = false, const unsigned int scale = 1) {
  std::vector<unsigned char> png;
  pngwriter pic((width - ghostcells * 2) * scale,
                (height - ghostcells * 2) * scale, 0, "tmp.png");

  // true == (int)1 -> if ghostcells true, indicies starts with 1 ends with
  // height-1
  for (unsigned int y = ghostcells; y < height - ghostcells; ++y) {
    for (unsigned int x = ghostcells; x < width - ghostcells; ++x) {
      for (unsigned scale_y = 0; scale_y < scale; ++scale_y) {
        for (unsigned scale_x = 0; scale_x < scale; ++scale_x) {
          pic.plot(((x - ghostcells) * scale) + scale_x,
                   pic.getwidth() - (((y - ghostcells) * scale) + scale_y),
                   colorTable->r(matrix[y * width + x]),
                   colorTable->g(matrix[y * width + x]),
                   colorTable->b(matrix[y * width + x]));
        }
      }
    }
  }

  pic.write_to_buffer(png);
  return png;
}

#endif
