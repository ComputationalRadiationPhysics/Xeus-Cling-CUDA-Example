#ifndef INPUT_READER_H
#define INPUT_READER_H

template <typename varTyp>
int read_input(const char *filename, varTyp matrix, const unsigned int width,
               const unsigned int height, const bool ghostcells = false) {
  std::ifstream input(filename);
  if (!input.is_open()) {
    std::cerr << "can't open file " << filename << std::endl;
    return -1;
  }

  unsigned int x = ghostcells, y = ghostcells, count_elements = 0;

  for (std::string word; input >> word;) {
    if (count_elements == width * height) {
      std::cerr << "to many elements in file " << filename << std::endl;
      input.close();
      return -2;
    }

    if (word == "x" || word == "X" || word == "1") {
      matrix[y * (width + (ghostcells * 2)) + x] = 1; // living cell
    } else {
      matrix[y * (width + (ghostcells * 2)) + x] = 0; // dead cell
    }

    // calculate new position
    ++x;
    if ((x % (width + ghostcells)) == 0) {
      x = ghostcells;
      ++y;
    }
    ++count_elements;
  }

  input.close();
  return 0;
}

#endif
