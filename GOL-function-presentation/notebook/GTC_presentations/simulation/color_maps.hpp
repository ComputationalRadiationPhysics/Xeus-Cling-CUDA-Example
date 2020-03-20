#ifndef COLOR_MAPS_H
#define COLOR_MAPS_H

template <typename varTyp>
struct ColorMap
{
	virtual int r(varTyp value){return (2500 + 500 * value)%65535;}
	virtual int g(varTyp value){return (10408 + 500 * value)%65535;}
	virtual int b(varTyp value){return (7401 + 500 * value)%65535;}
};

template <typename varTyp>
struct BlackWhiteMap : ColorMap<varTyp>
{
	int r(varTyp value){return value ? 65535 : 0;}
	int g(varTyp value){return value ? 65535 : 0;}
	int b(varTyp value){return value ? 65535 : 0;}
};

// define a color map for the heat map
// use the same code which has generated images of the game of life world
template <typename varTyp>
struct HeatMap : ColorMap<varTyp>
{
    int r(varTyp value){return value * 65535/8;}
    int g(varTyp value){return 0;}
    int b(varTyp value){return 0;}
};
HeatMap<int> h_map;

template <typename varTyp>
struct ColorHeatMap : ColorMap<varTyp>
{
    unsigned char turbo_srgb_bytes[9][3] = {{0,0,0},         //0
                                            {128, 128, 128}, //1
                                            {255, 255, 25},  //2
                                            {245, 130, 48},  //3
                                            {0, 130, 200},   //4
                                            {240, 50, 230},  //5
                                            {237, 77, 62},   //6
                                            {60, 180, 75},   //7
                                            {145, 30, 255}}; //8
    int r(varTyp value){return static_cast<int>(turbo_srgb_bytes[value][0]) * 256;}
    int g(varTyp value){return static_cast<int>(turbo_srgb_bytes[value][1]) * 256;}
    int b(varTyp value){return static_cast<int>(turbo_srgb_bytes[value][2]) * 256;}
};
ColorHeatMap<int> ch_map;

#endif
